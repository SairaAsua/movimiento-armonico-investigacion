"""Sanity check geométrico; no analiza movimiento humano ni valida a Laban.

Ejecutar: python redes_sanity.py
Biblioteca estándar solamente. Las 50 000 direcciones de Fibonacci constituyen
una cuadratura determinista aproximada de la esfera, no una muestra humana.
"""

from itertools import product
from math import acos, cos, degrees, pi, sin, sqrt

from direcciones_26_sintetico import templates as direction_templates_26


PHI = (1 + sqrt(5)) / 2


def unit(v):
    length = sqrt(sum(a * a for a in v))
    return tuple(a / length for a in v)


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def vertices_cuboctahedron():
    vertices = []
    for zero_axis in range(3):
        others = [i for i in range(3) if i != zero_axis]
        for a, b in product((-1, 1), repeat=2):
            v = [0, 0, 0]
            v[others[0]], v[others[1]] = a, b
            vertices.append(unit(v))
    return vertices


def vertices_icosahedron():
    vertices = []
    for zero_axis in range(3):
        for a, b in product((-1, 1), repeat=2):
            v = [0, 0, 0]
            v[(zero_axis + 1) % 3] = a
            v[(zero_axis + 2) % 3] = b * PHI
            vertices.append(unit(v))
    return vertices


def solids_26_candidate():
    """Realización euclidiana propia de 6 octa + 8 cubo + 12 icosa.

    Fügedi (1993, §§4-5 indexados) atribuye ese andamiaje a Choreutics y lo
    distingue de la notación posterior de miembros. Estos vectores exactos
    y su orientación compartida son elecciones del proyecto.
    """
    octa = [unit(v) for v in ((1, 0, 0), (-1, 0, 0), (0, 1, 0),
                              (0, -1, 0), (0, 0, 1), (0, 0, -1))]
    cube = [unit(v) for v in product((-1, 1), repeat=3)]
    ico = vertices_icosahedron()
    centers = {f"octa:{i}": v for i, v in enumerate(octa)}
    centers.update({f"cube:{i}": v for i, v in enumerate(cube)})
    centers.update({f"ico:{i}": v for i, v in enumerate(ico)})
    assert len(centers) == 26
    assert all(dot(v, w) < 1 - 1e-12 for i, v in enumerate(centers.values())
               for j, w in enumerate(centers.values()) if i != j)
    return centers


def edges(vertices):
    adjacent_dot = max(dot(vertices[0], other) for other in vertices[1:])
    links = [
        (i, j)
        for i in range(len(vertices))
        for j in range(i + 1, len(vertices))
        if abs(dot(vertices[i], vertices[j]) - adjacent_dot) < 1e-10
    ]
    return links, adjacent_dot


def sphere_directions(n):
    golden_angle = pi * (3 - sqrt(5))
    for j in range(n):
        y = 1 - 2 * (j + 0.5) / n
        radius = sqrt(1 - y * y)
        angle = golden_angle * j
        yield (radius * cos(angle), y, radius * sin(angle))


def summarize(name, vertices, expected_edges, expected_degree, expected_angle):
    assert len(vertices) == 12
    assert len(set(vertices)) == 12
    assert all(abs(dot(v, v) - 1) < 1e-12 for v in vertices)
    assert all(any(all(abs(a + b) < 1e-12 for a, b in zip(v, w)) for w in vertices) for v in vertices)
    links, adjacent_dot = edges(vertices)
    assert len(links) == expected_edges
    degrees_per_vertex = [sum(i in pair for pair in links) for i in range(12)]
    assert all(d == expected_degree for d in degrees_per_vertex)
    angle = degrees(acos(adjacent_dot))
    assert abs(angle - expected_angle) < 1e-9

    angles = []
    for u in sphere_directions(50_000):
        nearest_dot = max(dot(u, v) for v in vertices)
        angles.append(degrees(acos(max(-1, min(1, nearest_dot)))))
    angles.sort()
    mean = sum(angles) / len(angles)
    p95 = angles[int(0.95 * len(angles))]
    # Condicionado a que dos vértices consecutivos sean diferentes y equiprobables.
    random_transition_probability = 2 * len(links) / (12 * 11)
    print(
        f"{name}: vertices={len(vertices)}, edges={len(links)}, "
        f"degree={expected_degree}, adjacent_angle={angle:.6f}°, "
        f"uniform_mean_nearest={mean:.6f}°, uniform_p95_nearest={p95:.6f}°, "
        f"random_adjacent_transition={random_transition_probability:.6f}"
    )


