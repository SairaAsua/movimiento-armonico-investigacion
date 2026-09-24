"""Comprobación sintética: mismo recorrido circular, distinta ocupación temporal."""

from math import pi, cos, sin, sqrt, hypot


def q(t: float) -> float:
    return t + 0.8 * t * (1.0 - t)


def circle(u: float) -> tuple[float, float]:
    return cos(2.0 * pi * u), sin(2.0 * pi * u)


def measure(n: int = 100_000) -> tuple[float, float, float, float]:
    time_a = time_b = 0
    length_a = length_b = 0.0
    half_a = half_b = 0.0
    for i in range(n):
        t0, t1 = i / n, (i + 1) / n
        a0, a1 = circle(t0), circle(t1)
        b0, b1 = circle(q(t0)), circle(q(t1))
        da = hypot(a1[0] - a0[0], a1[1] - a0[1])
        db = hypot(b1[0] - b0[0], b1[1] - b0[1])
        length_a += da
        length_b += db
        if (t0 + t1) / 2 <= 0.5:
            time_a += 1
            half_a += da
        if q((t0 + t1) / 2) <= 0.5:
            time_b += 1
            half_b += db
    return time_a / n, time_b / n, half_a / length_a, half_b / length_b


if __name__ == "__main__":
    result = measure()
    exact_b_time = (1.8 - sqrt(1.64)) / 1.6
    assert abs(result[0] - 0.5) < 1e-4
    assert abs(result[1] - exact_b_time) < 1e-4
    assert abs(result[2] - 0.5) < 1e-4
    assert abs(result[3] - 0.5) < 1e-4
    print("tiempo A/B:", result[:2], "recorrido A/B:", result[2:])
