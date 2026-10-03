#!/usr/bin/env python3
"""Logical two-source gate for a proposed inter-member distance signal.

Research fixture only: no camera, HarMoCAP, Weaver, OSC or audio is run.
The time/quality thresholds below are invented to exercise state transitions.
"""

import json
from math import dist


MAX_SKEW_US = 10_000
MAX_AGE_US = 50_000


def observation(channel, frame, captured, available, xyz, *, state="observed",
                generation="g1", clock="clock1", calibration="cal1",
                clock_error=1_000, person="person_a"):
    return dict(channel=channel, frame=frame, captured_us=captured,
                available_us=available, xyz=xyz, state=state,
                generation=generation, clock_map=clock,
                calibration=calibration, clock_error_us=clock_error,
                person=person)


class PairGate:
    def __init__(self):
        self.latest = {"left": None, "right": None}
        self.last_frame = {"left": -1, "right": -1}
        self.last_pair = (-1, -1)
        self.active = False
        self.deadline_us = None
        self.events = []

    def _invalid(self, reason, now):
        if self.active:
            self.events.append(dict(at_us=now, state="invalid", reason=reason,
                                    proposed_output="reset"))
            self.active = False
            self.deadline_us = None

    def tick(self, now):
        if self.active and now > self.deadline_us:
            self._invalid("expired", now)

    def receive(self, obs, now):
        self.tick(now)
        if obs["person"] != "person_a":
            return  # Another person cannot change this person's active pair.
        side = obs["channel"]
        assert side in self.latest
        if obs["frame"] < self.last_frame[side]:
            return  # A state update for an older frame is reordered.
        if obs["available_us"] > now or obs["captured_us"] > obs["available_us"]:
            self.latest[side] = None
            self._invalid("bad_time", now)
            return
        if obs["state"] != "observed":
            self.last_frame[side] = obs["frame"]
            self.latest[side] = None
            self._invalid(obs["state"], now)
            return
        if obs["frame"] == self.last_frame[side]:
            return  # Duplicate observed input cannot renew a lease.
        self.last_frame[side] = obs["frame"]
        self.latest[side] = obs
        left, right = self.latest["left"], self.latest["right"]
        if left is None or right is None:
            return
        if any(left[key] != right[key] for key in ("generation", "clock_map", "calibration")):
            self._invalid("context_mismatch", now)
            return
        if max(now - left["captured_us"], now - right["captured_us"]) > MAX_AGE_US:
            self._invalid("source_age", now)
            return
        worst_skew = (abs(left["captured_us"] - right["captured_us"])
                      + left["clock_error_us"] + right["clock_error_us"])
        if worst_skew > MAX_SKEW_US:
            self._invalid("skew_bound", now)
            return
        pair = (left["frame"], right["frame"])
        if pair[0] <= self.last_pair[0] or pair[1] <= self.last_pair[1]:
            return  # Need a new independent observation from BOTH sides.
        self.last_pair = pair
        self.active = True
        self.deadline_us = min(left["captured_us"], right["captured_us"]) + MAX_AGE_US
        self.events.append(dict(at_us=now, state="eligible_numeric",
                                left_frame=pair[0], right_frame=pair[1],
                                left_captured_us=left["captured_us"],
                                right_captured_us=right["captured_us"],
                                worst_skew_us=worst_skew,
                                distance=dist(left["xyz"], right["xyz"]),
                                expires_after_us=self.deadline_us,
                                proposed_output="control_candidate"))


def demo_events():
    gate = PairGate()
    l, r = (0., 0., 0.), (1., 0., 0.)
    gate.receive(observation("left", 1, 0, 5_000, l), 5_000)
    gate.receive(observation("right", 1, 4_000, 6_000, r), 6_000)
    gate.receive(observation("left", 1, 0, 5_000, l), 20_000)
    gate.receive(observation("right", 2, 20_000, 21_000, r,
                             person="person_b"), 21_000)
    gate.tick(50_001)  # Other traffic and a duplicate did not renew the pair.
    gate.receive(observation("right", 2, 55_000, 56_000, r), 56_000)
    gate.receive(observation("left", 2, 57_000, 58_000, l), 58_000)
    gate.receive(observation("right", 2, 55_000, 61_000, r,
                             state="held"), 61_000)
    gate.receive(observation("right", 4, 70_000, 71_000, r,
                             calibration="cal2"), 71_000)
    gate.receive(observation("left", 3, 71_000, 72_000, l,
                             calibration="cal2"), 72_000)
    gate.receive(observation("left", 4, 90_000, 91_000, l,
                             calibration="cal2"), 91_000)
    gate.receive(observation("right", 5, 91_000, 92_000, r,
                             calibration="cal2", clock_error=10_000), 92_000)
    assert len(gate.events) == 6  # Small nominal skew, uncertainty too wide.
    gate.receive(observation("right", 6, 93_000, 94_000, r,
                             calibration="cal2"), 94_000)
    gate.receive(observation("right", 7, 95_000, 96_000, r,
                             calibration="cal3"), 96_000)
    expected = ["eligible_numeric", "expired", "eligible_numeric", "held",
                "eligible_numeric", "skew_bound", "eligible_numeric",
                "context_mismatch"]
    # A mismatch while inactive emits nothing; while active it requests reset.
    assert [e.get("reason", e["state"]) for e in gate.events] == expected
    assert all(e.get("distance", 1) == 1 for e in gate.events)
    assert [e["proposed_output"] for e in gate.events if e["state"] == "invalid"] == ["reset"] * 4
    return gate.events


def main():
    print(json.dumps(demo_events(), sort_keys=True))


if __name__ == "__main__":
    main()
