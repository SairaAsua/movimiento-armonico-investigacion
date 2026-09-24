"""Banco geométrico de planos 3D; sólo trayectorias sintéticas, sin datos humanos.

Ejecutar: python3 planos_sinteticos.py
La PCA/Jacobi de este archivo es una formalización del proyecto, no de Laban.
"""

from math import acos, cos, pi, sin, sqrt


def covariance(points):
    n = len(points)
    if n < 3:
        raise ValueError("Se necesitan al menos tres puntos")
    center = [sum(p[i] for p in points) / n for i in range(3)]
    return [[sum((p[i] - center[i]) * (p[j] - center[j]) for p in points) / n
             for j in range(3)] for i in range(3)]


def symmetric_eigensystem(matrix):
    """Autovalores/vectores de una matriz simétrica 3x3 mediante Jacobi."""
    a = [row[:] for row in matrix]
    v = [[1.0 if i == j else 0.0 for j in range(3)] for i in range(3)]
    scale = max(1.0, max(abs(a[i][j]) for i in range(3) for j in range(3)))
    for _ in range(60):
        p, q = max(((0, 1), (0, 2), (1, 2)), key=lambda ij: abs(a[ij[0]][ij[1]]))
        if abs(a[p][q]) < 1e-14 * scale:
            break
        tau = (a[q][q] - a[p][p]) / (2 * a[p][q])
        t = (1 if tau >= 0 else -1) / (abs(tau) + sqrt(1 + tau * tau))
        c = 1 / sqrt(1 + t * t)
        s = t * c
        old_pp, old_qq, old_pq = a[p][p], a[q][q], a[p][q]
        a[p][p] = old_pp - t * old_pq
        a[q][q] = old_qq + t * old_pq
        a[p][q] = a[q][p] = 0.0
        for r in range(3):
            if r not in (p, q):
                arp, arq = a[r][p], a[r][q]
                a[r][p] = a[p][r] = c * arp - s * arq
                a[r][q] = a[q][r] = s * arp + c * arq
            vrp, vrq = v[r][p], v[r][q]
            v[r][p] = c * vrp - s * vrq
            v[r][q] = s * vrp + c * vrq
    else:
        raise RuntimeError("Jacobi no convergió")
    ordered = sorted(((a[i][i], tuple(v[r][i] for r in range(3))) for i in range(3)),
                     reverse=True, key=lambda pair: pair[0])
    return ordered


def fit_plane(points):
    eig = symmetric_eigensystem(covariance(points))
    values = tuple(max(0.0, pair[0]) for pair in eig)
    return {"eigenvalues": values,
            "normal": eig[-1][1],
            "rms_perpendicular": sqrt(values[-1]),
            "secondary_spread": sqrt(values[1])}


def normal_angle_degrees(a, b):
    # Un plano no distingue n de -n.
    dot = sum(x * y for x, y in zip(a, b))
    return acos(min(1.0, max(0.0, abs(dot)))) * 180 / pi


def main():
    n = 120
    circle_xy = [(cos(2*pi*i/n), sin(2*pi*i/n), 0.0) for i in range(n)]
    circle_xz = [(cos(2*pi*i/n), 0.0, sin(2*pi*i/n)) for i in range(n)]
    tilt = 37 * pi / 180
    circle_tilted = [(cos(tilt) * x + sin(tilt) * z + 2, y - 3,
                      -sin(tilt) * x + cos(tilt) * z + 0.5)
                     for x, y, z in circle_xy]
    line = [(i / 60 - 1, 0.0, 0.0) for i in range(n)]
    # Misma línea principal; dos perturbaciones pequeñas y ortogonales.
    line_y = [(x, 0.01 * sin(2*pi*i/n), 0.0) for i, (x, _, _) in enumerate(line)]
    line_z = [(x, 0.0, 0.01 * sin(2*pi*i/n)) for i, (x, _, _) in enumerate(line)]
    volume = [(cos(2*pi*i/n), sin(2*pi*i/n), 0.4 * sin(4*pi*i/n))
              for i in range(n)]
    xy, xz, tilted = map(fit_plane, (circle_xy, circle_xz, circle_tilted))
    straight, nearly_y, nearly_z = map(fit_plane, (line, line_y, line_z))
    three_d = fit_plane(volume)
    assert xy["rms_perpendicular"] < 1e-12
    assert xy["secondary_spread"] > 0.7
    assert normal_angle_degrees(xy["normal"], xz["normal"]) > 89.99
    assert abs(normal_angle_degrees(xy["normal"], tilted["normal"]) - 37) < 1e-9
    assert max(abs(x - y) for x, y in zip(xy["eigenvalues"], tilted["eigenvalues"])) < 1e-12
    assert straight["secondary_spread"] < 1e-12
    assert nearly_y["rms_perpendicular"] < 1e-12
    assert nearly_z["rms_perpendicular"] < 1e-12
    assert nearly_y["secondary_spread"] < 0.01
    assert nearly_z["secondary_spread"] < 0.01
    assert normal_angle_degrees(nearly_y["normal"], nearly_z["normal"]) > 89.99
    assert three_d["rms_perpendicular"] > 0.2
    print("círculo XY:", xy)
    print("círculo XZ:", xz)
    print("ángulo de planos XY/XZ:", normal_angle_degrees(xy["normal"], xz["normal"]))
    print("círculo trasladado/inclinado:", tilted,
          "ángulo frente a XY:", normal_angle_degrees(xy["normal"], tilted["normal"]))
    print("línea exacta:", straight)
    print("líneas casi rectas: dispersión secundaria:",
          nearly_y["secondary_spread"], nearly_z["secondary_spread"],
          "ángulo entre normales:",
          normal_angle_degrees(nearly_y["normal"], nearly_z["normal"]))
    print("trayectoria volumétrica:", three_d)


if __name__ == "__main__":
    main()
