"""Same displacement multiset and Q, different path self-intersection.

These are planar point trajectories, not simultaneous rope centerlines or
observations of a person. Only the order of four displacement vectors changes.
"""

import json
import math


SIMPLE_STEPS = ((-2, 0), (-2, -1), (2, -1), (2, 2))
CROSSED_STEPS = ((2, 2), (-2, 0), (2, -1), (-2, -1))


def vertices(steps):
    points = [(0, 0)]
    for dx, dy in steps:
        x, y = points[-1]
        points.append((x + dx, y + dy))
    assert points[-1] == points[0]
    return points


def descriptor(steps):
    lengths = [math.hypot(dx, dy) for dx, dy in steps]
    arc = sum(lengths)
    qx = sum(dx * dx / length for (dx, _), length in zip(steps, lengths)) / arc
    qy = sum(dy * dy / length for (_, dy), length in zip(steps, lengths)) / arc
    return arc, (qx, qy, 0.0)


def orientation(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def proper_crossing(a, b, c, d):
    return orientation(a, b, c) * orientation(a, b, d) < 0 and (
        orientation(c, d, a) * orientation(c, d, b) < 0
    )


def nonadjacent_crossings(points):
    n = len(points) - 1
    result = []
    for i in range(n):
        for j in range(i + 2, n):
            if i == 0 and j == n - 1:
                continue  # The first and last edges share the closing vertex.
            if proper_crossing(points[i], points[i + 1], points[j], points[j + 1]):
                result.append((i, j))
    return result


def main():
    assert sorted(SIMPLE_STEPS) == sorted(CROSSED_STEPS)
    simple, crossed = vertices(SIMPLE_STEPS), vertices(CROSSED_STEPS)
    arc_simple, q_simple = descriptor(SIMPLE_STEPS)
    arc_crossed, q_crossed = descriptor(CROSSED_STEPS)
    assert abs(arc_simple - arc_crossed) < 1e-12
    assert max(abs(a - b) for a, b in zip(q_simple, q_crossed)) < 1e-12
    assert nonadjacent_crossings(simple) == []
    assert nonadjacent_crossings(crossed) == [(0, 2)]
    report = {
        "scope": "synthetic_planar_point_paths_not_simultaneous_rope_topology_or_people",
        "shared_displacement_multiset": sorted(SIMPLE_STEPS),
        "shared_arc_length": arc_simple,
        "shared_q_xyz": q_simple,
        "shared_start_end": [0, 0],
        "simple_path_vertices": simple,
        "simple_proper_crossings": [],
        "crossed_path_vertices": crossed,
        "crossed_proper_crossings_edge_pairs": [[0, 2]],
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
