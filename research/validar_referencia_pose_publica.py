#!/usr/bin/env python3
"""Valida dos CSV privados de referencia 2D y emite sólo agregados.

El acuerdo entre codificadores no mide por sí mismo exactitud anatómica ni
calidad de HarMoCAP. No escribe imágenes, coordenadas ni anotaciones en Git.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from collections import Counter
from pathlib import Path


SOURCE_SHA256 = "573ac41a261d71fc59fbf890d129964061f3c9346bcf6fcf5b4cecb3217e05aa"
JOINTS = ("shoulder_l", "shoulder_r", "wrist_l", "wrist_r", "hip_l", "hip_r")
PERSONS = ("A", "B")
STATUSES = {"visible", "occluded", "out_of_frame", "ambiguous_identity", "unresolvable"}
COLUMNS = ("sample_id", "person", "joint", "status", "x_px", "y_px",
           "uncertainty_px", "coder_id", "note")


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load_manifest(path: Path) -> tuple[dict, dict[str, dict]]:
    manifest = json.loads(path.read_text())
    if (manifest.get("protocol") != "reference_pose_public_video_v0.1"
            or manifest.get("source_sha256") != SOURCE_SHA256
            or manifest.get("source_dimensions_px") != [852, 480]
            or manifest.get("per_stratum") != 20):
        raise ValueError("Manifiesto incompatible con el protocolo y original publicados")
    samples = manifest.get("samples")
    if not isinstance(samples, list) or len(samples) != 40:
        raise ValueError("El manifiesto requiere 40 muestras")
    by_id: dict[str, dict] = {}
    bins: set[tuple[str, int]] = set()
    stratum_weights: Counter[str] = Counter()
    for sample in samples:
        sid = sample["sample_id"]
        stratum = sample["stratum"]
        bin_index = sample["bin_index"]
        weight = sample["design_weight_frames"]
        if (sid in by_id or stratum not in ("early", "late")
                or not isinstance(bin_index, int) or not 0 <= bin_index < 20
                or (stratum, bin_index) in bins
                or not isinstance(weight, int) or weight < 1
                or weight != sample["bin_frames"]):
            raise ValueError("IDs, bins o pesos inválidos en manifiesto")
        image = path.parent / sample["image"]
        if path.parent.resolve() not in image.resolve().parents or not image.is_file():
            raise ValueError("Falta una imagen privada del manifiesto")
        if digest(image) != sample["image_sha256"]:
            raise ValueError("Hash de imagen privada no coincide")
        by_id[sid] = sample
        bins.add((stratum, bin_index))
        stratum_weights[stratum] += weight
    if (bins != {(stratum, i) for stratum in ("early", "late") for i in range(20)}
            or dict(stratum_weights) != manifest.get("strata_source_frames")
            or sum(stratum_weights.values()) != 550):
        raise ValueError("El diseño estratificado no suma los 550 cuadros fuente")
    return manifest, by_id


def optional_number(value: str, label: str) -> float | None:
    if value == "":
        return None
    try:
        number = float(value)
    except ValueError as exc:
        raise ValueError(f"{label}: se requiere número finito") from exc
    if not math.isfinite(number):
        raise ValueError(f"{label}: se requiere número finito")
    return number


def load_coder(path: Path, sample_ids: set[str], dimensions: list[int]) -> tuple[dict, str]:
    rows: dict[tuple[str, str, str], dict] = {}
    coder_ids: set[str] = set()
    with path.open(newline="") as stream:
        reader = csv.DictReader(stream)
        if reader.fieldnames is None or set(reader.fieldnames) != set(COLUMNS):
            raise ValueError("CSV: columnas distintas de la plantilla de referencia")
        for n, raw in enumerate(reader, start=2):
            if None in raw or any(value is None for value in raw.values()):
                raise ValueError(f"CSV fila {n}: columnas de más o de menos")
            row = {key: value.strip() for key, value in raw.items()}
            key = (row["sample_id"], row["person"], row["joint"])
            if (key[0] not in sample_ids or key[1] not in PERSONS
                    or key[2] not in JOINTS or key in rows):
                raise ValueError(f"CSV fila {n}: clave desconocida o repetida")
            if row["status"] not in STATUSES:
                raise ValueError(f"CSV fila {n}: estado ausente o desconocido")
            if not row["coder_id"]:
                raise ValueError(f"CSV fila {n}: falta código de observador")
            coder_ids.add(row["coder_id"])
            x = optional_number(row["x_px"], f"CSV fila {n}, x")
            y = optional_number(row["y_px"], f"CSV fila {n}, y")
            uncertainty = optional_number(row["uncertainty_px"], f"CSV fila {n}, incertidumbre")
            if row["status"] == "visible":
                if (x is None or y is None or not 0 <= x < dimensions[0]
                        or not 0 <= y < dimensions[1]
                        or (uncertainty is not None and uncertainty < 0)):
                    raise ValueError(f"CSV fila {n}: coordenada o incertidumbre visible inválida")
            elif x is not None or y is not None or uncertainty is not None:
                raise ValueError(f"CSV fila {n}: un punto no visible debe dejar números vacíos")
            rows[key] = {"status": row["status"], "x": x, "y": y}
    expected = {(sid, person, joint) for sid in sample_ids
                for person in PERSONS for joint in JOINTS}
    if set(rows) != expected:
        raise ValueError(f"CSV incompleto: {len(expected - set(rows))} filas faltantes")
    if len(coder_ids) != 1:
        raise ValueError("Cada archivo debe contener un único código de observador")
    return rows, next(iter(coder_ids))


def fraction(numerator: int, denominator: int) -> float:
    return round(numerator / denominator, 6)


def percentile(values: list[float], q: float) -> float | None:
    if not values:
        return None
    ordered = sorted(values)
    position = (len(ordered) - 1) * q
    lo = math.floor(position)
    hi = math.ceil(position)
    return round(ordered[lo] + (ordered[hi] - ordered[lo]) * (position - lo), 3)


def coverage(rows: dict, samples: dict[str, dict]) -> dict:
    total = sum(s["design_weight_frames"] for s in samples.values())
    gates = {
        "torso": ("shoulder_l", "shoulder_r", "hip_l", "hip_r"),
        "torso_right_wrist": ("shoulder_l", "shoulder_r", "hip_l", "hip_r", "wrist_r"),
        "torso_both_wrists": JOINTS,
    }
    result = {}
    for name, joints in gates.items():
        valid = sum(sample["design_weight_frames"] for sid, sample in samples.items()
                    if all(rows[(sid, person, joint)]["status"] == "visible"
                           for person in PERSONS for joint in joints))
        result[name] = {"weighted_frames": valid, "denominator_frames": total,
                        "fraction": fraction(valid, total)}
    return result


def compare(a: dict, b: dict, samples: dict[str, dict]) -> dict:
    keys = sorted(a)
    agreement = sum(a[k]["status"] == b[k]["status"] for k in keys)
    weighted_total = sum(samples[k[0]]["design_weight_frames"] for k in keys)
    weighted_matches = sum(samples[k[0]]["design_weight_frames"] for k in keys
                           if a[k]["status"] == b[k]["status"])
    per_joint = {}
    for joint in JOINTS:
        subset = [k for k in keys if k[2] == joint]
        matches = sum(a[k]["status"] == b[k]["status"] for k in subset)
        per_joint[joint] = {"same_status": matches, "total": len(subset),
                            "fraction": fraction(matches, len(subset))}
    per_person = {}
    for person in PERSONS:
        subset = [k for k in keys if k[1] == person]
        matches = sum(a[k]["status"] == b[k]["status"] for k in subset)
        per_person[person] = {"same_status": matches, "total": len(subset),
                              "fraction": fraction(matches, len(subset))}
    per_stratum = {}
    for stratum in ("early", "late"):
        subset = [k for k in keys if samples[k[0]]["stratum"] == stratum]
        matches = sum(a[k]["status"] == b[k]["status"] for k in subset)
        weight_total = sum(samples[k[0]]["design_weight_frames"] for k in subset)
        weight_matches = sum(samples[k[0]]["design_weight_frames"] for k in subset
                             if a[k]["status"] == b[k]["status"])
        per_stratum[stratum] = {"same_status": matches, "total": len(subset),
                                "fraction": fraction(matches, len(subset)),
                                "weighted_fraction": fraction(weight_matches, weight_total)}
    distances = [math.hypot(a[k]["x"] - b[k]["x"], a[k]["y"] - b[k]["y"])
                 for k in keys if a[k]["status"] == b[k]["status"] == "visible"]
    return {
        "design": {"sampled_frames": len(samples), "source_frames": 550,
                   "keypoint_rows_per_coder": len(keys)},
        "status_agreement": {"same": agreement, "total": len(keys),
                             "fraction": fraction(agreement, len(keys)),
                             "weighted_fraction": fraction(weighted_matches, weighted_total),
                             "per_joint": per_joint, "per_person": per_person,
                             "per_stratum": per_stratum},
        "coordinate_agreement_when_both_visible_px": {
            "pairs": len(distances), "median": percentile(distances, 0.5),
            "p95": percentile(distances, 0.95),
            "max": round(max(distances), 3) if distances else None},
        "weighted_descriptor_coverage_by_coder": {
            "coder_1": coverage(a, samples), "coder_2": coverage(b, samples)},
        "interpretation": "Acuerdo y cobertura descriptivos de referencia 2D; no miden exactitud anatómica, HarMoCAP, Laban, HIT ni conciencia.",
    }


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("manifest", type=Path)
    ap.add_argument("coder_1_csv", type=Path)
    ap.add_argument("coder_2_csv", type=Path)
    args = ap.parse_args()
    manifest, samples = load_manifest(args.manifest)
    a, a_id = load_coder(args.coder_1_csv, set(samples), manifest["source_dimensions_px"])
    b, b_id = load_coder(args.coder_2_csv, set(samples), manifest["source_dimensions_px"])
    if a_id == b_id or args.coder_1_csv.resolve() == args.coder_2_csv.resolve():
        raise ValueError("Se requieren dos archivos y códigos de observador distintos")
    print(json.dumps(compare(a, b, samples), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
