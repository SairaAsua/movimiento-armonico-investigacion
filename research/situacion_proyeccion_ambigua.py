"""Same ideal 2D pose, different 3D path situation; synthetic only."""

from __future__ import annotations

import json
from math import sqrt


def project(point: tuple[float, float, float]) -> tuple[float, float]:
    x, y, z = point
    assert z > 0
    return x / z, y / z


def metrics(
    hand: list[tuple[float, float, float]],
    origin: tuple[float, float, float],
    reach: float,
) -> dict[str, float]:
    q = [(p[0] - origin[0], p[1] - origin[1], p[2] - origin[2]) for p in hand]
    radii = [sqrt(sum(v * v for v in point)) for point in q]
    segments = [tuple(q[i + 1][k] - q[i][k] for k in range(3)) for i in range(len(q) - 1)]
    segment_lengths = [sqrt(sum(v * v for v in d)) for d in segments]
    length = sum(segment_lengths)
    assert length > 0 and all(v > 0 for v in segment_lengths)
    minimum_radii = []
    for start, d, d_length in zip(q, segments, segment_lengths):
        t = max(0.0, min(1.0, -sum(start[k] * d[k] for k in range(3)) / d_length**2))
        minimum_radii.append(sqrt(sum((start[k] + t * d[k]) ** 2 for k in range(3))))
    radial_total = sum(
        radii[i] + radii[i + 1] - 2 * minimum_radii[i] for i in range(len(segments))
    )
    q_axes = [
        sum(d[k] ** 2 / d_length for d, d_length in zip(segments, segment_lengths)) / length
        for k in range(3)
    ]
    return {
        "rho_min": min(minimum_radii) / reach,
        "rho_max": max(radii) / reach,
        "V_r": radial_total / length,
        "Q_x": q_axes[0],
        "Q_y": q_axes[1],
        "Q_z": q_axes[2],
    }


def main() -> None:
    # Pinhole camera at (0,0,0), optical axis +Z. Body origin and shoulders
    # are identical in both worlds; only the hand's unobserved depth changes.
    origin = (0.0, 0.0, 2.0)
    image_u = (-0.5, 0.0, 0.5)
    hand_a = [(2.0 * u, 0.0, 2.0) for u in image_u]
    hand_b = [(3.0 * u, 0.0, 3.0) for u in image_u]
    image_a = [project(p) for p in hand_a]
    image_b = [project(p) for p in hand_b]
    assert image_a == image_b == [(u, 0.0) for u in image_u]
    assert project(origin) == (0.0, 0.0)

    a, b = metrics(hand_a, origin, reach=2.0), metrics(hand_b, origin, reach=2.0)
    assert a["rho_min"] == 0.0 and b["rho_min"] == 0.5
    assert a["Q_x"] == b["Q_x"] == 1.0
    assert abs(a["V_r"] - 1.0) < 1e-12
    assert abs(b["V_r"] - (2 * (sqrt(3.25) - 1) / 3)) < 1e-12
    print(
        json.dumps(
            {
                "kind": "synthetic_2d_pose_ambiguity_only",
                "camera_model": "ideal_normalized_pinhole",
                "same_projected_hand": image_a,
                "same_projected_origin": project(origin),
                "fixed_reach_3d": 2.0,
                "world_a": a,
                "world_b": b,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
