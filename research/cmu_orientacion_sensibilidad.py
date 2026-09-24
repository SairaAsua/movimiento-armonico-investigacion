"""Sensibilidad de C a error hipotético de orientación del torso en CMU 05_02.

Perturba sólo la orientación usada para proyectar la mano. No estima el error
real de marcadores ni de las cámaras de Saira. Requiere numpy y ezc3d.
"""

import numpy as np

from cmu_causal_c_replay import body_trajectories, FPS
from cmu_danza_05_02_audit import contrast


SEED = 20260924
REPLICATES = 200
RMS_DEGREES = (0.25, 0.5, 1.0, 2.0)
MODES = ('independent', 'rho_0.95', 'constant')


def errors(rng, frames, mode):
    """Vectores de rotación con E[||omega||²]=1 rad², antes de escalar."""
    z = rng.normal(size=(REPLICATES, frames, 3)) / np.sqrt(3)
    if mode == 'independent':
        return z
    if mode == 'constant':
        return np.broadcast_to(z[:, :1, :], z.shape)
    if mode == 'rho_0.95':
        rho = 0.95
        correlated = np.empty_like(z)
        correlated[:, 0] = z[:, 0]
        for t in range(1, frames):
            correlated[:, t] = rho * correlated[:, t - 1] + np.sqrt(1-rho*rho) * z[:, t]
        return correlated
    raise ValueError(mode)


def rotate(vectors, omega):
    """Rodrigues exacto de cada vector corporal con eje-ángulo omega."""
    theta = np.linalg.norm(omega, axis=-1)
    sin_over_theta = np.sinc(theta / np.pi)
    one_minus_cos_over_theta2 = np.empty_like(theta)
    np.divide(1 - np.cos(theta), theta * theta, out=one_minus_cos_over_theta2,
              where=theta > 1e-8)
    one_minus_cos_over_theta2[theta <= 1e-8] = 0.5
    cross1 = np.cross(omega, vectors[None, :, :])
    rotated = (vectors[None, :, :] + sin_over_theta[..., None] * cross1 +
               one_minus_cos_over_theta2[..., None] * np.cross(omega, cross1))
    assert np.allclose(np.linalg.norm(rotated, axis=-1),
                       np.linalg.norm(vectors, axis=-1)[None, :], atol=1e-10)
    return rotated


def contrast_many(x):
    dx = np.diff(x, axis=1)
    ds = np.linalg.norm(dx, axis=-1)
    front = (x[:, :-1, 2] + x[:, 1:, 2]) / 2 >= 0
    means = []
    for mask in (front, ~front):
        arc = np.sum(np.where(mask, ds, 0), axis=1)
        if np.any(arc <= 0):
            raise ValueError('Una región quedó sin recorrido')
        means.append(np.sum(np.where(mask, ds ** 2 * FPS, 0), axis=1) / arc)
    return means[0] - means[1]


def main():
    scale, paths = body_trajectories()
    rng = np.random.default_rng(SEED)
    print(f'fuente=CMU_05_02 escala_primer_1s={scale:.3f}mm seed={SEED} replicas={REPLICATES}')
    for side, x in paths.items():
        base, _ = contrast(x, FPS)
        print(f'{side} C_base={base:+.3f}L/s')
        for mode in MODES:
            unit_error = errors(rng, len(x), mode)
            for degrees in RMS_DEGREES:
                simulated = rotate(x, unit_error * np.deg2rad(degrees))
                c = contrast_many(simulated)
                low, med, high = np.percentile(c, (5, 50, 95))
                print(f'  {mode} rms={degrees:.2f}deg '
                      f'C_p5/med/p95={low:+.3f}/{med:+.3f}/{high:+.3f}L/s '
                      f'signo_opuesto={np.mean(np.sign(c) != np.sign(base)):.1%} '
                      f'desvio_absoluto_med={np.median(np.abs(c-base)):.3f}L/s')


if __name__ == '__main__':
    main()
