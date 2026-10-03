#!/usr/bin/env python3
"""Describe inter-wrist-marker distance in public CMU 05_02 C3D.

Requires numpy and ezc3d. Does not validate a camera, anatomy or rope flow.
The official C3D stays in the ignored local research/sources/cmu_mocap directory.
"""

import hashlib
import json
from math import cos, radians, sin
from pathlib import Path

import ezc3d
import numpy as np


SOURCE = Path(__file__).resolve().parent / "sources/cmu_mocap/05_02.c3d"
EXPECTED_SHA256 = "04bb9be74cd9183eb9f873b26c6eb4dbbf613747af5d6d0ef41f146b859d51d7"
REQUIRED = ("LSHO", "RSHO", "LFWT", "RFWT", "LWRA", "LWRB", "RWRA", "RWRB", "LWR0", "RWR0", "STRN", "RBAC")


def quantiles(values):
    return [round(float(x), 6) for x in np.quantile(values, [0, .05, .5, .95, 1])]


def shifted_pair_error(left, right, scale_mm, shift):
    """Pair different times only; each 3D marker path remains unchanged."""
    k = abs(shift)
    if shift > 0:
        l_ref, r_ref, r_shift = left[:-k], right[:-k], right[k:]
    else:
        l_ref, r_ref, r_shift = left[k:], right[k:], right[:-k]
    synchronous = np.linalg.norm(r_ref - l_ref, axis=1) / scale_mm
    asynchronous = np.linalg.norm(r_shift - l_ref, axis=1) / scale_mm
    error = np.abs(asynchronous - synchronous)
    shifted_displacement = np.linalg.norm(r_shift - r_ref, axis=1) / scale_mm
    assert np.max(error - shifted_displacement) < 1e-12
    return {
        "shift_frames": shift,
        "shift_ms": round(1000 * shift / 120, 6),
        "common_support_frames": len(error),
        "absolute_distance_error_L_p50_p95_max": [round(float(x), 6) for x in np.quantile(error, [.5, .95, 1])],
        "absolute_error_over_0p1L_frames": int(np.sum(error > .1)),
    }


def fixed_orthographic_views(delta, scale_mm, lateral0, up0, front0):
    """Four fixed virtual image planes, all viewing the same 3D motion."""
    norm_3d = np.linalg.norm(delta, axis=1) / scale_mm
    projections = []
    summaries = []
    for yaw_deg in (0, 45, 90, 135):
        yaw = radians(yaw_deg)
        horizontal = cos(yaw) * lateral0 + sin(yaw) * front0
        line_of_sight = -sin(yaw) * lateral0 + cos(yaw) * front0
        projected = np.hypot(delta @ horizontal, delta @ up0) / scale_mm
        assert np.max(np.abs(projected**2 - (norm_3d**2 - (delta @ line_of_sight / scale_mm)**2))) < 1e-11
        loss = norm_3d - projected
        assert np.min(loss) > -1e-12
        projections.append(projected)
        summaries.append({
            "fixed_camera_yaw_deg": yaw_deg,
            "projected_distance_L_p05_p50_p95": [
                round(float(x), 6) for x in np.quantile(projected, [.05, .5, .95])
            ],
            "projection_loss_L_p50_p95": [
                round(float(x), 6) for x in np.quantile(loss, [.5, .95])
            ],
            "loss_over_0p1L_frames": int(np.sum(loss > .1)),
        })
    per_frame_view_range = np.ptp(np.stack(projections), axis=0)
    return {
        "fixed_view_summary": summaries,
        "same_frame_four_view_range_L_p50_p95_max": [
            round(float(x), 6) for x in np.quantile(per_frame_view_range, [.5, .95, 1])
        ],
        "same_frame_view_range_over_0p1L_frames": int(np.sum(per_frame_view_range > .1)),
    }


def fixed_view_q_windows(path, scale_mm, lateral0, up0, front0):
    """One-second arc-weighted Q_up of the same relative wrist path in four views."""
    steps = np.diff(path, axis=0)
    window_segments = 119  # 120 recorded points at 120 Hz; no invented endpoint.
    gate_l = 0.5  # Illustrative observed projected arc in shoulder widths.
    summaries = []
    q_views = []
    eligible_views = []
    arc_views = []
    for yaw_deg in (0, 45, 90, 135):
        yaw = radians(yaw_deg)
        horizontal = cos(yaw) * lateral0 + sin(yaw) * front0
        dh = steps @ horizontal
        dv = steps @ up0
        ds = np.hypot(dh, dv)
        vertical_contribution = np.divide(dv * dv, ds, out=np.zeros_like(ds), where=ds > 0)
        arc = np.convolve(ds, np.ones(window_segments), mode="valid") / scale_mm
        vertical_arc = np.convolve(vertical_contribution, np.ones(window_segments), mode="valid") / scale_mm
        eligible = arc >= gate_l
        q = np.divide(vertical_arc, arc, out=np.full_like(arc, np.nan), where=arc > 0)
        assert np.all((q[eligible] >= 0) & (q[eligible] <= 1 + 1e-12))
        q_views.append(q)
        eligible_views.append(eligible)
        arc_views.append(arc)
        summaries.append({"fixed_camera_yaw_deg": yaw_deg,
                          "eligible_windows": int(np.sum(eligible)),
                          "q_up_p05_p50_p95_on_eligible": [
                              round(float(x), 6) for x in np.quantile(q[eligible], [.05, .5, .95])
                          ]})
    common = np.logical_and.reduce(eligible_views)
    q_common = np.stack(q_views)[:, common]
    ranges = np.ptp(q_common, axis=0)
    all_arcs = np.stack(arc_views)
    all_q = np.stack(q_views)
    gate_sensitivity = []
    for candidate_gate in (0.25, 0.5, 0.75, 1.0):
        candidate_common = np.all(all_arcs >= candidate_gate, axis=0)
        candidate_ranges = np.ptp(all_q[:, candidate_common], axis=0)
        gate_sensitivity.append({
            "projected_arc_gate_L": candidate_gate,
            "common_eligible_windows": int(np.sum(candidate_common)),
            "same_window_q_range_p50_p95": [
                round(float(x), 6) for x in np.quantile(candidate_ranges, [.5, .95])
            ],
        })
    assert gate_sensitivity[1]["common_eligible_windows"] == int(np.sum(common))
    assert gate_sensitivity[1]["same_window_q_range_p50_p95"] == [
        round(float(x), 6) for x in np.quantile(ranges, [.5, .95])
    ]
    return {"window_points": window_segments + 1, "projected_arc_gate_L": gate_l,
            "windows_total": len(q_views[0]), "per_view": summaries,
            "common_eligible_windows": int(np.sum(common)),
            "projected_arc_gate_sensitivity": gate_sensitivity,
            "same_window_q_up_four_view_range_p50_p90_p95_max": [
                round(float(x), 6) for x in np.quantile(ranges, [.5, .9, .95, 1])
            ]}


