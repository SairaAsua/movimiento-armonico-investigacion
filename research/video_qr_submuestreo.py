#!/usr/bin/env python3
"""Sensibilidad de Q proyectado, R modular y unwrap al submuestreo de cuatro MP4 sintéticos."""

import argparse
import hashlib
import json
import math
from pathlib import Path
import subprocess
import sys

from weaver_video_qr_factorial import (
    CYCLES, FPS, GEOMETRIES, LEFT_CENTER, RIGHT_CENTER, points_from_video,
)


STRIDES = (1, 2, 3, 5, 6, 10)  # 30, 15, 10, 6, 5, 3 cuadros/s.


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def revision(repo: Path) -> str:
    return subprocess.check_output(["git", "-C", str(repo), "rev-parse", "HEAD"], text=True).strip()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-dir", type=Path, required=True,
                        help="salida de weaver_video_qr_factorial.py")
    parser.add_argument("--phase-repo", type=Path, required=True,
                        help="checkout del banco de fase #26")
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    source, phase_repo, out = (p.resolve() for p in
                               (args.input_dir, args.phase_repo, args.output_dir))
    if out.exists():
        parser.error("--output-dir debe ser una ruta nueva")
    if not (phase_repo / "research/ejecutar_banco_fase_archivo.py").is_file():
        parser.error("falta el banco de fase #26")
    if not (source / "report.json").is_file():
        parser.error("falta el manifiesto del factorial MP4")
    sys.path.insert(0, str(phase_repo / "research"))
    from ejecutar_banco_fase_archivo import q_projected
    from video_fase_audio_diagnostico import unwrap

    original = json.loads((source / "report.json").read_text())
    assert original["phase_repo_commit"] == revision(phase_repo)
    cases = {}
    for geometry, axes in GEOMETRIES.items():
        for timing in ("aligned", "opposed"):
            key = f"{geometry}-{timing}"
            video = source / f"{key}.mp4"
            assert sha256(video) == original["cases"][key]["mp4_sha256"]
            times, left, right = points_from_video(video)
            assert len(times) == len(left) == len(right) == CYCLES * FPS
            q0 = original["cases"][key]["Q_projected_xy"][0]
            r0 = original["cases"][key]["R_from_pixels"]
            rows = {}
            for stride in STRIDES:
                estimates = []
                for offset in range(stride):
                    indices = list(range(offset, len(times), stride))
                    lp = [math.atan2(-(left[i][1] - LEFT_CENTER[1]) / 40,
                                     (left[i][0] - LEFT_CENTER[0]) / 40)
                          for i in indices]
                    rp = [math.atan2(-(right[i][1] - RIGHT_CENTER[1]) / axes[1],
                                     (right[i][0] - RIGHT_CENTER[0]) / axes[0])
                          for i in indices]
                    qx, _ = q_projected([right[i] for i in indices])
                    r_wrapped = abs(sum(complex(math.cos(a - b), math.sin(a - b))
                                        for a, b in zip(rp, lp))) / len(indices)
                    try:
                        unwrap(lp)
                        unwrap(rp)
                        phase_continuous_valid = True
                    except ValueError:
                        phase_continuous_valid = False
                    estimates.append({"offset_frames": offset, "sample_count": len(indices),
                                      "Qx_projected": qx, "R_wrapped_samples": r_wrapped,
                                      "phase_continuous_valid": phase_continuous_valid})
                rows[str(FPS / stride)] = {
                    "nominal_fps_after_decimation": FPS / stride,
                    "stride": stride, "offsets": stride,
                    "Qx_range": (min(x["Qx_projected"] for x in estimates),
                                 max(x["Qx_projected"] for x in estimates)),
                    "R_wrapped_range": (min(x["R_wrapped_samples"] for x in estimates),
                                        max(x["R_wrapped_samples"] for x in estimates)),
                    "phase_continuous_valid_offsets": sum(x["phase_continuous_valid"] for x in estimates),
                    "max_abs_Qx_change_from_30fps": max(abs(x["Qx_projected"] - q0) for x in estimates),
                    "max_abs_R_change_from_30fps": max(abs(x["R_wrapped_samples"] - r0) for x in estimates),
                }
            assert rows["30.0"]["phase_continuous_valid_offsets"] == 1
            assert rows["3.0"]["phase_continuous_valid_offsets"] == 0
            cases[key] = {"source_mp4_sha256": sha256(video),
                          "Qx_30fps": q0, "R_30fps": r0, "sampling": rows}

    assert all(cases[f"{geometry}-aligned"]["sampling"]["3.0"]["R_wrapped_range"][0] > .99
               for geometry in GEOMETRIES)
    report = {"scope": "synthetic_file_decimation_not_camera_fps_validation",
              "phase_repo_commit": revision(phase_repo),
              "input_factorial_report_sha256": sha256(source / "report.json"),
              "sampling_rule": "every kth decoded frame; test all k starting offsets, preserve original PTS",
              "cases": cases}
    out.mkdir(parents=True)
    (out / "report.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
