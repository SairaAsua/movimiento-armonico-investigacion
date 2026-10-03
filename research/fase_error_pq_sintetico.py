"""Propagate bounded individual phase errors to a p:q resultant (synthetic only)."""

import cmath
import json
import math


N = 4096
EPS = math.radians(5)


def resultant(phases):
    return sum((cmath.exp(1j * phase) for phase in phases), 0j) / len(phases)


def evaluate(p, q):
    theta = [2 * math.pi * n / N for n in range(N)]
    # q*phi_i - p*phi_j = 0 before measurement error.
    phi_i = [p * t for t in theta]
    phi_j = [q * t for t in theta]
    ei = [EPS * math.sin(3 * t) for t in theta]
    ej = [EPS * math.cos(5 * t) for t in theta]
    true_delta = [q * a - p * b for a, b in zip(phi_i, phi_j)]
    observed_delta = [d + q * a - p * b for d, a, b in zip(true_delta, ei, ej)]
    z_true = resultant(true_delta)
    z_observed = resultant(observed_delta)
    bound = 2 * math.sin(min(math.pi, (p + q) * EPS) / 2)
    assert abs(z_true - z_observed) <= bound + 1e-12
    assert abs(abs(z_true) - abs(z_observed)) <= bound + 1e-12
    return {
        "p": p,
        "q": q,
        "R_true": abs(z_true),
        "R_observed": abs(z_observed),
        "resultant_error": abs(z_true - z_observed),
        "bound": bound,
    }


cases = [evaluate(1, 1), evaluate(2, 1)]
theta = [2 * math.pi * n / N for n in range(N)]
shared = [EPS * math.sin(3 * t) for t in theta]
assert max(abs((1 - 1) * e) for e in shared) == 0
assert max(abs((1 - 2) * e) for e in shared) > 0
print(json.dumps({"samples": N, "per_signal_error_deg": 5, "cases": cases,
                  "shared_error_coefficients": {"1:1": 0, "2:1": -1}}, indent=2))
