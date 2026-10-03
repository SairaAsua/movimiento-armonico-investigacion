"""Shared noisy task-clock counterexample for residual hand coordination.

This linear timing-residual toy model is not a circular phase estimator or
human rope-flow measurement. It shows how a common imperfect reference can
manufacture residual covariance when two observed signals are conditionally
independent given their true common drive.
"""

import argparse
import json
import math
import random


def correlation(a, b):
    n = len(a)
    ma, mb = sum(a) / n, sum(b) / n
    covariance = sum((x - ma) * (y - mb) for x, y in zip(a, b))
    va = sum((x - ma) ** 2 for x in a)
    vb = sum((y - mb) ** 2 for y in b)
    return covariance / math.sqrt(va * vb)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phrases", type=int, default=400)
    parser.add_argument("--cycles", type=int, default=32)
    parser.add_argument("--seed", type=int, default=20261003)
    args = parser.parse_args()
    if args.phrases < 3 or args.cycles < 2:
        parser.error("need at least three phrases and two cycles per phrase")

    variance_drive = 1.0
    variance_clock = 0.25
    variance_hand = 0.09
    lam = variance_drive / (variance_drive + variance_clock)
    rng = random.Random(args.seed)
    corrected_a, corrected_b = [], []
    naive_a, naive_b = [], []
    perfect_a, perfect_b = [], []
    for _ in range(args.phrases):
        one_corrected_a, one_corrected_b = [], []
        one_naive_a, one_naive_b = [], []
        one_perfect_a, one_perfect_b = [], []
        for _ in range(args.cycles):
            drive = rng.gauss(0, math.sqrt(variance_drive))
            clock_error = rng.gauss(0, math.sqrt(variance_clock))
            hand_a_error = rng.gauss(0, math.sqrt(variance_hand))
            hand_b_error = rng.gauss(0, math.sqrt(variance_hand))
            observed_clock = drive + clock_error
            hand_a = drive + hand_a_error
            hand_b = drive + hand_b_error
            one_corrected_a.append(hand_a - lam * observed_clock)
            one_corrected_b.append(hand_b - lam * observed_clock)
            one_naive_a.append(hand_a - observed_clock)
            one_naive_b.append(hand_b - observed_clock)
            one_perfect_a.append(hand_a - drive)
            one_perfect_b.append(hand_b - drive)
        corrected_a.append(one_corrected_a)
        corrected_b.append(one_corrected_b)
        naive_a.append(one_naive_a)
        naive_b.append(one_naive_b)
        perfect_a.append(one_perfect_a)
        perfect_b.append(one_perfect_b)

    flatten = lambda grouped: [value for phrase in grouped for value in phrase]
    shifted_b = corrected_b[1:] + corrected_b[:1]
    conditional_variance = variance_drive * variance_clock / (variance_drive + variance_clock)
    report = {
        "scope": "synthetic_linear_timing_residuals_not_circular_phase_or_people",
        "phrases": args.phrases,
        "cycles_per_phrase": args.cycles,
        "seed": args.seed,
        "variance_drive": variance_drive,
        "variance_clock": variance_clock,
        "variance_hand_each": variance_hand,
        "population_ols_clock_coefficient": lam,
        "theoretical_corrected_residual_covariance": conditional_variance,
        "theoretical_corrected_residual_correlation": conditional_variance / (conditional_variance + variance_hand),
        "theoretical_naive_subtraction_correlation": variance_clock / (variance_clock + variance_hand),
        "sample_corrected_residual_correlation": correlation(flatten(corrected_a), flatten(corrected_b)),
        "sample_cross_phrase_pairing_correlation": correlation(flatten(corrected_a), flatten(shifted_b)),
        "sample_naive_subtraction_correlation": correlation(flatten(naive_a), flatten(naive_b)),
        "sample_perfect_clock_correlation": correlation(flatten(perfect_a), flatten(perfect_b)),
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
