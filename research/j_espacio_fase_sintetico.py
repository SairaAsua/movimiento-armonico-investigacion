"""Exact synthetic checks for space–phase information under different measures.

No human data, camera reconstruction or HIT validation is involved.
"""

from __future__ import annotations

import math


def mutual_information(joint: list[list[float]]) -> float:
    total = sum(map(sum, joint))
    assert total > 0
    rows = [sum(row) / total for row in joint]
    cols = [sum(row[j] for row in joint) / total for j in range(len(joint[0]))]
    return sum(
        (value / total) * math.log((value / total) / (rows[i] * cols[j]))
        for i, row in enumerate(joint)
        for j, value in enumerate(row)
        if value > 0
    )


def q(t: float) -> float:
    """Monotone one-lap temporal parameterization on 0 <= t <= 1."""
    return t + 0.8 * t * (1 - t)


def main() -> None:
    # Spatial bin S is q(t)<1/2 vs >=1/2. Independent clock bin Φ is
    # t<1/2 vs >=1/2. q crosses the spatial boundary at t_cross.
    t_cross = (1.8 - math.sqrt(1.64)) / 1.6
    joint_time = [[t_cross, 0.0], [0.5 - t_cross, 0.5]]
    joint_arc = [[0.5, 0.0], [q(0.5) - 0.5, 1.0 - q(0.5)]]
    j_time = mutual_information(joint_time)
    j_arc = mutual_information(joint_arc)
    assert abs(sum(map(sum, joint_time)) - 1) < 1e-12
    assert abs(sum(map(sum, joint_arc)) - 1) < 1e-12
    assert abs(j_time - 0.30633084489885887) < 1e-12
    assert abs(j_arc - 0.27435846855026524) < 1e-12
    assert j_time != j_arc

    # Two equally weighted cycles: each has maximal binary association,
    # but the direction of that association reverses between cycles.
    aligned = [[0.5, 0.0], [0.0, 0.5]]
    reversed_relation = [[0.0, 0.5], [0.5, 0.0]]
    pooled = [
        [(aligned[i][j] + reversed_relation[i][j]) / 2 for j in range(2)]
        for i in range(2)
    ]
    assert abs(mutual_information(aligned) - math.log(2)) < 1e-12
    assert abs(mutual_information(reversed_relation) - math.log(2)) < 1e-12
    assert abs(mutual_information(pooled)) < 1e-12

    print(f"misma ejecución: J_t={j_time:.9f}, J_s={j_arc:.9f} nats")
    print(
        "dos ciclos: J_ciclo_1=J_ciclo_2="
        f"{math.log(2):.9f}, J_pooled={mutual_information(pooled):.9f} nats"
    )


if __name__ == "__main__":
    main()
