#!/usr/bin/env python3
"""Contraste geométrico sintético: retícula de 45° vs cubo discreto.

Las etiquetas y la regla de vecino angular son operacionalizaciones de este
proyecto, no un transcriptor automático de kinetografía ni datos de Nico.
"""

from math import acos, asin, cos, degrees, pi, radians, sin, sqrt


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def angle(a, b):
    return degrees(acos(max(-1.0, min(1.0, dot(a, b)))))


def vector(azimuth_deg, elevation_deg):
    a, e = radians(azimuth_deg), radians(elevation_deg)
    return (cos(e) * cos(a), cos(e) * sin(a), sin(e))


def normalized(v):
    length = sqrt(dot(v, v))
    return tuple(x / length for x in v)


def templates():
    grid, cube = {}, {}
    for k in range(8):
        az = k * 45
        for level, elevation in (("low", -45), ("middle", 0), ("high", 45)):
            label = f"{k}:{level}"
            grid[label] = vector(az, elevation)
            cube[label] = normalized((round(cos(radians(az))),
                                      round(sin(radians(az))),
                                      -1 if elevation < 0 else 1 if elevation > 0 else 0))
    grid["pole_up"] = cube["pole_up"] = (0.0, 0.0, 1.0)
    grid["pole_down"] = cube["pole_down"] = (0.0, 0.0, -1.0)
    assert len(grid) == len(cube) == 26
    assert len({tuple(round(x, 12) for x in v) for v in grid.values()}) == 26
    assert all(abs(dot(v, v) - 1) < 1e-12 for v in grid.values())
    return grid, cube


def nearest(u, template):
    return sorted((angle(u, v), name) for name, v in template.items())[:2]


def voronoi_margin(u, template):
    """Distancia esférica exacta a salir de la celda del vecino elegido.

    Las fronteras de la regla de vecino angular son círculos máximos dados por
    u·(centro_elegido-centro_rival)=0. No son límites históricos de notación.
    """
    if abs(dot(u, u) - 1.0) > 1e-9:
        raise ValueError("u must be a unit direction")
    winner = nearest(u, template)[0][1]
    a = template[winner]
    boundaries = []
    for name, b in template.items():
        if name == winner:
            continue
        normal = normalized(tuple(x - y for x, y in zip(a, b)))
        signed = max(-1.0, min(1.0, dot(u, normal)))
        boundaries.append((degrees(asin(signed)), name, normal))
    margin_deg, rival, normal = min(boundaries)
    return winner, max(0.0, margin_deg), rival, normal


def main():
    grid, cube = templates()
    diagonal_label = "1:high"
    separation = angle(grid[diagonal_label], cube[diagonal_label])
    assert abs(degrees(asin(1 / sqrt(3))) - 35.264389682754654) < 1e-10
    assert abs(separation - 9.735610317245346) < 1e-10

    fixed = vector(41, -65)
    a, b = nearest(fixed, grid), nearest(fixed, cube)
    assert a[0][1] == "1:low" and b[0][1] == "pole_down"
    assert a[1][0] - a[0][0] > 4 and b[1][0] - b[0][0] > 4
    grid_margin = voronoi_margin(fixed, grid)[1]
    cube_margin = voronoi_margin(fixed, cube)[1]
    assert abs(grid_margin - 2.4454544720007245) < 1e-9
    assert abs(cube_margin - 2.4202336697013043) < 1e-9

    measured_az = 22
    front_plus_two = nearest(vector(measured_az - 2, 0), grid)
    front_minus_two = nearest(vector(measured_az + 2, 0), grid)
    assert front_plus_two[0][1] == "0:middle"
    assert front_minus_two[0][1] == "1:middle"

    u = vector(measured_az, 0)
    label, margin, rival, normal = voronoi_margin(u, grid)
    assert label == "0:middle" and rival == "1:middle"
    assert abs(margin - 0.5) < 1e-10
    # El segundo vecino está a 23°, el elegido a 22°: su diferencia (1°)
    # NO es la distancia angular real (0,5°) hasta cambiar de clase.
    assert abs((nearest(u, grid)[1][0] - nearest(u, grid)[0][0]) - 1) < 1e-10
    boundary = normalized(tuple(x - dot(u, normal) * n
                                for x, n in zip(u, normal)))
    assert abs(angle(u, boundary) - margin) < 1e-10
    inward = normalized(tuple(x + y for x, y in zip(u, boundary)))
    outward = normalized(tuple(x - 0.001 * n for x, n in zip(boundary, normal)))
    assert nearest(inward, grid)[0][1] == label
    assert nearest(outward, grid)[0][1] != label

    # Una cota angular hipotética de 0,4° sostiene la etiqueta bajo este
    # clasificador; 2° la deja ambigua. Aún falta incertidumbre del frente.
    assert 0.4 < margin < 2.0

    print(f"26 direcciones; diferencia diagonal alta grid/cubo: {separation:.6f}°")
    print(f"vector az=41°, el=-65°: grid={a[0][1]}, cubo={b[0][1]}")
    print(f"márgenes reales en ese vector: grid={grid_margin:.6f}°, cubo={cube_margin:.6f}°")
    print(f"mismo vector az=22°, frente ±2°: {front_plus_two[0][1]} / {front_minus_two[0][1]}")
    print(f"az=22°: margen Voronoi={margin:.6f}° hacia {rival}; gap de vecinos=1,000000°")


if __name__ == "__main__":
    main()
