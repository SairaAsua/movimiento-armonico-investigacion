#!/usr/bin/env python3
"""Mapeo numérico offline Q/R/situación al contrato fijado de Beacon.

No ejecuta Weaver, OSC, DSP ni audio; los casos son curvas ideales.
"""

from __future__ import annotations

import hashlib
import json

from beacon_factorial_controles import (CONTRACT, EXPECTED_SHA256,
                                       control_vector as qr_controls)
from laban_hit_factorial_sintetico import relative_phase_r, trajectory
from laban_hit_situacion_factorial import (PLANES, REACH, SITUATIONS, TIMINGS,
                                           shift_lateral)
from situacion_recorrido_sintetica import describe


BANDS = (4, 5, 6, 7, 8)


def situation_controls(rho_min: float | None, v_radial: float | None) -> tuple[float, float]:
    if rho_min is None or v_radial is None:
        return (0.0, 0.0)  # Instrucción de reset, no medida de un cuerpo.
    if not (0 <= rho_min and 0 <= v_radial <= 1):
        raise ValueError("métricas de situación fuera de dominio")
    return (0.2 + 0.8 * rho_min / (1.0 + rho_min),
            0.2 + 0.8 * v_radial)


def control_vector(q: list[float] | None, r: float | None,
                   rho_min: float | None, v_radial: float | None) -> tuple[float, ...]:
    return (*qr_controls(q, r), *situation_controls(rho_min, v_radial))


def main() -> None:
    raw = CONTRACT.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == EXPECTED_SHA256
    contract = json.loads(raw)
    assert contract["instrument"]["instrument_id"] == "beacon-spatial"
    gain = next(c for c in contract["capabilities"] if c["name"] == "band_gain")
    lo, hi = gain["arguments"][0]["range"]
    n_lo, n_hi = gain["parameters"]["N"]["bounds"]
    assert gain["address_pattern"] == "/beacon/gain/{N}"
    assert all(n_lo <= band <= n_hi for band in BANDS)

    rows = []
    for plane in PLANES:
        for timing in TIMINGS:
            base, phases = trajectory(plane, timing)
            r = relative_phase_r(phases)
            for situation, offset in SITUATIONS.items():
                geometry = describe(shift_lateral(base, offset), (0.0, 0.0, 0.0), REACH)
                q = geometry["Q"]
                rho = geometry["rho_min"]
                v_radial = geometry["radial_variation_over_path_length"]
                controls = control_vector(q, r, rho, v_radial)
                assert all(lo <= value <= hi for value in controls)
                rows.append({"plane": plane, "timing": timing,
                             "situation": situation, "Q": q, "R_1to1": round(r, 6),
                             "rho_min": rho, "V_r": v_radial,
                             "gains_by_band": {str(b): round(v, 6)
                                               for b, v in zip(BANDS, controls)}})
    assert len(rows) == 8
    assert len({tuple(row["gains_by_band"].values()) for row in rows}) == 8
    def row(plane: str, timing: str, situation: str) -> dict:
        return next(item for item in rows if (item["plane"], item["timing"],
                        item["situation"]) == (plane, timing, situation))
    for plane in PLANES:
        for timing in TIMINGS:
            a = row(plane, timing, "circle_about_origin")["gains_by_band"]
            b = row(plane, timing, "circle_shifted_lateral")["gains_by_band"]
            assert all(a[str(band)] == b[str(band)] for band in (4, 5, 6))
            assert (a["7"], a["8"]) != (b["7"], b["8"])
    assert control_vector([0.5, 0.5, 0.0], 1.0, None, None)[3:] == (0.0, 0.0)
    assert control_vector(None, None, 0.5, 0.2)[:3] == (0.0, 0.0, 0.0)
    assert control_vector(None, None, None, None) == (0.0,) * 5
    print(json.dumps({"kind": "synthetic_controls_no_osc_no_audio",
                      "contract_sha256": EXPECTED_SHA256,
                      "band_addresses": [f"/beacon/gain/{b}" for b in BANDS],
                      "rho_mapping": "g7=0.2+0.8*rho_min/(1+rho_min)",
                      "radial_variation_mapping": "g8=0.2+0.8*V_r",
                      "invalid_layer_controls": [0.0, 0.0],
                      "cases": rows}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
