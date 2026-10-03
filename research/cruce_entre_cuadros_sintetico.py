"""Two bounded-speed point paths with identical samples and different crossings.

This is an ideal instantaneous-sampling example in arbitrary spatial units.
It says nothing about actual cameras, exposure, rope mechanics, or people.
"""

import json
import math


BASE_LOOP = ((0, 0), (0.8, 0.8), (0.2, 0.8), (0.8, 0.2), (1, 0))


def length(points):
    return sum(math.dist(a, b) for a, b in zip(points, points[1:]))


def orientation(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def proper_crossing(a, b, c, d):
    return orientation(a, b, c) * orientation(a, b, d) < 0 and (
        orientation(c, d, a) * orientation(c, d, b) < 0
    )


def nonadjacent_crossings(points):
    result = []
    for i in range(len(points) - 1):
        for j in range(i + 2, len(points) - 1):
            if proper_crossing(points[i], points[i + 1], points[j], points[j + 1]):
                result.append((i, j))
    return result


def hidden_loop(start, scale):
    points = [(0, 0), (start, 0)]
    points.extend((start + scale * x, scale * y) for x, y in BASE_LOOP[1:])
    points.append((1, 0))
    return points


def main():
    straight = [(0, 0), (1, 0)]
    scale = 0.01
    loop = hidden_loop(0.5, scale)
    speed_ceiling = 1.1
    baseline_length = length(BASE_LOOP)
    loop_length = length(loop)
    maximum_scale_for_ceiling = (speed_ceiling - 1) / (baseline_length - 1)
    assert abs(loop_length - (1 + scale * (baseline_length - 1))) < 1e-12
    assert scale < maximum_scale_for_ceiling and loop_length < speed_ceiling
    assert straight[0] == loop[0] and straight[-1] == loop[-1]
    assert nonadjacent_crossings(straight) == []
    assert nonadjacent_crossings(loop) == [(1, 3)]
    report = {
        "scope": "synthetic_ideal_instantaneous_point_samples_only",
        "sample_times_seconds": [0, 1],
        "shared_sampled_positions": straight,
        "shared_sampled_q_xy": [1, 0],
        "speed_ceiling_units_per_second": speed_ceiling,
        "straight_arc_length_units": length(straight),
        "straight_proper_crossings": [],
        "hidden_loop_scale": scale,
        "maximum_hidden_loop_scale_at_speed_ceiling": maximum_scale_for_ceiling,
        "loop_arc_length_units": loop_length,
        "loop_proper_crossing_edge_pairs": nonadjacent_crossings(loop),
        "loop_vertices": loop,
        "base_loop_length_units": baseline_length,
    }
    print(json.dumps(report, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
