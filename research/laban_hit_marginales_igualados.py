#!/usr/bin/env python3
"""Synthetic matched-marginal timing control for a spatial/relational contrast.

No human data, rope physics, perceptual result, or causal coupling is modeled.
"""

from math import cos, pi, sin, sqrt

from laban_hit_factorial_sintetico import arc_weighted_q

CYCLES = 8
SAMPLES_PER_CYCLE = 1000
SWING = 1.8  # radians; phase derivative remains positive since SWING < 2


def phase_and_speed(cycle: int, u: float, swing: float) -> tuple[float, float]:
    """C1 cycle join: phase and angular speed agree at u=0 and u=1."""
    phase = 2 * pi * (cycle + u) + swing * sin(pi * u) ** 2
    speed = 2 * pi + swing * pi * sin(2 * pi * u)
    return phase, speed


def samples(plane: str, opposed: bool):
    left, right, speeds_left, speeds_right, differences = [], [], [], [], []
    for cycle in range(CYCLES):
        left_swing = SWING if cycle % 2 == 0 else -SWING
        right_swing = -left_swing if opposed else left_swing
        for frame in range(SAMPLES_PER_CYCLE):
            u = frame / SAMPLES_PER_CYCLE
            l_phase, l_speed = phase_and_speed(cycle, u, left_swing)
            r_phase, r_speed = phase_and_speed(cycle, u, right_swing)
            left.append((cos(l_phase), sin(l_phase), 0.0))
            right.append((cos(r_phase), sin(r_phase), 0.0) if plane == "lateral_anterior"
                         else (cos(r_phase), 0.0, sin(r_phase)))
            speeds_left.append(l_speed)
            speeds_right.append(r_speed)
            differences.append(r_phase - l_phase)
    # A full revolution closes at exactly the same position in both conditions.
    left.append((1.0, 0.0, 0.0))
    right.append((1.0, 0.0, 0.0))
    return left, right, speeds_left, speeds_right, differences


def concentration(differences):
    n = len(differences)
    return sqrt(sum(cos(d) for d in differences) ** 2
                + sum(sin(d) for d in differences) ** 2) / n


def event_only_concentration() -> float:
    """Both hands have the same completed-cycle events at t=0,1,...,8.

    Offline linear interpolation from those endpoints assigns identical task
    phases at every in-cycle sample, regardless of actual angular progress.
    """
    event_times = tuple(range(CYCLES + 1))
    differences = []
    for cycle in range(CYCLES):
        for frame in range(SAMPLES_PER_CYCLE):
            t = cycle + frame / SAMPLES_PER_CYCLE
            left_event_phase = 2 * pi * (t - event_times[cycle]) / (
                event_times[cycle + 1] - event_times[cycle]
            )
            right_event_phase = left_event_phase
            differences.append(right_event_phase - left_event_phase)
    return concentration(differences)


def main():
    for cycle in range(CYCLES - 1):
        for swing in (-SWING, SWING):
            end_phase, end_speed = phase_and_speed(cycle, 1.0, swing)
            start_phase, start_speed = phase_and_speed(cycle + 1, 0.0, -swing)
            assert abs(end_phase - start_phase) < 1e-12
            assert abs(end_speed - start_speed) < 1e-12
    assert 2 * pi - SWING * pi > 0
    r_events = event_only_concentration()
    assert r_events == 1.0
    results = {}
    for plane in ("lateral_anterior", "lateral_vertical"):
        for opposed in (False, True):
            left, right, vl, vr, delta = samples(plane, opposed)
            q_left, length_left = arc_weighted_q(left)
            q_right, length_right = arc_weighted_q(right)
            r = concentration(delta)
            results[(plane, opposed)] = (q_left, q_right, length_left,
                                           length_right, vl, vr, r)
            print(f"{plane} {'opposed' if opposed else 'aligned'} "
                  f"Q_right={tuple(round(x, 6) for x in q_right)} "
                  f"R={r:.6f} length={length_right:.6f}")
    for plane in ("lateral_anterior", "lateral_vertical"):
        a, b = results[(plane, False)], results[(plane, True)]
        assert a[0] == b[0]  # identical left path and timestamps
        assert max(abs(x - y) for x, y in zip(a[1], b[1])) < 1e-12
        assert abs(a[2] - b[2]) < 1e-10
        assert abs(a[3] - b[3]) < 1e-10
        assert a[4] == b[4]  # identical left speed series
        assert sorted(a[5]) == sorted(b[5])  # same right speed distribution
        assert a[6] > 0.999999 and abs(b[6] - 0.077246) < 1e-5
    for opposed in (False, True):
        a, b = results[("lateral_anterior", opposed)], results[("lateral_vertical", opposed)]
        assert abs(a[6] - b[6]) < 1e-12
        assert max(abs(x - y) for x, y in zip(a[1], b[1])) > 0.4
    print("matched_marginals=ok spatial_temporal_separation=ok")
    print(f"event_only_R={r_events:.6f} for aligned and opposed: within_cycle_phase_lost=ok")


if __name__ == "__main__":
    main()
