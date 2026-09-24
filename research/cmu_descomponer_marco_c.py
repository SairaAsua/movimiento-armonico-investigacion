"""Descompone exactamente el incremento de muñeca en un marco corporal variable.

CMU 05_02 es danza sin soga. Esta identidad algebraica no estima un mecanismo
causal ni un error de cámara. Requiere numpy y ezc3d.
"""

import hashlib

import ezc3d
import numpy as np

from cmu_causal_c_replay import CALIBRATION_FRAMES, FPS, body_trajectories
from cmu_danza_05_02_audit import EXPECTED_SHA256, REQUIRED, SOURCE, contrast_deltas


def source_geometry():
    assert hashlib.sha256(SOURCE.read_bytes()).hexdigest() == EXPECTED_SHA256
    c = ezc3d.c3d(str(SOURCE))
    p = c['parameters']['POINT']
    assert float(p['RATE']['value'][0]) == FPS and p['UNITS']['value'][0] == 'mm'
    xyz = c['data']['points'][:3]
    residual = c['data']['meta_points']['residuals'][0]
    labels = [s.split(':')[-1] for s in p['LABELS']['value'] + p['LABELS2']['value']]
    ids = {name: labels.index(name) for name in REQUIRED}
    for name, index in ids.items():
        if not np.all((residual[index] >= 0) & np.all(np.isfinite(xyz[:, index, :]), axis=0)):
            raise ValueError(f'marcador inválido: {name}')

    def marker(name):
        return xyz[:, ids[name], :].T

    sl, sr = marker('LSHO'), marker('RSHO')
    waist = (marker('LFWT') + marker('RFWT')) / 2
    shoulder = (sl + sr) / 2
    span = np.linalg.norm(sl - sr, axis=1)
    scale = float(np.median(span[:CALIBRATION_FRAMES]))
    lateral = (sl - sr) / span[:, None]
    up = shoulder - waist
    up -= np.sum(up * lateral, axis=1)[:, None] * lateral
    if np.min(np.linalg.norm(up, axis=1)) < 50:
        raise ValueError('marco degenerado')
    up /= np.linalg.norm(up, axis=1)[:, None]
    front = np.cross(lateral, up)
    if np.min(np.sum((marker('STRN') - marker('RBAC')) * front, axis=1)) <= 0:
        raise ValueError('frente inválido')
    axes = np.stack((lateral, up, front), axis=2)
    result = {}
    for side, names in (("izq", ("LWRA", "LWRB")), ("der", ("RWRA", "RWRB"))):
        wrist = (marker(names[0]) + marker(names[1])) / 2
        result[side] = (wrist - waist) / scale
    return axes, result


def mean_c(delta, front, frame_ids=None):
    if frame_ids is not None:
        delta, front = delta[frame_ids], front[frame_ids]
    c, regional = contrast_deltas(delta, front, FPS)
    return c, regional


def describe(label, dx, frame_component, relative_component, front, frame_ids):
    speed = np.linalg.norm(dx, axis=1) * FPS
    frame_speed = np.linalg.norm(frame_component, axis=1) * FPS
    relative_speed = np.linalg.norm(relative_component, axis=1) * FPS
    ids = frame_ids
    c_total, reg_total = mean_c(dx, front, ids)
    c_relative, _ = mean_c(relative_component, front, ids)
    c_frame, _ = mean_c(frame_component, front, ids)
    print(f'{label}: C_co={c_total:+.6f} C_relativo_en_ejes_actuales={c_relative:+.6f} '
          f'C_solo_marco={c_frame:+.6f} L/s')
    print(f'  rapidez mediana/p90 co={np.median(speed[ids]):.3f}/{np.percentile(speed[ids],90):.3f}, '
          f'solo_marco={np.median(frame_speed[ids]):.3f}/{np.percentile(frame_speed[ids],90):.3f}, '
          f'relativo={np.median(relative_speed[ids]):.3f}/{np.percentile(relative_speed[ids],90):.3f} L/s')
    print(f'  tramos ||solo_marco|| > 0,5 ||co||: '
          f'{np.mean(frame_speed[ids] > 0.5 * speed[ids]):.1%}; '
          f'arco frente/atrás co={reg_total[0][1]:.3f}/{reg_total[1][1]:.3f} L')


def main():
    axes, relative_world = source_geometry()
    scale, body_from_replay = body_trajectories()
    print(f'CMU 05_02, SHA-256={EXPECTED_SHA256}, escala causal={scale:.3f} mm')
    for side, r in relative_world.items():
        body = np.einsum('tij,ti->tj', axes, r)
        assert np.allclose(body, body_from_replay[side], atol=1e-12)
        total = np.diff(body, axis=0)
        relative = np.einsum('tij,ti->tj', axes[1:], np.diff(r, axis=0))
        frame = np.einsum('tij,ti->tj', axes[1:] - axes[:-1], r[:-1])
        assert np.allclose(total, relative + frame, atol=1e-12)
        # La norma no es aditiva: el término cruzado puede sumar o cancelar.
        assert np.allclose(np.sum(total**2, axis=1),
                           np.sum(relative**2, axis=1) + np.sum(frame**2, axis=1)
                           + 2 * np.sum(relative * frame, axis=1), atol=1e-12)
        front = (body[:-1, 2] + body[1:, 2]) / 2
        print(side)
        describe('toma completa', total, frame, relative, front, np.arange(len(total)))
        # Los tramos de la ventana (t−1 s, t] para la primera emisión válida
        # del exportador de contrato: llegada j=410..529, índices delta j−1.
        describe('ventana cuadro 529', total, frame, relative, front, np.arange(409, 529))


if __name__ == '__main__':
    main()
