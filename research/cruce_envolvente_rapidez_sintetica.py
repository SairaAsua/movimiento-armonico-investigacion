"""Reachability envelopes for pairs of nonadjacent 2D point-path intervals.

All distances, durations, speed limits, and errors are invented. The code
illustrates a conditional no-crossing gate, not camera or rope validation.
"""

import json
import math


def ellipse_half_width(chord_length, path_length_budget):
    if path_length_budget < chord_length:
        raise ValueError("speed budget incompatible with observed endpoints")
    return math.sqrt(path_length_budget**2 - chord_length**2) / 2


def path_length(points):
    return sum(math.dist(a, b) for a, b in zip(points, points[1:]))


def orientation(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def proper_crossing(a, b, c, d):
    return orientation(a, b, c) * orientation(a, b, d) < 0 and (
        orientation(c, d, a) * orientation(c, d, b) < 0
    )


def pair_crossings(first, second):
    return [
        (i, j)
        for i in range(len(first) - 1)
        for j in range(len(second) - 1)
        if proper_crossing(first[i], first[i + 1], second[j], second[j + 1])
    ]


def main():
    duration = 1.0
    speed_limit = 1.1
    endpoint_error = 0.01
    chord_length = 1.0
    far_gap = 0.8
    near_gap = 0.2

    exact_half_width = ellipse_half_width(chord_length, speed_limit * duration)
    outer_half_width = ellipse_half_width(
        chord_length, speed_limit * duration + 2 * endpoint_error
    )
    far_envelope_clearance = far_gap - 2 * outer_half_width
    assert far_envelope_clearance > 0
    assert far_gap < speed_limit * duration  # The coarser tube test cannot decide.

    near_straight_a = [(0, 0), (1, 0)]
    near_straight_b = [(0, near_gap), (1, near_gap)]
    near_bowed_a = [(0, 0), (0.5, 0.22), (1, 0)]
    assert pair_crossings(near_straight_a, near_straight_b) == []
    assert pair_crossings(near_bowed_a, near_straight_b) == [(0, 0), (1, 0)]
    assert path_length(near_bowed_a) < speed_limit * duration
    assert near_gap < 2 * exact_half_width

    report = {
        "scope": "synthetic_nonadjacent_2d_point_path_intervals_only",
        "duration_seconds_each": duration,
        "speed_limit_units_per_second": speed_limit,
        "hard_endpoint_error_units_each": endpoint_error,
        "chord_length_units_each": chord_length,
        "ellipse_half_width_exact_endpoints_units": exact_half_width,
        "ellipse_half_width_outer_error_units": outer_half_width,
        "far_parallel_chord_gap_units": far_gap,
        "far_outer_envelope_clearance_units": far_envelope_clearance,
        "far_coarse_tube_gate": "inconclusive",
        "far_ellipse_gate": "no_interinterval_crossing",
        "near_parallel_chord_gap_units": near_gap,
        "near_straight_pair_crossings": [],
        "near_bowed_pair_crossings": pair_crossings(near_bowed_a, near_straight_b),
        "near_bowed_path_length_units": path_length(near_bowed_a),
        "near_envelope_gate": "unknown",
    }
    print(json.dumps(report, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
