"""Adversarial position-error example for the proposed Q descriptor (not human data)."""

from math import hypot, sqrt


def q_xy(points):
    nx = ny = length = 0.0
    for (x0, y0), (x1, y1) in zip(points, points[1:]):
        dx, dy = x1 - x0, y1 - y0
        segment = hypot(dx, dy)
        if segment:
            nx += dx * dx / segment
            ny += dy * dy / segment
            length += segment
    return (nx / length, ny / length), length


def case(n, position_error=0.005):
    true = [(i / n, 0.0) for i in range(n + 1)]
    observed = [
        (i / n, 0.0 if i in (0, n) else position_error * (-1) ** i)
        for i in range(n + 1)
    ]
    q_true, l_true = q_xy(true)
    q_observed, l_observed = q_xy(observed)
    assert abs(q_true[0] - 1.0) < 1e-12 and q_true[1] == 0.0
    assert abs(sum(q_observed) - 1.0) < 1e-12
    assert max(abs(a[1] - b[1]) for a, b in zip(true, observed)) <= position_error

    # Each endpoint's position error is bounded by sigma, hence E <= 2*n*sigma.
    e_bound = 2 * n * position_error
    if l_observed > e_bound:
        component_bound = min(
            1.0, (2 / sqrt(3) + q_observed[1]) * e_bound / (l_observed - e_bound)
        )
        assert abs(q_true[1] - q_observed[1]) <= component_bound + 1e-12
    return q_observed, l_true, l_observed, e_bound


if __name__ == "__main__":
    for samples_per_second in (30, 120, 240):
        q, l_true, l_observed, e = case(samples_per_second)
        print(
            f"n={samples_per_second}: Q_observed=({q[0]:.6f}, {q[1]:.6f}, 0), "
            f"L_true={l_true:.6f} m, L_observed={l_observed:.6f} m, E_bound={e:.3f} m"
        )
    assert case(240)[0][1] > case(120)[0][1] > case(30)[0][1]
