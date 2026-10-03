#!/usr/bin/env python3
"""Compara orientación/PTS de OpenCV, FFmpeg, HarMoCAP y Weaver R08."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import sys
import tempfile

import cv2
import numpy as np


def capture(args: list[str], data: bytes | None = None) -> bytes:
    return subprocess.run(args, input=data, capture_output=True, check=True).stdout


def decode_cv(path: Path, autorotate: bool = True) -> tuple[list[np.ndarray], float, float]:
    cap = cv2.VideoCapture(str(path))
    if not cap.isOpened():
        raise ValueError("OpenCV no abrió el medio")
    orientation = cap.get(cv2.CAP_PROP_ORIENTATION_META)
    if not autorotate:
        assert cap.set(cv2.CAP_PROP_ORIENTATION_AUTO, 0)
    auto_state = cap.get(cv2.CAP_PROP_ORIENTATION_AUTO)
    frames = []
    while True:
        ok, bgr = cap.read()
        if not ok:
            break
        frames.append(cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB))
    cap.release()
    return frames, orientation, auto_state


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--harmocap-repo", type=Path, required=True)
    parser.add_argument("--weaver-repo", type=Path, required=True)
    args = parser.parse_args()
    harmocap = args.harmocap_repo.resolve()
    weaver = args.weaver_repo.resolve()
    sys.path[:0] = [str(harmocap / "src"), str(weaver / "src")]
    from harmocap.webapp.offline_time import probe_video_timeline
    from harmonic_weaver.lab.research.rope_media import probe as rope_probe

    width, height, count = 64, 32, 4
    source_frames = []
    for i in range(count):
        frame = np.zeros((height, width, 3), dtype=np.uint8)
        frame[3 + i:8 + i, 4:9] = (255, 0, 0)
        frame[20:25, 45 + i:50 + i] = (0, 0, 255)
        source_frames.append(frame)

    with tempfile.TemporaryDirectory(prefix="rotacion-pts-sintetica-") as directory:
        base = Path(directory) / "base.mp4"
        rotated = Path(directory) / "rotation_metadata_90.mp4"
        capture(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo",
                 "-pixel_format", "rgb24", "-video_size", f"{width}x{height}",
                 "-framerate", "10", "-i", "pipe:0", "-c:v", "libx264rgb",
                 "-crf", "0", "-pix_fmt", "rgb24", str(base)],
                b"".join(frame.tobytes() for frame in source_frames))
        capture(["ffmpeg", "-y", "-v", "error", "-display_rotation", "90",
                 "-i", str(base), "-c", "copy", str(rotated)])
        info = json.loads(capture(["ffprobe", "-v", "error", "-select_streams", "v:0",
                                   "-show_streams", "-show_frames", "-show_entries",
                                   "stream=width,height,time_base:stream_side_data=rotation:frame=best_effort_timestamp_time",
                                   "-of", "json", str(rotated)]))
        rotation = info["streams"][0]["side_data_list"][0]["rotation"]
        assert rotation == 90
        pts = [float(frame["best_effort_timestamp_time"]) for frame in info["frames"]]
        assert pts == [0.0, 0.1, 0.2, 0.3]

        plain_timeline = probe_video_timeline(base)
        rotated_timeline = probe_video_timeline(rotated)
        assert plain_timeline.ticks == rotated_timeline.ticks
        assert plain_timeline.time_base == rotated_timeline.time_base
        assert len(plain_timeline.ticks) == count

        cv_auto, cv_meta, auto_state = decode_cv(rotated)
        cv_raw, _, raw_state = decode_cv(rotated, autorotate=False)
        assert auto_state == 1 and raw_state == 0
        assert len(cv_auto) == len(cv_raw) == count
        assert all(frame.shape == (width, height, 3) for frame in cv_auto)
        assert all(frame.shape == (height, width, 3) for frame in cv_raw)

        ff_auto = np.frombuffer(capture(["ffmpeg", "-v", "error", "-i", str(rotated),
                                          "-f", "rawvideo", "-pix_fmt", "rgb24", "pipe:1"]),
                                dtype=np.uint8).reshape(count, width, height, 3)
        ff_raw = np.frombuffer(capture(["ffmpeg", "-v", "error", "-noautorotate",
                                         "-i", str(rotated), "-f", "rawvideo",
                                         "-pix_fmt", "rgb24", "pipe:1"]),
                               dtype=np.uint8).reshape(count, height, width, 3)
        assert all(np.array_equal(a, b) for a, b in zip(cv_auto, ff_auto))
        assert all(np.array_equal(a, b) for a, b in zip(cv_raw, ff_raw))
        assert all(np.array_equal(a, b) for a, b in zip(ff_raw, source_frames))
        assert all(np.array_equal(np.rot90(a), b) for a, b in zip(ff_raw, ff_auto))

        assert len(rope_probe(base)["frame_times_s"]) == count
        try:
            rope_probe(rotated)
        except ValueError as exc:
            assert "Rotated media requires explicit display-coordinate adapter" in str(exc)
            r08_rotated = "rejected_display_rotation"
        else:
            raise AssertionError("R08 aceptó un medio rotado sin adaptador")

        report = {
            "fixture": "four asymmetric RGB frames; rotation display matrix 90 degrees",
            "source_sha256": plain_timeline.source_sha256,
            "rotated_sha256": rotated_timeline.source_sha256,
            "source_pts_ticks": list(plain_timeline.ticks),
            "source_time_base": plain_timeline.time_base_text,
            "ffprobe_rotation_deg": rotation,
            "opencv_orientation_meta_deg": cv_meta,
            "opencv_version": cv2.__version__,
            "opencv_auto_shape_yx": list(cv_auto[0].shape[:2]),
            "opencv_raw_shape_yx": list(cv_raw[0].shape[:2]),
            "opencv_auto_equals_ffmpeg_auto_all_frames": True,
            "opencv_raw_equals_ffmpeg_noautorotate_all_frames": True,
            "r08_rotated": r08_rotated,
            "not": ["PyAV worker runtime", "physical camera", "pose accuracy", "Beacon audio"],
        }
        print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
