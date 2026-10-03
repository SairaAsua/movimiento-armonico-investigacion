"""Check partial-arc Q bounds with constructed polylines; no human data."""

from __future__ import annotations

from math import dist, isclose


Point = tuple[float, float, float]


def q_of_path(points: list[Point]) -> tuple[float, tuple[float, float, float]]:
    totals = [0.0, 0.0, 0.0]
    length = 0.0
    for a, b in zip(points, points[1:]):
        segment = tuple(y - x for x, y in zip(a, b))
        ds = dist(a, b)
        if ds == 0:
            continue
        length += ds
        for k in range(3):
            totals[k] += segment[k] ** 2 / ds
    if length <= 0:
        raise ValueError("A nonzero path is required")
    return length, tuple(value / length for value in totals)


def component_bounds(
    q_observed: tuple[float, float, float], observed_length: float, hidden_max: float
) -> tuple[tuple[float, float], ...]:
    if observed_length <= 0 or hidden_max < 0:
        raise ValueError("Invalid arc-length bounds")
    m_max = hidden_max / (observed_length + hidden_max)
    return tuple(((1 - m_max) * q, (1 - m_max) * q + m_max) for q in q_observed)


def assert_vector_close(actual: tuple[float, ...], expected: tuple[float, ...]) -> None:
    assert all(isclose(a, e, abs_tol=1e-12) for a, e in zip(actual, expected))


def main() -> None:
    origin: Point = (0.0, 0.0, 0.0)
    visible = [origin, (1.0, 0.0, 0.0), origin]
    hidden_x = [origin, (1.5, 0.0, 0.0), origin]
    hidden_y = [origin, (0.0, 1.5, 0.0), origin]
    lo, qo = q_of_path(visible)
    hx, qhx = q_of_path(hidden_x)
    hy, qhy = q_of_path(hidden_y)
    assert isclose(lo, 2) and isclose(hx, 3) and isclose(hy, 3)
    assert_vector_close(qo, (1, 0, 0))
    q_full_x = tuple((lo * a + hx * b) / (lo + hx) for a, b in zip(qo, qhx))
    q_full_y = tuple((lo * a + hy * b) / (lo + hy) for a, b in zip(qo, qhy))
    assert_vector_close(q_full_x, (1, 0, 0))
    assert_vector_close(q_full_y, (0.4, 0.6, 0))
    bounds = component_bounds(qo, lo, 3)
    assert bounds == ((0.4, 1.0), (0.0, 0.6), (0.0, 0.6))
    for q in (q_full_x, q_full_y):
        assert all(low - 1e-12 <= value <= high + 1e-12 for value, (low, high) in zip(q, bounds))
    assert not ((1 - 0.6) * (qo[0] - qo[1]) > 0.6)

    robust_bounds = component_bounds(qo, 3, 1)
    assert robust_bounds == ((0.75, 1.0), (0.0, 0.25), (0.0, 0.25))
    assert (1 - 0.25) * (qo[0] - qo[1]) > 0.25
    print("same visible path: Q full x=(1,0,0), Q full y=(0.4,0.6,0)")
    print(f"m_max=0.6 component bounds: {bounds}")
    print(f"m_max=0.25 component bounds: {robust_bounds}")


if __name__ == "__main__":
    main()
