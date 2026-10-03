"""Synthetic radial-threshold sensitivity; no camera or human inference."""

from __future__ import annotations

import json
from math import cos, pi, sin

from situacion_ocupacion_arco_sintetica import arc_fraction_inside
from situacion_recorrido_sintetica import norm, subtract


def circle(radius: float, segments: int = 720) -> list[tuple[float, float, float]]:
    return [
        (radius * cos(2 * pi * i / segments), radius * sin(2 * pi * i / segments), 0.0)
        for i in range(segments + 1)
    ]


def length(points: list[tuple[float, float, float]]) -> float:
    return sum(norm(subtract(b, a)) for a, b in zip(points, points[1:]))


def occupancy_interval(
    reference: list[tuple[float, float, float]],
    threshold: float,
    vertex_error_bound: float,
    length_error_bound: float,
) -> tuple[float, float]:
    """Conditional interval for a corresponding polyline at reach=1, origin=0."""
    base_length = length(reference)
    if base_length <= length_error_bound:
        return (0.0, 1.0)
    origin = (0.0, 0.0, 0.0)
    lower_threshold = threshold - vertex_error_bound
    lower_numerator = (
        base_length * arc_fraction_inside(reference, origin, 1.0, lower_threshold)
        if lower_threshold >= 0 else 0.0
    )
    upper_numerator = base_length * arc_fraction_inside(
        reference, origin, 1.0, threshold + vertex_error_bound
    )
    return (
        max(0.0, (lower_numerator - length_error_bound) / (base_length + length_error_bound)),
        min(1.0, (upper_numerator + length_error_bound) / (base_length - length_error_bound)),
    )


def main() -> None:
    inner, outer = circle(0.99), circle(1.01)
    origin = (0.0, 0.0, 0.0)
    inner_fraction = arc_fraction_inside(inner, origin, reach=1.0, normalized_radius=1.0)
    outer_fraction = arc_fraction_inside(outer, origin, reach=1.0, normalized_radius=1.0)
    max_vertex_error = max(norm(subtract(a, b)) for a, b in zip(inner, outer))
    assert len(inner) == len(outer) == 721
    assert abs(inner_fraction - 1.0) < 1e-10
    assert outer_fraction == 0.0
    assert abs(max_vertex_error - 0.02) < 1e-12
    assert 2 * (len(inner) - 1) * max_vertex_error > length(inner)
    reference = [(0.1, 0.0, 0.0), (0.9, 0.0, 0.0)]
    shifted = [(0.11, 0.0, 0.0), (0.91, 0.0, 0.0)]
    bracket = occupancy_interval(reference, 0.5, vertex_error_bound=0.01,
                                 length_error_bound=0.02)
    shifted_fraction = arc_fraction_inside(shifted, origin, 1.0, 0.5)
    assert bracket[0] < shifted_fraction < bracket[1]
    assert bracket[1] - bracket[0] < 0.11
    print(json.dumps({
        "kind": "synthetic_arc_occupancy_threshold_sensitivity",
        "segments": 720,
        "threshold_normalized": 1.0,
        "inner_fraction": inner_fraction,
        "outer_fraction": outer_fraction,
        "max_corresponding_vertex_displacement_R": max_vertex_error,
        "inner_length_R": length(inner),
        "generic_length_error_bound_R": 2 * 720 * max_vertex_error,
        "nonvacuous_line_bracket_at_0_5": bracket,
        "line_shifted_fraction_at_0_5": shifted_fraction,
        "limit": "Synthetic polygons; no measured camera error or Laban category",
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
