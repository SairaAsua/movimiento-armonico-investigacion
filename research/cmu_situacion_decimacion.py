#!/usr/bin/env python3
"""Sensibilidad de rho_min/V_r/Q al descarte de cuadros CMU 05_02.

No simula una cámara: no hay exposición, blur, compresión, pose 2D ni filtro
antialias. Sólo compara polilíneas construidas con menos muestras 3D.
"""

from __future__ import annotations

import json
import statistics

from cmu_causal_c_replay import FPS, body_trajectories
from cmu_danza_05_02_audit import EXPECTED_SHA256
from cmu_situacion_marcos import WINDOW_INTERVALS, measure


FACTORS = (2, 4, 5, 8, 10)  # 60, 30, 24, 15, 12 Hz nominales desde 120 Hz


def indices(start: int, stop: int, factor: int, phase: int) -> list[int]:
    """Conserva ambos extremos de la ventana e introduce una fase de grilla."""
    if factor < 1 or not 0 <= phase < factor or stop <= start:
        raise ValueError("Ventana, factor o fase inválidos")
    middle = [j for j in range(start + 1, stop)
              if (j - start - phase) % factor == 0]
    result = [start, *middle, stop]
    assert result[0] == start and result[-1] == stop
    assert len(result) == len(set(result))
    return result


def summarize(values: list[float]) -> dict:
    ordered = sorted(values)
    return {"comparisons": len(values), "min": round(ordered[0], 6),
            "median": round(statistics.median(values), 6),
            "max": round(ordered[-1], 6)}


def main() -> None:
    scale_mm, paths = body_trajectories()  # valida hash, unidades y marcadores
    result = {"source": "CMU 05_02 C3D; danza sin soga",
              "source_sha256": EXPECTED_SHA256,
              "source_fps": FPS,
              "scale": "median shoulder span in first 120 frames; not anatomical reach",
              "shoulder_scale_first_second_mm": round(scale_mm, 3),
              "windows": "nine fixed 120-interval windows; endpoints forced; all grid phases",
              "processing": "frame decimation without antialias, optical or pose model",
              "sides": {}}
    for side, path in paths.items():
        side_result = {}
        for factor in FACTORS:
            rho_delta, v_delta, q_l1 = [], [], []
            interior_counts = []
            for start in range(0, 1080, WINDOW_INTERVALS):
                stop = start + WINDOW_INTERVALS
                baseline = measure(path[start:stop + 1])
                for phase in range(factor):
                    sample_idx = indices(start, stop, factor, phase)
                    decimated = measure(path[sample_idx])
                    rho_delta.append(decimated["rho_min"] - baseline["rho_min"])
                    v_delta.append(decimated["radial_variation_over_path_length"]
                                   - baseline["radial_variation_over_path_length"])
                    q_l1.append(sum(abs(a - b) for a, b in zip(
                        decimated["Q"], baseline["Q"])))
                    interior_counts.append(len(sample_idx) - 2)
            expected = 9 * factor
            if not (len(rho_delta) == len(v_delta) == len(q_l1) == expected):
                raise AssertionError("No se recorrieron todas las ventanas/fases")
            side_result[str(FPS // factor)] = {
                "factor": factor, "grid_phase_comparisons": expected,
                "interior_points_min_max": [min(interior_counts), max(interior_counts)],
                "rho_min_signed_delta_L": summarize(rho_delta),
                "V_r_signed_delta": summarize(v_delta),
                "Q_L1_distance": summarize(q_l1),
            }
        result["sides"][side] = side_result
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
