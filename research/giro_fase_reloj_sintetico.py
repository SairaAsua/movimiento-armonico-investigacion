"""Logical timestamp counterexample for a three-point turn and an independent phase.

All rates, times and phases are constructed; no video, person or audio is run.
"""

import cmath
import json
import math


def phase_at(time_s, frequency_hz):
    return (2 * math.pi * frequency_hz * time_s) % (2 * math.pi)


def circular_difference(a, b):
    return math.atan2(math.sin(a - b), math.cos(a - b))


def mean_vector(phases):
    return sum((cmath.exp(1j * phase) for phase in phases), 0j) / len(phases)


def main():
    frequency_hz = 1.0
    feature_time_s = 0.25  # central vertex of points at 0, 0.25, 0.5 s
    available_at_s = 0.5  # only after the next point has arrived
    feature_phase = phase_at(feature_time_s, frequency_hz)
    wrong_phase = phase_at(available_at_s, frequency_hz)
    assert math.isclose(math.degrees(feature_phase), 90)
    assert math.isclose(math.degrees(wrong_phase), 180)

    fast_frequency_hz = 2.0
    one_frame_s = 1 / 30
    one_frame_phase_error_deg = math.degrees(2 * math.pi * fast_frequency_hz * one_frame_s)
    assert math.isclose(one_frame_phase_error_deg, 24)

    feature_times = tuple(range(8))  # all true event-locked phases are zero at 2 Hz
    delays = tuple(0.0 if i % 2 == 0 else 0.125 for i in range(8))
    correct_phases = [phase_at(t, fast_frequency_hz) for t in feature_times]
    delivered_phases = [phase_at(t + lag, fast_frequency_hz) for t, lag in zip(feature_times, delays)]
    correct_vector = mean_vector(correct_phases)
    delivered_vector = mean_vector(delivered_phases)
    assert math.isclose(abs(correct_vector), 1, abs_tol=1e-12)
    assert math.isclose(abs(delivered_vector), math.sqrt(0.5), abs_tol=1e-12)
    assert math.isclose(math.degrees(cmath.phase(delivered_vector)), 45, abs_tol=1e-12)

    # A known assignment error of +/-10 ms at 2 Hz implies at most 7.2 deg;
    # this is a deterministic design bound, not a measured camera uncertainty.
    assignment_uncertainty_s = 0.010
    phase_error_bound_deg = math.degrees(
        2 * math.pi * fast_frequency_hz * assignment_uncertainty_s
    )
    assert math.isclose(phase_error_bound_deg, 7.2)
    assert math.isclose(
        abs(circular_difference(phase_at(0.5 + assignment_uncertainty_s, 2), phase_at(0.5, 2))),
        math.radians(phase_error_bound_deg),
    )

    report = {
        "scope": "synthetic_logical_clock_and_independent_constructed_phase_not_human_HIT",
        "central_vertex": {
            "sample_times_s": (0.0, 0.25, 0.5),
            "feature_time_s": feature_time_s,
            "available_at_s": available_at_s,
            "phase_at_feature_deg": math.degrees(feature_phase),
            "phase_if_joined_at_delivery_deg": math.degrees(wrong_phase),
            "spurious_shift_deg": math.degrees(circular_difference(wrong_phase, feature_phase)),
        },
        "one_frame_at_30_fps_2_hz": {
            "delay_s": one_frame_s,
            "spurious_shift_deg": one_frame_phase_error_deg,
        },
        "eight_events_at_2_hz": {
            "delays_s": delays,
            "R_using_feature_times": abs(correct_vector),
            "R_using_delivery_times": abs(delivered_vector),
            "mean_angle_using_delivery_deg": math.degrees(cmath.phase(delivered_vector)),
        },
        "hypothetical_time_assignment_uncertainty_at_2_hz": {
            "uncertainty_s": assignment_uncertainty_s,
            "phase_error_bound_deg": phase_error_bound_deg,
        },
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
