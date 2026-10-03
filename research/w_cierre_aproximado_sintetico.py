"""A near-closed observed path admits different unobserved completions.

Synthetic 2D point geometry only. The construction is not rope topology.
"""

import json
import math

from q_giro_orden_sintetico import steps_from_closed_vertices, turn_signature


START = (0.0, 0.0)
CLOSURE_TOLERANCE = 0.1
END_DISTANCE = CLOSURE_TOLERANCE / 2
OBSERVED_OPEN = (
    START,
    (1.0, 0.0),
    (1.0, 1.0),
    (0.0, 1.0),
    (0.0, END_DISTANCE),
)


def completion(loop_side, side):
    """A loop of either orientation followed by a straight return to start."""
    end = OBSERVED_OPEN[-1]
    if loop_side == 0:
        return (START,)
    return (
        (side * loop_side, end[1]),
        (side * loop_side, end[1] + loop_side),
        (0.0, end[1] + loop_side),
        end,
        START,
    )


def summarize(extra):
    polygon = OBSERVED_OPEN + extra
    return {
        "W": turn_signature(steps_from_closed_vertices(polygon))["turning_number"],
        "unobserved_completion_vertices": extra,
        "completion_length": sum(
            math.dist(a, b) for a, b in zip(polygon[len(OBSERVED_OPEN) - 1 :], polygon[len(OBSERVED_OPEN) :])
        ),
        "largest_distance_of_completion_from_start": max(
            math.dist(point, START) for point in (OBSERVED_OPEN[-1],) + extra
        ),
    }


def main():
    side = END_DISTANCE / 4
    direct = summarize(completion(0, 1))
    positive_loop = summarize(completion(side, 1))
    negative_loop = summarize(completion(side, -1))
    assert (negative_loop["W"], direct["W"], positive_loop["W"]) == (0, 1, 2)
    assert math.dist(OBSERVED_OPEN[0], OBSERVED_OPEN[-1]) < CLOSURE_TOLERANCE
    assert all(
        item["largest_distance_of_completion_from_start"] < CLOSURE_TOLERANCE
        for item in (direct, positive_loop, negative_loop)
    )
    assert math.isclose(direct["completion_length"], END_DISTANCE)
    assert math.isclose(positive_loop["completion_length"], END_DISTANCE + 4 * side)

    tiny_side = END_DISTANCE / 1_000
    tiny_loop = summarize(completion(tiny_side, 1))
    assert tiny_loop["W"] == 2
    assert tiny_loop["largest_distance_of_completion_from_start"] < CLOSURE_TOLERANCE
    assert math.isclose(
        tiny_loop["completion_length"] - direct["completion_length"], 4 * tiny_side
    )

    report = {
        "scope": "synthetic_near_closed_projected_point_path_not_continuous_observation",
        "closure_tolerance": CLOSURE_TOLERANCE,
        "observed_open_prefix": OBSERVED_OPEN,
        "endpoint_distance": END_DISTANCE,
        "direct_chord": direct,
        "positive_hidden_loop": positive_loop,
        "negative_hidden_loop": negative_loop,
        "arbitrarily_small_loop_example": tiny_loop,
        "all_completion_vertices_inside_tolerance_disk": True,
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
