"""Presupuesto idealizado de triangulación estéreo; no usa videos humanos.

Ejecutar: python estereo_sintetico.py
Biblioteca estándar. Dos cámaras pinhole paralelas, rectificadas y sincronizadas.
No modela calibración, oclusión, lente, rolling shutter ni identidad de puntos.
"""

from math import acos, cos, degrees, sin, sqrt
from random import Random
from statistics import mean, median


def project(point, camera_x, focal_px):
    x, y, z = point
    return focal_px * (x - camera_x) / z, focal_px * y / z


def triangulate(left, right, baseline_m, focal_px):
    disparity = left[0] - right[0]
    if disparity <= 0:
        return None
    z = focal_px * baseline_m / disparity
    return (left[0] * z / focal_px, (left[1] + right[1]) * z / (2 * focal_px), z)


def angle_error(a, b):
    an = sqrt(sum(x * x for x in a))
    bn = sqrt(sum(x * x for x in b))
    value = sum(x * y for x, y in zip(a, b)) / (an * bn)
    return degrees(acos(max(-1.0, min(1.0, value))))


def quantile(values, fraction):
    ordered = sorted(values)
    return ordered[int(fraction * (len(ordered) - 1))]


def simulate(baseline_m, focal_px=1200, depth_m=3.0, noise_px=1.0,
             movement_m=0.15, trials=20_000):
    rng = Random(1729)
    p0 = (0.0, 0.0, depth_m)
    # Un desplazamiento lateral y uno en profundidad, de igual longitud.
    cases = {
        "lateral": (movement_m, 0.0, depth_m),
        "profundidad": (0.0, 0.0, depth_m + movement_m),
    }
    depth_errors = []
    angle_errors = {key: [] for key in cases}

    def observed(point):
        left = project(point, 0.0, focal_px)
        right = project(point, baseline_m, focal_px)
        left_noisy = tuple(v + rng.gauss(0, noise_px) for v in left)
        right_noisy = tuple(v + rng.gauss(0, noise_px) for v in right)
        return triangulate(left_noisy, right_noisy, baseline_m, focal_px)

    for _ in range(trials):
        start = observed(p0)
        if start is None:
            continue
        depth_errors.append(start[2] - depth_m)
        for key, p1 in cases.items():
            end = observed(p1)
            if end is None:
                continue
            truth = tuple(y - x for x, y in zip(p0, p1))
            estimate = tuple(y - x for x, y in zip(start, end))
            angle_errors[key].append(angle_error(truth, estimate))

    theoretical_depth_sd = sqrt(2) * noise_px * depth_m**2 / (focal_px * baseline_m)
    average_depth_error = mean(depth_errors)
    empirical_depth_sd = sqrt(mean((v - average_depth_error) ** 2 for v in depth_errors))
    return {
        "baseline_m": baseline_m,
        "disparity_px": focal_px * baseline_m / depth_m,
        "depth_sd_linear_m": theoretical_depth_sd,
        "depth_sd_mc_m": empirical_depth_sd,
        "depth_bias_mc_m": average_depth_error,
        "angle_lateral_median_deg": median(angle_errors["lateral"]),
        "angle_lateral_p95_deg": quantile(angle_errors["lateral"], 0.95),
        "angle_depth_median_deg": median(angle_errors["profundidad"]),
        "angle_depth_p95_deg": quantile(angle_errors["profundidad"], 0.95),
    }


def asynchronous_lateral_point(baseline_m, speed_m_s, offset_s,
                               depth_m=3.0, focal_px=1200):
    """Triangula erróneamente un móvil visto a t y t+offset_s.

    El objeto avanza a velocidad constante paralela a la línea base y está
    a profundidad fija. No hay ruido de píxel: aísla sólo el sesgo temporal.
    """
    p_left_time = (0.0, 0.0, depth_m)
    p_right_time = (speed_m_s * offset_s, 0.0, depth_m)
    estimate = triangulate(project(p_left_time, 0, focal_px),
                           project(p_right_time, baseline_m, focal_px),
                           baseline_m, focal_px)
    if speed_m_s * offset_s >= baseline_m:
        assert estimate is None
        return None
    expected_z = depth_m * baseline_m / (baseline_m - speed_m_s * offset_s)
    assert estimate is not None and abs(estimate[2] - expected_z) < 1e-10
    return estimate[2] - depth_m


if __name__ == "__main__":
    focal_px = 1200
    depth_m = 3.0
    noise_px = 1.0
    movement_m = 0.15
    print("Supuestos: f=1200 px; Z=3 m; sigma por coordenada=1 px; tramo=0,15 m; 20 000 ensayos.")
    print("B(m) d(px) sd_Z_lin(cm) sd_Z_MC(cm) bias_Z_MC(cm) lateral_med/p95(°) profundidad_med/p95(°)")
    for baseline_m in (0.25, 0.75, 1.5):
        r = simulate(baseline_m, focal_px, depth_m, noise_px, movement_m)
        print(f"{baseline_m:4.2f} {r['disparity_px']:5.1f} "
              f"{100*r['depth_sd_linear_m']:12.2f} {100*r['depth_sd_mc_m']:11.2f} "
              f"{100*r['depth_bias_mc_m']:13.2f} "
              f"{r['angle_lateral_median_deg']:6.1f}/{r['angle_lateral_p95_deg']:4.1f} "
              f"{r['angle_depth_median_deg']:6.1f}/{r['angle_depth_p95_deg']:4.1f}")

    # Identidades geométricas y caso sin ruido: pruebas de la implementación.
    for baseline_m in (0.25, 0.75, 1.5):
        point = (0.18, -0.11, 3.2)
        recovered = triangulate(project(point, 0, focal_px),
                                project(point, baseline_m, focal_px),
                                baseline_m, focal_px)
        assert recovered is not None
        assert max(abs(a - b) for a, b in zip(point, recovered)) < 1e-12

    print("Desfase ilustrativo: velocidad lateral=2 m/s; offset=10 ms; Z real=3 m; ruido=0 px.")
    for baseline_m in (0.25, 0.75, 1.5):
        bias = asynchronous_lateral_point(baseline_m, 2.0, 0.010)
        print(f"B={baseline_m:.2f} m: sesgo de profundidad={100*bias:.2f} cm")
    assert asynchronous_lateral_point(0.25, 2.0, 0.0) == 0
