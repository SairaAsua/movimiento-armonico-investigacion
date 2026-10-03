"""Synthetic checks for a proposed phrase-pair geometry gate.

All lengths, margins, errors and trajectories are constructed.  The sampled
curves are complete by fiat; this script neither bounds a real curve between
camera frames nor measures Nico, rope, visual quality, or HIT.
"""

from __future__ import annotations

from math import cos, dist, isfinite, pi, sin


N = 4096  # divisible by four; includes each diamond corner exactly
MARGIN = 0.1  # hypothetical, in units of a fixed body scale L=1


def circle(u: float) -> tuple[float, float, float]:
    return cos(2 * pi * u), sin(2 * pi * u), 0.0


def diamond(u: float) -> tuple[float, float, float]:
    # Same start, sense, four quarter-turn landmarks and Q as the circle.
    segment = min(int(4 * u), 3)
    local = 4 * u - segment
    vertices = ((1.0, 0.0), (0.0, 1.0), (-1.0, 0.0),
                (0.0, -1.0), (1.0, 0.0))
    a, b = vertices[segment], vertices[segment + 1]
    return a[0] * (1 - local) + b[0] * local, a[1] * (1 - local) + b[1] * local, 0.0


def sampled(function) -> list[tuple[float, float, float]]:
    return [function(k / N) for k in range(N + 1)]


def q_path(points: list[tuple[float, float, float]]) -> tuple[float, float, float]:
    sums = [0.0, 0.0, 0.0]
    length = 0.0
    for a, b in zip(points, points[1:]):
        step = tuple(y - x for x, y in zip(a, b))
        ds = dist(a, b)
        if ds:
            length += ds
            for axis in range(3):
                sums[axis] += step[axis] ** 2 / ds
    return tuple(value / length for value in sums)


def max_sampled_distance(a, b) -> float:
    assert len(a) == len(b)
    return max(dist(x, y) for x, y in zip(a, b))


def classify(distance: float, error_a: float | None, error_b: float | None,
             *, full_support: bool = True, same_discrete_structure: bool = True) -> str:
    """Apply the three-state rule to a *declared sampled* comparison.

    Errors must bound the entire registered curves on the common u coordinate,
    not merely be pointwise camera confidence or standard deviations.
    """
    if not same_discrete_structure:
        return "geometry_different"
    if (error_a is None or error_b is None or
            not all(isfinite(x) and x >= 0 for x in (distance, error_a, error_b))):
        return "geometry_indeterminate"
    error = error_a + error_b
    if distance - error > MARGIN:
        return "geometry_different"
    if full_support and distance + error < MARGIN:
        return "geometry_comparable"
    return "geometry_indeterminate"


def main() -> None:
    c = sampled(circle)
    d = sampled(diamond)
    qc, qd = q_path(c), q_path(d)
    assert all(abs(x - y) < 1e-12 for x, y in zip(qc, qd))
    assert all(abs(x - y) < 1e-12 for x, y in zip(qc, (0.5, 0.5, 0.0)))
    dc = max_sampled_distance(c, d)
    assert 0.29 < dc < 0.30

    # Time laws differ at the same clock instant but trace the same circle.
    def fast_then_slow(t: float) -> float:
        return t + 0.8 * t * (1 - t)

    assert fast_then_slow(0.0) == 0.0 and fast_then_slow(1.0) == 1.0
    assert all(fast_then_slow((k + 1) / N) > fast_then_slow(k / N)
               for k in range(N))
    assert abs(fast_then_slow(0.5) - 0.5) > 0.1
    timed_b = [circle(fast_then_slow(k / N)) for k in range(N + 1)]
    assert max_sampled_distance(c, timed_b) > 0.5  # different positions at the same clock times
    first_half_time_b = sum(fast_then_slow(k / N) <= 0.5 for k in range(N)) / N
    assert 0.32 < first_half_time_b < 0.33  # A spends 0.5 of the duration there
    # Registration by known arc fraction recovers circle(u) for both time laws.
    assert classify(max_sampled_distance(c, sampled(circle)), 0.01, 0.01) == "geometry_comparable"

    assert classify(dc, 0.01, 0.01) == "geometry_different"
    shifted = [(x + MARGIN, y, z) for x, y, z in c]
    assert classify(max_sampled_distance(c, shifted), 0.02, 0.02) == "geometry_indeterminate"
    # The chord closes an open observed route in the drawing only. Comparing
    # two copies would give zero distance if the invented samples were used;
    # it still cannot establish full observed support for a required return.
    open_route = [(0.0, 0.0, 0.0), (1.0, 0.0, 0.0), (1.0, 1.0, 0.0)]
    drawn_closed_route = open_route + [open_route[0]]
    assert drawn_closed_route[0] == drawn_closed_route[-1]
    assert classify(max_sampled_distance(drawn_closed_route, drawn_closed_route),
                    0.01, 0.01, full_support=False) == "geometry_indeterminate"
    assert classify(0.0, None, 0.01) == "geometry_indeterminate"
    # If one return is actually observed and the other execution omits it,
    # their predeclared discrete motif structures differ.
    assert classify(0.0, 0.01, 0.01, same_discrete_structure=False) == "geometry_different"
    print("OK: same Q / different curve; same curve / different time law; comparable, different, indeterminate")
    print(f"Q_circle={qc}; Q_diamond={qd}; sampled_max_distance={dc:.6f}; margin={MARGIN}")


if __name__ == "__main__":
    main()
