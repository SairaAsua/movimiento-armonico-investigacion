"""Sensibilidad hipotética del gate de C en dos cuadros CMU consecutivos.

Perturba sólo la orientación proyectada, no la trayectoria en sala ni la
posición del torso. No estima distribución de errores de cámaras reales.
"""

import numpy as np

from cmu_causal_c_replay import (
    FPS, MIN_ARC_PER_REGION, MIN_SEGMENTS_PER_REGION, body_trajectories,
)
from cmu_orientacion_sensibilidad import rotate

SEED = 20260924
REPLICATES = 1000
FRAME_START = 408
FRAME_STOP = 530  # exclusivo: cuadros 408..529
RMS_DEGREES = (0.25, 0.5, 1.0, 2.0)


def unit_error(rng, mode, frames):
    z = rng.normal(size=(REPLICATES, frames, 3)) / np.sqrt(3)
    if mode == "constant":
        return np.broadcast_to(z[:, :1], z.shape)
    if mode == "independent":
        return z
    if mode == "rho_0.95":
        out = np.empty_like(z)
        out[:, 0] = z[:, 0]
        for i in range(1, frames):
            out[:, i] = 0.95 * out[:, i - 1] + np.sqrt(1 - 0.95**2) * z[:, i]
        return out
    raise ValueError(mode)


def window_result(x):
    """x: (réplicas, 121 cuadros, xyz). Cada ventana tiene 120 tramos."""
    assert x.shape[1] == FPS + 1
    dx = np.diff(x, axis=1)
    ds = np.linalg.norm(dx, axis=2)
    front = (x[:, :-1, 2] + x[:, 1:, 2]) / 2 >= 0
    arcs = []
    counts = []
    speeds = []
    for mask in (front, ~front):
        arc = np.sum(np.where(mask, ds, 0), axis=1)
        count = np.sum(mask, axis=1)
        numerator = np.sum(np.where(mask, ds**2 * FPS, 0), axis=1)
        speed = np.divide(numerator, arc, out=np.full_like(arc, np.nan), where=arc > 0)
        arcs.append(arc)
        counts.append(count)
        speeds.append(speed)
    valid = (np.minimum(arcs[0], arcs[1]) >= MIN_ARC_PER_REGION) & (
        np.minimum(counts[0], counts[1]) >= MIN_SEGMENTS_PER_REGION
    )
    c = np.where(valid, speeds[0] - speeds[1], np.nan)
    return valid, c, arcs


def both_windows(x):
    return window_result(x[:, :121]), window_result(x[:, 1:])


def main():
    scale, trajectories = body_trajectories()  # incluye verificación SHA-256
    x = trajectories["izq"][FRAME_START:FRAME_STOP]
    assert x.shape == (122, 3)
    baseline_528, baseline_529 = both_windows(x[None, :, :])
    assert not baseline_528[0][0] and baseline_529[0][0]
    print(f'CMU 05_02 izquierda, escala causal {scale:.3f} mm, W=1 s, '
          f'gate {MIN_ARC_PER_REGION} L y {MIN_SEGMENTS_PER_REGION} tramos por región')
    print(f'baseline: cuadro 528 inválido; cuadro 529 C={baseline_529[1][0]:+.6f} L/s, '
          f'arco frontal={baseline_529[2][0][0]:.6f} L')
    rng = np.random.default_rng(SEED)
    for mode in ("independent", "rho_0.95", "constant"):
        field = unit_error(rng, mode, len(x))
        for degrees in RMS_DEGREES:
            perturbed = rotate(x, field * np.deg2rad(degrees))
            first, second = both_windows(perturbed)
            valid_528, valid_529 = first[0], second[0]
            valid_c = second[1][valid_529]
            q = np.percentile(valid_c, (5, 50, 95)) if len(valid_c) else (np.nan,)*3
            print(f'{mode:11s} {degrees:.2f}deg: '
                  f'528 válido={np.mean(valid_528):.1%}, '
                  f'529 válido={np.mean(valid_529):.1%}, '
                  f'528válido→529inválido={np.mean(valid_528 & ~valid_529):.1%}, '
                  f'C529 condicional p5/med/p95={q[0]:+.3f}/{q[1]:+.3f}/{q[2]:+.3f} L/s')


if __name__ == '__main__':
    main()
