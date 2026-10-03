"""Prospective turn events versus retrospective closed-cycle W.

Timestamps are synthetic logical capture/availability times with zero modeled
latency. No HarMoCAP, Weaver, Beacon, video, or person is run here.
"""

import json
import math

from q_giro_orden_sintetico import steps_from_closed_vertices, turn_signature


TIMES_US = (0, 250_000, 500_000, 750_000, 1_000_000)
SIMPLE = ((0, 0), (1, 0), (1, 1), (0, 1), (0, 0))
CROSSED = ((0, 0), (1, 0), (1, 1), (0.5, -0.5), (0, 0))


def local_signed_turn(prev, current, next_):
    a = (current[0] - prev[0], current[1] - prev[1])
    b = (next_[0] - current[0], next_[1] - current[1])
    if a == (0, 0) or b == (0, 0):
        raise ValueError("zero displacement cannot define a turn")
    return math.atan2(a[0] * b[1] - a[1] * b[0], a[0] * b[0] + a[1] * b[1])


def observations_and_outputs(points):
    observations = [
        {"source_time_us": t, "point_xy": p} for t, p in zip(TIMES_US, points)
    ]
    turns = []
    resets = []
    valid_run = []
    for next_index, point in enumerate(points):
        if point is None:
            valid_run = []
            resets.append(
                {
                    "invalid_emitted_at_us": TIMES_US[next_index],
                    "reason": "gap_in_point_identity_or_observation",
                    "reset_candidate": True,
                }
            )
            continue
        valid_run.append((next_index, point))
        if len(valid_run) >= 3:
            (_, prev), (i, current), (_, next_) = valid_run[-3:]
            turns.append(
                {
                    "vertex_index": i,
                    "feature_time_us": TIMES_US[i],
                    "available_at_us": TIMES_US[next_index],
                    "signed_turn_rad": local_signed_turn(prev, current, next_),
                }
            )
    if not resets and points[-1] == points[0]:
        cycle_w = {
            "cycle_turning_number": turn_signature(steps_from_closed_vertices(points))[
                "turning_number"
            ],
            "feature_window_end_us": TIMES_US[-1],
            "available_at_us": TIMES_US[-1],
            "scope": "complete_closed_sampled_polygon",
        }
    else:
        cycle_w = {
            "cycle_turning_number": None,
            "available_at_us": TIMES_US[-1],
            "scope": "invalid_incomplete_cycle",
        }
    return observations, turns, cycle_w, resets


def main():
    simple_observations, simple_turns, simple_w, simple_resets = observations_and_outputs(SIMPLE)
    crossed_observations, crossed_turns, crossed_w, crossed_resets = observations_and_outputs(CROSSED)
    assert simple_resets == crossed_resets == []
    assert simple_observations[:3] == crossed_observations[:3]
    assert simple_turns[0] == crossed_turns[0]
    assert simple_turns[1] != crossed_turns[1]
    assert simple_w["cycle_turning_number"] == 1
    assert crossed_w["cycle_turning_number"] == 0
    assert all(turn["available_at_us"] >= TIMES_US[2] for turn in simple_turns)
    assert simple_w["available_at_us"] == crossed_w["available_at_us"] == TIMES_US[-1]

    missing = (SIMPLE[0], SIMPLE[1], SIMPLE[2], None, SIMPLE[4])
    _, missing_turns, missing_w, missing_resets = observations_and_outputs(missing)
    assert missing_turns == [simple_turns[0]]
    assert missing_w["cycle_turning_number"] is None
    assert missing_resets == [
        {
            "invalid_emitted_at_us": TIMES_US[3],
            "reason": "gap_in_point_identity_or_observation",
            "reset_candidate": True,
        }
    ]

    report = {
        "scope": "synthetic_planar_point_cycles_not_live_audio_or_people",
        "time_kind": "synthetic_logical_zero_latency_not_measured",
        "shared_observation_prefix_through_us": TIMES_US[2],
        "simple": {
            "observations": simple_observations,
            "causal_local_turns": simple_turns,
            "retrospective_cycle_W": simple_w,
        },
        "crossed": {
            "observations": crossed_observations,
            "causal_local_turns": crossed_turns,
            "retrospective_cycle_W": crossed_w,
        },
        "missing_fourth_observation_example": {
            "causal_local_turns": missing_turns,
            "retrospective_cycle_W": missing_w,
            "reset_candidates": missing_resets,
        },
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
