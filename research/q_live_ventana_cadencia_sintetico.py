"""Audita una ventana temporal de Q_live con una circunferencia ideal.

No modela captura, ruido, pose humana ni audio. Usa solo la biblioteca estándar.
"""

from math import cos, hypot, isclose, pi, sin


FPS = 1200
WINDOW_S = 0.3
ARC_FRACTION = 0.3


def trajectory(hz):
    count = round(FPS / hz)
    assert isclose(count / FPS, 1 / hz)
    return [(cos(2 * pi * hz * i / FPS), sin(2 * pi * hz * i / FPS))
            for i in range(count + 1)]


def q_from_last_segments(points, count):
    chosen = points[-count - 1:]
    length = 0.0
    x_weight = 0.0
    for a, b in zip(chosen, chosen[1:]):
        dx, dy = b[0] - a[0], b[1] - a[1]
        ds = hypot(dx, dy)
        length += ds
        x_weight += dx * dx / ds
    return x_weight / length, 1 - x_weight / length


def qx_continuous(arc_fraction):
    # Tangente al círculo: u_x = -sin(theta). El arco termina en theta=2pi.
    return 0.5 - sin(4 * pi * arc_fraction) / (8 * pi * arc_fraction)


def main():
    results = {}
    for hz in (1, 2):
        points = trajectory(hz)
        by_time = q_from_last_segments(points, round(FPS * WINDOW_S))
        by_arc = q_from_last_segments(points, round((len(points) - 1) * ARC_FRACTION))
        results[hz] = (by_time, by_arc)
        expected_time = qx_continuous(WINDOW_S * hz)
        expected_arc = qx_continuous(ARC_FRACTION)
        assert abs(by_time[0] - expected_time) < 2e-5
        assert abs(by_arc[0] - expected_arc) < 2e-5
        print(f'{hz} Hz: Q_time={by_time}, Q_last_30pct_arc={by_arc}')

    q1, a1 = results[1]
    q2, a2 = results[2]
    assert abs(q1[0] - q2[0]) > 0.14
    assert abs(a1[0] - a2[0]) < 2e-5
    # Mapeo de tres bandas propuesto: g_x=0.2+0.4*Q_x.
    print(f'Diferencia de g_x por cadencia, ventana temporal: {0.4 * abs(q1[0] - q2[0]):.6f}')
    print(f'Diferencia de g_x por cadencia, ventana de arco: {0.4 * abs(a1[0] - a2[0]):.6f}')


if __name__ == '__main__':
    main()
