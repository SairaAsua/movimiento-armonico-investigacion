"""Exact-cycle counterexample: phase concentration depends on phase coordinate.

Uses constructed phases only; no human movement, video, camera, or audio.
"""

from __future__ import annotations

import json
from math import cos, hypot, pi, sin


def concentration(phases_a: list[float], phases_b: list[float]) -> float:
    assert len(phases_a) == len(phases_b) and phases_a
    n = len(phases_a)
    return hypot(
        sum(cos(a - b) for a, b in zip(phases_a, phases_b)),
        sum(sin(a - b) for a, b in zip(phases_a, phases_b)),
    ) / n


def main() -> None:
    samples = 4096
    distortion = 0.9
    theta = [2 * pi * k / samples for k in range(samples)]
    transformed = [t + distortion * sin(t) for t in theta]
    # d(transformed)/d(theta) = 1 + distortion*cos(theta) >= 0.1.
    assert 1 - distortion > 0
    assert all(b > a for a, b in zip(transformed, transformed[1:]))
    # Both coordinates have exactly the same cycle crossings at 0 and 2*pi.
    assert transformed[0] == theta[0] == 0
    assert abs((2 * pi + distortion * sin(2 * pi)) - 2 * pi) < 1e-15

    result = {
        "samples_per_cycle": samples,
        "distortion": distortion,
        "minimum_phase_derivative": 1 - distortion,
        "R_true_same_phase": concentration(theta, theta),
        "R_one_coordinate_changed": concentration(transformed, theta),
        "R_both_coordinates_changed": concentration(transformed, transformed),
    }
    assert result["R_true_same_phase"] == 1.0
    assert result["R_both_coordinates_changed"] == 1.0
    assert abs(result["R_one_coordinate_changed"] - 0.8075237981225447) < 1e-12
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
