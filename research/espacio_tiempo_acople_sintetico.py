"""Control exacto/numerico: margenes iguales, distinto acople espacio-tiempo.

No usa datos humanos ni intenta estimar energia.
"""

import math


TAU = 2 * math.pi
EPS = 0.5


def state(t, sign):
    angle = TAU * t + sign * EPS * math.sin(TAU * t)
    speed = TAU * (1 + sign * EPS * math.cos(TAU * t))
    angular_accel = -sign * EPS * TAU**2 * math.sin(TAU * t)
    accel_norm_sq = angular_accel**2 + speed**4
    return angle, speed, accel_norm_sq


def summarize(sign, n=200_000):
    front_speed_arc = 0.0
    rear_speed_arc = 0.0
    front_length = 0.0
    rear_length = 0.0
    speed_time = 0.0
    accel_sq_time = 0.0
    for i in range(n):
        t = (i + 0.5) / n
        theta, speed, accel_sq = state(t, sign)
        ds = speed / n  # Radio unitario.
        speed_time += speed / n
        accel_sq_time += accel_sq / n
        if math.cos(theta) >= 0:  # Frente: x>0 en el marco fijado.
            front_speed_arc += speed * ds
            front_length += ds
        else:
            rear_speed_arc += speed * ds
            rear_length += ds
    contrast = front_speed_arc / front_length - rear_speed_arc / rear_length
    return contrast, speed_time, accel_sq_time, front_length, rear_length


def main():
    a = summarize(+1)
    b = summarize(-1)
    # B(t) tiene el perfil temporal de A(t+1/2), con la curva girada media vuelta.
    for k in (1, 2):
        assert math.isclose(a[k], b[k], rel_tol=1e-10, abs_tol=1e-10), (k, a, b)
    # La pertenencia a hemisferio se decide en muestras finitas, no en el cruce exacto.
    for length in (a[3], a[4], b[3], b[4]):
        assert abs(length - math.pi) < 5e-5
    assert a[0] > 0.1 and b[0] < -0.1
    assert math.isclose(a[0], -b[0], rel_tol=1e-10, abs_tol=1e-10)
    print('A:', a)
    print('B:', b)
    print('Mismo recorrido, duracion, margenes temporales y aceleracion total;')
    print('contraste de rapidez frente/atras opuesto.')


if __name__ == '__main__':
    main()
