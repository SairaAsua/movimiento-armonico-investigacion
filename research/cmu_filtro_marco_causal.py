"""Ensayo causal de filtrado de orientación: jitter vs retardo en CMU 05_02.

El marco derivado de marcadores CMU es referencia interna, no verdad anatómica.
Requiere numpy y ezc3d; no acciona HarMoCAP ni Beacon.
"""

import hashlib

import ezc3d
import numpy as np

from cmu_causal_c_replay import CALIBRATION_FRAMES, FPS
from cmu_danza_05_02_audit import EXPECTED_SHA256, REQUIRED, SOURCE, contrast


SEED = 20260925
REPLICATES = 60
NOISE_RMS_DEG = 1.0
WINDOWS = (1, 3, 5, 9)


def load_geometry():
    assert hashlib.sha256(SOURCE.read_bytes()).hexdigest() == EXPECTED_SHA256
    c = ezc3d.c3d(str(SOURCE))
    p = c['parameters']['POINT']
    assert float(p['RATE']['value'][0]) == FPS and p['UNITS']['value'][0] == 'mm'
    xyz = c['data']['points'][:3]
    residual = c['data']['meta_points']['residuals'][0]
    labels = [s.split(':')[-1] for s in p['LABELS']['value'] + p['LABELS2']['value']]
    assert len(labels) == xyz.shape[1] and xyz.shape[2] == 1123
    ids = {name: labels.index(name) for name in REQUIRED}
    for name, i in ids.items():
        assert np.all((residual[i] >= 0) & np.all(np.isfinite(xyz[:, i, :]), axis=0)), name

    def marker(name):
        return xyz[:, ids[name], :].T

    sl, sr = marker('LSHO'), marker('RSHO')
    waist = (marker('LFWT') + marker('RFWT')) / 2
    shoulder_mid = (sl + sr) / 2
    span = np.linalg.norm(sl - sr, axis=1)
    scale = float(np.median(span[:CALIBRATION_FRAMES]))
    lateral = (sl - sr) / span[:, None]
    up = shoulder_mid - waist
    up -= np.sum(up * lateral, axis=1)[:, None] * lateral
    assert np.min(np.linalg.norm(up, axis=1)) > 50
    up /= np.linalg.norm(up, axis=1)[:, None]
    front = np.cross(lateral, up)
    assert np.min(np.sum((marker('STRN') - marker('RBAC')) * front, axis=1)) > 0
    frame = np.stack((lateral, up, front), axis=-1)  # columnas: ejes en sala
    assert np.allclose(np.linalg.det(frame), 1, atol=1e-10)
    rel = {}
    for side, a, b in [('izq', 'LWRA', 'LWRB'), ('der', 'RWRA', 'RWRB')]:
        rel[side] = ((marker(a) + marker(b)) / 2 - waist) / scale
    return scale, frame, rel


def noise_rotation(rng, frames):
    # Error isotrópico RMS 1° por cuadro, independiente, compartido por manos.
    omega = rng.normal(size=(REPLICATES, frames, 3)) * np.deg2rad(NOISE_RMS_DEG) / np.sqrt(3)
    angle = np.linalg.norm(omega, axis=-1)
    a = np.sinc(angle / np.pi)
    b = np.empty_like(angle)
    np.divide(1 - np.cos(angle), angle * angle, out=b, where=angle > 1e-8)
    b[angle <= 1e-8] = 0.5
    k = np.zeros((*omega.shape[:-1], 3, 3))
    x, y, z = np.moveaxis(omega, -1, 0)
    k[..., 0, 1], k[..., 0, 2] = -z, y
    k[..., 1, 0], k[..., 1, 2] = z, -x
    k[..., 2, 0], k[..., 2, 1] = -y, x
    rot = np.eye(3) + a[..., None, None] * k + b[..., None, None] * (k @ k)
    assert np.allclose(np.linalg.det(rot), 1, atol=1e-10)
    return rot


