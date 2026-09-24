"""Control 2x2: plano de trayectoria y fase relativa son ejes distinguibles.

No simula rope flow real ni valida a Laban o HIT. Usa sólo biblioteca estándar.
"""

from math import cos, pi, sin, sqrt

CYCLES = 8
SAMPLES_PER_SECOND = 1000
TOTAL_SAMPLES = CYCLES * SAMPLES_PER_SECOND
PHASE_SWING_RAD = pi / 2


def trajectory(plane, timing):
    points = []
    phases = []
    for i in range(TOTAL_SAMPLES + 1):
        t = i / SAMPLES_PER_SECOND
        phase = 2 * pi * t
        if timing == "drift":
            phase += PHASE_SWING_RAD * sin(2 * pi * t / CYCLES)
        c, s = cos(phase), sin(phase)
        points.append((c, s, 0.0) if plane == "lateral_anterior" else (c, 0.0, s))
        phases.append(phase)
    return points, phases


def arc_weighted_q(points):
    arc = [0.0, 0.0, 0.0]
    total = 0.0
    for a, b in zip(points, points[1:]):
        d = [b[k] - a[k] for k in range(3)]
        ds = sqrt(sum(component * component for component in d))
        assert ds > 0
        total += ds
        for k in range(3):
            arc[k] += d[k] ** 2 / ds
    q = tuple(component / total for component in arc)
    assert abs(sum(q) - 1) < 1e-12
    return q, total


def relative_phase_r(right_phases):
    # Evaluar por tiempo, sin duplicar el punto final de la ventana periódica.
    re = im = 0.0
    for i, phase in enumerate(right_phases[:-1]):
        difference = phase - 2 * pi * i / SAMPLES_PER_SECOND
        re += cos(difference)
        im += sin(difference)
    return sqrt(re * re + im * im) / TOTAL_SAMPLES


def main():
    results = {}
    for plane in ("lateral_anterior", "lateral_vertical"):
        for timing in ("locked", "drift"):
            points, phases = trajectory(plane, timing)
            q, length = arc_weighted_q(points)
            r = relative_phase_r(phases)
            results[(plane, timing)] = q, r
            print(f'{plane:18s} {timing:6s} Q={tuple(round(x, 6) for x in q)} '
                  f'R_1:1={r:.6f} vueltas={CYCLES} recorrido={length:.6f}')
    for plane in ("lateral_anterior", "lateral_vertical"):
        locked = results[(plane, "locked")][0]
        drift = results[(plane, "drift")][0]
        assert max(abs(a - b) for a, b in zip(locked, drift)) < 0.0001
        assert results[(plane, "locked")][1] > 0.999999
        assert results[(plane, "drift")][1] < 0.6
    for timing in ("locked", "drift"):
        a = results[("lateral_anterior", timing)]
        b = results[("lateral_vertical", timing)]
        assert abs(a[1] - b[1]) < 1e-12
        assert max(abs(x - y) for x, y in zip(a[0], b[0])) > 0.4
    print('OK: los controles espaciales y temporales se cruzan sin confundirse')


if __name__ == '__main__':
    main()
