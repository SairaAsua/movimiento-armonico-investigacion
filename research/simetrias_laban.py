"""Chequeo geométrico sin datos humanos de reflejos en V(phi)."""

from itertools import combinations, product
from math import sqrt


PHI = (1 + sqrt(5)) / 2


def vertices():
    return [(0, a, b * PHI) for a, b in product((-1, 1), repeat=2)] + [
        (a, b * PHI, 0) for a, b in product((-1, 1), repeat=2)
    ] + [(a * PHI, 0, b) for a, b in product((-1, 1), repeat=2)]


def d2(a, b):
    return sum((x - y) ** 2 for x, y in zip(a, b))


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def sub(a, b):
    return tuple(x - y for x, y in zip(a, b))


def scale(s, a):
    return tuple(s * x for x in a)


def cross(a, b):
    return (a[1] * b[2] - a[2] * b[1],
            a[2] * b[0] - a[0] * b[2],
            a[0] * b[1] - a[1] * b[0])


def edge_frame(a, b):
    e1 = scale(1 / sqrt(dot(a, a)), a)
    residual = sub(b, scale(dot(e1, b), e1))
    e2 = scale(1 / sqrt(dot(residual, residual)), residual)
    return (e1, e2, cross(e1, e2))


def rotate_between_frames(point, source, target):
    return tuple(sum(dot(point, source[k]) * target[k][i] for k in range(3)) for i in range(3))


def canonical_cycle(path, anchor=1):
    path = list(path)
    i = path.index(anchor)
    forward = tuple(path[i:] + path[:i])
    path.reverse()
    i = path.index(anchor)
    backward = tuple(path[i:] + path[:i])
    return min(forward, backward)


def edge_set(points):
    return {
        (i, j)
        for i, j in combinations(range(len(points)), 2)
        if abs(d2(points[i], points[j]) - 4) < 1e-9
    }


