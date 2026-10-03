"""Shared-camera artifact in an apparent spatial -> spatial+phase gain.

Purely synthetic orthographic projection; no human movement or camera data.
"""

from cmath import exp
from math import atan2, cos, hypot, pi, sin


SAMPLES = 200_000


def q_y(ellipse_y_radius: float) -> float:
    """Arc-weighted Q_y of x=cos(theta), y=radius*sin(theta)."""
    numerator = length = 0.0
    for i in range(SAMPLES):
        angle = 2 * pi * (i + 0.5) / SAMPLES
        dx = -sin(angle)
        dy = ellipse_y_radius * cos(angle)
        speed = hypot(dx, dy)
        numerator += dy * dy / speed
        length += speed
    return numerator / length


def apparent_phase_r(camera_y_scale: float) -> float:
    """Relative-phase concentration of a projected circle against its true clock."""
    z = 0j
    for i in range(SAMPLES):
        angle = 2 * pi * (i + 0.5) / SAMPLES
        apparent = atan2(camera_y_scale * sin(angle), cos(angle))
        z += exp(1j * (apparent - angle))
    return abs(z / SAMPLES)


def conditional_mse(rows: list[tuple[float, float, float]], features: tuple[int, ...]):
    """Population lookup predictor over four equally probable constructed states."""
    groups = {}
    for row in rows:
        key = tuple(round(row[j], 12) for j in features)
        groups.setdefault(key, []).append(row[2])
    return sum(
        sum((y - sum(group) / len(group)) ** 2 for y in group)
        for group in groups.values()
    ) / len(rows)


def main():
    # Intrinsic ellipse geometry r and camera foreshortening c are independent.
    # X = spatial Q_y from the projected ellipse; H = apparent phase R of a
    # separate uniform reference circle seen by the same camera; Y = true Q_y.
    rows = []
    for r in (1.0, 2.0):
        for c in (0.5, 1.0):
            rows.append((q_y(r * c), apparent_phase_r(c), q_y(r)))
    for (r, c), row in zip(
        ((1.0, 0.5), (1.0, 1.0), (2.0, 0.5), (2.0, 1.0)), rows
    ):
        print(f"r={r:g}, c={c:g}: Q_observed={row[0]:.9f}, "
              f"R_apparent={row[1]:.9f}, Q_true={row[2]:.9f}")

    losses = {
        "none": conditional_mse(rows, ()),
        "Q": conditional_mse(rows, (0,)),
        "R": conditional_mse(rows, (1,)),
        "Q+R": conditional_mse(rows, (0, 1)),
    }
    for name, loss in losses.items():
        print(f"MSE[{name}]={loss:.9f}")
    assert abs(rows[1][0] - rows[2][0]) < 1e-12  # Same projected circle.
    assert abs(rows[1][1] - rows[2][1]) > 0.02  # Different camera artifact.
    assert abs(losses["none"] - losses["R"]) < 1e-12
    assert losses["Q"] > 0 and losses["Q+R"] < 1e-20


if __name__ == "__main__":
    main()
