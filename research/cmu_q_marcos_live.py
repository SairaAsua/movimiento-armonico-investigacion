"""Compara Q causal co-rotante y Q de desplazamiento relativo sin giro del marco.

CMU 05_02 es danza sin soga; no mide el error del sistema de Saira.
"""

import numpy as np

from cmu_causal_c_replay import CALIBRATION_FRAMES, FPS, body_trajectories
from cmu_descomponer_marco_c import source_geometry
from cmu_q_live_replay import MIN_ARC_L, estimate, replay, segments


def window_values(deltas, window_frames):
    """Cada resultado usa sólo deltas de llegada ya disponibles."""
    results = []
    for j in range(CALIBRATION_FRAMES, len(deltas) + 1):
        start = max(CALIBRATION_FRAMES, j - window_frames + 1)
        items = []
        for k in range(start, j + 1):
            d = deltas[k - 1]
            ds = float(np.linalg.norm(d))
            if ds > 0:
                items.append((k, ds, np.outer(d, d) / ds))
        results.append((j, estimate(items, min_arc=MIN_ARC_L)))
    return results


def main():
    axes, relative_world = source_geometry()
    scale, body = body_trajectories()
    print(f'CMU 05_02, escala_primer_1s={scale:.3f}mm, '
          f'fps_nominal={FPS}, arco_minimo={MIN_ARC_L}L')
    for side, r in relative_world.items():
        co = np.diff(body[side], axis=0)
        physical_relative = np.einsum('tij,ti->tj', axes[1:], np.diff(r, axis=0))
        frame = np.einsum('tij,ti->tj', axes[1:] - axes[:-1], r[:-1])
        assert np.allclose(co, physical_relative + frame, atol=1e-12)
        for seconds in (0.5, 1.0, 2.0):
            frames = round(seconds * FPS)
            co_out = window_values(co, frames)
            rel_out = window_values(physical_relative, frames)
            independent = replay(list(segments(body[side])), frames)
            assert [j for j, _ in co_out] == [j for j, _ in independent]
            for (_, a), (_, b) in zip(co_out, independent):
                assert (a is None) == (b is None)
                if a is not None:
                    assert np.allclose(a[0], b[0], rtol=0, atol=1e-12)
            assert [j for j, _ in co_out] == [j for j, _ in rel_out]
            co_valid = sum(a is not None for _, a in co_out)
            rel_valid = sum(b is not None for _, b in rel_out)
            both = [(a[0], b[0]) for (_, a), (_, b) in zip(co_out, rel_out)
                    if a is not None and b is not None]
            distances = np.array([np.sum(np.abs(a - b)) for a, b in both])
            print(f'{side} W={seconds:.1f}s '
                  f'co={co_valid}/{len(co_out)} rel={rel_valid}/{len(rel_out)} '
                  f'ambos={len(both)} '
                  f'|delta_Q|_1 mediana/p90/max='
                  f'{np.median(distances):.3f}/'
                  f'{np.percentile(distances, 90):.3f}/'
                  f'{np.max(distances):.3f}')


if __name__ == '__main__':
    main()
