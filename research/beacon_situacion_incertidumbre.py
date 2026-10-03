#!/usr/bin/env python3
"""Propaga cotas geométricas hipotéticas al mapeo numérico Beacon.

No estima error de cámara, renderiza audio ni modela discriminación humana.
"""

from __future__ import annotations

import json

from beacon_situacion_controles import situation_controls
from laban_hit_factorial_sintetico import trajectory
from laban_hit_situacion_factorial import REACH, SITUATIONS, shift_lateral
from situacion_error_sintetico import interval_for_normalized_radius
from situacion_recorrido_sintetica import describe


def mapped_intervals(metrics: dict, segments: int, delta: float,
                     reach_bound: float = 0.0) -> dict[str, list[float]]:
    """Intervalos conservadores de g7/g8 bajo error duro simultáneo.

    La cota de V_r usa L_observado <= max(L_verdadero, L_observado),
    por lo que no necesita conocer la longitud verdadera.
    """
    rho_lo, rho_hi = interval_for_normalized_radius(
        metrics["rho_min"], REACH, delta, reach_bound)
    v = metrics["radial_variation_over_path_length"]
    length = metrics["path_length"]
    if segments < 1 or length <= 0:
        raise ValueError("polilínea no degenerada requerida")
    v_error = min(1.0, 6.0 * segments * delta / length)
    v_lo, v_hi = max(0.0, v - v_error), min(1.0, v + v_error)
    return {
        "g7": [situation_controls(rho_lo, 0.0)[0],
               situation_controls(rho_hi, 0.0)[0]],
        "g8": [situation_controls(0.0, v_lo)[1],
               situation_controls(0.0, v_hi)[1]],
        "V_r_error_bound": v_error,
    }


def disjoint(a: list[float], b: list[float]) -> bool:
    return a[1] < b[0] or b[1] < a[0]


def main() -> None:
    points, _ = trajectory("lateral_anterior", "locked")
    metrics = {
        name: describe(shift_lateral(points, offset), (0.0, 0.0, 0.0), REACH)
        for name, offset in SITUATIONS.items()
    }
    cases = []
    for delta in (0.01, 0.31):  # unidades geométricas construidas; no píxeles ni mm
        intervals = {name: mapped_intervals(metric, len(points) - 1, delta)
                     for name, metric in metrics.items()}
        a, b = (intervals[name] for name in SITUATIONS)
        result = {
            "delta_absolute_hypothetical": delta,
            "intervals": intervals,
            "g7_disjoint": disjoint(a["g7"], b["g7"]),
            "g8_disjoint": disjoint(a["g8"], b["g8"]),
        }
        cases.append(result)
    assert cases[0]["g7_disjoint"] and not cases[0]["g8_disjoint"]
    assert not cases[1]["g7_disjoint"] and not cases[1]["g8_disjoint"]
    assert all(c["intervals"][name]["V_r_error_bound"] == 1.0
               for c in cases for name in SITUATIONS)
    print(json.dumps({"kind": "synthetic_control_interval_bounds_no_audio",
                      "reach_absolute": REACH,
                      "segments": len(points) - 1,
                      "metrics": metrics,
                      "cases": cases}, indent=2))


if __name__ == "__main__":
    main()
