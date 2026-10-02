#!/usr/bin/env python3
"""Coteja cuadros OpenCV y FFmpeg/PTS sin publicar ni guardar imágenes."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path

import cv2
import numpy as np


def pts_originales(path: Path) -> np.ndarray:
    raw = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0",
         "-show_entries", "frame=best_effort_timestamp_time", "-of", "csv=p=0", str(path)],
        check=True, capture_output=True,
    ).stdout
    return np.array([float(x) for x in raw.splitlines() if x.strip()], dtype=float)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("video", type=Path)
    ap.add_argument("--start-pts", type=float, required=True)
    ap.add_argument("--end-pts", type=float, required=True)
    args = ap.parse_args()
    if args.end_pts <= args.start_pts:
        ap.error("intervalo temporal no vacío requerido")

    pts = pts_originales(args.video)
    selected = np.flatnonzero((pts >= args.start_pts) & (pts < args.end_pts))
    if not len(selected) or selected[-1] - selected[0] + 1 != len(selected):
        raise ValueError("Intervalo sin cuadros contiguos")
    cap = cv2.VideoCapture(str(args.video))
    if not cap.isOpened() or not cap.set(cv2.CAP_PROP_POS_FRAMES, int(selected[0])):
        raise RuntimeError("OpenCV no pudo abrir o buscar el cuadro inicial")
    w, h = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frame_bytes = w * h * 3
    filt = f"select=between(n\\,{selected[0]}\\,{selected[-1]}),format=bgr24"
    proc = subprocess.Popen(
        ["ffmpeg", "-v", "error", "-i", str(args.video), "-map", "0:v:0",
         "-an", "-sn", "-dn", "-vf", filt, "-fps_mode", "passthrough",
         "-f", "rawvideo", "-pix_fmt", "bgr24", "-"],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    assert proc.stdout is not None and proc.stderr is not None
    equal = 0
    max_mae = 0.0
    offsets = []
    try:
        for idx in selected:
            chunk = proc.stdout.read(frame_bytes)
            if len(chunk) != frame_bytes:
                raise RuntimeError(f"FFmpeg no entregó el cuadro completo {idx}")
            ok, cv_frame = cap.read()
            if not ok or int(cap.get(cv2.CAP_PROP_POS_FRAMES)) != idx + 1:
                raise RuntimeError(f"OpenCV no entregó el cuadro esperado {idx}")
            ff_frame = np.frombuffer(chunk, dtype=np.uint8).reshape((h, w, 3))
            equal += int(np.array_equal(cv_frame, ff_frame))
            max_mae = max(max_mae, float(np.mean(np.abs(
                cv_frame.astype(np.int16) - ff_frame.astype(np.int16)))))
            offsets.append(float(pts[idx] - cap.get(cv2.CAP_PROP_POS_MSEC) / 1000))
        if proc.stdout.read(1):
            raise RuntimeError("FFmpeg entregó cuadros adicionales")
        error = proc.stderr.read().decode("utf-8", errors="replace")
        if proc.wait() != 0:
            raise RuntimeError(f"FFmpeg falló: {error[-500:]}")
    finally:
        cap.release()
        if proc.poll() is None:
            proc.kill()
            proc.wait()

    sha = hashlib.sha256()
    with args.video.open("rb") as stream:
        for part in iter(lambda: stream.read(1024 * 1024), b""):
            sha.update(part)
    print(json.dumps({
        "video_sha256": sha.hexdigest(),
        "source_frames": len(selected),
        "source_index_first": int(selected[0]),
        "source_index_last": int(selected[-1]),
        "pixel_exact_equal_frames": equal,
        "max_mean_absolute_pixel_difference": max_mae,
        "pts_minus_opencv_pos_s_first": offsets[0],
        "pts_minus_opencv_pos_s_min": min(offsets),
        "pts_minus_opencv_pos_s_max": max(offsets),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
