"""Contraejemplo sin datos humanos: mismo recorrido de mano, dos orígenes del giro."""

from math import cos, pi, sin


def rotate_z(angle, point):
    x, y, z = point
    return (cos(angle) * x - sin(angle) * y,
            sin(angle) * x + cos(angle) * y,
            z)


def close(a, b, tol=1e-12):
    return all(abs(x - y) < tol for x, y in zip(a, b))


hand_in_thorax = (1.0, 0.0, 0.0)
for step in range(11):
    angle = pi * step / 20  # 0 a 90 grados

    # A: pelvis y tórax giran juntos en la sala; no hay torsión entre ambos.
    pelvis_yaw_a = angle
    thorax_yaw_a = angle
    hand_world_a = rotate_z(thorax_yaw_a, hand_in_thorax)
    hand_in_pelvis_a = rotate_z(thorax_yaw_a - pelvis_yaw_a, hand_in_thorax)
    twist_a = thorax_yaw_a - pelvis_yaw_a

    # B: pelvis fija y tórax gira respecto de ella.
    pelvis_yaw_b = 0.0
    thorax_yaw_b = angle
    hand_world_b = rotate_z(thorax_yaw_b, hand_in_thorax)
    hand_in_pelvis_b = rotate_z(thorax_yaw_b - pelvis_yaw_b, hand_in_thorax)
    twist_b = thorax_yaw_b - pelvis_yaw_b

    assert close(hand_world_a, hand_world_b)
    assert close(hand_in_pelvis_a, hand_in_thorax)
    assert close(hand_in_pelvis_b, hand_world_b)
    assert abs(twist_a) < 1e-12
    assert abs(twist_b - angle) < 1e-12

assert not close(hand_in_pelvis_a, hand_in_pelvis_b)
print("OK: la mano en sala coincide; giro global y torsión local difieren")

# La derivada en el marco co-rotante tampoco es la velocidad física en sala.
# Caso C: mano fija en el tórax; el cuerpo gira 90 grados en sala.
fixed_body_hand = (1.0, 0.0, 0.0)
world_start = rotate_z(0.0, fixed_body_hand)
world_end = rotate_z(pi / 2, fixed_body_hand)
body_start = rotate_z(0.0, world_start)
body_end = rotate_z(-pi / 2, world_end)
assert close(body_start, body_end)
assert not close(world_start, world_end)

# Caso D: mano fija en sala; el cuerpo gira los mismos 90 grados bajo ella.
fixed_world_hand = (1.0, 0.0, 0.0)
body_start = rotate_z(0.0, fixed_world_hand)
body_end = rotate_z(-pi / 2, fixed_world_hand)
assert not close(body_start, body_end)
assert close(fixed_world_hand, world_start)

print("OK: giro con mano corporal fija da desplazamiento en sala y cero relativo")
print("OK: giro bajo mano fija en sala da cero desplazamiento en sala y cambio relativo")
