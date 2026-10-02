#!/usr/bin/env python3
"""Contraejemplos de orientación Q frente a situación de un recorrido 3D.

Curvas ideales, sin movimiento humano ni clasificación Laban automática.
"""

from __future__ import annotations

import json
import math
from typing import Sequence


Point = tuple[float, float, float]


def subtract(a: Point, b: Point) -> Point:
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def dot(a: Point, b: Point) -> float:
    return sum(x * y for x, y in zip(a, b))


def norm(a: Point) -> float:
    return math.sqrt(dot(a, a))


def segment_min_radius(a: Point, b: Point) -> float:
    """Distancia exacta de 0 al segmento finito [a,b], no a su línea infinita."""
    delta = subtract(b, a)
    square = dot(delta, delta)
    if square == 0:
        return norm(a)
    t = min(1.0, max(0.0, -dot(a, delta) / square))
    return norm(tuple(a[j] + t * delta[j] for j in range(3)))


def describe(points: Sequence[Point], origin: Point, reach: float) -> dict:
    if len(points) < 2 or not math.isfinite(reach) or reach <= 0:
        raise ValueError("Se requieren al menos dos puntos y alcance positivo")
    if len(origin) != 3 or any(not math.isfinite(v) for v in origin):
        raise ValueError("Origen 3D finito requerido")
    if any(len(p) != 3 or any(not math.isfinite(v) for v in p) for p in points):
        raise ValueError("Puntos 3D finitos requeridos")
    centered = [subtract(p, origin) for p in points]
    segments = [(a, b, subtract(b, a)) for a, b in zip(centered, centered[1:])]
    lengths = [norm(delta) for _, _, delta in segments]
    total = sum(lengths)
    if total == 0:
        raise ValueError("Recorrido sin longitud: orientación y variación radial indefinidas")
    q = [sum(delta[j] ** 2 / length for (_, _, delta), length
             in zip(segments, lengths) if length > 0) / total for j in range(3)]
    minimum = min(segment_min_radius(a, b) for a, b, _ in segments) / reach
    maximum = max(norm(p) for p in centered) / reach
    radial_variation = sum(norm(a) + norm(b) - 2 * segment_min_radius(a, b)
                           for a, b, _ in segments) / total
    return {"Q": [round(v, 6) for v in q], "rho_min": round(minimum, 6),
            "rho_max": round(maximum, 6),
            "radial_variation_over_path_length": round(radial_variation, 6),
            "path_length": round(total, 6)}


def main() -> None:
    central = [(-1.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 0.0, 0.0)]
    translated = [(-1.0, 0.5, 0.0), (0.0, 0.5, 0.0), (1.0, 0.5, 0.0)]
    far_on_center_line = [(0.4, 0.0, 0.0), (0.6, 0.0, 0.0), (0.8, 0.0, 0.0)]
    peripheral_arc = [(1.5 * math.cos(math.pi * i / 32),
                       1.5 * math.sin(math.pi * i / 32), 0.0)
                      for i in range(33)]
    curves = {"central_line": central, "parallel_offset_line": translated,
              "far_segment_on_central_support": far_on_center_line,
              "semicircular_arc": peripheral_arc}
    result = {name: describe(points, (0.0, 0.0, 0.0), 1.5)
              for name, points in curves.items()}
    assert all(result[name]["Q"] == [1.0, 0.0, 0.0]
               for name in ("central_line", "parallel_offset_line",
                            "far_segment_on_central_support"))
    assert [result[name]["rho_min"] for name in (
        "central_line", "parallel_offset_line", "far_segment_on_central_support")
        ] == [0.0, 0.333333, 0.266667]
    assert result["central_line"]["radial_variation_over_path_length"] == 1.0
    assert 0 < result["semicircular_arc"]["radial_variation_over_path_length"] < 0.03
    offset = (7.0, -3.0, 2.0)
    moved = [tuple(p[j] + offset[j] for j in range(3)) for p in translated]
    assert describe(moved, offset, 1.5) == result["parallel_offset_line"]
    scaled = [tuple(2 * p[j] for j in range(3)) for p in translated]
    scaled_result = describe(scaled, (0.0, 0.0, 0.0), 3.0)
    assert scaled_result["Q"] == result["parallel_offset_line"]["Q"]
    assert scaled_result["rho_min"] == result["parallel_offset_line"]["rho_min"]
    assert scaled_result["radial_variation_over_path_length"] == result[
        "parallel_offset_line"]["radial_variation_over_path_length"]
    perturbed = [(p[0] + (0.02 if i % 2 else -0.02), p[1], p[2])
                 for i, p in enumerate(translated)]
    noisy = describe(perturbed, (0.01, 0.0, 0.0), 1.5)
    assert abs(noisy["rho_min"] - result["parallel_offset_line"]["rho_min"]) <= (
        0.02 + 0.01) / 1.5 + 1e-6
    print(json.dumps({"kind": "synthetic_geometry_only", "reach": 1.5,
                      "cases": result}, indent=2))


if __name__ == "__main__":
    main()
