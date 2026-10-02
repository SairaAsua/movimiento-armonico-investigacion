#!/usr/bin/env python3
"""Prepara correspondencia A/B y compara poses privadas con dos referencias 2D.

La asignación de identidad es humana y ciega a las coordenadas de referencia.
Sólo imprime agregados; las entradas y la plantilla de identidad quedan fuera de Git.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
from collections import Counter
from pathlib import Path

from validar_referencia_pose_publica import (JOINTS, PERSONS, fraction, load_coder,
                                              load_manifest, percentile)


IDENTITY_COLUMNS = ("sample_id", "person", "status", "track_id", "reviewer_id", "note")
IDENTITY_STATUSES = {"matched", "unmatched", "ambiguous"}
MODEL_PROTOCOL = "harmocap_public_video_reference_export_v0.1"


def load_model(path: Path, manifest: dict, samples: dict[str, dict]) -> dict[str, dict]:
    model = json.loads(path.read_text())
    if (model.get("protocol") != MODEL_PROTOCOL
            or model.get("source_sha256") != manifest["source_sha256"]
            or model.get("tracking_stride") != 1):
        raise ValueError("Exportación de modelo incompatible con original o tracking continuo")
    by_id = {}
    for row in model.get("samples", []):
        sid = row.get("sample_id")
        if (sid not in samples or sid in by_id
                or row.get("source_frame_index") != samples[sid]["source_frame_index"]
                or abs(row.get("pts_s", -1) - samples[sid]["pts_s"]) > 1e-6
                or row.get("dimensions_px") != manifest["source_dimensions_px"]):
            raise ValueError("Índice, PTS, dimensión o muestra de modelo inconsistente")
        detections = row.get("detections")
        if not isinstance(detections, list) or row.get("raw_detection_count", -1) < len(detections):
            raise ValueError("Conteo de detecciones inválido")
        ids = set()
        for det in detections:
            tid = det.get("track_id")
            if not isinstance(tid, int) or tid in ids or set(det.get("keypoints", {})) != set(JOINTS):
                raise ValueError("ID de detección duplicado o puntos incompletos")
            ids.add(tid)
            for point in det["keypoints"].values():
                if (not all(isinstance(point.get(k), (int, float))
                            and math.isfinite(point[k]) for k in ("x_px", "y_px", "confidence"))
                        or not 0 <= point["confidence"] <= 1):
                    raise ValueError("Coordenada o confianza de modelo inválida")
        by_id[sid] = {**row, "detections_by_id": {d["track_id"]: d for d in detections}}
    if set(by_id) != set(samples):
        raise ValueError("La exportación no contiene exactamente las muestras del manifiesto")
    return by_id


def private_path(path: Path) -> Path:
    target = path.resolve()
    repo = Path(__file__).resolve().parents[1]
    if target == repo or repo in target.parents:
        raise ValueError("La plantilla con identidades debe quedar fuera del repositorio público")
    return target


def prepare(path: Path, model: dict[str, dict]) -> None:
    target = private_path(path)
    if target.exists():
        raise ValueError("No se sobrescribe una revisión de identidad existente")
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("x", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=IDENTITY_COLUMNS)
        writer.writeheader()
        for sid in sorted(model):
            for person in PERSONS:
                writer.writerow({"sample_id": sid, "person": person, "status": "",
                                 "track_id": "", "reviewer_id": "", "note": ""})
    print(json.dumps({"template_rows": len(model) * len(PERSONS),
                      "status": "private_template_created"}))


def render_overlays(path: Path, model: dict[str, dict], samples: dict[str, dict],
                    manifest_path: Path) -> None:
    """Dibuja puntos e IDs del modelo sin asignar A/B; uso sólo de revisión privada."""
    import cv2

    target = private_path(path)
    if target.exists() and any(target.iterdir()):
        raise ValueError("No se sobrescriben vistas de revisión existentes")
    target.mkdir(parents=True, exist_ok=True)
    colors = ((0, 200, 255), (255, 140, 0), (160, 80, 255), (0, 200, 80))
    for sid in sorted(model):
        frame = cv2.imread(str(manifest_path.parent / samples[sid]["image"]))
        if frame is None:
            raise ValueError("No se pudo leer una imagen privada de muestra")
        for det in model[sid]["detections"]:
            color = colors[det["track_id"] % len(colors)]
            for point in det["keypoints"].values():
                x, y = round(point["x_px"]), round(point["y_px"])
                if 0 <= x < frame.shape[1] and 0 <= y < frame.shape[0]:
                    cv2.circle(frame, (x, y), 4, color, -1, cv2.LINE_AA)
            k = det["keypoints"]["shoulder_l"]
            x, y = round(k["x_px"]), round(k["y_px"])
            x = min(max(x, 0), frame.shape[1] - 110)
            y = min(max(y - 12, 18), frame.shape[0] - 4)
            cv2.putText(frame, f"track {det['track_id']}", (x, y),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2, cv2.LINE_AA)
        if not cv2.imwrite(str(target / f"{sid}.png"), frame):
            raise ValueError("No se pudo guardar una vista privada")


def load_identity(path: Path, model: dict[str, dict]) -> dict[tuple[str, str], dict]:
    rows = {}
    reviewers = set()
    with path.open(newline="") as stream:
        reader = csv.DictReader(stream)
        if reader.fieldnames is None or set(reader.fieldnames) != set(IDENTITY_COLUMNS):
            raise ValueError("Plantilla de identidad con columnas inesperadas")
        for n, raw in enumerate(reader, start=2):
            if None in raw or any(v is None for v in raw.values()):
                raise ValueError(f"Identidad fila {n}: columnas de más o de menos")
            row = {k: v.strip() for k, v in raw.items()}
            key = (row["sample_id"], row["person"])
            if key[0] not in model or key[1] not in PERSONS or key in rows:
                raise ValueError(f"Identidad fila {n}: muestra/persona desconocida o duplicada")
            if row["status"] not in IDENTITY_STATUSES or not row["reviewer_id"]:
                raise ValueError(f"Identidad fila {n}: estado o revisor ausente")
            reviewers.add(row["reviewer_id"])
            if row["status"] == "matched":
                try:
                    tid = int(row["track_id"])
                except ValueError as exc:
                    raise ValueError(f"Identidad fila {n}: falta track_id entero") from exc
                if tid not in model[key[0]]["detections_by_id"]:
                    raise ValueError(f"Identidad fila {n}: track_id ausente en el cuadro")
                row["track_id"] = tid
            elif row["track_id"]:
                raise ValueError(f"Identidad fila {n}: track_id sólo con matched")
            rows[key] = row
    if set(rows) != {(sid, person) for sid in model for person in PERSONS}:
        raise ValueError("Revisión de identidad incompleta")
    if len(reviewers) != 1:
        raise ValueError("La revisión de identidad debe usar un solo código de revisor")
    for sid in model:
        ids = [rows[(sid, person)]["track_id"] for person in PERSONS
               if rows[(sid, person)]["status"] == "matched"]
        if len(ids) != len(set(ids)):
            raise ValueError("Una detección no puede asignarse a A y B en el mismo cuadro")
    return rows


def report_for_coder(reference: dict, identity: dict, model: dict, samples: dict) -> dict:
    counts = Counter()
    distances: dict[str, list[tuple[float, int]]] = {joint: [] for joint in JOINTS}
    strata_counts: dict[str, Counter] = {"early": Counter(), "late": Counter()}
    strata_distances: dict[str, list[tuple[float, int]]] = {"early": [], "late": []}
    confidence_groups: dict[str, list[float]] = {"ge_0p5": [], "lt_0p5": []}
    for (sid, person, joint), ref in reference.items():
        if ref["status"] != "visible":
            continue
        weight = samples[sid]["design_weight_frames"]
        stratum = samples[sid]["stratum"]
        counts["visible_reference_points"] += 1
        counts["weighted_visible_reference_points"] += weight
        strata_counts[stratum]["visible_reference_points"] += 1
        strata_counts[stratum]["weighted_visible_reference_points"] += weight
        mapping = identity[(sid, person)]
        if mapping["status"] != "matched":
            counts[mapping["status"] + "_points"] += 1
            counts["weighted_" + mapping["status"] + "_points"] += weight
            strata_counts[stratum][mapping["status"] + "_points"] += 1
            strata_counts[stratum]["weighted_" + mapping["status"] + "_points"] += weight
            continue
        point = model[sid]["detections_by_id"][mapping["track_id"]]["keypoints"][joint]
        distance = math.hypot(point["x_px"] - ref["x"], point["y_px"] - ref["y"])
        distances[joint].append((distance, weight))
        strata_distances[stratum].append((distance, weight))
        group = "ge_0p5" if point["confidence"] >= 0.5 else "lt_0p5"
        confidence_groups[group].append(distance)
        counts["matched_visible_points"] += 1
        counts["weighted_matched_visible_points"] += weight
        strata_counts[stratum]["matched_visible_points"] += 1
        strata_counts[stratum]["weighted_matched_visible_points"] += weight
    def summarize(pairs: list[tuple[float, int]]) -> dict:
        vals = [v for v, _ in pairs]
        weighted_n = sum(w for _, w in pairs)
        return {"points": len(vals), "weighted_point_frames": weighted_n,
                "median_px": percentile(vals, 0.5), "p95_px": percentile(vals, 0.95),
                "weighted_mean_px": round(sum(v * w for v, w in pairs) / weighted_n, 3)
                if weighted_n else None}
    all_pairs = [pair for pairs in distances.values() for pair in pairs]
    def with_rate(items: Counter) -> dict:
        result = dict(items)
        denominator = items["weighted_visible_reference_points"]
        result["weighted_matched_fraction_of_visible"] = (
            fraction(items["weighted_matched_visible_points"], denominator)
            if denominator else None)
        return result
    return {"reference_denominator_and_mapping": dict(counts),
            "weighted_matched_fraction_of_visible": (
                fraction(counts["weighted_matched_visible_points"],
                         counts["weighted_visible_reference_points"])
                if counts["weighted_visible_reference_points"] else None),
            "pixel_error_conditional_on_visible_and_matched": {
                "all": summarize(all_pairs),
                "per_joint": {joint: summarize(distances[joint]) for joint in JOINTS},
                "per_stratum": {stratum: {"mapping": with_rate(strata_counts[stratum]),
                                           "error": summarize(strata_distances[stratum])}
                                for stratum in ("early", "late")},
                "by_model_confidence": {
                    group: {"points": len(vals), "median_px": percentile(vals, 0.5)}
                    for group, vals in confidence_groups.items()}}}


def compare(samples: dict, model: dict, identity: dict,
            ref1: dict, ref2: dict) -> dict:
    counts = Counter(row["status"] for row in identity.values())
    matched_ids_by_person = {person: [] for person in PERSONS}
    for sid in sorted(model):
        for person in PERSONS:
            row = identity[(sid, person)]
            if row["status"] == "matched":
                matched_ids_by_person[person].append(row["track_id"])
    transitions = {
        person: {"distinct_ids_in_sample": len(set(ids)),
                 "changes_between_successive_matched_samples": sum(a != b for a, b in zip(ids, ids[1:]))}
        for person, ids in matched_ids_by_person.items()
    }
    unassigned = sum(len(model[sid]["detections_by_id"]) - sum(
        identity[(sid, p)]["status"] == "matched" for p in PERSONS) for sid in model)
    return {
        "design": {"sampled_frames": len(samples), "source_frames": sum(
            s["design_weight_frames"] for s in samples.values()),
            "reference": "two independent 2D coders; original annotations kept separate"},
        "identity_review": {"person_sample_rows": len(identity), "statuses": dict(counts),
                            "unassigned_model_detections": unassigned,
                            "sampled_track_continuity": transitions},
        "coder_1": report_for_coder(ref1, identity, model, samples),
        "coder_2": report_for_coder(ref2, identity, model, samples),
        "limits": "Error en píxeles condicionado a punto visible e identidad asignada; faltantes y ambiguos quedan en denominador separado. La muestra no valida 3D, soga, belleza ni HIT.",
    }


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest="command", required=True)
    prep = sub.add_parser("prepare", help="Crear CSV privado de identidad vacío")
    comp = sub.add_parser("compare", help="Emitir sólo agregados de comparación")
    for parser in (prep, comp):
        parser.add_argument("manifest", type=Path)
        parser.add_argument("model_export", type=Path)
    prep.add_argument("identity_csv", type=Path)
    prep.add_argument("--overlays-dir", type=Path,
                      help="Opcional: 40 imágenes privadas con puntos/track ID para revisión")
    comp.add_argument("coder_1_csv", type=Path)
    comp.add_argument("coder_2_csv", type=Path)
    comp.add_argument("identity_csv", type=Path)
    args = ap.parse_args()
    manifest, samples = load_manifest(args.manifest)
    model = load_model(args.model_export, manifest, samples)
    if args.command == "prepare":
        if private_path(args.identity_csv).exists():
            raise ValueError("No se sobrescribe una revisión de identidad existente")
        if args.overlays_dir is not None:
            overlay_path = private_path(args.overlays_dir)
            if overlay_path.exists() and any(overlay_path.iterdir()):
                raise ValueError("No se sobrescriben vistas de revisión existentes")
        if args.overlays_dir is not None:
            render_overlays(args.overlays_dir, model, samples, args.manifest)
        prepare(args.identity_csv, model)
        return
    first, id1 = load_coder(args.coder_1_csv, set(samples), manifest["source_dimensions_px"])
    second, id2 = load_coder(args.coder_2_csv, set(samples), manifest["source_dimensions_px"])
    if id1 == id2 or args.coder_1_csv.resolve() == args.coder_2_csv.resolve():
        raise ValueError("Se requieren dos observadores de referencia distintos")
    identity = load_identity(args.identity_csv, model)
    print(json.dumps(compare(samples, model, identity, first, second),
                     indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
