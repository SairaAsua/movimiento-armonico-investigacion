"""Control geométrico sintético de redes sobre círculos; sin datos humanos.

Ejecutar: python redes_circulos_nulos.py
Compara proximidad radial a vértices y muestra optimismo por ajustar giro a
cada trayectoria. Los círculos NO representan una escala de Laban ni rope flow.
"""

from math import acos, cos, degrees, pi, sin, sqrt
from random import Random
from statistics import mean, median

from redes_sanity import dot, vertices_cuboctahedron, vertices_icosahedron


def cross(a, b):
    return (a[1] * b[2] - a[2] * b[1],
            a[2] * b[0] - a[0] * b[2],
            a[0] * b[1] - a[1] * b[0])


def unit(v):
    size = sqrt(dot(v, v))
    return tuple(x / size for x in v)


def circle(normal, samples=24):
    anchor = (0.0, 0.0, 1.0) if abs(normal[2]) < 0.9 else (1.0, 0.0, 0.0)
    first = unit(cross(normal, anchor))
    second = cross(normal, first)
    return [tuple(cos(2 * pi * j / samples) * first[k]
                  + sin(2 * pi * j / samples) * second[k]
                  for k in range(3)) for j in range(samples)]


def rotate_z(v, angle):
    c, s = cos(angle), sin(angle)
    return (c * v[0] - s * v[1], s * v[0] + c * v[1], v[2])


def mean_nearest_angle(path, vertices, yaw):
    rotated = [rotate_z(v, yaw) for v in vertices]
    return mean(degrees(acos(max(-1.0, min(1.0, max(dot(p, v) for v in rotated)))))
                for p in path)


def summarize(name, vertices, paths, yaws):
    development = paths[0]
    chosen_yaw = min(yaws, key=lambda a: mean_nearest_angle(development, vertices, a))
    test = paths[1:]
    fixed = [mean_nearest_angle(p, vertices, chosen_yaw) for p in test]
    free = [min(mean_nearest_angle(p, vertices, a) for a in yaws) for p in test]
    assert all(a + 1e-10 >= b for a, b in zip(fixed, free))
    gap = [a - b for a, b in zip(fixed, free)]
    print(f"{name}: yaw_desarrollo={degrees(chosen_yaw):.0f}°, "
          f"error_fijo_test={mean(fixed):.2f}°, "
          f"error_giro_libre_test={mean(free):.2f}°, "
          f"optimismo_mediano={median(gap):.2f}°, "
          f"optimismo_max={max(gap):.2f}°")
    return fixed


if __name__ == "__main__":
    rng = Random(1701)
    normals = []
    for _ in range(201):
        z = rng.uniform(-1, 1)
        azimuth = rng.uniform(0, 2 * pi)
        radius = sqrt(1 - z * z)
        normals.append((radius * cos(azimuth), radius * sin(azimuth), z))
    paths = [circle(n) for n in normals]
    yaws = [j * pi / 36 for j in range(72)]
    assert all(abs(dot(p, p) - 1) < 1e-12 for path in paths for p in path)
    cube = summarize("cuboctaedro", vertices_cuboctahedron(), paths, yaws)
    ico = summarize("icosaedro", vertices_icosahedron(), paths, yaws)
    print(f"Círculos nulos test donde error fijo icosa < cubo: "
          f"{sum(i < c for i, c in zip(ico, cube))}/{len(cube)}; "
          f"empates={sum(abs(i-c)<1e-10 for i,c in zip(ico,cube))}")
