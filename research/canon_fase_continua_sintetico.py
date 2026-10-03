#!/usr/bin/env python3
"""Continuous ideal curves: same global Q/phase, different lead sequence.

This repairs the artificial gaps in canon_fase_orden_sintetico.py. It still has
no rope, body mechanics, perception, physiology or historical Laban labels.
"""

import json
from cmath import exp
from math import atan2, cos, pi, sin, sqrt

from laban_hit_factorial_sintetico import arc_weighted_q


SIGNS = {"grouped": (1, 1, -1, -1),
         "alternating": (1, -1, 1, -1)}
SAMPLES_PER_CYCLE = 1000
SWING = 1.2


def bump(u):
    return sin(pi * u) ** 4


def phase(cycle, u, sign):
    return 2 * pi * (cycle + u) + sign * SWING * bump(u)


def angular_speed(u, sign):
    return 2 * pi + sign * SWING * 4 * pi * sin(pi * u) ** 3 * cos(pi * u)


def event_time(sign):
    """First crossing of phase pi in a cycle; unique because speed > 0."""
    low, high = 0.0, 1.0
    for _ in range(60):
        middle = (low + high) / 2
        if phase(0, middle, sign) < pi:
            low = middle
        else:
            high = middle
    return (low + high) / 2


def describe(signs):
    left, right, phase_differences, right_speeds = [], [], [], []
    for cycle, sign in enumerate(signs):
        for index in range(SAMPLES_PER_CYCLE):
            u = index / SAMPLES_PER_CYCLE
            left_phase = 2 * pi * (cycle + u)
            right_phase = phase(cycle, u, sign)
            left.append((cos(left_phase), sin(left_phase), 0.0))
            right.append((cos(right_phase), sin(right_phase), 0.0))
            phase_differences.append(right_phase - left_phase)
            right_speeds.append(angular_speed(u, sign))
    left.append((1.0, 0.0, 0.0))
    right.append((1.0, 0.0, 0.0))
    q_left, length_left = arc_weighted_q(left)
    q_right, length_right = arc_weighted_q(right)
    z = sum(exp(1j * value) for value in phase_differences) / len(phase_differences)
    lead = ["right" if event_time(sign) < .5 else "left" for sign in signs]
    return {"q_left": q_left, "q_right": q_right,
            "length_left": length_left, "length_right": length_right,
            "R": abs(z), "mean_angle": atan2(z.imag, z.real),
            "right_speeds": right_speeds,
            "lead_order": lead,
            "lead_transitions": sum(a != b for a, b in zip(lead, lead[1:])),
            "right_event_u_by_cycle": [event_time(sign) for sign in signs]}


def main():
    # max |4 pi sin^3(pi u) cos(pi u)| = 3 sqrt(3) pi / 4.
    assert 2 * pi - SWING * 3 * sqrt(3) * pi / 4 > 0
    assert bump(0) == 0 and abs(bump(1)) < 1e-50
    for sign in (-1, 1):
        assert abs(angular_speed(0, sign) - 2 * pi) < 1e-12
        assert abs(angular_speed(1, sign) - 2 * pi) < 1e-12
    outputs = {name: describe(signs) for name, signs in SIGNS.items()}
    a, b = outputs["grouped"], outputs["alternating"]
    for key in ("q_left", "q_right"):
        assert max(abs(x - y) for x, y in zip(a[key], b[key])) < 1e-12
    for key in ("length_left", "length_right", "R", "mean_angle"):
        assert abs(a[key] - b[key]) < 1e-12
    assert sorted(a["right_speeds"]) == sorted(b["right_speeds"])
    assert a["lead_order"] == ["right", "right", "left", "left"]
    assert b["lead_order"] == ["right", "left", "right", "left"]
    assert a["lead_transitions"] == 1 and b["lead_transitions"] == 3
    print(json.dumps({name: {
        "Q_left": [round(x, 9) for x in data["q_left"]],
        "Q_right": [round(x, 9) for x in data["q_right"]],
        "R_1to1": round(data["R"], 9),
        "mean_relative_angle_rad": round(data["mean_angle"], 9),
        "right_path_length": round(data["length_right"], 9),
        "lead_order": data["lead_order"],
        "lead_transitions": data["lead_transitions"],
        "right_event_u_by_cycle": [round(x, 9) for x in data["right_event_u_by_cycle"]],
    } for name, data in outputs.items()}, sort_keys=True))


if __name__ == "__main__":
    main()
