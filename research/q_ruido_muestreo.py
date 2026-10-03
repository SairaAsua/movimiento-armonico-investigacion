"""Synthetic camera-noise counterexample for an arc-length-weighted Q.

One identical 3D line is traversed with two monotone time laws. This is a
measurement simulation, not a model of Nico, a camera, or Laban's equations.
"""

import argparse
import json
import math
import random
import statistics


def quantile(values, fraction):
    ordered = sorted(values)
    position = fraction * (len(ordered) - 1)
    low = int(position)
    high = min(low + 1, len(ordered) - 1)
    weight = position - low
    return ordered[low] * (1 - weight) + ordered[high] * weight


def q_and_length(samples):
    numerator = 0.0
    length = 0.0
    for previous, current in zip(samples, samples[1:]):
        dx, dy, dz = (b - a for a, b in zip(previous, current))
        step = math.sqrt(dx * dx + dy * dy + dz * dz)
        if step == 0:
            continue
        numerator += dx * dx / step
        length += step
    return numerator / length, length


def time_law(t, name):
    return t if name == "uniform" else t + 0.8 * t * (1 - t)


def run(fps, sigma, repetitions, seed):
    rng = random.Random(seed)
    results = {name: {"Q_x": [], "length": []} for name in ("uniform", "early_fast")}
    paired_q_difference = []
    for _ in range(repetitions):
        errors = [tuple(rng.gauss(0, sigma) for _ in range(3)) for _ in range(fps + 1)]
        this_pair = {}
        for name in results:
            samples = []
            for index, error in enumerate(errors):
                t = index / fps
                samples.append((time_law(t, name) + error[0], error[1], error[2]))
            q, length = q_and_length(samples)
            results[name]["Q_x"].append(q)
            results[name]["length"].append(length)
            this_pair[name] = q
        paired_q_difference.append(this_pair["early_fast"] - this_pair["uniform"])
    summary = {}
    for name, measures in results.items():
        summary[name] = {
            metric: {"mean": statistics.mean(values), "p05": quantile(values, 0.05), "p95": quantile(values, 0.95)}
            for metric, values in measures.items()
        }
    return {
        "fps": fps,
        "profiles": summary,
        "paired_Qx_early_minus_uniform": {
            "mean": statistics.mean(paired_q_difference),
            "p05": quantile(paired_q_difference, 0.05),
            "p95": quantile(paired_q_difference, 0.95),
        },
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sigma", type=float, default=0.002, help="independent position noise, geometry units per axis")
    parser.add_argument("--repetitions", type=int, default=400)
    parser.add_argument("--seed", type=int, default=20261003)
    args = parser.parse_args()
    if not 0 <= args.sigma < 1 or args.repetitions < 2:
        parser.error("require 0 <= sigma < 1 and at least two repetitions")
    counts = (30, 120, 480, 1920)
    report = {
        "scope": "synthetic_3d_iid_position_noise_not_camera_measurement",
        "true_Q_x": 1.0,
        "true_length": 1.0,
        "sigma_per_axis": args.sigma,
        "repetitions": args.repetitions,
        "seed": args.seed,
        "noise_only_expected_step_length_3d": 4 * args.sigma / math.sqrt(math.pi),
        "rows": [run(fps, args.sigma, args.repetitions, args.seed + fps) for fps in counts],
    }
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
