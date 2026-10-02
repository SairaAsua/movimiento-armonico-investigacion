"""Exact synthetic checks for space–phase information under different measures.

No human data, camera reconstruction or HIT validation is involved.
"""

from __future__ import annotations

import math


def binary_entropy(probability: float) -> float:
    return -sum(p * math.log(p) for p in (probability, 1 - probability) if p > 0)


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


def task_joint(*, shared_residual: bool) -> list[list[list[float]]]:
    """Exact P(T,S,Phi) with balanced T and Bernoulli(1/4) residuals."""
    joint = [[[0.0 for _ in range(2)] for _ in range(2)] for _ in range(2)]
    residual = [(0, 0.75), (1, 0.25)]
    for task in range(2):
        for error_s, weight_s in residual:
            for error_phi, weight_phi in residual:
                if shared_residual and error_s != error_phi:
                    continue
                weight = 0.5 * weight_s * (1 if shared_residual else weight_phi)
                joint[task][task ^ error_s][task ^ error_phi] += weight
    return joint


def conditional_mutual_information(joint: list[list[list[float]]]) -> float:
    return sum(
        sum(map(sum, table)) * mutual_information(table)
        for table in joint
    )


def pooled_task_joint(joint: list[list[list[float]]]) -> list[list[float]]:
    return [[sum(joint[t][s][phi] for t in range(2)) for phi in range(2)] for s in range(2)]


def main() -> None:
    # A single uniform lap and an external clock make both bins equal solely
    # because they share the progress of the task. Maximal J is not evidence
    # of special coordination or a HIT prediction.
    uniform = [[0.5, 0.0], [0.0, 0.5]]
    assert abs(mutual_information(uniform) - math.log(2)) < 1e-12

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

    task_only = task_joint(shared_residual=False)
    residual_link = task_joint(shared_residual=True)
    expected_raw = math.log(2) - binary_entropy(0.375)
    expected_conditional = binary_entropy(0.25)
    assert abs(sum(sum(map(sum, table)) for table in task_only) - 1) < 1e-12
    assert abs(sum(sum(map(sum, table)) for table in residual_link) - 1) < 1e-12
    assert abs(mutual_information(pooled_task_joint(task_only)) - expected_raw) < 1e-12
    assert abs(conditional_mutual_information(task_only)) < 1e-12
    assert abs(mutual_information(pooled_task_joint(residual_link)) - math.log(2)) < 1e-12
    assert abs(conditional_mutual_information(residual_link) - expected_conditional) < 1e-12

    print(f"misma ejecución: J_t={j_time:.9f}, J_s={j_arc:.9f} nats")
    print(f"vuelta uniforme y reloj común: J_t=J_s={mutual_information(uniform):.9f} nats")
    print(
        "dos ciclos: J_ciclo_1=J_ciclo_2="
        f"{math.log(2):.9f}, J_pooled={mutual_information(pooled):.9f} nats"
    )
    print(
        "reloj común con errores independientes: "
        f"I(S;Phi)={expected_raw:.9f}, I(S;Phi|T)=0.000000000 nats"
    )
    print(
        "residuo compartido: "
        f"I(S;Phi)={math.log(2):.9f}, I(S;Phi|T)={expected_conditional:.9f} nats"
    )


if __name__ == "__main__":
    main()
