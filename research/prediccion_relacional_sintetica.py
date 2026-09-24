"""Prueba de representación relacional y corte temporal; datos sintéticos.

Ejecutar: python prediccion_relacional_sintetica.py
Sin librerías externas, datos humanos ni pretensión de validar HIT.
"""

from math import sqrt
from random import Random


def solve(matrix, values):
    n = len(values)
    augmented = [list(row) + [value] for row, value in zip(matrix, values)]
    for col in range(n):
        pivot = max(range(col, n), key=lambda row: abs(augmented[row][col]))
        augmented[col], augmented[pivot] = augmented[pivot], augmented[col]
        assert abs(augmented[col][col]) > 1e-10
        augmented[col], augmented[pivot] = augmented[pivot], augmented[col]
        scale = augmented[col][col]
        augmented[col] = [v / scale for v in augmented[col]]
        for row in range(n):
            if row == col:
                continue
            multiplier = augmented[row][col]
            augmented[row] = [a - multiplier * b for a, b in zip(augmented[row], augmented[col])]
    return [row[-1] for row in augmented]


def fit(rows, features):
    design = [features(row) for row in rows]
    n = len(design[0])
    gram = [[sum(x[i] * x[j] for x in design) for j in range(n)] for i in range(n)]
    rhs = [sum(x[i] * row["y_next"] for x, row in zip(design, rows)) for i in range(n)]
    return solve(gram, rhs)


def rmse(rows, features, coefficients):
    return sqrt(sum((row["y_next"] - sum(a * b for a, b in zip(features(row), coefficients))) ** 2
                    for row in rows) / len(rows))


def make_sessions(relational_signal):
    rng = Random(42 if relational_signal else 43)
    sessions = []
    for session_id in range(10):
        rows = []
        for k in range(200):
            left = rng.gauss(0, 1)
            right = rng.gauss(0, 1)
            relation = left * right  # Ejemplo algebraico de descriptor derivado.
            noise = rng.gauss(0, 0.3)
            next_value = (1.5 * relation if relational_signal else 0.0) + noise
            rows.append({"session_id": session_id, "origin_cycle": k,
                         "feature_latest_cycle": k, "target_cycle": k + 1,
                         "feature_available_cycle": k,
                         "left": left, "right": right, "relation": relation,
                         "y_next": next_value})
        sessions.append(rows)
    return sessions


def basic(row):
    return (1.0, row["left"], row["right"])


def with_relation(row):
    return basic(row) + (row["relation"],)


def matched_nonlinear(row):
    left, right = row["left"], row["right"]
    # Un comparador que recibe las señales individuales y sus interacciones.
    return basic(row) + (left * left, right * right, left * right)


def row_key(row):
    return row["session_id"], row["origin_cycle"]


def require_causal_rows(rows):
    """El rasgo debe existir al cerrar el ciclo origen, antes del objetivo."""
    for row in rows:
        if not (row["feature_latest_cycle"] <= row["origin_cycle"]
                and row["feature_available_cycle"] <= row["origin_cycle"]
                and row["origin_cycle"] < row["target_cycle"]):
            raise ValueError(f"future feature at {row_key(row)}")


def require_same_support(base_rows, extended_rows):
    """Dos pérdidas sólo son comparables sobre unidades y objetivos idénticos."""
    a, b = [row_key(row) for row in base_rows], [row_key(row) for row in extended_rows]
    if len(a) != len(set(a)) or len(b) != len(set(b)) or set(a) != set(b):
        raise ValueError("model evaluations have different or duplicate row keys")
    base_targets = {row_key(row): (row["target_cycle"], row["y_next"])
                    for row in base_rows}
    extended_targets = {row_key(row): (row["target_cycle"], row["y_next"])
                        for row in extended_rows}
    if base_targets != extended_targets:
        raise ValueError("model evaluations have different targets for the same rows")


def demonstrate_support_bias():
    """Mundo nulo: el aparente beneficio es selección de episodios fáciles."""
    rng = Random(88)
    train, test = [], []
    for session_id in range(10):
        for k in range(100):
            left, right = rng.gauss(0, 1), rng.gauss(0, 1)
            easy = k % 2 == 0
            row = {"session_id": session_id, "origin_cycle": k,
                   "feature_latest_cycle": k, "feature_available_cycle": k,
                   "target_cycle": k + 1, "left": left, "right": right,
                   "relation": left * right,
                   "y_next": rng.gauss(0, 0.2 if easy else 2.0), "easy": easy}
            (train if session_id < 6 else test).append(row)
    require_causal_rows(train + test)
    base_fit = fit(train, basic)
    relation_fit = fit(train, with_relation)
    easy_test = [row for row in test if row["easy"]]
    full_base = rmse(test, basic, base_fit)
    selected_relation = rmse(easy_test, with_relation, relation_fit)
    matched_base = rmse(easy_test, basic, base_fit)
    try:
        require_same_support(test, easy_test)
    except ValueError:
        pass
    else:
        raise AssertionError("different support must be rejected")
    require_same_support(easy_test, list(reversed(easy_test)))
    altered_target = [dict(row) for row in easy_test]
    altered_target[0]["target_cycle"] += 1
    try:
        require_same_support(easy_test, altered_target)
    except ValueError:
        pass
    else:
        raise AssertionError("changed target must be rejected")
    assert full_base > 3 * selected_relation
    assert abs(matched_base - selected_relation) < 0.03
    print(f"soporte desigual (comparación inválida): base todos={full_base:.4f}, "
          f"+relación fáciles={selected_relation:.4f}")
    print(f"soporte idéntico (mundo nulo): base fáciles={matched_base:.4f}, "
          f"+relación fáciles={selected_relation:.4f}")

    leaked = dict(test[0], feature_available_cycle=test[0]["target_cycle"])
    try:
        require_causal_rows([leaked])
    except ValueError:
        print("rasgo futuro: rechazado por corte temporal")
    else:
        raise AssertionError("future feature must be rejected")


def report(relational_signal):
    sessions = make_sessions(relational_signal)
    train = [row for session in sessions[:6] for row in session]
    test = [row for session in sessions[6:] for row in session]
    require_causal_rows(train + test)
    require_same_support(test, list(reversed(test)))
    assert all(row["feature_latest_cycle"] == row["origin_cycle"]
               and row["target_cycle"] == row["origin_cycle"] + 1
               for row in train + test)
    print("mundo", "relación en resultado futuro" if relational_signal else "relación sin valor futuro")
    for name, features in (("lineal individual", basic),
                           ("lineal + relación", with_relation),
                           ("individual no lineal", matched_nonlinear)):
        coefficients = fit(train, features)
        print(f"  {name}: RMSE en cuatro sesiones reservadas = {rmse(test, features, coefficients):.4f}")


if __name__ == "__main__":
    report(False)
    report(True)
    demonstrate_support_bias()
