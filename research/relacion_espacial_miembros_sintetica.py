#!/usr/bin/env python3
"""Counterexample: individual Q and phase do not determine 3D hand separation.

Ideal curves only. No rope, human motion, perception or physiology is modeled.
"""

from math import atan2, cos, pi, sin, sqrt

from laban_hit_factorial_sintetico import arc_weighted_q


SAMPLES = 2000
SEPARATION = 1.0
HEIGHT = 0.5


def sample(condition: str):
    left, right, phases = [], [], []
    for i in range(SAMPLES + 1):
        phase = 2 * pi * i / SAMPLES
        x, y, z = cos(phase), sin(phase), HEIGHT * sin(2 * phase)
        left.append((x - SEPARATION / 2, y, z))
        right.append((x + SEPARATION / 2, y, z if condition == "parallel" else -z))
        phases.append(phase)
    return left, right, phases


def speeds(points):
    dt = 1 / SAMPLES
    return [sqrt(sum((b[k] - a[k]) ** 2 for k in range(3))) / dt
            for a, b in zip(points, points[1:])]


def separations(left, right):
    return [sqrt(sum((r[k] - l[k]) ** 2 for k in range(3)))
            for l, r in zip(left, right)]


def phase_relation(left, right):
    """Known x-y orbit centres; exclude duplicated final sample."""
    re = im = 0.0
    for l, r in zip(left[:-1], right[:-1]):
        phi_l = atan2(l[1], l[0] + SEPARATION / 2)
        phi_r = atan2(r[1], r[0] - SEPARATION / 2)
        dphi = phi_r - phi_l
        re += cos(dphi)
        im += sin(dphi)
    return sqrt(re * re + im * im) / SAMPLES, atan2(im, re)


def main():
    l0, r0, phase0 = sample("parallel")
    l1, r1, phase1 = sample("opposed_vertical")
    assert l0 == l1 and phase0 == phase1
    # A view perpendicular to the vertical axis observes identical projected paths.
    assert [(x, y) for x, y, _ in r0] == [(x, y) for x, y, _ in r1]
    q_l0, len_l0 = arc_weighted_q(l0)
    q_l1, len_l1 = arc_weighted_q(l1)
    q_r0, len_r0 = arc_weighted_q(r0)
    q_r1, len_r1 = arc_weighted_q(r1)
    for a, b in ((q_l0, q_l1), (q_r0, q_r1)):
        assert max(abs(x - y) for x, y in zip(a, b)) < 1e-12
    assert abs(len_l0 - len_l1) < 1e-12
    assert abs(len_r0 - len_r1) < 1e-12
    assert max(abs(a - b) for a, b in zip(speeds(r0), speeds(r1))) < 1e-12
    # Phase from each hand’s x-y orbit about its known centre is identical.
    for left, right in ((l0, r0), (l1, r1)):
        r, mean_angle = phase_relation(left, right)
        assert abs(r - 1) < 1e-12 and abs(mean_angle) < 1e-12
    d0, d1 = separations(l0, r0), separations(l1, r1)
    assert max(abs(x - SEPARATION) for x in d0) < 1e-12
    assert abs(min(d1) - SEPARATION) < 1e-12
    assert abs(max(d1) - sqrt(SEPARATION**2 + (2 * HEIGHT) ** 2)) < 1e-12
    print("Q_left=", tuple(round(x, 6) for x in q_l0))
    print("Q_right=", tuple(round(x, 6) for x in q_r0))
    print("R_1:1=1, mean_relative_phase=0 in both constructions")
    print(f"separation parallel={min(d0):.6f}..{max(d0):.6f}; "
          f"opposed_vertical={min(d1):.6f}..{max(d1):.6f}")
    print("same individual Q/speed/phase and x-y projection; different 3D relation=ok")


if __name__ == "__main__":
    main()
