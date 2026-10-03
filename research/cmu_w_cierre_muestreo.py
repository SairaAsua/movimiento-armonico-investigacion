"""Closure gap and sampled turning on public CMU dance 05_02.

Requires numpy and ezc3d. Download the official 05_02.c3d separately to
research/sources/cmu_mocap/. No data or video is redistributed by this script.
The straight closing chord is an algorithmic convention, not observed motion.
"""

import hashlib
import json
from pathlib import Path

import ezc3d
import numpy as np

from q_giro_orden_sintetico import steps_from_closed_vertices, turn_signature


HERE = Path(__file__).resolve().parent
SOURCE = HERE / "sources/cmu_mocap/05_02.c3d"
EXPECTED_SHA256 = "04bb9be74cd9183eb9f873b26c6eb4dbbf613747af5d6d0ef41f146b859d51d7"
REQUIRED = ("LSHO", "RSHO", "LFWT", "RFWT", "LWRA", "LWRB", "RWRA", "RWRB", "STRN", "RBAC")
WINDOW_FRAMES = 120
STRIDES = (1, 4, 8)


def load_projected_wrist_paths():
    raw = SOURCE.read_bytes()
    if hashlib.sha256(raw).hexdigest() != EXPECTED_SHA256:
        raise ValueError("CMU source SHA-256 differs from audited file")
    c3d = ezc3d.c3d(str(SOURCE))
    parameters = c3d["parameters"]["POINT"]
    xyz = c3d["data"]["points"][:3]
    residual = c3d["data"]["meta_points"]["residuals"][0]
    labels = [
        label.split(":")[-1]
        for label in parameters["LABELS"]["value"] + parameters["LABELS2"]["value"]
    ]
    if (float(parameters["RATE"]["value"][0]), parameters["UNITS"]["value"][0], xyz.shape[2]) != (120.0, "mm", 1123):
        raise ValueError("unexpected file clock, units or frame count")
    if len(labels) != xyz.shape[1] or len(set(labels)) != len(labels):
        raise ValueError("ambiguous CMU marker labels")
    indices = {name: labels.index(name) for name in REQUIRED}
    valid = np.ones(xyz.shape[2], dtype=bool)
    for index in indices.values():
        valid &= (residual[index] >= 0) & np.all(np.isfinite(xyz[:, index, :]), axis=0)
    if not np.all(valid):
        raise ValueError("required markers are not all present by C3D residual")

    def marker(name):
        return xyz[:, indices[name], :].T

    waist = (marker("LFWT") + marker("RFWT")) / 2
    shoulder = (marker("LSHO") + marker("RSHO")) / 2
    shoulder_span = np.linalg.norm(marker("LSHO") - marker("RSHO"), axis=1)
    scale_mm = float(np.median(shoulder_span))
    lateral = marker("LSHO") - marker("RSHO")
    lateral /= np.linalg.norm(lateral, axis=1)[:, None]
    up = shoulder - waist
    up -= np.sum(up * lateral, axis=1)[:, None] * lateral
    up_norm = np.linalg.norm(up, axis=1)
    if np.min(up_norm) < 50:
        raise ValueError("body up axis is degenerate")
    up /= up_norm[:, None]
    front = np.cross(lateral, up)
    if np.min(np.sum((marker("STRN") - marker("RBAC")) * front, axis=1)) <= 0:
        raise ValueError("projected front contradicts sternum/back check")

    paths = {}
    for side, first, second in (("left", "LWRA", "LWRB"), ("right", "RWRA", "RWRB")):
        relative = ((marker(first) + marker(second)) / 2 - waist) / scale_mm
        paths[side] = np.stack(
            (np.sum(relative * lateral, axis=1), np.sum(relative * front, axis=1)),
            axis=1,
        )
    return paths, scale_mm


def straight_closed_w(path):
    points = [tuple(map(float, row)) for row in path]
    points.append(points[0])  # unobserved chord; never a physical trajectory claim
    try:
        return turn_signature(steps_from_closed_vertices(points))["turning_number"]
    except ValueError:
        return None


def main():
    paths, scale_mm = load_projected_wrist_paths()
    rows = []
    for side, path in paths.items():
        for start in range(0, len(path) - WINDOW_FRAMES, WINDOW_FRAMES):
            end = start + WINDOW_FRAMES
            window = path[start : end + 1]
            gap = float(np.linalg.norm(window[-1] - window[0]))
            length = float(np.sum(np.linalg.norm(np.diff(window, axis=0), axis=1)))
            values = {str(stride): straight_closed_w(window[::stride]) for stride in STRIDES}
            rows.append(
                {
                    "side": side,
                    "first_frame": start,
                    "last_frame": end,
                    "closure_gap_shoulder_widths": gap,
                    "observed_path_length_shoulder_widths": length,
                    "gap_to_path_length": gap / length,
                    "W_by_stride_with_unobserved_straight_chord": values,
                    "W_changes_across_strides": len(set(values.values())) > 1,
                }
            )
    near_0_1 = [row for row in rows if row["closure_gap_shoulder_widths"] < 0.1]
    summary = {
        "windows_total": len(rows),
        "windows_near_0_1_shoulder_widths": len(near_0_1),
        "windows_W_changes_120_30_15_hz": sum(row["W_changes_across_strides"] for row in rows),
        "near_0_1_windows_W_changes": sum(row["W_changes_across_strides"] for row in near_0_1),
        "threshold_0_1_is_illustrative_not_pre_registered": True,
    }
    assert summary == {
        "windows_total": 18,
        "windows_near_0_1_shoulder_widths": 3,
        "windows_W_changes_120_30_15_hz": 9,
        "near_0_1_windows_W_changes": 2,
        "threshold_0_1_is_illustrative_not_pre_registered": True,
    }
    report = {
        "scope": "public_CMU_05_02_dance_not_rope_flow_not_Nico_not_physical_W",
        "source_sha256": EXPECTED_SHA256,
        "frame_rate_from_file_hz": 120,
        "shoulder_scale_mm_retrospective_whole_take": scale_mm,
        "path_definition": "body_corotating_wrist_pair_mean_projected_lateral_anterior",
        "window_definition": "fixed_nonoverlapping_120_frame_intervals_121_samples_not_task_cycles",
        "closure_policy": "straight_unobserved_chord_for_diagnostic_only",
        "decimation": "every_1_4_8_frames_keep_both_window_endpoints_no_antialias",
        "error_bound": "not_estimated",
        "summary": summary,
        "windows": rows,
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
