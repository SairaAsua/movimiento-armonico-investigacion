#!/usr/bin/env python3
"""Perturbaciones hipotéticas de 1 mm sobre CMU; no simula cámaras reales."""

from __future__ import annotations

import json
import statistics

import numpy as np

from cmu_causal_c_replay import body_trajectories
from cmu_danza_05_02_audit import EXPECTED_SHA256
from cmu_situacion_marcos import WINDOW_INTERVALS, measure
from situacion_error_sintetico import radial_variation_bound


SEED = 20261002
REPS = 30
POSITION_BOUND_MM = 1.0


def unit_vectors(rng: np.random.Generator, count: int) -> np.ndarray:
    vectors = rng.normal(size=(count, 3))
    return vectors / np.linalg.norm(vectors, axis=1)[:, None]


def perturbations(rng: np.random.Generator, count: int,
                  magnitude_L: float) -> dict[str, np.ndarray]:
    a, b = unit_vectors(rng, 2)
    b -= a * float(np.dot(a, b))
    b /= np.linalg.norm(b)
    phase = rng.uniform(0, 2 * np.pi)
    theta = np.linspace(phase, phase + 2 * np.pi, count)
    return {
        "constant_offset": np.repeat(unit_vectors(rng, 1), count, axis=0)
                           * magnitude_L,
        "one_cycle_smooth_drift": (
            np.cos(theta)[:, None] * a + np.sin(theta)[:, None] * b
        ) * magnitude_L,
        "independent_frame_jitter": unit_vectors(rng, count) * magnitude_L,
    }


def summarize(values: list[float]) -> dict:
    return {"median": round(statistics.median(values), 6),
            "max": round(max(values), 6)}


def main() -> None:
    scale_mm, paths = body_trajectories()  # valida hash y marcadores.
    delta_L = POSITION_BOUND_MM / scale_mm
    rng = np.random.default_rng(SEED)
    result = {"kind": "hypothetical_error_on_external_mocap_not_camera_accuracy",
              "source": "CMU 05_02 C3D modern dance; no rope flow",
              "source_sha256": EXPECTED_SHA256,
              "frame": "co_rotating_waist_origin",
              "scale_mm": round(scale_mm, 6),
              "position_error_norm_mm_every_sample": POSITION_BOUND_MM,
              "same_error_envelope_different_time_structure": True,
              "seed": SEED, "repetitions_per_window": REPS,
              "windows_per_wrist": 9, "sides": {}}
    for side, path in paths.items():
        stats = {name: {"abs_V_r_delta": [], "abs_rho_min_delta_mm": [],
                        "path_length_ratio": []}
                 for name in ("constant_offset", "one_cycle_smooth_drift",
                              "independent_frame_jitter")}
        for start in range(0, 1080, WINDOW_INTERVALS):
            points = path[start:start + WINDOW_INTERVALS + 1]
            baseline = measure(points)
            length_mm = baseline["path_length"] * scale_mm
            for _ in range(REPS):
                for name, noise in perturbations(rng, len(points), delta_L).items():
                    assert np.allclose(np.linalg.norm(noise, axis=1), delta_L,
                                       rtol=1e-12, atol=1e-12)
                    perturbed = measure(points + noise)
                    dv = abs(perturbed["radial_variation_over_path_length"]
                             - baseline["radial_variation_over_path_length"])
                    worst_bound = radial_variation_bound(
                        WINDOW_INTERVALS, POSITION_BOUND_MM, length_mm,
                        perturbed["path_length"] * scale_mm)
                    assert dv <= worst_bound + 2e-6
                    stats[name]["abs_V_r_delta"].append(dv)
                    stats[name]["abs_rho_min_delta_mm"].append(abs(
                        perturbed["rho_min"] - baseline["rho_min"]) * scale_mm)
                    stats[name]["path_length_ratio"].append(
                        perturbed["path_length"] / baseline["path_length"])
        result["sides"][side] = {
            name: {"comparisons": len(series["abs_V_r_delta"]),
                   "abs_V_r_delta": summarize(series["abs_V_r_delta"]),
                   "abs_rho_min_delta_mm": summarize(series["abs_rho_min_delta_mm"]),
                   "path_length_ratio": summarize(series["path_length_ratio"])}
            for name, series in stats.items()}
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
