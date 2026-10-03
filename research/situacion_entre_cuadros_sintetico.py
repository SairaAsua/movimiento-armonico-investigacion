#!/usr/bin/env python3
"""Excursiones invisibles entre muestras y cota por velocidad relativa.

Sólo curvas matemáticas; no velocidad medida de rope flow ni cámara.
"""

from __future__ import annotations

import json
import math
import random

from situacion_error_sintetico import interval_for_normalized_radius
from situacion_recorrido_sintetica import describe


def sampling_distance_bound(max_relative_speed: float, max_gap_s: float) -> float:
    if (not math.isfinite(max_relative_speed) or max_relative_speed < 0
            or not math.isfinite(max_gap_s) or max_gap_s < 0):
        raise ValueError("velocidad y hueco finitos no negativos requeridos")
    return max_relative_speed * max_gap_s / 2.0


def main() -> None:
    origin = (0.0, 0.0, 0.0)
    reach = 1.0
    a, epsilon, duration = 0.5, 0.1, 1.0
    start = (a, 0.0, 0.0)
    middle = origin
    end = (a, epsilon, 0.0)
    visible = describe([start, end], origin, reach)
    hidden_excursion = describe([start, middle, end], origin, reach)
    total_length = math.dist(start, middle) + math.dist(middle, end)
    speed_cap = total_length / duration  # Tramos recorridos a rapidez constante.
    middle_time = math.dist(start, middle) / speed_cap
    gap_bound = sampling_distance_bound(speed_cap, duration)
    assert visible["rho_min"] == 0.5 and hidden_excursion["rho_min"] == 0.0
    assert abs(visible["rho_min"] - hidden_excursion["rho_min"]) <= gap_bound + 1e-6
    assert visible["radial_variation_over_path_length"] < 0.1
    assert hidden_excursion["radial_variation_over_path_length"] == 1.0
    assert 0 < middle_time < duration

    # Caso de igualdad: mismos dos cuadros en radio V*h/2, viaje al centro y vuelta.
    radial_start = (0.5, 0.0, 0.0)
    radial_end = radial_start
    true_radial_min = describe([radial_start, origin, radial_end], origin, reach)["rho_min"]
    observed_radial_min = math.dist(radial_start, origin) / reach
    assert observed_radial_min - true_radial_min == sampling_distance_bound(1.0, 1.0)

    rng = random.Random(20261002)
    max_ratio = 0.0
    for _ in range(500):
        points = [tuple(rng.uniform(-1.0, 1.0) for _ in range(3))
                  for _ in range(11)]
        dense = describe(points, origin, reach)
        sparse = describe([points[0], points[-1]], origin, reach)
        # Los diez tramos duran 0,1 s; esta es una curva continua a trozos.
        vmax = max(math.dist(p, q) / 0.1 for p, q in zip(points, points[1:]))
        bound = sampling_distance_bound(vmax, 1.0)
        for metric in ("rho_min", "rho_max"):
            error = abs(dense[metric] - sparse[metric])
            assert error <= bound + 2e-6
            max_ratio = max(max_ratio, error / bound)

    # Si además cada punto medido tiene cota δ y R tiene error, ambas se suman.
    measurement_bound = 0.02
    reach_bound = 0.01
    low, high = interval_for_normalized_radius(
        visible["rho_min"], reach, measurement_bound + gap_bound, reach_bound)
    assert low - 2e-6 <= hidden_excursion["rho_min"] <= high + 2e-6
    print(json.dumps({"kind": "synthetic_between_frames_only",
                      "duration_s": duration, "hidden_middle_time_s": round(middle_time, 6),
                      "relative_speed_cap_units_per_s": round(speed_cap, 6),
                      "sampling_distance_bound_units": round(gap_bound, 6),
                      "same_visible_endpoints": {
                          "sampled_rho_min": visible["rho_min"],
                          "hidden_rho_min": hidden_excursion["rho_min"],
                          "sampled_V_r": visible["radial_variation_over_path_length"],
                          "hidden_V_r": hidden_excursion["radial_variation_over_path_length"]},
                      "tight_radial_case_error": observed_radial_min - true_radial_min,
                      "random_piecewise_cases": 500,
                      "max_observed_error_over_bound": round(max_ratio, 6),
                      "example_combined_rho_interval": [round(low, 6), round(high, 6)]},
                     indent=2))


if __name__ == "__main__":
    main()
