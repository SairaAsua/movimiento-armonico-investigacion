"""Equal Q/radial extrema/V_r can hide different arc-length radial occupancy.

Synthetic geometry only. No Laban category, video, or human inference.
"""

from __future__ import annotations

import json
from math import sqrt

from situacion_recorrido_sintetica import describe, dot, norm, subtract


def arc_fraction_inside(
    points: list[tuple[float, float, float]],
    origin: tuple[float, float, float],
    reach: float,
    normalized_radius: float,
) -> float:
    """Exact fraction of a finite polyline's arc inside a centered ball."""
    if not (reach > 0 and normalized_radius >= 0):
        raise ValueError("positive reach and nonnegative threshold required")
    radius2 = (reach * normalized_radius) ** 2
    centered = [subtract(point, origin) for point in points]
    total = 0.0
    inside = 0.0
    for a, b in zip(centered, centered[1:]):
        d = subtract(b, a)
        length = norm(d)
        if length == 0:
            continue
        total += length
        quad_a = dot(d, d)
        quad_b = 2 * dot(a, d)
        quad_c = dot(a, a) - radius2
        discriminant = quad_b**2 - 4 * quad_a * quad_c
        if discriminant < 0:
            continue
        root_low = (-quad_b - sqrt(discriminant)) / (2 * quad_a)
        root_high = (-quad_b + sqrt(discriminant)) / (2 * quad_a)
        fraction = max(0.0, min(1.0, root_high) - max(0.0, root_low))
        inside += fraction * length
    if total == 0:
        raise ValueError("zero-length path has no arc occupancy")
    return inside / total


def main() -> None:
    near_center = [0.2, 0.3, 0.2, 0.3, 0.2, 0.3, 0.2, 0.3, 0.2, 1.0]
    near_edge = [0.2, 1.0, 0.9, 1.0, 0.9, 1.0, 0.9, 1.0, 0.9, 1.0]
    origin = (0.0, 0.0, 0.0)
    result = {}
    for name, radii in (("mostly_inner_arc", near_center), ("mostly_outer_arc", near_edge)):
        points = [(radius, 0.0, 0.0) for radius in radii]
        result[name] = {
            **describe(points, origin, reach=1.0),
            "arc_fraction_at_radius_0_4": round(
                arc_fraction_inside(points, origin, 1.0, 0.4), 6
            ),
        }
    a, b = result.values()
    for key in ("Q", "rho_min", "rho_max", "radial_variation_over_path_length", "path_length"):
        assert a[key] == b[key], key
    assert a["Q"] == [1.0, 0.0, 0.0]
    assert a["rho_min"] == 0.2 and a["rho_max"] == 1.0
    assert a["radial_variation_over_path_length"] == 1.0
    assert a["path_length"] == 1.6
    assert a["arc_fraction_at_radius_0_4"] == 0.625
    assert b["arc_fraction_at_radius_0_4"] == 0.125
    print(json.dumps({"kind": "synthetic_arc_occupancy_only", "threshold_normalized": 0.4,
                      "cases": result}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
