"""Contraejemplos exactos para Q, tensor direccional y subespacios.

Sólo usa tramos sintéticos adimensionales; no contiene datos humanos.
Ejecutar: python research/q_tensor_subespacios_sintetico.py
"""

import json
from math import isclose, sqrt


def tensor(tramos):
    """Segundo momento de direcciones, ponderado por longitud de arco."""
    total = sum(sqrt(sum(x * x for x in d)) for d in tramos)
    if total <= 0:
        raise ValueError("el recorrido debe tener longitud positiva")
    m = [[0.0 for _ in range(3)] for _ in range(3)]
    for d in tramos:
        length = sqrt(sum(x * x for x in d))
        if length == 0:
            continue
        for i in range(3):
            for j in range(3):
                m[i][j] += d[i] * d[j] / (length * total)
    return m


def q(m):
    return [m[i][i] for i in range(3)]


def same(a, b, tolerance=1e-12):
    return all(isclose(x, y, rel_tol=0, abs_tol=tolerance) for x, y in zip(a, b))


def same_matrix(a, b):
    return all(same(x, y) for x, y in zip(a, b))


def main():
    root2 = sqrt(2)
    diagonal_pos = (1 / root2, 1 / root2, 0)
    diagonal_neg = (1 / root2, -1 / root2, 0)
    lateral = (1, 0, 0)
    superior = (0, 1, 0)

    pos = tensor([diagonal_pos, diagonal_pos])
    neg = tensor([diagonal_neg, diagonal_neg])
    plano = tensor([lateral, superior])
    assert same(q(pos), [0.5, 0.5, 0])
    assert same(q(pos), q(neg)) and same(q(pos), q(plano))
    assert isclose(pos[0][1], 0.5, abs_tol=1e-12)
    assert isclose(neg[0][1], -0.5, abs_tol=1e-12)
    assert isclose(plano[0][1], 0, abs_tol=1e-12)
    # Determinante del bloque lateral-superior: 0 para cada línea, 1/4 para el plano.
    determinant = lambda m: m[0][0] * m[1][1] - m[0][1] ** 2
    assert isclose(determinant(pos), 0, abs_tol=1e-12)
    assert isclose(determinant(neg), 0, abs_tol=1e-12)
    assert isclose(determinant(plano), 0.25, abs_tol=1e-12)

    grouped = tensor([lateral, lateral, superior, superior])
    alternating = tensor([lateral, superior, lateral, superior])
    reversed_path = tensor([tuple(-x for x in diagonal_pos), diagonal_pos])
    assert same_matrix(grouped, alternating)
    assert same_matrix(pos, reversed_path)
    # Un cambio fijo de ejes de 45 grados convierte diagonal_pos en lateral.
    rotated = (
        (diagonal_pos[0] + diagonal_pos[1]) / root2,
        (-diagonal_pos[0] + diagonal_pos[1]) / root2,
        diagonal_pos[2],
    )
    assert same(q(tensor([rotated, rotated])), [1, 0, 0])

    print(json.dumps({
        "Q_comun_LUA": q(pos),
        "M_linea_positiva": pos,
        "M_linea_negativa": neg,
        "M_plano": plano,
        "det_bloque_LU": {
            "linea_positiva": determinant(pos),
            "linea_negativa": determinant(neg),
            "plano": determinant(plano),
        },
        "mismo_M_distinto_orden": same_matrix(grouped, alternating),
        "mismo_M_sentido_invertido": same_matrix(pos, reversed_path),
        "Q_tras_rotar_ejes_45_grados": q(tensor([rotated, rotated])),
        "tipo": "sintetico_sin_datos_humanos",
    }, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
