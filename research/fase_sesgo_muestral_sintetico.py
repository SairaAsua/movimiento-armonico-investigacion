"""Chequeo sin datos humanos del sesgo de concentración circular por duplicación."""

import cmath
import math
import random


def r2_ppc(phases):
    n = len(phases)
    assert n >= 2
    resultant = sum(cmath.exp(1j * angle) for angle in phases)
    r2 = abs(resultant / n) ** 2
    ppc = (n * r2 - 1) / (n - 1)
    direct = sum(
        math.cos(phases[j] - phases[k])
        for j in range(n)
        for k in range(j + 1, n)
    ) * 2 / (n * (n - 1))
    assert math.isclose(ppc, direct, abs_tol=1e-12)
    return r2, ppc


def main():
    rng = random.Random(17)
    k, repeats, trials = 3, 4, 20_000
    ppc_independent = 0.0
    ppc_repeated = 0.0
    r2_repeated = 0.0
    for _ in range(trials):
        independent = [rng.random() * 2 * math.pi for _ in range(k)]
        copied = [phase for phase in independent for _ in range(repeats)]
        _, ppc_k = r2_ppc(independent)
        r2_n, ppc_n = r2_ppc(copied)
        ppc_independent += ppc_k
        ppc_repeated += ppc_n
        r2_repeated += r2_n
    ppc_independent /= trials
    ppc_repeated /= trials
    r2_repeated /= trials
    expected_repeated = (repeats - 1) / (k * repeats - 1)
    assert abs(ppc_independent) < 0.02
    assert abs(ppc_repeated - expected_repeated) < 0.02
    assert abs(r2_repeated - 1 / k) < 0.02
    print(f"PPC independiente: {ppc_independent:.5f} (esperado 0)")
    print(f"R² con copias: {r2_repeated:.5f} (esperado {1 / k:.5f})")
    print(f"PPC con copias: {ppc_repeated:.5f} (esperado {expected_repeated:.5f})")


if __name__ == "__main__":
    main()