def main():
    raw = SOURCE.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == EXPECTED_SHA256
    c = ezc3d.c3d(str(SOURCE))
    point = c["parameters"]["POINT"]
    fps = float(point["RATE"]["value"][0])
    units = point["UNITS"]["value"][0]
    xyz = c["data"]["points"][:3]
    residual = c["data"]["meta_points"]["residuals"][0]
    labels = [s.split(":")[-1] for s in point["LABELS"]["value"] + point["LABELS2"]["value"]]
    assert fps == 120 and units == "mm" and xyz.shape[2] == 1123
    assert len(labels) == xyz.shape[1] and len(set(labels)) == len(labels)
    indices = {name: labels.index(name) for name in REQUIRED}
    valid = np.ones(xyz.shape[2], dtype=bool)
    for index in indices.values():
        valid &= (residual[index] >= 0) & np.all(np.isfinite(xyz[:, index, :]), axis=0)
    assert np.all(valid)  # Do not silently describe a selected subset of frames.

    def marker(name):
        return xyz[:, indices[name], :].T

    left = (marker("LWRA") + marker("LWRB")) / 2
    right = (marker("RWRA") + marker("RWRB")) / 2
    shoulders = marker("LSHO") - marker("RSHO")
    # A fixed descriptive scale uses only the first second, before later frames.
    scale_mm = float(np.median(np.linalg.norm(shoulders[:120], axis=1)))
    assert scale_mm > 0
    delta = right - left
    distance_l = np.linalg.norm(delta, axis=1) / scale_mm

    lateral = shoulders / np.linalg.norm(shoulders, axis=1)[:, None]
    shoulder_mid = (marker("LSHO") + marker("RSHO")) / 2
    waist_mid = (marker("LFWT") + marker("RFWT")) / 2
    up = shoulder_mid - waist_mid
    up -= np.sum(up * lateral, axis=1)[:, None] * lateral
    up /= np.linalg.norm(up, axis=1)[:, None]
    front = np.cross(lateral, up)
    assert np.min(np.sum((marker("STRN") - marker("RBAC")) * front, axis=1)) > 0
    body_delta = np.stack([np.sum(delta * axis, axis=1) for axis in (lateral, up, front)], axis=1) / scale_mm
    assert np.max(np.abs(np.linalg.norm(body_delta, axis=1) - distance_l)) < 1e-12

    # Orthographic lateral/up view is a constructed projection, not camera footage.
    projected_l = np.linalg.norm(body_delta[:, :2], axis=1)
    projection_loss = distance_l - projected_l
    assert np.min(projection_loss) > -1e-12
    alt_l = np.linalg.norm(marker("RWR0") - marker("LWR0"), axis=1) / scale_mm
    proxy_gap = np.abs(alt_l - distance_l)
    report = {
        "source_sha256": EXPECTED_SHA256,
        "frames": int(xyz.shape[2]),
        "fps_file": fps,
        "valid_residual_frames": int(np.sum(valid)),
        "scale_first_second_mm": round(scale_mm, 6),
        "distance_pairmid_L_min_p05_p50_p95_max": quantiles(distance_l),
        "signed_body_up_delta_L_min_p05_p50_p95_max": quantiles(body_delta[:, 1]),
        "projection_loss_L_min_p05_p50_p95_max": quantiles(projection_loss),
        "projection_loss_over_0p1L_frames": int(np.sum(projection_loss > .1)),
        "alternate_LWR0_RWR0_abs_gap_L_min_p05_p50_p95_max": quantiles(proxy_gap),
        "max_world_body_distance_discrepancy_L": round(float(np.max(np.abs(np.linalg.norm(body_delta, axis=1) - distance_l))), 12),
        "artificial_right_signal_time_shifts": [
            shifted_pair_error(left, right, scale_mm, shift)
            for shift in (1, -1, 2, -2, 4, -4, 8, -8)
        ],
        "fixed_orthographic_views": fixed_orthographic_views(
            delta, scale_mm, lateral[0], up[0], front[0]
        ),
        "fixed_view_q_windows": fixed_view_q_windows(
            right - shoulder_mid, scale_mm, lateral[0], up[0], front[0]
        ),
    }
    print(json.dumps(report, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
