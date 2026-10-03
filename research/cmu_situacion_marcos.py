#!/usr/bin/env python3
"""Sensibilidad de situación de recorrido a ejes móviles en CMU 05_02.

Banco externo de ingeniería: danza sin soga, no validación de Laban/Nico.
Requiere numpy, ezc3d y el C3D original verificado por source_geometry().
"""

from __future__ import annotations

import json
import statistics

import numpy as np

from cmu_descomponer_marco_c import source_geometry
from cmu_causal_c_replay import body_trajectories
from cmu_danza_05_02_audit import EXPECTED_SHA256
from situacion_recorrido_sintetica import describe


FPS = 120
WINDOW_INTERVALS = 120


def measure(path: np.ndarray) -> dict:
    # El archivo previo dividió mm por la mediana de hombros del primer segundo.
    # reach=1 aquí significa 1 ancho de hombros, NO alcance anatómico.
    return describe([tuple(map(float, row)) for row in path], (0.0, 0.0, 0.0), 1.0)


def main() -> None:
    axes, relative_world = source_geometry()
    scale_mm, reference_body = body_trajectories()
    if axes.shape != (1123, 3, 3):
        raise ValueError("Forma inesperada del marco CMU")
    result = {"source": "CMU 05_02 C3D, danza moderna sin soga",
              "source_sha256": EXPECTED_SHA256, "fps_nominal": FPS,
              "scale": "one median shoulder span from first 120 frames; not anatomical reach",
              "windows": "9 consecutive 120-interval windows; endpoints shared; final 42 frames excluded",
              "sides": {}}
    for side, relative in relative_world.items():
        # axes[t] tiene como columnas los tres ejes del torso en coordenadas sala.
        corotating = np.einsum("tij,ti->tj", axes, relative)
        fixed_axes = np.einsum("ij,ti->tj", axes[0], relative)
        if not np.allclose(corotating, reference_body[side], atol=1e-12):
            raise AssertionError("Marco co-rotante no coincide con replay CMU existente")
        if not np.allclose(np.linalg.norm(corotating, axis=1),
                           np.linalg.norm(fixed_axes, axis=1), atol=1e-12):
            raise AssertionError("Las rotaciones no conservaron radio por cuadro")
        rows = []
        for start in range(0, 1080, WINDOW_INTERVALS):
            stop = start + WINDOW_INTERVALS
            moving = measure(corotating[start:stop + 1])
            frozen = measure(fixed_axes[start:stop + 1])
            vertex_min_moving = float(np.min(np.linalg.norm(
                corotating[start:stop + 1], axis=1)))
            vertex_min_frozen = float(np.min(np.linalg.norm(
                fixed_axes[start:stop + 1], axis=1)))
            if abs(vertex_min_moving - vertex_min_frozen) > 1e-12:
                raise AssertionError("Radio mínimo en vértices debería ser invariante")
            rows.append({"start_frame": start, "end_frame": stop,
                         "rho_min_corotating_L": moving["rho_min"],
                         "rho_min_fixed_axes_L": frozen["rho_min"],
                         "V_r_corotating": moving["radial_variation_over_path_length"],
                         "V_r_fixed_axes": frozen["radial_variation_over_path_length"],
                         "path_length_corotating_L": moving["path_length"],
                         "path_length_fixed_axes_L": frozen["path_length"],
                         "Q_corotating": moving["Q"], "Q_fixed_axes": frozen["Q"]})
        v_diffs = [abs(r["V_r_corotating"] - r["V_r_fixed_axes"]) for r in rows]
        result["sides"][side] = {
            "window_count": len(rows),
            "median_abs_V_r_difference": round(statistics.median(v_diffs), 6),
            "max_abs_rho_min_difference_L": round(max(abs(
                r["rho_min_corotating_L"] - r["rho_min_fixed_axes_L"]) for r in rows), 6),
            "max_abs_V_r_difference": round(max(v_diffs), 6),
            "max_Q_L1_difference": round(max(sum(abs(a - b) for a, b in zip(
                r["Q_corotating"], r["Q_fixed_axes"])) for r in rows), 6),
            "rows": rows,
        }
    result["shoulder_scale_first_second_mm"] = round(scale_mm, 3)
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
