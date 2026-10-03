"""Conservative 2D point-path crossing certificates under endpoint error.

The guarantee concerns only proper crossings of observed straight segments.
It does not certify the continuous motion between samples or rope topology.
"""

import json
import math


def orientation(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def margin(a, b, c, epsilon):
    """Upper bound on orientation error if every endpoint moves <= epsilon."""
    ab = math.dist(a, b)
    ac = math.dist(a, c)
    return 2 * epsilon * (ab + ac) + 4 * epsilon * epsilon


def certified_sign(a, b, c, epsilon):
    value = orientation(a, b, c)
    bound = margin(a, b, c, epsilon)
    if abs(value) <= bound:
        return 0
    return 1 if value > 0 else -1


def pair_certificate(a, b, c, d, epsilon):
    signs = [
        certified_sign(a, b, c, epsilon),
        certified_sign(a, b, d, epsilon),
        certified_sign(c, d, a, epsilon),
        certified_sign(c, d, b, epsilon),
    ]
    if all(signs) and signs[0] == -signs[1] and signs[2] == -signs[3]:
        return "proper_crossing"
    if signs[0] == signs[1] != 0 or signs[2] == signs[3] != 0:
        return "no_proper_crossing"
    return "unknown"


def path_certificates(points, epsilon):
    n = len(points) - 1
    pairs = {}
    for i in range(n):
        for j in range(i + 2, n):
            if i == 0 and j == n - 1:
                continue
            pairs[f"{i}-{j}"] = pair_certificate(
                points[i], points[i + 1], points[j], points[j + 1], epsilon
            )
    return pairs


def main():
    simple = [(0, 0), (-2, 0), (-4, -1), (-2, -2), (0, 0)]
    crossed = [(0, 0), (2, 2), (0, 2), (2, 1), (0, 0)]
    epsilon_fixture = 0.05
    simple_pairs = path_certificates(simple, epsilon_fixture)
    crossed_pairs = path_certificates(crossed, epsilon_fixture)
    assert set(simple_pairs.values()) == {"no_proper_crossing"}
    assert crossed_pairs == {"0-2": "proper_crossing", "1-3": "no_proper_crossing"}

    a, b = (0, 0), (2, 0)
    c, d = (1, -0.01), (1, 0.01)
    shifted_c, shifted_d = (1, 0.01), (1, 0.03)
    epsilon_near = 0.02
    assert math.dist(c, shifted_c) <= epsilon_near + 1e-12
    assert math.dist(d, shifted_d) <= epsilon_near + 1e-12
    assert pair_certificate(a, b, c, d, 0) == "proper_crossing"
    assert pair_certificate(a, b, shifted_c, shifted_d, 0) == "no_proper_crossing"
    assert pair_certificate(a, b, c, d, epsilon_near) == "unknown"

    report = {
        "scope": "synthetic_planar_point_path_polylines_only",
        "fixture_endpoint_error_bound_units": epsilon_fixture,
        "simple_pair_certificates": simple_pairs,
        "crossed_pair_certificates": crossed_pairs,
        "near_contact_observed_pair": [a, b, c, d],
        "near_contact_compatible_non_crossing_pair": [a, b, shifted_c, shifted_d],
        "near_contact_endpoint_error_bound_units": epsilon_near,
        "near_contact_certificate": "unknown",
    }
    print(json.dumps(report, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
