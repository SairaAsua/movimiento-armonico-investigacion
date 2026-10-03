"""Quantify post-hoc p:q selection under an ideal independent-cycle null.

Synthetic phases only. The model does not represent rope flow, shared task
timing, camera error, or neighboring-cycle dependence.
"""

from __future__ import annotations

from math import cos, gcd, pi, sin
from random import Random


RATIOS = tuple(
    (p, q) for p in range(1, 5) for q in range(1, 5) if gcd(p, q) == 1
)
REPETITIONS = 10_000
SEED = 20261003


def concentration(a: list[float], b: list[float], p: int, q: int) -> float:
    if len(a) != len(b) or not a:
        raise ValueError("Equal nonempty phase arrays required")
    real = sum(cos(q * x - p * y) for x, y in zip(a, b)) / len(a)
    imag = sum(sin(q * x - p * y) for x, y in zip(a, b)) / len(a)
    return (real * real + imag * imag) ** 0.5


def quantile(values: list[float], fraction: float) -> float:
    ordered = sorted(values)
    return ordered[int(fraction * len(ordered)) - 1]


def experiment(cycles: int, rng: Random) -> dict[str, float]:
    fixed: list[float] = []
    searched: list[float] = []
    squared: list[float] = []
    for _ in range(REPETITIONS):
        a = [rng.uniform(0, 2 * pi) for _ in range(cycles)]
        b = [rng.uniform(0, 2 * pi) for _ in range(cycles)]
        values = [concentration(a, b, p, q) for p, q in RATIOS]
        fixed.append(values[RATIOS.index((1, 1))])
        searched.append(max(values))
        squared.append(fixed[-1] ** 2)
    threshold = quantile(fixed, 0.95)
    return {
        "E_R11_squared": sum(squared) / REPETITIONS,
        "null_expected_R_squared": 1 / cycles,
        "fixed_mean": sum(fixed) / REPETITIONS,
        "searched_mean": sum(searched) / REPETITIONS,
        "fixed_q95": threshold,
        "searched_q95": quantile(searched, 0.95),
        "searched_above_fixed_q95": sum(x > threshold for x in searched)
        / REPETITIONS,
    }


def main() -> None:
    assert len(RATIOS) == 11
    rng = Random(SEED)
    for cycles in (8, 32):
        result = experiment(cycles, rng)
        assert abs(result["E_R11_squared"] - 1 / cycles) < 0.01
        assert result["searched_mean"] > result["fixed_mean"]
        assert result["searched_q95"] > result["fixed_q95"]
        print(f"K={cycles}, M={len(RATIOS)}, reps={REPETITIONS}: {result}")


if __name__ == "__main__":
    main()
