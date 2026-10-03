"""Pérdidas factoriales exactas con un resultado puramente aditivo.

Ejecutar: python3 research/factorial_sin_interaccion_sintetico.py
Mundo algebraico construido: no simula rope flow, HIT ni personas.
"""

from fractions import Fraction


def losses(rho: Fraction) -> tuple[Fraction, Fraction, Fraction, Fraction, Fraction]:
    assert -1 < rho < 1
    rows = [
        (left, phase, (1 + rho * left * phase) / 4, left + phase)
        for left in (-1, 1)
        for phase in (-1, 1)
    ]
    assert sum(weight for _, _, weight, _ in rows) == 1

    def mse(predict):
        return sum(weight * (outcome - predict(left, phase)) ** 2
                   for left, phase, weight, outcome in rows)

    # E[Y | L] = (1 + rho)L; E[Y | H] = (1 + rho)H.
    e00 = mse(lambda left, phase: 0)
    e10 = mse(lambda left, phase: (1 + rho) * left)
    e01 = mse(lambda left, phase: (1 + rho) * phase)
    e11 = mse(lambda left, phase: left + phase)
    s = e10 + e01 - e00 - e11

    # El coeficiente poblacional adicional de L*H es cero en este mundo.
    interaction_numerator = sum(weight * outcome * left * phase
                                for left, phase, weight, outcome in rows)
    assert interaction_numerator == 0
    assert e00 == 2 + 2 * rho
    assert e10 == e01 == 1 - rho ** 2
    assert e11 == 0
    assert s == -2 * rho * (1 + rho)
    return e00, e10, e01, e11, s


if __name__ == "__main__":
    expected = {
        Fraction(-1, 2): (Fraction(1), Fraction(3, 4), Fraction(3, 4), Fraction(0), Fraction(1, 2)),
        Fraction(0): (Fraction(2), Fraction(1), Fraction(1), Fraction(0), Fraction(0)),
        Fraction(1, 2): (Fraction(3), Fraction(3, 4), Fraction(3, 4), Fraction(0), Fraction(-3, 2)),
    }
    for rho, values in expected.items():
        actual = losses(rho)
        assert actual == values
        print(f"rho={rho}: E00={actual[0]}, E10={actual[1]}, "
              f"E01={actual[2]}, E11={actual[3]}, S={actual[4]}")
