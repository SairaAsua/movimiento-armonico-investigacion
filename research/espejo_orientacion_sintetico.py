"""Prueba sintética de signo bajo espejo; no procesa video humano."""

from math import atan2, hypot, isclose, pi


def signed_area(points):
    return sum(x * yy - xx * y for (x, y), (xx, yy) in zip(points, points[1:] + points[:1])) / 2


def perimeter(points):
    return sum(hypot(xx - x, yy - y) for (x, y), (xx, yy) in zip(points, points[1:] + points[:1]))


points = [(1, 0), (0, 1), (-1, 0), (0, -1)]  # horario en imagen: y hacia abajo
mirrored = [(-x, y) for x, y in points]
assert signed_area(points) > 0
assert isclose(signed_area(mirrored), -signed_area(points))
assert isclose(perimeter(mirrored), perimeter(points))

for x, y in points:
    original_phase = atan2(y, x)
    mirrored_phase = atan2(y, -x)
    assert isclose((mirrored_phase + original_phase - pi) % (2 * pi), 0, abs_tol=1e-12)

print(f"área original={signed_area(points):.1f}; reflejada={signed_area(mirrored):.1f}; perímetro={perimeter(points):.3f} en ambas")