def causal_rotation_average(observed, width):
    # Media retrospectiva de matrices; proyección polar a SO(3). Sin cuadros futuros.
    cumul = np.concatenate((np.zeros_like(observed[..., :1, :, :]),
                            np.cumsum(observed, axis=-3)), axis=-3)
    ends = np.arange(1, observed.shape[-3] + 1)
    starts = np.maximum(0, ends - width)
    mean = (cumul[..., ends, :, :] - cumul[..., starts, :, :]) / (ends - starts)[..., None, None]
    u, _, vh = np.linalg.svd(mean)
    sign = np.linalg.det(u @ vh)
    correction = np.broadcast_to(np.eye(3), mean.shape).copy()
    correction[..., 2, 2] = sign
    return u @ correction @ vh


def angle_error_degrees(reference, estimated):
    cosine = (np.einsum('tij,...tij->...t', reference, estimated) - 1) / 2
    return np.rad2deg(np.arccos(np.clip(cosine, -1, 1)))


def contrast_many(paths):
    dx = np.diff(paths, axis=-2)
    ds = np.linalg.norm(dx, axis=-1)
    front = (paths[..., :-1, 2] + paths[..., 1:, 2]) / 2 >= 0
    means = []
    for mask in (front, ~front):
        arc = np.sum(np.where(mask, ds, 0), axis=-1)
        if np.any(arc <= 0):
            raise ValueError('Región vacía')
        means.append(np.sum(np.where(mask, ds * ds * FPS, 0), axis=-1) / arc)
    return means[0] - means[1]


def main():
    scale, frame, rel = load_geometry()
    rng = np.random.default_rng(SEED)
    noisy = frame[None] @ noise_rotation(rng, len(frame))
    # Truncar el futuro no debe alterar ningún marco ya emitido.
    for cutoff in (250, 600, 900):
        assert np.allclose(causal_rotation_average(noisy[:, :cutoff], 5),
                           causal_rotation_average(noisy, 5)[:, :cutoff], atol=1e-10)
    print(f'CMU_05_02 escala_primer_1s={scale:.3f}mm seed={SEED} replicas={REPLICATES} '
          f'error_independiente_rms={NOISE_RMS_DEG}deg fps={FPS}')
    baseline = {side: contrast(np.einsum('tij,ti->tj', frame, path), FPS)[0]
                for side, path in rel.items()}
    print('C_base ' + ' '.join(f'{s}={v:+.3f}L/s' for s, v in baseline.items()))
    for width in WINDOWS:
        clean_filtered = causal_rotation_average(frame, width)
        noisy_filtered = causal_rotation_average(noisy, width)
        assert np.allclose(np.linalg.det(noisy_filtered), 1, atol=1e-10)
        clean_angle = angle_error_degrees(frame, clean_filtered)
        noisy_angle = angle_error_degrees(frame, noisy_filtered)
        print(f'W={width}frames edad_media_muestras={(width-1)/(2*FPS)*1000:.1f}ms '
              f'angulo_solo_filtrar_p50/p90={np.percentile(clean_angle,50):.3f}/'
              f'{np.percentile(clean_angle,90):.3f}deg '
              f'angulo_ruido_filtrado_p50/p90={np.percentile(noisy_angle,50):.3f}/'
              f'{np.percentile(noisy_angle,90):.3f}deg')
        for side, path in rel.items():
            clean_path = np.einsum('tij,ti->tj', clean_filtered, path)
            noisy_paths = np.einsum('rtij,ti->rtj', noisy_filtered, path)
            clean_c, _ = contrast(clean_path, FPS)
            noisy_c = contrast_many(noisy_paths)
            lo, med, hi = np.percentile(noisy_c, (5, 50, 95))
            print(f'  {side} C_solo_filtrar={clean_c:+.3f}L/s '
                  f'C_ruido_filtrado_p5/med/p95={lo:+.3f}/{med:+.3f}/{hi:+.3f}L/s '
                  f'desvio_med_vs_base={np.median(np.abs(noisy_c-baseline[side])):.3f}L/s')


if __name__ == '__main__':
    main()
