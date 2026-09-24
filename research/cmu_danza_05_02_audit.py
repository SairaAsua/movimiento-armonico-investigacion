"""Audita una toma C3D publica de CMU sin llamar a sus marcadores articulaciones.

Requiere numpy y ezc3d. Entrada por defecto: sources/cmu_mocap/05_02.c3d.
"""

import hashlib
from pathlib import Path

import ezc3d
import numpy as np


HERE = Path(__file__).resolve().parent
SOURCE = HERE / 'sources/cmu_mocap/05_02.c3d'
EXPECTED_SHA256 = '04bb9be74cd9183eb9f873b26c6eb4dbbf613747af5d6d0ef41f146b859d51d7'
REQUIRED = ('LSHO', 'RSHO', 'LFWT', 'RFWT', 'LWRA', 'LWRB', 'RWRA', 'RWRB', 'STRN', 'RBAC')


def contrast(x, fps):
    # x: coordenada de un punto respecto al torso en longitudes de hombro.
    dx = np.diff(x, axis=0)
    midpoint_front = (x[:-1, 2] + x[1:, 2]) / 2
    return contrast_deltas(dx, midpoint_front, fps)


def contrast_deltas(dx, midpoint_front, fps):
    # Misma clasificación regional; sólo cambia la definición de desplazamiento.
    ds = np.linalg.norm(dx, axis=1)
    results = []
    for mask in (midpoint_front >= 0, midpoint_front < 0):
        total_arc = float(np.sum(ds[mask]))
        if total_arc <= 0:
            raise ValueError('Una region no tiene recorrido valido')
        mean_speed_arc = float(np.sum(ds[mask] ** 2 * fps) / total_arc)
        results.append((mean_speed_arc, total_arc, int(np.sum(mask))))
    return results[0][0] - results[1][0], results


def plane_q(dx):
    # Componentes laterales, superiores y anteriores en el marco declarado.
    ds = np.linalg.norm(dx, axis=1)
    valid = ds > 0
    if not np.any(valid):
        raise ValueError('Sin recorrido para Q')
    q = np.sum((dx[valid] ** 2) / ds[valid, None], axis=0) / np.sum(ds[valid])
    assert np.isclose(np.sum(q), 1, atol=1e-10)
    return q


def radial_turns(x):
    # Giro firmado del radio muñeca-cintura en el plano lateral/anterior.
    side, front = x[:, 0], x[:, 2]
    radius = np.hypot(side, front)
    if np.min(radius) <= 0.2:
        raise ValueError('Radio proyectado cercano al origen: giro no identificable')
    increments = np.arctan2(side[:-1] * front[1:] - front[:-1] * side[1:],
                            side[:-1] * side[1:] + front[:-1] * front[1:])
    if np.max(np.abs(increments)) >= np.pi:
        raise ValueError('Salto angular ambiguo entre cuadros')
    return (float(np.sum(increments) / (2 * np.pi)),
            float(np.sum(increments[increments > 0]) / (2 * np.pi)),
            float(-np.sum(increments[increments < 0]) / (2 * np.pi)))


