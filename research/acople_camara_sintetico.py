"""Sensibilidad de un descriptor proyectado a FPS, escala, ruido y cuadros perdidos.

Escenarios inventados; no representan los equipos de Saira ni a Nico.
"""

import math
import random
import statistics


EPS = 0.5
F_CYCLE = 2.0  # Hz hipoteticos
DURATION = 3.0  # segundos, seis vueltas
REPS = 120


def points(fps, radius, sign, sigma, dropout, rng, dropout_mode='uniform'):
    n = int(round(DURATION * fps))
    out = []
    for i in range(n + 1):
        t = i / fps
        q = 2 * math.pi * F_CYCLE * t
        theta = q + sign * EPS * math.sin(q)
        if dropout_mode == 'accent_region':
            # Oclusion concentrada en el hemisferio donde esta el acento rapido.
            missing_probability = dropout if sign * math.cos(theta) > 0.5 and sign * math.cos(q) > 0 else 0
        else:
            missing_probability = dropout
        if rng.random() < missing_probability:
            out.append(None)
        else:
            out.append((radius * math.cos(theta) + rng.gauss(0, sigma),
                        radius * math.sin(theta) + rng.gauss(0, sigma)))
    return out


def contrast_projected(pts, fps, radius):
    sums = [[0.0, 0.0], [0.0, 0.0]]  # [sum(ds*speed), sum(ds)]
    kept = 0
    for p0, p1 in zip(pts, pts[1:]):
        if p0 is None or p1 is None:
            continue  # No unir un hueco con velocidad inventada.
        ds = math.hypot(p1[0] - p0[0], p1[1] - p0[1])
        if ds == 0:
            continue
        side = 0 if (p0[0] + p1[0]) / 2 >= 0 else 1
        sums[side][0] += ds * ds * fps
        sums[side][1] += ds
        kept += 1
    if not all(s[1] for s in sums):
        return math.nan, kept / (len(pts) - 1)
    front = sums[0][0] / sums[0][1]
    rear = sums[1][0] / sums[1][1]
    return (front - rear) / radius, kept / (len(pts) - 1)


def scenario(fps, radius, sigma, dropout, dropout_mode='uniform'):
    rng = random.Random(20260924)
    ideal = {}
    estimates = {+1: [], -1: []}
    coverage = []
    for sign in (+1, -1):
        ideal[sign] = contrast_projected(
            points(fps, radius, sign, 0, 0, random.Random(0)), fps, radius
        )[0]
        for _ in range(REPS):
            value, kept = contrast_projected(
                points(fps, radius, sign, sigma, dropout, rng, dropout_mode), fps, radius
            )
            if math.isfinite(value):
                estimates[sign].append(value)
            coverage.append(kept)
    signs_correct = sum(1 for sign in (+1, -1) for v in estimates[sign] if sign * v > 0)
    total = sum(map(len, estimates.values()))
    mean_abs_error = statistics.mean(abs(v - ideal[sign])
                                     for sign in (+1, -1) for v in estimates[sign])
    return ideal, estimates, mean_abs_error, signs_correct / total, statistics.mean(coverage)


def main():
    print('fps  radius_px  sigma_px  dropout  mode           ideal_A/B  mean_A/B  MAE  sign_ok  kept')
    for fps, radius, sigma, dropout, mode in [
        (30, 50, 1, 0, 'uniform'), (60, 50, 1, 0, 'uniform'), (120, 50, 1, 0, 'uniform'),
        (30, 15, 2, 0.1, 'uniform'), (60, 15, 2, 0.1, 'uniform'), (120, 15, 2, 0.1, 'uniform'),
        (60, 50, 1, 0.1, 'uniform'), (60, 50, 1, 0.4, 'accent_region'),
    ]:
        ideal, est, mae, sign_ok, kept = scenario(fps, radius, sigma, dropout, mode)
        print(f'{fps:3d} {radius:10d} {sigma:9d} {dropout:8.1f} {mode:14s} '
              f'{ideal[+1]:+.2f}/{ideal[-1]:+.2f} '
              f'{statistics.mean(est[+1]):+.2f}/{statistics.mean(est[-1]):+.2f} '
              f'{mae:.2f} {sign_ok:.2f} {kept:.2f}')


if __name__ == '__main__':
    main()
