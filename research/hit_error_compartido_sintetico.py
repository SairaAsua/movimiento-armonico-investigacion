"""Exact artifact-proxy counterexample for an incremental Laban/HIT model."""

from fractions import Fraction
from itertools import product


def mean(values):
    return sum(values, Fraction(0)) / len(values)


rows = [(Fraction(l), Fraction(l + e), Fraction(e + n))
        for l, e, n in product((-1, 1), repeat=3)]
assert len(rows) == 8


def mse(predict):
    return mean([(y - predict(a, h)) ** 2 for y, a, h in rows])


e00 = mse(lambda a, h: Fraction(0))
e10 = mse(lambda a, h: a / 2)
e01 = mse(lambda a, h: Fraction(0))
e11 = mse(lambda a, h: (2 * a - h) / 3)
s = e10 + e01 - e00 - e11
cov_yh = mean([y * h for y, a, h in rows])
cov_ah = mean([a * h for y, a, h in rows])

assert (e00, e10, e01, e11, s) == (1, Fraction(1, 2), 1,
                                      Fraction(1, 3), Fraction(1, 6))
assert cov_yh == 0 and cov_ah == 1
assert mean([(y - a / 2) * a for y, a, h in rows]) == 0
assert mean([(y - (2 * a - h) / 3) * a for y, a, h in rows]) == 0
assert mean([(y - (2 * a - h) / 3) * h for y, a, h in rows]) == 0
print(f"Cov(Y,H)={cov_yh}, Cov(A,H)={cov_ah}")
print(f"E00={e00}, E10={e10}, E01={e01}, E11={e11}, S={s}")
