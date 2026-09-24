#!/usr/bin/env python3
"""Inspección instrumental de originales de video; no mide movimiento humano.

Uso: python3 inspeccionar_video.py archivo.mp4 [otro.mov ...]
Entrega un objeto JSON por archivo en stdout. Requiere ffprobe en PATH.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
import shutil
import statistics
import subprocess
import sys


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def as_float(value: object) -> float | None:
    try:
        result = float(value)
    except (TypeError, ValueError):
        return None
    return result if math.isfinite(result) else None


def inspect(path: Path) -> dict[str, object]:
    command = [
        "ffprobe", "-v", "error", "-select_streams", "v:0",
        "-show_streams", "-show_frames", "-show_entries",
        "stream=codec_name,width,height,r_frame_rate,avg_frame_rate,time_base,nb_frames:"
        "frame=best_effort_timestamp_time,pts_time,pkt_duration_time",
        "-of", "json", str(path),
    ]
    process = subprocess.run(command, capture_output=True, text=True, check=False)
    if process.returncode:
        raise ValueError(f"ffprobe falló: {process.stderr.strip()[:500]}")
    data = json.loads(process.stdout)
    streams = data.get("streams", [])
    if not streams:
        raise ValueError("No se encontró pista de video v:0")
    stream = streams[0]
    frames = data.get("frames", [])
    frame_times: list[float | None] = []
    for frame in frames:
        value = as_float(frame.get("best_effort_timestamp_time"))
        if value is None:
            value = as_float(frame.get("pts_time"))
        frame_times.append(value)
    pts = [value for value in frame_times if value is not None]
    missing_pts = len(frame_times) - len(pts)
    # No unir PTS a través de cuadros sin timestamp: el salto no identifica
    # ni duración entre cuadros consecutivos ni pérdida de captura.
    adjacent_pairs = [(a, b) for a, b in zip(frame_times, frame_times[1:])
                      if a is not None and b is not None]
    deltas = [b - a for a, b in adjacent_pairs]
    untimed_runs = 0
    in_run = False
    for value in frame_times:
        if value is None and not in_run:
            untimed_runs += 1
            in_run = True
        elif value is not None:
            in_run = False
    positive = [d for d in deltas if d > 0]
    median = statistics.median(positive) if positive else None
    # Intervalos largos son indicios para revisar; VFR no implica cuadros perdidos.
    long_intervals = sum(d > 1.5 * median for d in positive) if median else None
    report: dict[str, object] = {
        "schema": "ropeflow_video_inspection_v0.2",
        "sha256": sha256_file(path),
        "size_bytes": path.stat().st_size,
        "video_stream": {
            "codec": stream.get("codec_name"),
            "width_px": stream.get("width"),
            "height_px": stream.get("height"),
            "r_frame_rate_metadata": stream.get("r_frame_rate"),
            "avg_frame_rate_metadata": stream.get("avg_frame_rate"),
            "time_base": stream.get("time_base"),
            "nb_frames_metadata": stream.get("nb_frames"),
        },
        "decoded_frames": len(frames),
        "frames_without_pts": missing_pts,
        "untimed_runs": untimed_runs,
        "adjacent_timed_pairs": len(adjacent_pairs),
        "first_pts_s": pts[0] if pts else None,
        "last_pts_s": pts[-1] if pts else None,
        "nonpositive_pts_intervals": sum(d <= 0 for d in deltas),
        "median_positive_interval_s": median,
        "min_positive_interval_s": min(positive) if positive else None,
        "max_positive_interval_s": max(positive) if positive else None,
        "intervals_over_1_5x_median": long_intervals,
        "notes": [
            "PTS y FPS son relativos al archivo y pueden ser estimados o reescritos: no sincronizan cámaras ni miden deriva entre relojes.",
            "Un intervalo largo puede ser VFR deliberado, conversión o pérdida; requiere revisar original y cámara.",
            "Los intervalos se calculan sólo entre cuadros consecutivos con PTS; los huecos sin PTS se informan aparte.",
            "El hash identifica bytes originales; una transcodificación genera otro identificador.",
        ],
    }
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("videos", nargs="+", type=Path)
    args = parser.parse_args()
    if shutil.which("ffprobe") is None:
        parser.error("Se requiere ffprobe en PATH")
    failed = False
    for path in args.videos:
        try:
            result = inspect(path)
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            result = {"schema": "ropeflow_video_inspection_v0.2", "error": str(exc)}
            failed = True
        print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