def main():
    points = vertices()
    assert len(points) == 12
    edges = edge_set(points)
    assert len(edges) == 30
    for signs in product((-1, 1), repeat=3):
        transformed = [tuple(s * x for s, x in zip(signs, p)) for p in points]
        mapping = [next(i for i, q in enumerate(points) if d2(p, q) < 1e-12) for p in transformed]
        assert len(set(mapping)) == 12
        assert {(min(mapping[i], mapping[j]), max(mapping[i], mapping[j])) for i, j in edges} == edges
        assert sum(1 for i, j in edges if abs(d2(points[i], points[j]) - d2(transformed[i], transformed[j])) > 1e-9) == 0
    print("12 vértices, 30 aristas; ocho cambios de signo preservan la geometría")

    # Nombres de vértice de White 2020 (p. 4) y secuencia de sus figuras 5–6.
    p = PHI
    named = {
        1: (0, 1, p), 2: (0, -1, p),
        3: (p, 0, 1), 4: (-p, 0, 1),
        5: (1, p, 0), 6: (-1, p, 0),
        7: (1, -p, 0), 8: (-1, -p, 0),
        9: (0, 1, -p), 10: (0, -1, -p),
        11: (p, 0, -1), 12: (-p, 0, -1),
    }
    white_scale = (1, 3, 5, 9, 11, 7, 10, 12, 8, 2, 4, 6)
    assert set(white_scale) == set(named)
    assert all(abs(d2(named[white_scale[k]], named[white_scale[(k + 1) % 12]]) - 4) < 1e-9 for k in range(12))
    assert all(d2(named[white_scale[k]], named[white_scale[(k + 6) % 12]]) > 0 and
               all(abs(a + b) < 1e-9 for a, b in zip(named[white_scale[k]], named[white_scale[(k + 6) % 12]]))
               for k in range(12))

    neighbors = {
        i: {j for j in named if j != i and abs(d2(named[i], named[j]) - 4) < 1e-9}
        for i in named
    }
    opposites = {
        i: next(j for j in named if all(abs(a + b) < 1e-9 for a, b in zip(named[i], named[j])))
        for i in named
    }
    counts = [0, 0]
    anti_cycles = set()

    def walk(path, seen):
        tail = path[-1]
        if len(path) == 12:
            # Inicio fijo en 1; aceptar un solo sentido por ciclo.
            if 1 in neighbors[tail] and path[1] < tail:
                counts[0] += 1
                if all(path[(k + 6) % 12] == opposites[path[k]] for k in range(12)):
                    counts[1] += 1
                    anti_cycles.add(tuple(path))
            return
        for nxt in neighbors[tail] - seen:
            walk(path + (nxt,), seen | {nxt})

    walk((1,), {1})
    assert counts == [1280, 20], counts
    print("escala White: 12 pasos por aristas y antipodalidad a seis pasos; 1280 ciclos, 20 antipodales")

    # Una rotación queda determinada por la imagen de una arista orientada.
    # El icosaedro tiene 30 aristas, por tanto se verifican 60 mapas propios.
    source = edge_frame(named[1], named[3])
    rotations = set()
    labels = tuple(named)
    for i in labels:
        for j in neighbors[i]:
            target = edge_frame(named[i], named[j])
            mapped = []
            for k in labels:
                point = rotate_between_frames(named[k], source, target)
                hits = [h for h in labels if d2(point, named[h]) < 1e-9]
                assert len(hits) == 1
                mapped.append(hits[0])
            rotations.add(tuple(mapped))
    assert len(rotations) == 60
    orbit = set()
    for perm in rotations:
        mapping = dict(zip(labels, perm))
        orbit.add(canonical_cycle(tuple(mapping[k] for k in white_scale)))
    assert orbit == anti_cycles
    print("las 20 rutas antipodales son una sola órbita bajo las 60 rotaciones propias")

    # Q suma cuadrados de componentes de desplazamiento: pierde signos.
    mirrored = tuple(next(j for j in labels if d2((-named[i][0], named[i][1], named[i][2]), named[j]) < 1e-9)
                     for i in white_scale)
    assert canonical_cycle(mirrored) != canonical_cycle(white_scale)

    def q_stream(path):
        out = []
        for k in range(12):
            delta = sub(named[path[(k + 1) % 12]], named[path[k]])
            out.append(tuple(x * x / dot(delta, delta) for x in delta))
        return out

    original_q = q_stream(white_scale)
    mirrored_q = q_stream(mirrored)
    assert all(all(abs(a - b) < 1e-9 for a, b in zip(left, right))
               for left, right in zip(original_q, mirrored_q))
    # Fixture Q→g documentado para bandas 4/5/6 de Beacon: controles iguales
    # no pueden transportar la diferencia de lateralidad hacia el audio.
    def gains(q):
        return tuple(0.2 + 0.4 * value for value in q)

    original_controls = [gains(q) for q in original_q]
    mirrored_controls = [gains(q) for q in mirrored_q]
    assert all(abs(sum(g) - 1.0) < 1e-12 for g in original_controls)
    assert all(all(abs(x - y) < 1e-12 for x, y in zip(a, b))
               for a, b in zip(original_controls, mirrored_controls))
    signed_original = [sub(named[white_scale[(k + 1) % 12]], named[white_scale[k]])[0]
                       for k in range(12)]
    signed_mirror = [sub(named[mirrored[(k + 1) % 12]], named[mirrored[k]])[0]
                     for k in range(12)]
    assert all(abs(a + b) < 1e-12 for a, b in zip(signed_original, signed_mirror))
    assert any(abs(a - b) > 1e-9 for a, b in zip(signed_original, signed_mirror))
    mean_q = tuple(sum(row[k] for row in original_q) / 12 for k in range(3))
    assert all(abs(x - 1 / 3) < 1e-9 for x in mean_q)
    print("Q instantánea y móvil no distingue la ruta de su espejo lateral; Q del ciclo = (1/3,1/3,1/3)")
    print("fixture Beacon Q→g: 12 controles de tres bandas idénticos; "
          "componente lateral firmada distingue el espejo")


if __name__ == "__main__":
    main()
