"""Hard-error angle bound for a causal turn of a sampled 2D point path.

All lengths and errors are invented. No camera, person, rope or audio is used.
"""

import json
import math
import random

from w_giro_tiempo_beacon_sintetico import local_signed_turn


def circular_distance(a, b):
    return abs(math.atan2(math.sin(a - b), math.cos(a - b)))


def turn_error_gate(points, epsilon):
    if epsilon < 0:
        raise ValueError("epsilon must be nonnegative")
    p, q, r = points
    first = math.dist(p, q)
    second = math.dist(q, r)
    if min(first, second) <= 2 * epsilon:
        return {
            "nominal_turn_rad": local_signed_turn(p, q, r) if min(first, second) > 0 else None,
            "angular_error_bound_rad": None,
            "signed_turn_status": "unknown_short_edge",
        }
    nominal = local_signed_turn(p, q, r)
    bound = math.asin(2 * epsilon / first) + math.asin(2 * epsilon / second)
    # A signed principal angle has cuts at both 0 (sign) and pi/-pi (wrap).
    distance_to_zero = abs(nominal)
    distance_to_reversal = math.pi - abs(nominal)
    if bound >= distance_to_zero and bound >= distance_to_reversal:
        status = "unknown_sign_and_branch"
    elif bound >= distance_to_zero:
        status = "unknown_sign"
    elif bound >= distance_to_reversal:
        status = "unknown_branch"
    else:
        status = "signed_turn_certified"
    return {
        "nominal_turn_rad": nominal,
        "angular_error_bound_rad": bound,
        "signed_turn_status": status,
    }


def random_point_in_disk(rng, center, radius):
    angle = rng.uniform(0, 2 * math.pi)
    distance = radius * math.sqrt(rng.random())
    return (
        center[0] + distance * math.cos(angle),
        center[1] + distance * math.sin(angle),
    )


def main():
    cases = {
        "right_angle_certified": {
            "points": ((0, 0), (1, 0), (1, 1)),
            "epsilon": 0.05,
        },
        "near_straight_unknown": {
            "points": ((0, 0), (1, 0), (2, 0.01)),
            "epsilon": 0.02,
        },
        "near_reversal_unknown": {
            "points": ((0, 0), (1, 0), (0.01, 0.01)),
            "epsilon": 0.02,
        },
        "short_edge_unknown": {
            "points": ((0, 0), (0.01, 0), (1, 1)),
            "epsilon": 0.01,
        },
    }
    rng = random.Random(20261003)
    output = {}
    for name, case in cases.items():
        points = case["points"]
        epsilon = case["epsilon"]
        result = turn_error_gate(points, epsilon)
        bound = result["angular_error_bound_rad"]
        largest_observed_error = 0.0
        if bound is not None:
            for _ in range(10_000):
                perturbed = tuple(random_point_in_disk(rng, p, epsilon) for p in points)
                error = circular_distance(
                    local_signed_turn(*perturbed), result["nominal_turn_rad"]
                )
                assert error <= bound + 1e-12
                largest_observed_error = max(largest_observed_error, error)
        output[name] = {
            "observed_points": points,
            "epsilon": epsilon,
            **result,
            "largest_error_in_10000_draws_rad": largest_observed_error if bound is not None else None,
        }
    assert output["right_angle_certified"]["signed_turn_status"] == "signed_turn_certified"
    assert output["near_straight_unknown"]["signed_turn_status"] == "unknown_sign"
    assert output["near_reversal_unknown"]["signed_turn_status"] == "unknown_branch"
    assert output["short_edge_unknown"]["signed_turn_status"] == "unknown_short_edge"
    assert turn_error_gate(((0, 0), (0, 0), (1, 1)), 0.01)["signed_turn_status"] == "unknown_short_edge"
    # Perturb only the third vertex: both observed configurations are compatible.
    straight = cases["near_straight_unknown"]["points"]
    reversed_side = (*straight[:2], (2, -0.01))
    assert math.dist(straight[2], reversed_side[2]) <= cases["near_straight_unknown"]["epsilon"]
    assert local_signed_turn(*straight) * local_signed_turn(*reversed_side) < 0
    reverse = cases["near_reversal_unknown"]["points"]
    opposite_branch = (*reverse[:2], (0.01, -0.01))
    assert math.dist(reverse[2], opposite_branch[2]) <= cases["near_reversal_unknown"]["epsilon"]
    assert local_signed_turn(*reverse) > 0 > local_signed_turn(*opposite_branch)
    print(json.dumps({"scope": "synthetic_projected_point_turn_hard_error", "cases": output}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
