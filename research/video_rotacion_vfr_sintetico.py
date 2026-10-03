#!/usr/bin/env python3
"""Comprueba que hornear una rotación no fabrique cuadros en video VFR."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
import tempfile

import cv2
import numpy as np

from auditar_derivado_video import audit
from video_rotacion_pts_sintetico import capture, decode_cv


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--harmocap-repo", type=Path, required=True)
    parser.add_argument("--weaver-repo", type=Path, required=True)
    parser.add_argument("--check-r09", action="store_true",
                        help="ejecutar file_frames() real; requiere PyAV en el entorno")
    args = parser.parse_args()
    sys.path[:0] = [str(args.harmocap_repo.resolve() / "src"),
                    str(args.weaver_repo.resolve() / "src")]
    from harmocap.webapp.offline_time import probe_video_timeline
    from harmonic_weaver.lab.research.rope_media import probe as rope_probe
    if args.check_r09:
        from harmonic_weaver.lab.research.rope_media import frame_png as rope_frame_png
        from harmonic_weaver.lab.perception_worker import file_frames

    width, height = 64, 32
    frames = []
    for i in range(4):
        frame = np.zeros((height, width, 3), dtype=np.uint8)
        frame[3 + i:8 + i, 4:9] = (255, 0, 0)
        frame[20:25, 45 + i:50 + i] = (0, 0, 255)
        frames.append(frame)

    with tempfile.TemporaryDirectory(prefix="rotacion-vfr-sintetica-") as directory:
        directory = Path(directory)
        base = directory / "base_cfr.mp4"
        source = directory / "source_vfr.mp4"
        rotated = directory / "rotation_vfr.mp4"
        default = directory / "baked_default.mp4"
        preserved = directory / "baked_vfr.mp4"
        changed_pixels = directory / "baked_vfr_changed_pixels.mp4"
        capture(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo",
                 "-pixel_format", "rgb24", "-video_size", f"{width}x{height}",
                 "-framerate", "10", "-i", "pipe:0", "-c:v", "libx264rgb",
                 "-crf", "0", "-pix_fmt", "rgb24", "-video_track_timescale", "10240",
                 str(base)], b"".join(frame.tobytes() for frame in frames))
        # Fijar la base del filtro en 1/10 s: PTS 0, 1, 3 y 6.
        capture(["ffmpeg", "-y", "-v", "error", "-i", str(base),
                 "-vf", r"settb=1/10,setpts=if(eq(N\,0)\,0\,if(eq(N\,1)\,1\,if(eq(N\,2)\,3\,6)))",
                 "-fps_mode", "vfr", "-c:v", "libx264rgb", "-crf", "0",
                 "-pix_fmt", "rgb24", "-video_track_timescale", "10240",
                 str(source)])
        capture(["ffmpeg", "-y", "-v", "error", "-display_rotation", "90",
                 "-i", str(source), "-c", "copy", str(rotated)])

        def bake(path: Path, fps_mode: str | None) -> None:
            command = ["ffmpeg", "-y", "-v", "error", "-i", str(rotated),
                       "-map", "0:v:0", "-an", "-c:v", "libx264rgb",
                       "-crf", "0", "-pix_fmt", "rgb24",
                       "-video_track_timescale", "10240"]
            if fps_mode:
                command += ["-fps_mode", fps_mode]
            capture(command + [str(path)])

        bake(default, None)
        bake(preserved, "vfr")
        capture(["ffmpeg", "-y", "-v", "error", "-i", str(preserved),
                 "-vf", "drawbox=x=0:y=0:w=4:h=4:color=white:t=fill",
                 "-fps_mode", "vfr", "-c:v", "libx264rgb", "-crf", "0",
                 "-pix_fmt", "rgb24", "-video_track_timescale", "10240",
                 str(changed_pixels)])

        src_time = probe_video_timeline(source)
        rotated_time = probe_video_timeline(rotated)
        default_time = probe_video_timeline(default)
        preserved_time = probe_video_timeline(preserved)
        assert src_time.time_base_text == rotated_time.time_base_text == "1/10240"
        assert src_time.ticks == rotated_time.ticks == (0, 1024, 3072, 6144)
        assert default_time.ticks == (0, 1024, 2048, 3072, 4096, 5120, 6144)
        assert preserved_time.time_base == rotated_time.time_base
        assert preserved_time.ticks == rotated_time.ticks

        shown, _, _ = decode_cv(rotated)
        default_frames, _, _ = decode_cv(default)
        preserved_frames, preserved_rotation, _ = decode_cv(preserved)
        assert len(shown) == len(preserved_frames) == 4
        assert len(default_frames) == 7
        assert all(np.array_equal(a, b) for a, b in zip(shown, preserved_frames))
        assert preserved_rotation == 0
        assert rope_probe(default)["frame_times_s"] == [tick / 10240 for tick in default_time.ticks]
        assert rope_probe(preserved)["frame_times_s"] == [0.0, 0.1, 0.3, 0.6]
        default_audit = audit(rotated, default, probe_video_timeline)
        preserved_audit = audit(rotated, preserved, probe_video_timeline)
        assert not default_audit["exact_match"]
        assert default_audit["first_pts_mismatch_index"] == 2
        assert default_audit["first_pixel_mismatch_index"] == 2
        assert preserved_audit["exact_match"]
        assert preserved_audit["source_pts_count"] == 4
        assert preserved_audit["derived_pts_count"] == 4
        changed_audit = audit(rotated, changed_pixels, probe_video_timeline)
        assert not changed_audit["exact_match"]
        assert changed_audit["first_pts_mismatch_index"] is None
        assert changed_audit["first_pixel_mismatch_index"] == 0

        r09_report = {"checked": False}
        if args.check_r09:
            import av

            def check_r09(path: Path, expected_frames: list[np.ndarray], ticks: tuple[int, ...]) -> list[tuple]:
                decoded = list(file_frames(path))
                assert len(decoded) == len(expected_frames) == len(ticks)
                for (bgr, timing), rgb, tick in zip(decoded, expected_frames, ticks):
                    assert np.array_equal(bgr[:, :, ::-1], rgb)
                    assert timing["source_pts"] == tick
                    assert (timing["time_base_num"], timing["time_base_den"]) == (1, 10240)
                    assert timing["source_time_s"] == tick / 10240
                    assert timing["timestamp_origin"] == "pts"
                return decoded

            check_r09(rotated, shown, rotated_time.ticks)
            default_r09 = check_r09(default, default_frames, default_time.ticks)
            preserved_r09 = check_r09(preserved, preserved_frames, preserved_time.ticks)
            for path, sha256, decoded in ((default, default_time.source_sha256, default_r09),
                                          (preserved, preserved_time.source_sha256, preserved_r09)):
                for index, (pose_bgr, _) in enumerate(decoded):
                    png = rope_frame_png(path, index, sha256)
                    rope_bgr = cv2.imdecode(np.frombuffer(png, dtype=np.uint8), cv2.IMREAD_COLOR)
                    assert rope_bgr is not None
                    assert np.array_equal(rope_bgr, pose_bgr)
            r09_report = {
                "checked": True,
                "pyav_version": av.__version__,
                "rotated_frames": len(shown),
                "default_baked_frames": len(default_frames),
                "vfr_baked_frames": len(preserved_frames),
                "all_display_pixels_and_pts_equal_opencv_ffprobe": True,
                "r08_frame_png_equals_r09_pixels_all_derived_frames": True,
            }

        print(json.dumps({
            "fixture": "four asymmetric frames with VFR PTS and 90-degree display matrix",
            "source_sha256": src_time.source_sha256,
            "rotated_sha256": rotated_time.source_sha256,
            "default_baked_sha256": default_time.source_sha256,
            "vfr_baked_sha256": preserved_time.source_sha256,
            "source_pts_ticks": list(src_time.ticks),
            "default_baked_pts_ticks": list(default_time.ticks),
            "vfr_baked_pts_ticks": list(preserved_time.ticks),
            "vfr_baked_pixels_equal_rotated_display_all_frames": True,
            "r08_accepts_both_baked_files": True,
            "lineage_audit_default_exact_match": default_audit["exact_match"],
            "lineage_audit_default_first_pts_mismatch_index": default_audit["first_pts_mismatch_index"],
            "lineage_audit_default_first_pixel_mismatch_index": default_audit["first_pixel_mismatch_index"],
            "lineage_audit_vfr_exact_match": preserved_audit["exact_match"],
            "lineage_audit_changed_pixels_pts_match": changed_audit["first_pts_mismatch_index"] is None,
            "lineage_audit_changed_pixels_first_mismatch_index": changed_audit["first_pixel_mismatch_index"],
            "r09_file_frames": r09_report,
            "not": ["camera timestamp fidelity", "pose inference", "human video", "Beacon audio"],
        }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
