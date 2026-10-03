"""Sharp 2x2 space-phase MI bounds with known phase and unknown region.

Synthetic probability masses only; no camera, rope-flow or human inference.
"""

from __future__ import annotations

import json
from itertools import product

from j_espacio_fase_sintetico import mutual_information


def sharp_bounds(observed: list[list[float]], missing_by_phase: list[float]) -> dict:
    assert len(observed) == 2 and all(len(row) == 2 for row in observed)
    assert len(missing_by_phase) == 2
    assert all(value >= 0 for row in observed for value in row)
    assert all(value >= 0 for value in missing_by_phase)
    phase = [sum(observed[s][j] for s in range(2)) + missing_by_phase[j] for j in range(2)]
    assert all(value > 0 for value in phase)
    assert abs(sum(phase) - 1) < 1e-12

    # a and b are P(S=0|Phi=0) and P(S=0|Phi=1).
    intervals = [
        (observed[0][j] / phase[j], (observed[0][j] + missing_by_phase[j]) / phase[j])
        for j in range(2)
    ]

    def complete(a: float, b: float) -> list[list[float]]:
        return [[phase[0] * a, phase[1] * b],
                [phase[0] * (1 - a), phase[1] * (1 - b)]]

    (a_low, a_high), (b_low, b_high) = intervals
    if max(a_low, b_low) <= min(a_high, b_high):
        common = (max(a_low, b_low) + min(a_high, b_high)) / 2
        minimum = (0.0, common, common)
    elif a_low > b_high:
        minimum = (mutual_information(complete(a_low, b_high)), a_low, b_high)
    else:
        minimum = (mutual_information(complete(a_high, b_low)), a_high, b_low)

    corners = [
        (mutual_information(complete(a, b)), a, b)
        for a, b in product((a_low, a_high), (b_low, b_high))
    ]
    maximum = max(corners)
    return {
        "coverage": sum(map(sum, observed)),
        "coverage_by_phase": [sum(observed[s][j] for s in range(2)) / phase[j] for j in range(2)],
        "J_valid_only_nats": mutual_information(observed),
        "J_complete_min_nats": minimum[0],
        "J_complete_max_nats": maximum[0],
        "min_completion": complete(minimum[1], minimum[2]),
        "max_completion": complete(maximum[1], maximum[2]),
        "conditional_intervals_S0_by_phase": intervals,
    }


def main() -> None:
    selective = sharp_bounds([[0.25, 0.125], [0.125, 0.25]], [0.125, 0.125])
    assert selective["coverage"] == 0.75
    assert selective["coverage_by_phase"] == [0.75, 0.75]
    assert abs(selective["J_valid_only_nats"] - 0.056633012265132426) < 1e-12
    assert abs(selective["J_complete_min_nats"]) < 1e-12
    assert abs(selective["J_complete_max_nats"] - 0.13081203594113697) < 1e-12

    robust = sharp_bounds([[0.4, 0.05], [0.05, 0.4]], [0.05, 0.05])
    assert robust["coverage"] == 0.9
    assert robust["coverage_by_phase"] == [0.9, 0.9]
    assert robust["J_complete_min_nats"] > 0
    assert robust["J_complete_max_nats"] > robust["J_complete_min_nats"]

    none_missing = sharp_bounds([[0.25, 0.25], [0.25, 0.25]], [0.0, 0.0])
    assert none_missing["J_complete_min_nats"] == none_missing["J_complete_max_nats"] == 0

    print(json.dumps({"kind": "synthetic_sharp_MI_bounds_2x2", "selective": selective,
                      "robust_association": robust,
                      "limit": "Known phase and missing region; exact probability masses, not sampled confidence intervals"},
                     ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
