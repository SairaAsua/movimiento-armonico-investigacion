#!/usr/bin/env python3
"""Cota suficiente de error para V_r en danza CMU externa, no cámaras propias."""

from __future__ import annotations

import json
import statistics

import numpy as np

from cmu_causal_c_replay import body_trajectories
from cmu_danza_05_02_audit import EXPECTED_SHA256
from cmu_situacion_decimacion import indices
from cmu_situacion_marcos import WINDOW_INTERVALS, measure
from situacion_error_sintetico import radial_variation_bound


TARGET_BOUND = 0.1
HYPOTHETICAL_DELTA_MM = 1.0
FACTORS = (1, 4, 5)  # 120, 30, 24 Hz nominales desde el C3D de 120 Hz.


def summarize(values: list[float]) -> dict:
    return {"min": round(min(values), 6),
            "median": round(statistics.median(values), 6),
            "max": round(max(values), 6)}


def main() -> None:
    scale_mm, paths = body_trajectories()  # verifica fuente, hash y marcadores.
    result = {"kind": "external_mocap_design_calculation_not_camera_validation",
              "source": "CMU 05_02 C3D modern dance; no rope flow",
              "source_sha256": EXPECTED_SHA256,
              "frame": "co_rotating_waist_origin",
              "scale_mm": round(scale_mm, 6),
              "target_abs_V_r_bound": TARGET_BOUND,
              "hypothetical_position_bound_mm": HYPOTHETICAL_DELTA_MM,
              "windows": "nine 1s windows per wrist; decimated endpoints forced",
              "sides": {}}
    for side, path in paths.items():
        summaries = {}
        for factor in FACTORS:
            caps_mm, bounds_if_1mm, segment_counts = [], [], []
            for start in range(0, 1080, WINDOW_INTERVALS):
                stop = start + WINDOW_INTERVALS
                for phase in range(factor):
                    sample_indices = (list(range(start, stop + 1)) if factor == 1
                                      else indices(start, stop, factor, phase))
                    n = len(sample_indices) - 1
                    length_mm = measure(path[sample_indices])["path_length"] * scale_mm
                    direct_mm = float(np.linalg.norm(np.diff(path[sample_indices], axis=0),
                                                      axis=1).sum() * scale_mm)
                    assert abs(length_mm - direct_mm) < 0.001
                    assert length_mm > 0 and n > 0
                    # max(L_true,L_observed) >= L_observed; esta condición basta,
                    # pero no es necesaria, para que la cota sea <= TARGET_BOUND.
                    cap_mm = TARGET_BOUND * length_mm / (6 * n)
                    caps_mm.append(cap_mm)
                    bounds_if_1mm.append(radial_variation_bound(
                        n, HYPOTHETICAL_DELTA_MM, length_mm, length_mm))
                    segment_counts.append(n)
                    assert radial_variation_bound(n, cap_mm, length_mm, length_mm) <= (
                        TARGET_BOUND + 1e-12)
            summaries[str(120 // factor)] = {
                "comparisons": len(caps_mm),
                "segments_min_max": [min(segment_counts), max(segment_counts)],
                "delta_mm_sufficient_for_abs_Vr_bound_le_0p1": summarize(caps_mm),
                "bound_if_hypothetical_delta_1mm": summarize(bounds_if_1mm),
                "fraction_bound_le_0p1_at_1mm": round(sum(
                    b <= TARGET_BOUND for b in bounds_if_1mm) / len(bounds_if_1mm), 6),
            }
        result["sides"][side] = summaries
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
