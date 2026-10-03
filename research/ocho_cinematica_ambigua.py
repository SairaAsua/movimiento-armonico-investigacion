"""Un mismo ocho de la mano admite dos configuraciones articulares.

Ejecutar: python ocho_cinematica_ambigua.py
Brazo plano ideal de dos segmentos iguales; no hay personas, soga ni dinámica muscular.
"""

from math import acos, atan2, cos, dist, pi, sin


N = 1440
L1 = L2 = 1.0  # unidades arbitrarias


def endpoint(t):
    """Ocho cerrado con cruce en (1.2, 0) en t=0, pi y 2*pi."""
    return (1.2 + 0.2 * sin(t), 0.15 * sin(2 * t))


def arm(point, elbow_sign):
    """Cinemática inversa exacta; signo +1 o -1 elige una rama del codo."""
    x, y = point
    radius2 = x * x + y * y
    c2 = (radius2 - L1 * L1 - L2 * L2) / (2 * L1 * L2)
    assert -1 < c2 < 1, "el punto debe estar dentro del espacio alcanzable"
    q2 = elbow_sign * acos(c2)
    q1 = atan2(y, x) - atan2(L2 * sin(q2), L1 + L2 * cos(q2))
    elbow = (L1 * cos(q1), L1 * sin(q1))
    hand = (elbow[0] + L2 * cos(q1 + q2),
            elbow[1] + L2 * sin(q1 + q2))
    return elbow, hand, (q1, q2)


def twice_signed_area(points):
    return sum(a[0] * b[1] - b[0] * a[1]
               for a, b in zip(points, points[1:]))


def main():
    points = [endpoint(2 * pi * k / N) for k in range(N + 1)]
    first = twice_signed_area(points[: N // 2 + 1]) / 2
    second = twice_signed_area(points[N // 2:]) / 2
    assert first * second < 0, "los lóbulos deben tener sentidos opuestos"

    max_hand_error = 0.0
    min_elbow_separation = float("inf")
    max_joint_angle_difference = 0.0
    for target in points:
        elbow_a, hand_a, q_a = arm(target, +1)
        elbow_b, hand_b, q_b = arm(target, -1)
        max_hand_error = max(max_hand_error, dist(target, hand_a),
                             dist(target, hand_b), dist(hand_a, hand_b))
        min_elbow_separation = min(min_elbow_separation, dist(elbow_a, elbow_b))
        max_joint_angle_difference = max(max_joint_angle_difference,
                                         abs(q_a[1] - q_b[1]))

    assert max_hand_error < 1e-12
    assert min_elbow_separation > 1.0
    assert max_joint_angle_difference > pi
    print(f"áreas firmadas de lóbulos: {first:.6f}, {second:.6f}")
    print(f"error máximo de mano entre ramas: {max_hand_error:.3g}")
    print(f"separación mínima de codos: {min_elbow_separation:.6f}")
    print(f"diferencia máxima de ángulo de codo: {max_joint_angle_difference:.6f} rad")
    print("Misma trayectoria y reloj de mano; configuración articular distinta.")


if __name__ == "__main__":
    main()
