#!/usr/bin/env python3
"""Audita correspondencia exacta de PTS y píxeles visibles entre dos videos.

Uso: python auditar_derivado_video.py ORIGINAL DERIVADO --harmocap-repo PATH
Imprime sólo metadatos y diferencias; no guarda ni publica cuadros.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys

import cv2
import numpy as np


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def read_visible_frames(path: Path):
    cap = cv2.VideoCapture(str(path))
    if not cap.isOpened():
        raise ValueError("OpenCV no abrió el video")
    if not cap.set(cv2.CAP_PROP_ORIENTATION_AUTO, 1):
        cap.release()
        raise ValueError("OpenCV no pudo activar la orientación de visualización")
    if cap.get(cv2.CAP_PROP_ORIENTATION_AUTO) != 1:
        cap.release()
        raise ValueError("OpenCV no confirmó la orientación de visualización")
    try:
        while True:
            ok, bgr = cap.read()
            if not ok:
                break
            yield bgr
    finally:
        cap.release()


def audit(source: Path, derived: Path, probe_video_timeline) -> dict:
    original = probe_video_timeline(source)
    converted = probe_video_timeline(derived)
    original_times = [tick * original.time_base for tick in original.ticks]
    converted_times = [tick * converted.time_base for tick in converted.ticks]
    n_common = min(len(original_times), len(converted_times))
    first_time_mismatch = next((i for i in range(n_common)
                                if original_times[i] != converted_times[i]), None)
    if first_time_mismatch is None and len(original_times) != len(converted_times):
        first_time_mismatch = n_common

    source_frames = read_visible_frames(source)
    derived_frames = read_visible_frames(derived)
    first_pixel_mismatch = None
    source_count = derived_count = 0
    first_source_shape = first_derived_shape = None
    index = 0
    while True:
        try:
            src = next(source_frames)
        except StopIteration:
            src = None
        try:
            dst = next(derived_frames)
        except StopIteration:
            dst = None
        if src is None and dst is None:
            break
        if src is not None:
            source_count += 1
            first_source_shape = first_source_shape or list(src.shape)
        if dst is not None:
            derived_count += 1
            first_derived_shape = first_derived_shape or list(dst.shape)
        if first_pixel_mismatch is None and (src is None or dst is None or
                                             src.shape != dst.shape or
                                             not np.array_equal(src, dst)):
            first_pixel_mismatch = index
        index += 1

    # El inventario ffprobe y la decodificación deben referirse al mismo número de cuadros.
    inventory_matches_decode = (source_count == len(original_times) and
                                derived_count == len(converted_times))
    files_stable = (file_sha256(source) == original.source_sha256 and
                    file_sha256(derived) == converted.source_sha256)
    passed = (first_time_mismatch is None and first_pixel_mismatch is None and
              inventory_matches_decode and files_stable)
    return {
        "schema": "visible_video_derivative_audit_v0.1",
        "exact_match": passed,
        "source_sha256": original.source_sha256,
        "derived_sha256": converted.source_sha256,
        "source_time_base": original.time_base_text,
        "derived_time_base": converted.time_base_text,
        "source_pts_count": len(original_times),
        "derived_pts_count": len(converted_times),
        "source_decoded_count": source_count,
        "derived_decoded_count": derived_count,
        "source_visible_shape_yxc": first_source_shape,
        "derived_visible_shape_yxc": first_derived_shape,
        "first_pts_mismatch_index": first_time_mismatch,
        "first_pixel_mismatch_index": first_pixel_mismatch,
        "inventory_matches_decode": inventory_matches_decode,
        "files_stable_during_audit": files_stable,
        "opencv_version": cv2.__version__,
        "scope": "Exact display-pixel/PTS lineage in this decoder; not camera sync or anatomical validity",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("derived", type=Path)
    parser.add_argument("--harmocap-repo", type=Path, required=True)
    args = parser.parse_args()
    sys.path.insert(0, str(args.harmocap_repo.resolve() / "src"))
    from harmocap.webapp.offline_time import probe_video_timeline

    report = audit(args.source, args.derived, probe_video_timeline)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["exact_match"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
