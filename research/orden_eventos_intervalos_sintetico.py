#!/usr/bin/env python3
"""Strict event order from closed time-support intervals, not frame arrival order.

All numbers are invented. Intervals are assumed to be simultaneous hard bounds
in a common clock; this script does not estimate camera or clock uncertainty.
"""

import json
from dataclasses import dataclass
from math import ceil, floor


@dataclass(frozen=True)
class Event:
    name: str
    earliest_us: int
    latest_us: int
    available_at_us: int
    source_frame_ids: tuple[int, ...]

    def __post_init__(self):
        assert 0 <= self.earliest_us <= self.latest_us <= self.available_at_us
        assert self.source_frame_ids


def order(first: Event, second: Event):
    """Return proven temporal relation and possible lag from first to second."""
    lag = (second.earliest_us - first.latest_us,
           second.latest_us - first.earliest_us)
    if lag[0] > 0:
        relation = f"{first.name}_before_{second.name}"
    elif lag[1] < 0:
        relation = f"{second.name}_before_{first.name}"
    else:
        relation = "unresolved"
    return {"relation": relation, "lag_us_interval": lag,
            "decision_available_at_us": max(first.available_at_us, second.available_at_us)}


def map_interval(name, start, end, available_common_us, frame_ids, *, offset, rate, error):
    """Affine source→common clock; error must be a validated hard bound."""
    assert rate > 0 and error >= 0 and start <= end
    a = floor(offset + rate * start - error)
    b = ceil(offset + rate * end + error)
    return Event(name, a, b, available_common_us, frame_ids)


def main():
    clear = order(Event("left", 10, 20, 25, (1, 2)),
                  Event("right", 31, 40, 45, (3, 4)))
    reverse = order(Event("left", 31, 40, 45, (3, 4)),
                    Event("right", 10, 20, 25, (1, 2)))
    overlap = order(Event("left", 10, 25, 30, (1, 2)),
                    Event("right", 20, 35, 40, (3, 4)))
    touching = order(Event("left", 10, 20, 25, (1, 2)),
                     Event("right", 20, 30, 35, (3, 4)))
    same_frame = order(Event("left", 10, 20, 25, (7,)),
                       Event("right", 10, 20, 25, (7,)))
    # A nominal 12 us separation becomes unresolvable with ±8 us per source.
    a = map_interval("left", 100, 100, 130, (1,), offset=0, rate=1, error=8)
    b = map_interval("right", 112, 112, 140, (2,), offset=0, rate=1, error=8)
    clock_uncertain = order(a, b)
    assert clear == {"relation": "left_before_right", "lag_us_interval": (11, 30),
                     "decision_available_at_us": 45}
    assert reverse["relation"] == "right_before_left" and reverse["lag_us_interval"] == (-30, -11)
    assert all(case["relation"] == "unresolved" for case in (overlap, touching, same_frame, clock_uncertain))
    assert touching["lag_us_interval"] == (0, 20)
    assert clock_uncertain["lag_us_interval"] == (-4, 28)
    print(json.dumps({"clear": clear, "reverse": reverse,
                      "overlap": overlap, "touching": touching,
                      "same_frame": same_frame, "clock_uncertain": clock_uncertain},
                     sort_keys=True))


if __name__ == "__main__":
    main()
