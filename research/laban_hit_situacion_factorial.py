#!/usr/bin/env python3
"""Control sintético 2×2×2: plano Q, situación radial y fase R separables.

Reutiliza la ley temporal del factorial Laban–HIT; ninguna curva es rope flow.
"""

from __future__ import annotations

import json
import math

from laban_hit_factorial_sintetico import relative_phase_r, trajectory
from situacion_recorrido_sintetica import describe


PLANES = ("lateral_anterior", "lateral_vertical")
TIMINGS = ("locked", "drift")
SITUATIONS = {"circle_about_origin": 0.0, "circle_shifted_lateral": 0.6}
REACH = 2.0  # unidad geométrica declarada, no alcance de una persona


def shift_lateral(points: list[tuple[float, float, float]], offset: float):
    return [(x + offset, y, z) for x, y, z in points]


def main() -> None:
    rows = []
    for plane in PLANES:
        for timing in TIMINGS:
            base, phases = trajectory(plane, timing)
            phase_r = relative_phase_r(phases)
            for situation, offset in SITUATIONS.items():
                points = shift_lateral(base, offset)
                if offset:
                    assert max(abs(math.dist(a, b) - math.dist(c, d))
                               for a, b, c, d in zip(base, base[1:],
                                                      points, points[1:])) < 1e-12
                metric = describe(points, (0.0, 0.0, 0.0), REACH)
                rows.append({"plane": plane, "timing": timing,
                             "situation": situation, "Q": metric["Q"],
                             "rho_min": metric["rho_min"],
                             "rho_max": metric["rho_max"],
                             "V_r": metric["radial_variation_over_path_length"],
                             "R_1to1": round(phase_r, 6),
                             "length": metric["path_length"]})
    def row(plane, timing, situation):
        return next(r for r in rows if (r["plane"], r["timing"], r["situation"])
                    == (plane, timing, situation))
    for plane in PLANES:
        for timing in TIMINGS:
            a = row(plane, timing, "circle_about_origin")
            b = row(plane, timing, "circle_shifted_lateral")
            assert a["Q"] == b["Q"] and a["R_1to1"] == b["R_1to1"]
            assert a["length"] == b["length"]
            assert abs(a["rho_min"] - b["rho_min"]) > 0.2
        for situation in SITUATIONS:
            a = row(plane, "locked", situation)
            b = row(plane, "drift", situation)
            assert max(abs(x - y) for x, y in zip(a["Q"], b["Q"])) < 0.0001
            assert abs(a["rho_min"] - b["rho_min"]) < 0.001
            assert a["R_1to1"] > 0.999 and b["R_1to1"] < 0.6
    for timing in TIMINGS:
        for situation in SITUATIONS:
            a = row("lateral_anterior", timing, situation)
            b = row("lateral_vertical", timing, situation)
            assert a["R_1to1"] == b["R_1to1"]
            assert abs(a["rho_min"] - b["rho_min"]) < 0.001
            assert max(abs(x - y) for x, y in zip(a["Q"], b["Q"])) > 0.4
    print(json.dumps({"kind": "synthetic_geometry_and_constructed_phase_only",
                      "reach": REACH, "factorial": rows}, indent=2))


if __name__ == "__main__":
    main()
