#!/usr/bin/env python3
"""Resumen técnico de un video original; no estima pose ni calidad de movimiento."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path

import numpy as np


def ejecutar(*args: str) -> bytes:
    proc = subprocess.run(args, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return proc.stdout


def cuadros_pts(path: Path) -> np.ndarray:
    raw = ejecutar(
        "ffprobe", "-v", "error", "-select_streams", "v:0",
        "-show_entries", "frame=best_effort_timestamp_time", "-of", "csv=p=0", str(path),
    )
    return np.array([float(line) for line in raw.splitlines() if line.strip()], dtype=float)


def diferencias_grises(path: Path, lado: int) -> np.ndarray:
    frame_bytes = lado * lado
    command = [
        "ffmpeg", "-v", "error", "-i", str(path), "-map", "0:v:0", "-an", "-sn", "-dn",
        "-fps_mode", "passthrough", "-vf", f"scale={lado}:{lado},format=gray",
        "-f", "rawvideo", "-pix_fmt", "gray", "-",
    ]
    proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    assert proc.stdout is not None and proc.stderr is not None
    previous = None
    differences: list[float] = []
    count = 0
    while True:
        chunk = proc.stdout.read(frame_bytes)
        if not chunk:
            break
        if len(chunk) != frame_bytes:
            proc.kill()
            raise RuntimeError("Cuadro gris incompleto")
        current = np.frombuffer(chunk, dtype=np.uint8).astype(np.int16)
        if previous is not None:
            differences.append(float(np.mean(np.abs(current - previous)) / 255.0))
        previous = current
        count += 1
    error = proc.stderr.read().decode("utf-8", errors="replace")
    if proc.wait() != 0:
        raise RuntimeError(f"ffmpeg falló: {error[-500:]}")
    if count != len(differences) + 1:
        raise RuntimeError("Conteo de cuadros internos inconsistente")
    return np.array(differences, dtype=float)


def resumen(path: Path, lado: int) -> dict:
    pts = cuadros_pts(path)
    differences = diferencias_grises(path, lado)
    if len(pts) < 2 or len(differences) != len(pts) - 1:
        raise RuntimeError(f"PTS y cuadros decodificados no coinciden: {len(pts)} / {len(differences) + 1}")
    intervals = np.diff(pts)
    if not np.all(intervals > 0):
        raise RuntimeError("PTS repetidos o no monótonos: revisar original")
    sha = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            sha.update(chunk)
    largest = np.argsort(differences)[-5:][::-1]
    return {
        "sha256": sha.hexdigest(),
        "decoded_frames": len(pts),
        "pts_first_s": float(pts[0]),
        "pts_last_s": float(pts[-1]),
        "interval_median_ms": float(np.median(intervals) * 1000),
        "interval_max_ms": float(np.max(intervals) * 1000),
        "gray_side_px": lado,
        "frame_difference_definition": "mean(abs(gray_t-gray_prev))/255 at reduced resolution; includes camera and scene motion",
        "frame_difference_median": float(np.median(differences)),
        "frame_difference_p95": float(np.percentile(differences, 95)),
        "frame_difference_p99": float(np.percentile(differences, 99)),
        "frame_difference_max": float(np.max(differences)),
        "top_difference_pts_s": [float(pts[i + 1]) for i in largest],
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("video", type=Path, help="Original local; nunca se publica ni modifica")
    parser.add_argument("--gray-side", type=int, default=64)
    args = parser.parse_args()
    if args.gray_side < 8:
        parser.error("--gray-side debe ser al menos 8")
    print(json.dumps(resumen(args.video, args.gray_side), ensure_ascii=False, indent=2))
