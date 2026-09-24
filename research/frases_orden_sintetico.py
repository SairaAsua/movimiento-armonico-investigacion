"""Dos frases sintéticas con igual ocupación, diferente recurrencia ordenada."""

from collections import Counter


def summary(states: str) -> tuple[Counter[str], int, tuple[int, int]]:
    counts = Counter(states)
    adjacent_equal = sum(a == b for a, b in zip(states, states[1:]))
    lag_three = sum(states[i] == states[i + 3] for i in range(len(states) - 3))
    return counts, adjacent_equal, (lag_three, len(states) - 3)


if __name__ == "__main__":
    a, b = summary("ABCABC"), summary("ABCBAC")
    assert a[0] == b[0] == Counter({"A": 2, "B": 2, "C": 2})
    assert a[1] == b[1] == 0
    assert a[2] == (3, 3)
    assert b[2] == (1, 3)
    print("ABCABC:", a, "ABCBAC:", b)
