"""Ambiguous torso phase under a pointwise orientation-error bound.

Synthetic analytic fixture; no human or camera measurements.
"""

from __future__ import annotations

import cmath
import math


def concentration(deltas: list[float]) -> float:
    return abs(sum(cmath.exp(1j * d) for d in deltas) / len(deltas))


def main() -> None:
    amplitude = 0.04  # radians, hypothetical
    error_bound = 0.10  # radians, hypothetical hard bound
    cycles = 4
    samples_per_cycle = 100
    observed_deltas: list[float] = []
    true_deltas: list[float] = []
    max_pointwise_error = 0.0

    for cycle in range(cycles):
        sign = 1 if cycle % 2 == 0 else -1
        for sample in range(samples_per_cycle):
            t = cycle + (sample + 0.5) / samples_per_cycle
            observed = amplitude * math.sin(2 * math.pi * t)
            true = sign * observed
            max_pointwise_error = max(max_pointwise_error, abs(observed - true))
            observed_deltas.append(0.0)
            true_deltas.append(0.0 if sign == 1 else math.pi)

    observed_r = concentration(observed_deltas)
    true_r = concentration(true_deltas)
    assert max_pointwise_error <= 2 * amplitude <= error_bound
    assert math.isclose(observed_r, 1.0, abs_tol=1e-14)
    assert true_r < 1e-14
    print(f"samples={cycles * samples_per_cycle}")
    print(f"max_orientation_error_rad={max_pointwise_error:.6f}")
    print(f"hypothetical_error_bound_rad={error_bound:.6f}")
    print(f"observed_R_1_1={observed_r:.6f}")
    print(f"compatible_true_R_1_1={true_r:.6f}")


if __name__ == "__main__":
    main()
