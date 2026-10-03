#!/usr/bin/env python3
"""Same individual circular paths and global phase, different bout order.

Independent ideal bouts with resets between them. No human, rope or Laban
category is simulated. The phase and event times are known by construction.
"""

import json
from cmath import exp
from math import atan2, cos, hypot, pi, sin


SAMPLES = 720
OFFSET = pi / 3
PATTERNS = {"grouped": (1, 1, -1, -1),
            "alternating": (1, -1, 1, -1)}


def q_xy(phase_offset):
    points = [(cos(2 * pi * i / SAMPLES + phase_offset),
               sin(2 * pi * i / SAMPLES + phase_offset))
              for i in range(SAMPLES + 1)]
    arc = q_x = q_y = 0.0
    for (x0, y0), (x1, y1) in zip(points, points[1:]):
        dx, dy = x1 - x0, y1 - y0
        ds = hypot(dx, dy)
        arc += ds
        q_x += dx * dx / ds
        q_y += dy * dy / ds
    return q_x / arc, q_y / arc, arc


def describe(pattern):
    phase_samples = []
    lead_order = []
    event_pairs = []
    right_q = []
    for sign in pattern:
        delta = sign * OFFSET
        left_event_t = 0.5
        right_event_t = 0.5 - delta / (2 * pi)
        assert 0 < right_event_t < 1
        lead_order.append("right" if right_event_t < left_event_t else "left")
        event_pairs.append((right_event_t, left_event_t))
        right_q.append(q_xy(delta))
        for i in range(SAMPLES):
            theta = 2 * pi * (i + .5) / SAMPLES
            phase_samples.append(exp(1j * ((theta + delta) - theta)))
    z = sum(phase_samples) / len(phase_samples)
    angle = atan2(z.imag, z.real)
    assert abs(abs(z) - .5) < 1e-12 and abs(angle) < 1e-12
    assert max(abs(a - b) for row in right_q for a, b in zip(row, right_q[0])) < 1e-12
    transitions = sum(a != b for a, b in zip(lead_order, lead_order[1:]))
    return {"R_1to1": round(abs(z), 12), "mean_relative_angle_rad": 0.0,
            "Q_xy_per_hand": [round(x, 12) for x in q_xy(0)[:2]],
            "arc_per_bout": round(q_xy(0)[2], 12),
            "lead_order": lead_order, "lead_transitions": transitions,
            "right_then_left_event_times_by_bout": [[round(x, 12), y] for x, y in event_pairs]}


def main():
    output = {name: describe(pattern) for name, pattern in PATTERNS.items()}
    a, b = output.values()
    for key in ("R_1to1", "mean_relative_angle_rad", "Q_xy_per_hand", "arc_per_bout"):
        assert a[key] == b[key]
    assert a["lead_transitions"] == 1 and b["lead_transitions"] == 3
    print(json.dumps(output, sort_keys=True))


if __name__ == "__main__":
    main()
