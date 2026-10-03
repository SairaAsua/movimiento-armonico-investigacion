"""Synthetic Q tradeoff between noisy short steps and missing curved geometry.

The helix-like ellipse and Gaussian position errors are constructed examples,
not observed rope flow or camera specifications.
"""

import argparse
import json
import math
import random
import statistics


DENSE_FPS = 1920
COUNTS = (4, 8, 15, 30, 60, 120, 240, 480, 960, 1920)


def curve(t):
    return (math.cos(2 * math.pi * t), 0.4 * math.sin(2 * math.pi * t), 0.3 * t)


def q_and_length(points):
    numerators = [0.0, 0.0, 0.0]
    length = 0.0
    for a, b in zip(points, points[1:]):
        steps = [b[k] - a[k] for k in range(3)]
        norm = math.sqrt(sum(v * v for v in steps))
        if norm == 0:
            continue
        length += norm
        for k, value in enumerate(steps):
            numerators[k] += value * value / norm
    return [value / length for value in numerators], length


def quantile(values, fraction):
    ordered = sorted(values)
    index = fraction * (len(ordered) - 1)
    lower = int(index)
    weight = index - lower
    return ordered[lower] * (1 - weight) + ordered[min(lower + 1, len(ordered) - 1)] * weight


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sigma", type=float, default=0.01, help="position error SD, geometry units per axis")
    parser.add_argument("--repetitions", type=int, default=200)
    parser.add_argument("--seed", type=int, default=20261004)
    args = parser.parse_args()
    if not 0 <= args.sigma < 1 or args.repetitions < 2:
        parser.error("require 0 <= sigma < 1 and at least two repetitions")

    reference_q, reference_length = q_and_length([curve(i / 200000) for i in range(200001)])
    true_dense = [curve(i / DENSE_FPS) for i in range(DENSE_FPS + 1)]
    rows = {}
    for fps in COUNTS:
        if DENSE_FPS % fps:
            raise AssertionError("sampling grid must be nested")
        indices = range(0, DENSE_FPS + 1, DENSE_FPS // fps)
        q, length = q_and_length([true_dense[i] for i in indices])
        rows[fps] = {
            "fps": fps,
            "noiseless_Q_L1_error": sum(abs(q[k] - reference_q[k]) for k in range(3)),
            "noiseless_length_relative_error": abs(length / reference_length - 1),
            "noisy_Q_L1_error": [],
            "noisy_length_relative_error": [],
        }

    rng = random.Random(args.seed)
    for _ in range(args.repetitions):
        errors = [tuple(rng.gauss(0, args.sigma) for _ in range(3)) for _ in true_dense]
        noisy_dense = [tuple(true_dense[i][k] + errors[i][k] for k in range(3)) for i in range(len(true_dense))]
        for fps in COUNTS:
            indices = range(0, DENSE_FPS + 1, DENSE_FPS // fps)
            q, length = q_and_length([noisy_dense[i] for i in indices])
            rows[fps]["noisy_Q_L1_error"].append(sum(abs(q[k] - reference_q[k]) for k in range(3)))
            rows[fps]["noisy_length_relative_error"].append(abs(length / reference_length - 1))

    for row in rows.values():
        for name in ("noisy_Q_L1_error", "noisy_length_relative_error"):
            values = row[name]
            row[name] = {"mean": statistics.mean(values), "p05": quantile(values, 0.05), "p95": quantile(values, 0.95)}
    report = {
        "scope": "synthetic_nested_sampling_iid_3d_noise_not_camera_measurement",
        "curve": "(cos(2*pi*t), 0.4*sin(2*pi*t), 0.3*t), t in [0,1]",
        "reference_Q": reference_q,
        "reference_length": reference_length,
        "sigma_per_axis": args.sigma,
        "seed": args.seed,
        "repetitions": args.repetitions,
        "rows": [rows[fps] for fps in COUNTS],
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
