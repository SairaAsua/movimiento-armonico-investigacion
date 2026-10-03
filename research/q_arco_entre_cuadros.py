"""Exact-sample aliasing and a curvature-gated Q check; synthetic mathematics only."""

from math import cos, hypot, pi, sin


def q_polyline(points):
    numerator = [0.0, 0.0]
    length = 0.0
    for (x0, y0), (x1, y1) in zip(points, points[1:]):
        dx, dy = x1 - x0, y1 - y0
        chord = hypot(dx, dy)
        if chord:
            numerator[0] += dx * dx / chord
            numerator[1] += dy * dy / chord
            length += chord
    return tuple(value / length for value in numerator), length


def alias_case(frames_per_second=30, amplitude=0.005, quadrature=120_000):
    """A 1 m x-traverse; y makes one full oscillation between every two samples."""
    sampled = [
        (i / frames_per_second, amplitude * sin(2 * pi * i))
        for i in range(frames_per_second + 1)
    ]
    q_sampled, length_sampled = q_polyline(sampled)
    assert abs(q_sampled[1]) < 1e-25
    assert abs(length_sampled - 1.0) < 1e-12

    numerator_y = length = 0.0
    for i in range(quadrature):
        t = (i + 0.5) / quadrature
        dy_dt = amplitude * 2 * pi * frames_per_second * cos(
            2 * pi * frames_per_second * t
        )
        speed = hypot(1.0, dy_dt)
        length += speed / quadrature
        numerator_y += dy_dt * dy_dt / speed / quadrature
    q_continuous_y = numerator_y / length
    assert 0 < q_continuous_y < 1
    return q_sampled[1], q_continuous_y, length


def circle_case(radius=10.0, arc_length=1.0, segments=30):
    """Unit-speed circular arc, with known curvature 1/radius."""
    points = [
        (radius * sin(s / radius), radius * (1 - cos(s / radius)))
        for s in (arc_length * i / segments for i in range(segments + 1))
    ]
    sampled, chord_length = q_polyline(points)
    true_x = 0.5 + sin(2 * arc_length / radius) * radius / (4 * arc_length)
    true = (true_x, 1 - true_x)
    h_max = arc_length / segments
    bound = min(1.0, 3 * h_max / radius)
    assert all(abs(a - b) <= bound for a, b in zip(sampled, true))
    return true, sampled, chord_length, bound


if __name__ == "__main__":
    observed_y, continuous_y, continuous_length = alias_case()
    print(
        f"alias: Q_y(sampled)={observed_y:.6f}, "
        f"Q_y(continuous)={continuous_y:.6f}, L={continuous_length:.6f} m"
    )
    true, sampled, chord_length, bound = circle_case()
    print(
        f"circle: Q_true={true}, Q_sampled={sampled}, "
        f"L_chord={chord_length:.9f} m, bound={bound:.6f}"
    )
