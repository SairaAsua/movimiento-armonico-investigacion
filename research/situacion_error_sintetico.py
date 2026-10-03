#!/usr/bin/env python3
"""Verifica cotas geométricas, no estima error de ninguna cámara."""

from __future__ import annotations

import json
import math
import random

from situacion_recorrido_sintetica import describe


def interval_for_normalized_radius(measured: float, measured_reach: float,
                                   position_bound: float, reach_bound: float) -> tuple[float, float]:
    """Intervalo del radio verdadero si ambas cotas son duras y simultáneas."""
    if (not all(math.isfinite(x) for x in (measured, measured_reach,
                                          position_bound, reach_bound))
            or measured < 0 or position_bound < 0 or reach_bound < 0
            or measured_reach <= reach_bound):
        raise ValueError("cotas y escala incompatibles")
    distance = measured * measured_reach
    return (max(0.0, distance - position_bound) / (measured_reach + reach_bound),
            (distance + position_bound) / (measured_reach - reach_bound))


def radial_variation_bound(segment_count: int, position_bound: float,
                           true_length: float, measured_length: float) -> float:
    """Cota conservadora de |V_r observado − verdadero| para malla fija."""
    if (segment_count < 1 or position_bound < 0 or true_length <= 0
            or measured_length <= 0):
        raise ValueError("recorridos no degenerados requeridos")
    return min(1.0, 6.0 * segment_count * position_bound
               / max(true_length, measured_length))


def norm(v: tuple[float, float, float]) -> float:
    return math.sqrt(sum(x * x for x in v))


def perturb(points: list[tuple[float, float, float]], bound: float,
            rng: random.Random) -> list[tuple[float, float, float]]:
    output = []
    for point in points:
        direction = tuple(rng.uniform(-1.0, 1.0) for _ in range(3))
        length = norm(direction)
        magnitude = bound * rng.random()
        output.append(tuple(point[j] + magnitude * direction[j] / length
                            for j in range(3)))
    return output


def check_pair(true_points: list[tuple[float, float, float]],
               observed_points: list[tuple[float, float, float]],
               true_reach: float, measured_reach: float,
               position_bound: float, reach_bound: float) -> dict:
    true = describe(true_points, (0.0, 0.0, 0.0), true_reach)
    observed = describe(observed_points, (0.0, 0.0, 0.0), measured_reach)
    for key in ("rho_min", "rho_max"):
        lo, hi = interval_for_normalized_radius(observed[key], measured_reach,
                                                position_bound, reach_bound)
        # describe() redondea a seis decimales; la cota analítica no lo hace.
        assert lo - 2e-6 <= true[key] <= hi + 2e-6, (key, lo, true[key], hi)
    v_bound = radial_variation_bound(len(true_points) - 1, position_bound,
                                     true["path_length"], observed["path_length"])
    v_error = abs(true["radial_variation_over_path_length"]
                  - observed["radial_variation_over_path_length"])
    assert v_error <= v_bound + 2e-6, (v_error, v_bound)
    return {"segments": len(true_points) - 1,
            "V_r_true": true["radial_variation_over_path_length"],
            "V_r_observed": observed["radial_variation_over_path_length"],
            "V_r_error": round(v_error, 6), "V_r_bound": round(v_bound, 6)}


def main() -> None:
    rng = random.Random(20261002)
    try:
        interval_for_normalized_radius(0.5, 0.1, 0.01, 0.1)
    except ValueError:
        pass
    else:
        raise AssertionError("una escala que puede ser cero no tiene intervalo finito")
    random_cases = 0
    max_v_error = 0.0
    for _ in range(1000):
        count = rng.randint(2, 24)
        points = [tuple(rng.uniform(-2.0, 2.0) for _ in range(3))
                  for _ in range(count)]
        delta = rng.uniform(0.001, 0.08)
        reach = rng.uniform(0.5, 2.5)
        reach_error = rng.uniform(0, 0.1 * reach)
        measured_reach = reach + rng.uniform(-reach_error, reach_error)
        result = check_pair(points, perturb(points, delta, rng), reach,
                            measured_reach, delta, reach_error)
        max_v_error = max(max_v_error, result["V_r_error"])
        random_cases += 1

    absolute = [(0.5, 0.0, 0.0), (0.8, 0.4, 0.0), (1.1, 0.1, 0.0)]
    true_origin = (0.2, 0.0, 0.0)
    observed_origin = (0.2, 0.02, 0.0)
    true_relative = [tuple(p[j] - true_origin[j] for j in range(3))
                     for p in absolute]
    observed_relative = [tuple(p[j] + (0.03 if j == 0 else 0.0)
                               - observed_origin[j] for j in range(3))
                         for p in absolute]
    origin_example = check_pair(true_relative, observed_relative,
                                1.0, 1.01, 0.03 + 0.02, 0.02)

    circles = {}
    for segments in (32, 128):
        points = [(math.cos(2 * math.pi * i / segments),
                   math.sin(2 * math.pi * i / segments), 0.0)
                  for i in range(segments + 1)]
        circles[str(segments)] = check_pair(points, perturb(points, 0.01, rng),
                                             1.0, 1.02, 0.01, 0.02)
    assert circles["128"]["V_r_bound"] == 1.0
    print(json.dumps({"kind": "synthetic_mathematical_bounds_only",
                      "random_cases": random_cases,
                      "max_random_V_r_error": round(max_v_error, 6),
                      "point_plus_origin_example": origin_example,
                      "circle_cases": circles}, indent=2))


if __name__ == "__main__":
    main()
