"""Replay causal de Q de planos sobre CMU 05_02; no es captura ni audio live.

La entrada C3D, los marcadores, el marco y la escala se verifican en
cmu_causal_c_replay.body_trajectories(). Requiere numpy y ezc3d.
"""

from collections import deque

import numpy as np

from cmu_causal_c_replay import body_trajectories, CALIBRATION_FRAMES, FPS

WINDOW_SECONDS = (0.5, 1.0, 2.0)
MIN_ARC_L = 0.5  # Exploratorio; no es umbral de Laban ni de Nico.
MIN_SEGMENTS = 2


def segments(x):
    for j in range(CALIBRATION_FRAMES, len(x)):
        d = x[j] - x[j - 1]
        ds = float(np.linalg.norm(d))
        if ds > 0:
            yield (j, ds, np.outer(d, d) / ds)


def estimate(items, min_arc=MIN_ARC_L):
    if len(items) < MIN_SEGMENTS:
        return None
    arc = sum(s[1] for s in items)
    if arc < min_arc:
        return None
    moment = sum((s[2] for s in items), np.zeros((3, 3))) / arc
    q = np.diag(moment).copy()
    eig = np.linalg.eigvalsh(moment)
    assert np.all(q >= -1e-12) and np.isclose(q.sum(), 1, atol=1e-12)
    return q, eig, arc


def replay(items, frames):
    past = deque()
    output = []
    for item in items:
        j = item[0]
        past.append(item)
        while past and past[0][0] <= j - frames:
            past.popleft()
        current = estimate(past)
        reference = estimate([s for s in items if j - frames < s[0] <= j])
        assert (current is None) == (reference is None)
        if current is not None:
            for a, b in zip(current, reference):
                assert np.allclose(a, b, rtol=0, atol=1e-12)
        output.append((j, current))
    return output


def main():
    scale, trajectories = body_trajectories()
    print(f'fuente=CMU 05_02 C3D, escala_primer_1s={scale:.3f}mm '
          f'fps_nominal={FPS}; no timestamp óptico ni latencia medida')
    print(f'gate exploratorio: arco>={MIN_ARC_L}L, tramos>={MIN_SEGMENTS}')
    for side, x in trajectories.items():
        items = list(segments(x))
        for cutoff in (2 * FPS, 5 * FPS, 8 * FPS):
            prefix = [s for s in items if s[0] <= cutoff]
            earlier = replay(prefix, FPS)
            full = replay(items, FPS)[:len(prefix)]
            for (_, a), (_, b) in zip(earlier, full):
                assert (a is None) == (b is None)
                if a is not None:
                    assert all(np.allclose(v, w, atol=1e-12) for v, w in zip(a, b))
        for seconds in WINDOW_SECONDS:
            output = replay(items, round(seconds * FPS))
            valid = [(j, v) for j, v in output if v is not None]
            qs = np.array([v[0] for _, v in valid])
            eigenvalues = np.array([v[1] for _, v in valid])
            first = valid[0][0] / FPS if valid else None
            print(f'{side} W={seconds:.1f}s validos={len(valid)}/{len(output)} '
                  f'primero={first:.3f}s '
                  f'Q_media_lateral/superior/anterior='
                  f'{np.mean(qs, axis=0).round(3).tolist()} '
                  f'lambda_min/mid_mediana='
                  f'{np.median(eigenvalues[:, 0]):.3f}/'
                  f'{np.median(eigenvalues[:, 1]):.3f}')


if __name__ == '__main__':
    main()
