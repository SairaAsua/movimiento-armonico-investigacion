"""Replay causal del contraste espacial C sobre CMU 05_02; no es audio live.

Requiere numpy y ezc3d. Solo usa el archivo C3D local verificado por hash.
La escala se fija con los primeros 120 cuadros; cada emisión usa tramos ya recibidos.
"""

from collections import deque
from itertools import groupby

import ezc3d
import numpy as np

from cmu_danza_05_02_audit import EXPECTED_SHA256, REQUIRED, SOURCE
import hashlib


FPS = 120
CALIBRATION_FRAMES = 120
WINDOW_SECONDS = (0.5, 1.0, 2.0)
MIN_ARC_PER_REGION = 0.5  # longitudes de hombro; umbral exploratorio, no fisiológico
MIN_SEGMENTS_PER_REGION = 2
SENSITIVITY_ARCS = (0.1, 0.25, 0.5, 1.0)


def body_trajectories():
    assert hashlib.sha256(SOURCE.read_bytes()).hexdigest() == EXPECTED_SHA256
    c = ezc3d.c3d(str(SOURCE))
    p = c['parameters']['POINT']
    assert float(p['RATE']['value'][0]) == FPS
    assert p['UNITS']['value'][0] == 'mm'
    xyz = c['data']['points'][:3]
    residual = c['data']['meta_points']['residuals'][0]
    labels = [s.split(':')[-1] for s in p['LABELS']['value'] + p['LABELS2']['value']]
    assert len(labels) == xyz.shape[1] and xyz.shape[2] == 1123
    ids = {name: labels.index(name) for name in REQUIRED}
    for name, i in ids.items():
        if not np.all((residual[i] >= 0) & np.all(np.isfinite(xyz[:, i, :]), axis=0)):
            raise ValueError(f'Marcador inválido: {name}')

    def marker(name):
        return xyz[:, ids[name], :].T

    sl, sr = marker('LSHO'), marker('RSHO')
    wl, wr = marker('LFWT'), marker('RFWT')
    shoulder_mid, waist_mid = (sl + sr) / 2, (wl + wr) / 2
    span = np.linalg.norm(sl - sr, axis=1)
    scale = float(np.median(span[:CALIBRATION_FRAMES]))
    lateral = (sl - sr) / span[:, None]
    up = shoulder_mid - waist_mid
    up -= np.sum(up * lateral, axis=1)[:, None] * lateral
    if np.min(np.linalg.norm(up, axis=1)) < 50:
        raise ValueError('Marco corporal degenerado')
    up /= np.linalg.norm(up, axis=1)[:, None]
    front = np.cross(lateral, up)
    if np.min(np.sum((marker('STRN') - marker('RBAC')) * front, axis=1)) <= 0:
        raise ValueError('Convención de frente no válida')

    out = {}
    for side, a, b in [('izq', 'LWRA', 'LWRB'), ('der', 'RWRA', 'RWRB')]:
        rel = ((marker(a) + marker(b)) / 2 - waist_mid) / scale
        out[side] = np.stack([np.sum(rel * axis, axis=1)
                              for axis in (lateral, up, front)], axis=1)
    return scale, out


def segments(x):
    """Tramos al llegar cada cuadro; su región usa ambos extremos ya observados."""
    delta = np.diff(x, axis=0)
    ds = np.linalg.norm(delta, axis=1)
    front = (x[:-1, 2] + x[1:, 2]) / 2 >= 0
    # Cada tupla corresponde al cuadro de llegada j, empezando en j=120.
    return [(j, bool(front[j - 1]), float(ds[j - 1]), float(ds[j - 1] ** 2 * FPS))
            for j in range(CALIBRATION_FRAMES, len(x))]


def value(window, min_arc=MIN_ARC_PER_REGION):
    arcs = [0.0, 0.0]
    speed_numerators = [0.0, 0.0]
    counts = [0, 0]
    for _, front, ds, speed_num in window:
        k = int(front)
        arcs[k] += ds
        speed_numerators[k] += speed_num
        counts[k] += 1
    if min(arcs) < min_arc or min(counts) < MIN_SEGMENTS_PER_REGION:
        return None
    return speed_numerators[1] / arcs[1] - speed_numerators[0] / arcs[0]


def replay(items, window_frames, min_arc=MIN_ARC_PER_REGION):
    past = deque()
    emitted = []
    for item in items:
        j = item[0]
        past.append(item)
        # Ventana retrospectiva (t-W, t], en tiempos de llegada del archivo.
        while past and past[0][0] <= j - window_frames:
            past.popleft()
        causal = value(past, min_arc)
        # Cálculo independiente por lote de exactamente los mismos tramos.
        offline = value([s for s in items if j - window_frames < s[0] <= j], min_arc)
        assert causal == offline or (causal is not None and offline is not None and
                                     np.isclose(causal, offline, atol=1e-12))
        emitted.append((j, causal))
    return emitted


def main():
    scale, trajectories = body_trajectories()
    print(f'fuente=05_02.c3d sha256={EXPECTED_SHA256} fps={FPS} escala_primer_1s={scale:.3f}mm')
    print(f'calibracion=cuadros_0..{CALIBRATION_FRAMES-1} emisiones_desde_cuadro={CALIBRATION_FRAMES}')
    print(f'gate_arco_por_region={MIN_ARC_PER_REGION}L gate_tramos_por_region={MIN_SEGMENTS_PER_REGION}')
    for side, x in trajectories.items():
        items = segments(x)
        # Propiedad causal: truncar el futuro no altera emisiones anteriores.
        for cutoff in (2 * FPS, 5 * FPS, 8 * FPS):
            prefix = [s for s in items if s[0] <= cutoff]
            assert replay(prefix, FPS) == replay(items, FPS)[:len(prefix)]
        for seconds in WINDOW_SECONDS:
            output = replay(items, round(seconds * FPS))
            good = [(j, c) for j, c in output if c is not None]
            if seconds == 1.0:
                runs = [(valid, len(list(group)))
                        for valid, group in groupby(c is not None for _, c in output)]
                print(f'{side} W=1.0s rachas_validas_cuadros='
                      f'{[n for valid, n in runs if valid]} '
                      f'rachas_invalidas_cuadros={[n for valid, n in runs if not valid]}')
            if good:
                vals = np.array([c for _, c in good])
                print(f'{side} W={seconds:.1f}s validos={len(good)}/{len(output)} '
                      f'fraccion={len(good)/len(output):.3f} primero={good[0][0]/FPS:.3f}s '
                      f'C_min/mediana/max={np.min(vals):.3f}/{np.median(vals):.3f}/{np.max(vals):.3f}L/s')
            else:
                print(f'{side} W={seconds:.1f}s validos=0/{len(output)}')
        print(f'{side} sensibilidad W=1.0s, arco_minimo_por_region:')
        for min_arc in SENSITIVITY_ARCS:
            output = replay(items, FPS, min_arc)
            good = [c for _, c in output if c is not None]
            first = next((j / FPS for j, c in output if c is not None), None)
            first_text = f'{first:.3f}s' if first is not None else 'ninguna'
            print(f'  {min_arc:.2f}L: {len(good)}/{len(output)} '
                  f'({len(good)/len(output):.1%}), primera={first_text}')


if __name__ == '__main__':
    main()
