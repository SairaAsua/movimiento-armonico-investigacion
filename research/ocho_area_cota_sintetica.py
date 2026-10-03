"""Cota determinista del área firmada de un lóbulo poligonal proyectado.

Ejecutar: python ocho_area_cota_sintetica.py
Usa una curva construida y error hipotético; no calibra cámaras ni movimiento humano.
"""

from math import cos, dist, isfinite, pi, sin
from random import Random

from ocho_cinematica_ambigua import N, endpoint


def cross(a, b):
    return a[0] * b[1] - a[1] * b[0]


def area_and_bound(vertices, errors):
    """Polígono cerrado implícitamente; |error de vértice i| <= errors[i]."""
    n = len(vertices)
    if n < 3 or len(errors) != n:
        raise ValueError("se requieren >=3 vértices y una cota por vértice")
    if any(not isfinite(v) for p in vertices for v in p):
        raise ValueError("vértice no finito")
    if any(not isfinite(e) or e < 0 for e in errors):
        raise ValueError("cota de vértice inválida")
    area = sum(cross(vertices[i], vertices[(i + 1) % n]) for i in range(n)) / 2
    linear = sum(errors[i] * dist(vertices[(i + 1) % n], vertices[(i - 1) % n])
                 for i in range(n)) / 2
    quadratic = sum(errors[i] * errors[(i + 1) % n] for i in range(n)) / 2
    return area, linear + quadratic


def synthetic_lobes():
    points = [endpoint(2 * pi * k / N) for k in range(N + 1)]
    # Se elimina el último punto repetido: el cruce es un solo vértice del polígono.
    return points[: N // 2], points[N // 2: -1]


def main():
    rng = Random(20261003)
    for index, vertices in enumerate(synthetic_lobes(), start=1):
        epsilon = 0.005  # unidades arbitrarias hipotéticas, no píxeles de cámara
        bounds = [epsilon] * len(vertices)
        area, limit = area_and_bound(vertices, bounds)
        assert abs(area) > limit
        # Comprobación adversa numérica de la implementación; la prueba es la desigualdad.
        for _ in range(50):
            perturbed = []
            for x, y in vertices:
                radius = epsilon * rng.random() ** 0.5
                angle = 2 * pi * rng.random()
                perturbed.append((x + radius * cos(angle), y + radius * sin(angle)))
            changed_area, _ = area_and_bound(perturbed, [0.0] * len(vertices))
            assert abs(changed_area - area) <= limit + 1e-12
        _, broad_limit = area_and_bound(vertices, [0.01] * len(vertices))
        assert broad_limit >= abs(area)
        mirrored, _ = area_and_bound([(-x, y) for x, y in vertices], bounds)
        assert abs(mirrored + area) < 1e-12
        print(f"lóbulo {index}: área={area:.15f}, cota(0.005)={limit:.15f}, "
              f"cota(0.01)={broad_limit:.15f}; espejo invierte signo")


if __name__ == "__main__":
    main()
