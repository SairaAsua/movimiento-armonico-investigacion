#!/usr/bin/env python3
"""Conservative label sequences from synthetic interval-censored events.

The linear extensions of hard pairwise precedence form a *superset* of
physically feasible event orders. Invariance across that superset is sufficient,
not necessary, for a sequence claim. No camera uncertainty is estimated here.
"""

import json
from dataclasses import dataclass
from itertools import permutations, product


@dataclass(frozen=True)
class Event:
    name: str
    start: int
    end: int
    leaders: tuple[str, ...]

    def __post_init__(self):
        assert self.start <= self.end
        assert self.leaders and set(self.leaders) <= {"D", "I"}


def possible_label_sequences(events: tuple[Event, ...]) -> set[str]:
    """Enumerate all labelings of all linear extensions of strict interval order."""
    assert 1 <= len(events) <= 7  # a small exact audit, not a streaming algorithm
    assert len({event.name for event in events}) == len(events)
    must_precede = {(i, j) for i, a in enumerate(events)
                    for j, b in enumerate(events) if i != j and a.end < b.start}
    sequences = set()
    for order in permutations(range(len(events))):
        rank = {index: place for place, index in enumerate(order)}
        if all(rank[i] < rank[j] for i, j in must_precede):
            for labels in product(*(events[i].leaders for i in order)):
                sequences.add("".join(labels))
    return sequences


def summary(events: tuple[Event, ...]) -> dict:
    sequences = possible_label_sequences(events)
    counts = sorted({sum(a != b for a, b in zip(seq, seq[1:]))
                     for seq in sequences})
    return {"label_sequences": sorted(sequences),
            "switch_counts": counts,
            "label_sequence_invariant": len(sequences) == 1,
            "switch_count_invariant": len(counts) == 1}


def main():
    same_leader_overlap = summary((Event("a", 0, 2, ("D",)),
                                   Event("b", 1, 3, ("D",)),
                                   Event("c", 4, 5, ("I",))))
    different_leader_overlap = summary((Event("a", 0, 2, ("D",)),
                                        Event("b", 1, 3, ("I",)),
                                        Event("c", 4, 5, ("D",))))
    uncertain_label = summary((Event("a", 0, 0, ("D",)),
                               Event("b", 1, 1, ("D", "I")),
                               Event("c", 2, 2, ("D",)),
                               Event("d", 3, 3, ("I",))))
    touching = summary((Event("a", 0, 1, ("D",)),
                        Event("b", 1, 2, ("I",))))
    assert same_leader_overlap == {
        "label_sequences": ["DDI"], "switch_counts": [1],
        "label_sequence_invariant": True, "switch_count_invariant": True}
    assert different_leader_overlap["label_sequences"] == ["DID", "IDD"]
    assert different_leader_overlap["switch_counts"] == [1, 2]
    assert uncertain_label["label_sequences"] == ["DDDI", "DIDI"]
    assert uncertain_label["switch_counts"] == [1, 3]
    assert touching["label_sequences"] == ["DI", "ID"]
    print(json.dumps({"same_leader_overlap": same_leader_overlap,
                      "different_leader_overlap": different_leader_overlap,
                      "uncertain_label": uncertain_label,
                      "touching": touching}, sort_keys=True))


if __name__ == "__main__":
    main()