def main():
    raw = SOURCE.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == EXPECTED_SHA256
    c = ezc3d.c3d(str(SOURCE))
    point = c['parameters']['POINT']
    fps = float(point['RATE']['value'][0])
    units = point['UNITS']['value'][0]
    xyz = c['data']['points'][:3]
    residual = c['data']['meta_points']['residuals'][0]
    labels = [s.split(':')[-1] for s in point['LABELS']['value'] + point['LABELS2']['value']]
    assert len(labels) == xyz.shape[1]
    assert fps == 120 and units == 'mm' and xyz.shape[2] == 1123
    assert len(set(labels)) == len(labels)
    indices = {name: labels.index(name) for name in REQUIRED}
    valid = np.ones(xyz.shape[2], dtype=bool)
    for name, i in indices.items():
        valid &= (residual[i] >= 0) & np.all(np.isfinite(xyz[:, i, :]), axis=0)
    # Este cálculo exige todos los cuadros de la toma; no rellena huecos.
    if not np.all(valid):
        raise ValueError(f'{np.sum(~valid)} cuadros sin todos los marcadores requeridos')

    def marker(name):
        return xyz[:, indices[name], :].T

    shoulder_l, shoulder_r = marker('LSHO'), marker('RSHO')
    waist_l, waist_r = marker('LFWT'), marker('RFWT')
    shoulder_mid = (shoulder_l + shoulder_r) / 2
    waist_mid = (waist_l + waist_r) / 2
    shoulder_span = np.linalg.norm(shoulder_l - shoulder_r, axis=1)
    scale = float(np.median(shoulder_span))
    lateral = shoulder_l - shoulder_r
    lateral /= np.linalg.norm(lateral, axis=1)[:, None]
    up = shoulder_mid - waist_mid
    up -= np.sum(up * lateral, axis=1)[:, None] * lateral
    up_len = np.linalg.norm(up, axis=1)
    if np.min(up_len) < 50:  # mm, solo guarda contra degeneracion evidente de esta toma.
        raise ValueError('Eje superior degenerado')
    up /= up_len[:, None]
    front = np.cross(lateral, up)
    sternum_back = np.sum((marker('STRN') - marker('RBAC')) * front, axis=1)
    if np.min(sternum_back) <= 0:
        raise ValueError('La convencion de frente no coincide con esternon-espalda')

    print(f'archivo={SOURCE.name} sha256={EXPECTED_SHA256} ezc3d={ezc3d.__version__}')
    print(f'frames={xyz.shape[2]} fps_archivo={fps:.0f} duracion_entre_primer_y_ultimo={(xyz.shape[2]-1)/fps:.3f}s unidades={units}')
    print(f'marcadores_requeridos={len(REQUIRED)} cobertura_residual={np.mean(valid):.3f}')
    print(f'escala_mediana_hombros={scale:.1f}mm rango={np.min(shoulder_span):.1f}..{np.max(shoulder_span):.1f}mm')
    print(f'esternon_menos_espalda_proyeccion_frente={np.min(sternum_back):.1f}..{np.max(sternum_back):.1f}mm')

    for side, a, b in [('izq', 'LWRA', 'LWRB'), ('der', 'RWRA', 'RWRB')]:
        wrist_markers_mid = (marker(a) + marker(b)) / 2
        rel = (wrist_markers_mid - waist_mid) / scale
        body = np.stack((np.sum(rel * lateral, axis=1),
                         np.sum(rel * up, axis=1),
                         np.sum(rel * front, axis=1)), axis=1)
        world_path = float(np.sum(np.linalg.norm(np.diff(wrist_markers_mid, axis=0), axis=1)) / scale)
        body_path = float(np.sum(np.linalg.norm(np.diff(body, axis=0), axis=1)))
        cvalue, regional = contrast(body, fps)
        print(f'{side}: recorrido_marcadores_sala={world_path:.2f}L '
              f'recorrido_relativo_torso={body_path:.2f}L '
              f'C_frente_menos_atras={cvalue:.3f}L/s')
        print(f'  frente: rapidez_arco={regional[0][0]:.3f}L/s '
              f'longitud={regional[0][1]:.2f}L tramos={regional[0][2]}; '
              f'atras: rapidez_arco={regional[1][0]:.3f}L/s '
              f'longitud={regional[1][1]:.2f}L tramos={regional[1][2]}')
        world_dx = np.diff(wrist_markers_mid, axis=0) / scale
        world_in_body_axes = np.stack((np.sum(world_dx * lateral[:-1], axis=1),
                                       np.sum(world_dx * up[:-1], axis=1),
                                       np.sum(world_dx * front[:-1], axis=1)), axis=1)
        q_world = plane_q(world_in_body_axes)
        q_body = plane_q(np.diff(body, axis=0))
        print('  Q_sala_reexpresada=' + '/'.join(f'{v:.3f}' for v in q_world) +
              ' Q_relativo_torso=' + '/'.join(f'{v:.3f}' for v in q_body) +
              ' (lateral/superior/anterior)')
        region = (body[:-1, 2] + body[1:, 2]) / 2
        delta_corotating = np.diff(body, axis=0)
        delta_translation_only = np.diff(wrist_markers_mid - waist_mid, axis=0) / scale
        delta_world = np.diff(wrist_markers_mid, axis=0) / scale
        c_waist_centered, _ = contrast_deltas(delta_translation_only, region, fps)
        c_world, _ = contrast_deltas(delta_world, region, fps)
        speeds_co = np.linalg.norm(delta_corotating, axis=1) * fps
        speeds_tr = np.linalg.norm(delta_translation_only, axis=1) * fps
        print(f'  C_marcos: co_rotante={cvalue:.3f} '
              f'cintura_centrada_sin_corregir_giro={c_waist_centered:.3f} '
              f'sala={c_world:.3f}L/s '
              f'diferencia_abs_rapidez_co_vs_cintura mediana/p90='
              f'{np.median(np.abs(speeds_co-speeds_tr)):.3f}/'
              f'{np.percentile(np.abs(speeds_co-speeds_tr), 90):.3f}L/s')
        reversed_body = body[::-1]
        reversed_c, _ = contrast(reversed_body, fps)
        reversed_q = plane_q(np.diff(reversed_body, axis=0))
        turns = radial_turns(body)
        reversed_turns = radial_turns(reversed_body)
        assert np.isclose(reversed_c, cvalue, atol=1e-10)
        assert np.allclose(reversed_q, q_body, atol=1e-10)
        assert np.allclose(reversed_turns,
                           (-turns[0], turns[2], turns[1]), atol=1e-10)
        print(f'  reversa: C={reversed_c:.3f}L/s Q_igual={np.allclose(reversed_q, q_body)} '
              f'giro_radial_neto={turns[0]:+.3f}->{reversed_turns[0]:+.3f} vueltas '
              f'positivo/negativo={turns[1]:.3f}/{turns[2]:.3f} vueltas')
        for stride in (2, 4, 8, 16):
            c_by_offset = [contrast(body[offset::stride], fps / stride)[0]
                           for offset in range(stride)]
            print(f'  C_stride_{stride}: min/mediana/max=' +
                  '/'.join(f'{v:.3f}' for v in
                           (min(c_by_offset), float(np.median(c_by_offset)), max(c_by_offset))) + 'L/s')
        virtual_name = 'LWR0' if side == 'izq' else 'RWR0'
        virtual = xyz[:3, labels.index(virtual_name), :].T
        virtual_rel = (virtual - waist_mid) / scale
        virtual_body = np.stack((np.sum(virtual_rel * lateral, axis=1),
                                 np.sum(virtual_rel * up, axis=1),
                                 np.sum(virtual_rel * front, axis=1)), axis=1)
        virtual_c, _ = contrast(virtual_body, fps)
        separation_mm = np.linalg.norm(virtual - wrist_markers_mid, axis=1)
        print(f'  sensibilidad_{virtual_name}: C={virtual_c:.3f}L/s '
              f'separacion_mediana_marcadores={np.median(separation_mm):.1f}mm')


if __name__ == '__main__':
    main()
