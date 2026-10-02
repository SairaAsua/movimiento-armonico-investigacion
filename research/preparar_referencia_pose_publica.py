#!/usr/bin/env python3
"""Prepara fuera de Git una muestra ciega de cuadros para referencia 2D.

Nunca incluye predicciones del modelo. El directorio de salida contiene imágenes
de personas y debe mantenerse privado; se rechaza una ruta dentro del repo.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import random
import subprocess
from pathlib import Path

import cv2


SOURCE_URL = "https://commons.wikimedia.org/wiki/File:Persona_dance_rehearsal.webm"
SOURCE_SHA256 = "573ac41a261d71fc59fbf890d129964061f3c9346bcf6fcf5b4cecb3217e05aa"
JOINTS = ("shoulder_l", "shoulder_r", "wrist_l", "wrist_r", "hip_l", "hip_r")


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def timestamps(path: Path) -> list[float]:
    raw = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0",
         "-show_entries", "frame=best_effort_timestamp_time", "-of", "csv=p=0", str(path)],
        check=True, capture_output=True,
    ).stdout
    return [float(x) for x in raw.splitlines() if x.strip()]


def seleccionar(indices: list[int], n_bins: int, rng: random.Random, stratum: str) -> list[dict]:
    if len(indices) < n_bins:
        raise ValueError(f"{stratum}: menos cuadros que bins solicitados")
    result = []
    for b in range(n_bins):
        lo, hi = b * len(indices) // n_bins, (b + 1) * len(indices) // n_bins
        candidates = indices[lo:hi]
        result.append({"source_frame_index": rng.choice(candidates),
                       "stratum": stratum, "bin_index": b,
                       "bin_frames": len(candidates),
                       "design_weight_frames": len(candidates)})
    return result


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("video", type=Path)
    ap.add_argument("out_dir", type=Path)
    ap.add_argument("--expected-sha256", required=True)
    ap.add_argument("--start-pts", type=float, default=152)
    ap.add_argument("--split-pts", type=float, default=160)
    ap.add_argument("--end-pts", type=float, default=174)
    ap.add_argument("--per-stratum", type=int, default=20)
    ap.add_argument("--seed", type=int, default=20261002)
    args = ap.parse_args()
    repo = Path(__file__).resolve().parents[1]
    out = args.out_dir.resolve()
    if out == repo or repo in out.parents:
        ap.error("la salida con imágenes debe quedar fuera del repositorio público")
    if out.exists() and any(out.iterdir()):
        ap.error("el directorio de salida debe estar vacío para no sobrescribir anotaciones")
    if not (args.start_pts < args.split_pts < args.end_pts) or args.per_stratum < 1:
        ap.error("se requieren dos estratos temporales no vacíos y bins positivos")
    if args.expected_sha256.lower() != SOURCE_SHA256:
        ap.error("este paquete corresponde sólo al original de Commons citado")
    source_hash = digest(args.video)
    if source_hash.lower() != args.expected_sha256.lower():
        raise ValueError("SHA-256 del original no coincide con el esperado")
    pts = timestamps(args.video)
    if len(pts) < 2 or any(b <= a for a, b in zip(pts, pts[1:])):
        raise ValueError("PTS faltantes o no monótonos")
    early = [i for i, t in enumerate(pts) if args.start_pts <= t < args.split_pts]
    late = [i for i, t in enumerate(pts) if args.split_pts <= t < args.end_pts]
    rng = random.Random(args.seed)
    chosen = (seleccionar(early, args.per_stratum, rng, "early")
              + seleccionar(late, args.per_stratum, rng, "late"))
    chosen.sort(key=lambda row: row["source_frame_index"])
    out.mkdir(parents=True, exist_ok=True)
    frames_dir = out / "frames"
    frames_dir.mkdir()
    cap = cv2.VideoCapture(str(args.video))
    if not cap.isOpened():
        raise RuntimeError("OpenCV no pudo abrir el original")
    width, height = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    template = []
    for k, item in enumerate(chosen, start=1):
        idx = item["source_frame_index"]
        if not cap.set(cv2.CAP_PROP_POS_FRAMES, idx):
            raise RuntimeError(f"OpenCV no pudo buscar el cuadro {idx}")
        ok, frame = cap.read()
        if not ok or int(cap.get(cv2.CAP_PROP_POS_FRAMES)) != idx + 1:
            raise RuntimeError(f"OpenCV no entregó el cuadro {idx}")
        name = f"sample_{k:03d}.png"
        image_path = frames_dir / name
        if not cv2.imwrite(str(image_path), frame):
            raise RuntimeError(f"No se pudo escribir {name}")
        item.update({"sample_id": f"S{k:03d}", "pts_s": pts[idx],
                     "image": f"frames/{name}", "image_sha256": digest(image_path)})
        for person in ("A", "B"):
            for joint in JOINTS:
                template.append({"sample_id": item["sample_id"], "person": person,
                                 "joint": joint, "status": "", "x_px": "", "y_px": "",
                                 "uncertainty_px": "", "coder_id": "", "note": ""})
    cap.release()
    manifest = {
        "protocol": "reference_pose_public_video_v0.1",
        "source_url": SOURCE_URL,
        "source_license_as_listed": "CC BY-SA 4.0",
        "source_sha256": source_hash,
        "source_dimensions_px": [width, height],
        "selection": "One uniformly random source frame from each equal-count bin within each PTS stratum; no model scores used",
        "seed": args.seed, "per_stratum": args.per_stratum,
        "strata_source_frames": {"early": len(early), "late": len(late)},
        "samples": chosen,
    }
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")
    with (out / "annotation_template.csv").open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(template[0]))
        writer.writeheader()
        writer.writerows(template)
    (out / "README_PRIVATE.txt").write_text(
        "Paquete de imágenes de personas para anotación privada. No subir a GitHub.\n"
        f"Original: {SOURCE_URL}\nLicencia publicada: CC BY-SA 4.0; conservar atribución.\n"
        "Cada codificador trabaja en copia separada de annotation_template.csv y no ve poses del modelo.\n"
    )
    print(json.dumps({"samples": len(chosen), "template_rows": len(template),
                      "strata_source_frames": manifest["strata_source_frames"],
                      "source_sha256": source_hash, "out_dir": str(out)}, indent=2))


if __name__ == "__main__":
    main()
