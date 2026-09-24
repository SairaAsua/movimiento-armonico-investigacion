"""Contraejemplo sintético: una sola vista no identifica una curva 3D.

Ejecutar: python proyeccion_2d_ambigua.py
Biblioteca estándar; no usa video humano ni valida Laban/HarMoCAP.
"""

from math import cos, dist, pi, sin


def project(point):
    """Cámara pinhole ideal con focal normalizada 1, sin distorsión."""
    x, y, z = point
    assert z > 0
    return x / z, y / z


def path_length(points):
    return sum(dist(a, b) for a, b in zip(points, points[1:]))


def main():
    n = 720
    angles = [2 * pi * k / n for k in range(n + 1)]
    image_curve = [(0.2 * cos(t), 0.2 * sin(t)) for t in angles]

    def lift(depth):
        return [(u * z, v * z, z)
                for (u, v), z in zip(image_curve, depth)]

    flat_depth = [2.0 for _ in angles]
    varying_depth = [2.0 + 0.6 * sin(2 * t) for t in angles]
    flat = lift(flat_depth)
    spatial = lift(varying_depth)

    max_image_difference = max(
        dist(project(a), project(b)) for a, b in zip(flat, spatial)
    )
    flat_length, spatial_length = path_length(flat), path_length(spatial)
    assert max_image_difference < 1e-12
    assert spatial_length > flat_length * 1.4
    assert max(varying_depth) - min(varying_depth) > 1.19

    print(f"diferencia máxima en imagen={max_image_difference:.12f}")
    print(f"longitud 3D A={flat_length:.6f}; B={spatial_length:.6f}")
    print(f"profundidad A={min(flat_depth):.1f}..{max(flat_depth):.1f}; "
          f"B={min(varying_depth):.1f}..{max(varying_depth):.1f}")


if __name__ == "__main__":
    main()
