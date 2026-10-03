#!/usr/bin/env python3
"""Contraejemplo exacto: el giro del marco cambia una relación angular 2:1."""

from __future__ import annotations

import cmath
import json
from math import pi, sin


def concentration(values: list[float]) -> tuple[float, float]:
    z = sum((cmath.exp(1j * value) for value in values), 0j) / len(values)
    return abs(z), cmath.phase(z)


def main() -> None:
    cycles, samples_per_cycle, amplitude = 10, 2000, 0.8
    time = [index / samples_per_cycle for index in range(cycles * samples_per_cycle)]
    turn = [2 * pi * t for t in time]
    body_turn = [amplitude * sin(value) for value in turn]

    # En ambos casos las fases angulares permanecen monótonas también en cuerpo:
    # las derivadas mínimas son 0.2ω (señal lenta) y 0.4ω (rápida, caso B).
    def pair(world_fast: list[float], world_slow: list[float]) -> dict:
        world_delta = [fast - 2 * slow for fast, slow in zip(world_fast, world_slow)]
        body_delta = [(fast - theta) - 2 * (slow - theta)
                      for fast, slow, theta in zip(world_fast, world_slow, body_turn)]
        assert all(abs(body - (world + theta)) < 1e-11
                   for body, world, theta in zip(body_delta, world_delta, body_turn))
        world_r, world_mu = concentration(world_delta)
        body_r, body_mu = concentration(body_delta)
        return {"R_world": world_r, "mu_world_rad": world_mu,
                "R_body": body_r, "mu_body_rad": body_mu}

    lock_in_world = pair([2 * value for value in turn], turn)
    lock_in_body = pair([2 * value - theta for value, theta in zip(turn, body_turn)], turn)
    assert abs(lock_in_world["R_world"] - 1) < 1e-12
    assert 0.84 < lock_in_world["R_body"] < 0.85
    assert 0.84 < lock_in_body["R_world"] < 0.85
    assert abs(lock_in_body["R_body"] - 1) < 1e-12

    # En 1:1 el mismo giro se resta de ambas fases y se cancela exactamente.
    fast_equal = [value + 0.35 * sin(value) for value in turn]
    delta_world_1 = [fast - slow for fast, slow in zip(fast_equal, turn)]
    delta_body_1 = [(fast - theta) - (slow - theta)
                    for fast, slow, theta in zip(fast_equal, turn, body_turn)]
    assert all(abs(a - b) < 1e-11 for a, b in zip(delta_world_1, delta_body_1))
    r_1_world, mu_1_world = concentration(delta_world_1)
    r_1_body, mu_1_body = concentration(delta_body_1)
    assert abs(r_1_world - r_1_body) < 1e-12
    assert abs(mu_1_world - mu_1_body) < 1e-12

    print(json.dumps({
        "fixture": "planar angular phases; 10 cycles; body yaw=0.8 sin(2πt) rad",
        "relation": "2:1; delta=phi_fast-2phi_slow",
        "lock_in_world": lock_in_world,
        "lock_in_body": lock_in_body,
        "one_to_one_control": {"R_world": r_1_world, "R_body": r_1_body,
                               "mu_world_rad": mu_1_world, "mu_body_rad": mu_1_body},
        "scope": "constructed angular phases, not event phase, body motion or causal coupling",
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
