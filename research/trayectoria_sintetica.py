"""Casos sintéticos para distinguir ubicación, línea y recorrido.

Ejecutar: python trayectoria_sintetica.py
Usa sólo la biblioteca estándar. No contiene datos humanos ni valida categorías Laban.
"""

from math import cos, pi, sin, sqrt


def add(a, b):
    return tuple(x + y for x, y in zip(a, b))


def sub(a, b):
    return tuple(x - y for x, y in zip(a, b))


def norm(v):
    return sqrt(sum(x * x for x in v))


def matvec(m, v):
    return tuple(sum(row[j] * v[j] for j in range(3)) for row in m)


def transpose(m):
    return tuple(tuple(m[j][i] for j in range(3)) for i in range(3))


def rotation_z(angle):
    c, s = cos(angle), sin(angle)
    return ((c, -s, 0), (s, c, 0), (0, 0, 1))


IDENTITY = rotation_z(0)
ORIGIN = (0.0, 0.0, 0.0)


def radial_position(p, centre, orientation):
    return matvec(transpose(orientation), sub(p, centre))


def limb_axis(distal, proximal, orientation):
    """Eje anatómico proximal→distal; distinto de velocidad del extremo."""
    return matvec(transpose(orientation), sub(distal, proximal))


def co_rotating_displacement(p0, p1, c0, c1, r0, r1):
    return sub(radial_position(p1, c1, r1), radial_position(p0, c0, r0))


def world_displacement_in_initial_body_frame(p0, p1, r0):
    return matvec(transpose(r0), sub(p1, p0))


def direction_if_resolved(displacement, position_error_bound):
    """Con dos posiciones de error acotado por ε, Δ puede errar hasta 2ε.

    Es una regla conservadora de demostración, no un umbral estadístico calibrado.
    """
    length = norm(displacement)
    if length <= 2 * position_error_bound:
        return None
    return tuple(x / length for x in displacement)


def path_features(points):
    radii = [norm(p) for p in points]
    length = sum(norm(sub(b, a)) for a, b in zip(points, points[1:]))
    return {"start": points[0], "end": points[-1],
            "min_radius": min(radii), "max_radius": max(radii),
            "polyline_length": length}


def main():
    # La mano parte a la derecha, pero se desplaza hacia arriba.
    a0, a1 = (1.0, 0.0, 0.0), (1.0, 1.0, 0.0)
    start_radial = radial_position(a0, ORIGIN, IDENTITY)
    move = world_displacement_in_initial_body_frame(a0, a1, IDENTITY)
    assert start_radial == (1.0, 0.0, 0.0)
    assert move == (0.0, 1.0, 0.0)

    # La dirección del brazo respecto del hombro no es la velocidad de la mano.
    shoulder0 = shoulder1 = ORIGIN
    assert limb_axis(a0, shoulder0, IDENTITY) == (1.0, 0.0, 0.0)
    assert limb_axis(a1, shoulder1, IDENTITY) == (1.0, 1.0, 0.0)
    assert move == (0.0, 1.0, 0.0)

    # Traslación conjunta: la mano se mueve, pero el eje del brazo no cambia.
    shoulder2, hand2 = (0.0, 1.0, 0.0), (1.0, 1.0, 0.0)
    assert limb_axis(hand2, shoulder2, IDENTITY) == limb_axis(a0, shoulder0, IDENTITY)
    assert world_displacement_in_initial_body_frame(a0, hand2, IDENTITY) == move

    # Trasladar ambos puntos no altera la línea de movimiento.
    b0, b1 = add(a0, (2, 0, 0)), add(a1, (2, 0, 0))
    assert world_displacement_in_initial_body_frame(b0, b1, IDENTITY) == move
    assert radial_position(b0, ORIGIN, IDENTITY) != start_radial

    # Mover toda la escena deja iguales posición y desplazamiento corporales.
    scene_shift = (2.0, -3.0, 0.5)
    assert radial_position(add(a0, scene_shift), scene_shift, IDENTITY) == start_radial
    assert co_rotating_displacement(add(a0, scene_shift), add(a1, scene_shift),
                                     scene_shift, scene_shift, IDENTITY, IDENTITY) == move

    # Rotar toda la escena con el marco corporal conserva sus coordenadas locales.
    quarter_turn = rotation_z(pi / 2)
    assert norm(sub(radial_position(matvec(quarter_turn, a0), ORIGIN, quarter_turn),
                    start_radial)) < 1e-12

    # Una mano inmóvil respecto del torso gira en mundo; los dos marcos difieren.
    r1 = rotation_z(pi / 2)
    p0 = (1.0, 0.0, 0.0)
    p1 = matvec(r1, p0)
    relative = co_rotating_displacement(p0, p1, ORIGIN, ORIGIN, IDENTITY, r1)
    global_move = world_displacement_in_initial_body_frame(p0, p1, IDENTITY)
    assert norm(relative) < 1e-12
    assert norm(global_move) > 1

    # Dos lazos tienen idénticos extremos, pero uno toca el centro y otro no.
    circular = [(cos(2*pi*i/100), sin(2*pi*i/100), 0) for i in range(101)]
    through_centre = [(1.0, 0.0, 0.0), (0.0, 0.0, 0.0),
                      (-1.0, 0.0, 0.0), (0.0, 0.0, 0.0),
                      (1.0, 0.0, 0.0)]
    circle_features = path_features(circular)
    centre_features = path_features(through_centre)
    assert norm(sub(circle_features["start"], centre_features["start"])) < 1e-12
    assert norm(sub(circle_features["end"], centre_features["end"])) < 1e-12
    assert abs(circle_features["min_radius"] - 1) < 1e-12
    assert centre_features["min_radius"] == 0
    assert 6.28 < circle_features["polyline_length"] < 6.29
    assert centre_features["polyline_length"] == 4

    # Una dirección bajo la cota de error posicional se declara indefinida.
    assert direction_if_resolved((0.005, 0, 0), 0.01) is None
    assert direction_if_resolved(move, 0.01) == move

    print("posición inicial:", start_radial, "desplazamiento:", move)
    print("giro corporal: cambio relativo:", relative,
          "desplazamiento en mundo:", global_move)
    print("lazo exterior:", circle_features)
    print("lazo por el centro:", centre_features)
    print("movimiento pequeño: dirección indefinida")


if __name__ == "__main__":
    main()
