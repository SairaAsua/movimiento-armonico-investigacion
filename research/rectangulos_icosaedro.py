"""Chequeo geométrico sintético; no contiene datos ni ecuaciones de Laban."""

from itertools import combinations, product
from math import dist, isclose, sqrt


def vertices(r):
    result = []
    for a, b in product((-1, 1), repeat=2):
        result.extend(((0, a, b * r), (a, b * r, 0), (a * r, 0, b)))
    assert len(result) == len(set(result)) == 12
    return result


def report(r):
    points = vertices(r)
    pairs = [(i, j, dist(points[i], points[j])) for i, j in combinations(range(12), 2)]
    edge = min(d for _, _, d in pairs)
    nearest = [(i, j) for i, j, d in pairs if isclose(d, edge, abs_tol=1e-10)]
    degrees = [sum(i == k or j == k for i, j in nearest) for k in range(12)]
    return edge, len(nearest), sorted(set(degrees))


if __name__ == "__main__":
    phi = (1 + sqrt(5)) / 2
    for label, r in (("cuadrado", 1), ("intermedio", 1.4), ("aureo", phi)):
        edge, count, degrees = report(r)
        print(f"{label}: r={r:.6f}, distancia mínima={edge:.6f}, pares mínimos={count}, grados={degrees}")
    assert report(1)[1:] == (24, [4])
    assert report(phi)[1:] == (30, [5])
