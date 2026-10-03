#!/usr/bin/env python3
"""Sensibilidad de situación del recorrido al origen corporal en CMU 05_02.

Compara centro de cintura con punto medio cintura-hombros en el mismo marco
co-rotante. Ambos son proxies geométricos, no centros anatómicos certificados.
"""

from __future__ import annotations

import json
import statistics

import ezc3d
import numpy as np

from cmu_causal_c_replay import body_trajectories
from cmu_danza_05_02_audit import EXPECTED_SHA256, SOURCE
from cmu_descomponer_marco_c import source_geometry
from cmu_situacion_marcos import FPS, WINDOW_INTERVALS, measure


def midtorso_shift(scale_mm: float) -> np.ndarray:
    """Origen medio entre centros de cintura/hombros, relativo a cintura."""
    c3d = ezc3d.c3d(str(SOURCE))
    xyz = c3d["data"]["points"][:3]
    p = c3d["parameters"]["POINT"]
    labels = [name.split(":")[-1] for name in p["LABELS"]["value"]
              + p["LABELS2"]["value"]]
    def marker(name: str) -> np.ndarray:
        return xyz[:, labels.index(name), :].T
    shoulders = (marker("LSHO") + marker("RSHO")) / 2
    waist = (marker("LFWT") + marker("RFWT")) / 2
    shift = (shoulders - waist) / (2 * scale_mm)
    if shift.shape != (1123, 3) or not np.all(np.isfinite(shift)):
        raise ValueError("Origen medio inválido")
    return shift


def main() -> None:
    axes, relative_waist = source_geometry()  # verifica hash y marcadores
    scale_mm, expected_body = body_trajectories()
    shift = midtorso_shift(scale_mm)
    shift_norm = np.linalg.norm(shift, axis=1)
    result = {
        "source": "CMU 05_02 C3D; danza sin soga",
        "source_sha256": EXPECTED_SHA256, "fps_nominal": FPS,
        "scale": "median shoulder span of first 120 frames, not anatomical reach",
        "shoulder_scale_first_second_mm": round(scale_mm, 3),
        "origin_shift_L_median": round(float(np.median(shift_norm)), 6),
        "origin_shift_L_max": round(float(np.max(shift_norm)), 6),
        "windows": "9 windows of 120 intervals, 0-9 s, shared endpoints",
        "sides": {},
    }
    for side, relative in relative_waist.items():
        waist_path = np.einsum("tij,ti->tj", axes, relative)
        middle_path = np.einsum("tij,ti->tj", axes, relative - shift)
        if not np.allclose(waist_path, expected_body[side], atol=1e-12):
            raise AssertionError("El origen cintura no coincide con el replay anterior")
        shift_body = np.einsum("tij,ti->tj", axes, shift)
        if (not np.allclose(waist_path - middle_path, shift_body, atol=1e-12)
                or not np.allclose(np.linalg.norm(shift_body, axis=1),
                                   shift_norm, atol=1e-12)):
            raise AssertionError("El cambio de origen no conserva la geometría")
        rows = []
        for start in range(0, 1080, WINDOW_INTERVALS):
            stop = start + WINDOW_INTERVALS
            waist = measure(waist_path[start:stop + 1])
            middle = measure(middle_path[start:stop + 1])
            local_shift = float(np.max(shift_norm[start:stop + 1]))
            rho_diff = abs(waist["rho_min"] - middle["rho_min"])
            if rho_diff > local_shift + 2e-6:  # margen por redondeo de métricas
                raise AssertionError("Se excedió la cota geométrica de cambio de origen")
            rows.append({"start_frame": start, "end_frame": stop,
                         "rho_min_waist_L": waist["rho_min"],
                         "rho_min_midtorso_L": middle["rho_min"],
                         "V_r_waist": waist["radial_variation_over_path_length"],
                         "V_r_midtorso": middle["radial_variation_over_path_length"],
                         "path_length_waist_L": waist["path_length"],
                         "path_length_midtorso_L": middle["path_length"],
                         "max_origin_shift_window_L": round(local_shift, 6)})
        rho_diffs = [abs(r["rho_min_waist_L"] - r["rho_min_midtorso_L"])
                     for r in rows]
        v_diffs = [abs(r["V_r_waist"] - r["V_r_midtorso"]) for r in rows]
        result["sides"][side] = {
            "window_count": len(rows),
            "median_abs_rho_min_difference_L": round(statistics.median(rho_diffs), 6),
            "max_abs_rho_min_difference_L": round(max(rho_diffs), 6),
            "median_abs_V_r_difference": round(statistics.median(v_diffs), 6),
            "max_abs_V_r_difference": round(max(v_diffs), 6),
            "rows": rows,
        }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