def summarize_26_direction_coverage():
    """Línea base de vecino angular; no compara escalas históricas equivalentes."""
    grid, _ = direction_templates_26()
    centers = list(grid.items())
    angles = []
    counts = {name: 0 for name in grid}
    for u in sphere_directions(50_000):
        name, center = max(centers, key=lambda pair: dot(u, pair[1]))
        counts[name] += 1
        angles.append(degrees(acos(max(-1.0, min(1.0, dot(u, center))))))
    angles.sort()
    n = len(angles)
    mean = sum(angles) / n
    p95 = angles[int(0.95 * n)]
    fractions = {
        level: sum(count for name, count in counts.items()
                   if name.endswith(level)) / n
        for level in ("low", "middle", "high")
    }
    poles = (counts["pole_up"] + counts["pole_down"]) / n
    assert abs(sum(fractions.values()) + poles - 1.0) < 1e-12
    print(f"fugedi2016_grid26: centers=26, uniform_mean_nearest={mean:.6f}°, "
          f"uniform_p95_nearest={p95:.6f}°, "
          f"low/middle/high/poles={fractions['low']:.4f}/"
          f"{fractions['middle']:.4f}/{fractions['high']:.4f}/{poles:.4f}, "
          f"min/max_class_share={min(counts.values())/n:.5f}/"
          f"{max(counts.values())/n:.5f}")


def compare_two_26_geometries():
    """Mismo número de centros no implica el mismo catálogo métrico."""
    grid, _ = direction_templates_26()
    solids = solids_26_candidate()
    shared = sum(any(dot(a, b) > 1 - 1e-12 for b in solids.values())
                 for a in grid.values())
    assert shared == 6  # cuatro rumbos horizontales cardinales y dos polos
    # El centro cúbico (+,+,+) no cae en la elevación alta de 45°.
    cube_high = unit((1, 1, 1))
    grid_high = grid["1:high"]
    separation = degrees(acos(max(-1, min(1, dot(cube_high, grid_high)))))
    assert abs(separation - 9.735610317245346) < 1e-9

    results = {}
    for name, centers in (("fugedi2016_grid26", grid),
                          ("octa_cube_ico26_candidate", solids)):
        angles = []
        for u in sphere_directions(50_000):
            best = max(dot(u, v) for v in centers.values())
            angles.append(degrees(acos(max(-1, min(1, best)))))
        angles.sort()
        results[name] = (sum(angles) / len(angles), angles[int(.95 * len(angles))])
    print(f"grid26_vs_solids26: shared_exact_centers={shared}/26, "
          f"cube_diagonal_vs_grid_high={separation:.6f}°, "
          f"grid_uniform_mean/p95={results['fugedi2016_grid26'][0]:.6f}/"
          f"{results['fugedi2016_grid26'][1]:.6f}°, "
          f"solids_uniform_mean/p95={results['octa_cube_ico26_candidate'][0]:.6f}/"
          f"{results['octa_cube_ico26_candidate'][1]:.6f}°")


if __name__ == "__main__":
    summarize("cuboctahedron", vertices_cuboctahedron(), 24, 4, 60)
    summarize("icosahedron", vertices_icosahedron(), 30, 5, degrees(acos(1 / sqrt(5))))
    summarize_26_direction_coverage()
    compare_two_26_geometries()
