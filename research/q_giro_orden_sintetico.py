"""Signed turning of closed planar point paths: order beyond Q.

Synthetic geometry only. Not a historical Laban equation, rope topology,
physiological metric, or live Beacon signal.
"""

import json
import math

from q_cruces_orden_sintetico import (
    CROSSED_STEPS,
    SIMPLE_STEPS,
    descriptor,
    nonadjacent_crossings,
    vertices,
)
from cruce_trayectoria_incertidumbre import certified_sign


def turn_signature(steps):
    if any(dx == 0 and dy == 0 for dx, dy in steps):
        raise ValueError("zero-length edge has no tangent direction")
    if any(abs(math.fsum(component)) > 1e-12 for component in zip(*steps)):
        raise ValueError("turning number here requires a closed polygon")
    angles = []
    for a, b in zip(steps, steps[1:] + steps[:1]):
        determinant = a[0] * b[1] - a[1] * b[0]
        dot = a[0] * b[0] + a[1] * b[1]
        if determinant == 0 and dot < 0:
            raise ValueError("antiparallel consecutive edges have ambiguous turn sign")
        angles.append(math.atan2(determinant, dot))
    total = sum(angles) / (2 * math.pi)
    nearest_integer = round(total)
    assert abs(total - nearest_integer) < 1e-12
    return {
        "turning_number": nearest_integer,
        "absolute_turn_pi": sum(abs(angle) for angle in angles) / math.pi,
        "signed_turns_pi": [angle / math.pi for angle in angles],
    }


def steps_from_closed_vertices(points):
    assert points[-1] == points[0]
    return tuple(
        (b[0] - a[0], b[1] - a[1]) for a, b in zip(points, points[1:])
    )


def turning_number_certificate(points, epsilon):
    """Sufficient error gate for the sampled polygon, not its hidden path."""
    if points[-1] != points[0] or epsilon < 0:
        return {"status": "invalid_closure_or_error_bound", "value": None}
    n = len(points) - 1
    if any(math.dist(points[i], points[i + 1]) <= 2 * epsilon for i in range(n)):
        return {"status": "unknown_short_edge", "value": None}
    if any(
        certified_sign(points[(i - 1) % n], points[i], points[(i + 1) % n], epsilon) == 0
        for i in range(n)
    ):
        return {"status": "unknown_turn_margin", "value": None}
    return {
        "status": "certified_for_sampled_polygon",
        "value": turn_signature(steps_from_closed_vertices(points))["turning_number"],
    }


def main():
    simple = turn_signature(SIMPLE_STEPS)
    crossed = turn_signature(CROSSED_STEPS)
    assert simple["turning_number"] == 1
    assert crossed["turning_number"] == 0
    assert descriptor(SIMPLE_STEPS)[1] == descriptor(CROSSED_STEPS)[1]

    reversed_steps = tuple((-dx, -dy) for dx, dy in reversed(SIMPLE_STEPS))
    mirrored_steps = tuple((-dx, dy) for dx, dy in SIMPLE_STEPS)
    assert turn_signature(reversed_steps)["turning_number"] == -1
    assert turn_signature(mirrored_steps)["turning_number"] == -1
    assert descriptor(reversed_steps)[1] == descriptor(SIMPLE_STEPS)[1]
    assert descriptor(mirrored_steps)[1] == descriptor(SIMPLE_STEPS)[1]

    crossing_same_turn_vertices = [
        (-1, -3), (1, 2), (1, 3), (0, -1), (-1, 0), (-1, -3)
    ]
    crossing_same_turn = turn_signature(
        steps_from_closed_vertices(crossing_same_turn_vertices)
    )
    crossing_pairs = nonadjacent_crossings(crossing_same_turn_vertices)
    assert crossing_same_turn["turning_number"] == simple["turning_number"]
    assert len(crossing_pairs) == 2

    epsilon_fixture = 0.05
    simple_certificate = turning_number_certificate(vertices(SIMPLE_STEPS), epsilon_fixture)
    crossed_certificate = turning_number_certificate(vertices(CROSSED_STEPS), epsilon_fixture)
    assert simple_certificate == {"status": "certified_for_sampled_polygon", "value": 1}
    assert crossed_certificate == {"status": "certified_for_sampled_polygon", "value": 0}

    near = [(0, 0), (1, 0), (0.5, 0.01), (0, 1), (0, 0)]
    near_compatible = [(0, 0), (1, 0), (0.5, -0.01), (0, 1), (0, 0)]
    epsilon_near = 0.02
    assert math.dist(near[2], near_compatible[2]) <= epsilon_near + 1e-12
    assert turn_signature(steps_from_closed_vertices(near))["turning_number"] == 1
    assert turn_signature(steps_from_closed_vertices(near_compatible))["turning_number"] == 0
    near_certificate = turning_number_certificate(near, epsilon_near)
    assert near_certificate == {"status": "unknown_turn_margin", "value": None}

    report = {
        "scope": "synthetic_closed_planar_point_polygons_only",
        "same_q_xyz": descriptor(SIMPLE_STEPS)[1],
        "simple": {
            **simple,
            "proper_crossings": nonadjacent_crossings(vertices(SIMPLE_STEPS)),
            "epsilon_0_05_certificate": simple_certificate,
        },
        "same_q_crossed": {
            **crossed,
            "proper_crossings": nonadjacent_crossings(vertices(CROSSED_STEPS)),
            "epsilon_0_05_certificate": crossed_certificate,
        },
        "simple_time_reversed_turning_number": turn_signature(reversed_steps)[
            "turning_number"
        ],
        "simple_mirrored_turning_number": turn_signature(mirrored_steps)[
            "turning_number"
        ],
        "different_polygon_same_turning_number": {
            "vertices": crossing_same_turn_vertices,
            "turning_number": crossing_same_turn["turning_number"],
            "proper_crossings": crossing_pairs,
        },
        "near_foldback_observed": {
            "vertices": near,
            "turning_number": 1,
            "epsilon_0_02_certificate": near_certificate,
        },
        "near_foldback_compatible_alternative": {
            "vertices": near_compatible,
            "turning_number": 0,
        },
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
