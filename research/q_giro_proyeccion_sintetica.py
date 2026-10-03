"""Same nonplanar 3D point path, different 2D turning by view.

Orthographic axis projections are idealized observations. This does not
measure people, rope, physical cameras, or a historical Laban scale.
"""

import json

from q_cruces_orden_sintetico import nonadjacent_crossings
from cruce_trayectoria_incertidumbre import orientation, pair_certificate
from q_giro_orden_sintetico import steps_from_closed_vertices, turn_signature


VERTICES_3D = ((-2, 2, -1), (1, -1, 1), (0, 3, -3), (-1, 2, 2))


def closed_projection(indices):
    projected = [tuple(point[index] for index in indices) for point in VERTICES_3D]
    return projected + [projected[0]]


def scalar_triple(a, b, c):
    return sum(
        a[i] * (b[(i + 1) % 3] * c[(i + 2) % 3] - b[(i + 2) % 3] * c[(i + 1) % 3])
        for i in range(3)
    )


def turning(points):
    return turn_signature(steps_from_closed_vertices(points))["turning_number"]


def main():
    xy = closed_projection((0, 1))
    xz = closed_projection((0, 2))
    origin = VERTICES_3D[0]
    vectors = [tuple(point[i] - origin[i] for i in range(3)) for point in VERTICES_3D[1:]]
    volume6 = scalar_triple(*vectors)
    xy_sheared = [(x + 0.3 * y, 1.2 * y) for x, y in xy]
    xy_mirrored = [(x, -y) for x, y in xy]

    assert volume6 == 31  # No single plane contains the four 3D vertices.
    assert turning(xy) == 1 and nonadjacent_crossings(xy) == []
    assert turning(xz) == 0 and nonadjacent_crossings(xz) == [(0, 2)]
    for i, j in ((0, 2), (1, 3)):
        a, b, c, d = xy[i], xy[i + 1], xy[j], xy[j + 1]
        assert pair_certificate(a, b, c, d, 0) == "no_proper_crossing"
        assert all(
            orientation(*triple) != 0
            for triple in ((a, b, c), (a, b, d), (c, d, a), (c, d, b))
        )  # The XY nonadjacent edges neither cross nor touch.
    assert turning(xy_sheared) == turning(xy)
    assert turning(xy_mirrored) == -turning(xy)

    report = {
        "scope": "one_synthetic_nonplanar_3d_point_polygon_two_orthographic_views",
        "vertices_3d": VERTICES_3D,
        "six_times_signed_tetrahedron_volume": volume6,
        "xy_projected_vertices": xy,
        "xy_turning_number": turning(xy),
        "xy_proper_crossings": nonadjacent_crossings(xy),
        "xz_projected_vertices": xz,
        "xz_turning_number": turning(xz),
        "xz_proper_crossings": nonadjacent_crossings(xz),
        "xy_orientation_preserving_shear_turning_number": turning(xy_sheared),
        "xy_mirror_turning_number": turning(xy_mirrored),
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
