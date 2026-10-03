#!/usr/bin/env python3
"""Casos sintéticos para el gate de calidad de situación del recorrido.

No son datos humanos ni estimaciones de cobertura de una cámara.
"""

import json
import math

from situacion_recorrido_sintetica import describe, describe_gated


def main() -> None:
    origin = (0.0, 0.0, 0.0)
    central = [(-1.0, 1.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 0.0)]
    peripheral = [(-1.0, 1.0, 0.0), (0.0, 1.0, 0.0), (1.0, 1.0, 0.0)]
    times = [0.0, 0.01, 0.02]

    valid = describe_gated(central, origin, 1.0, [True] * 3, times, 0.015)
    assert valid["status"] == "computed_candidate"
    assert valid["metrics"]["rho_min"] == 0.0

    # Si el punto central no fue observado, unir los extremos da otra curva.
    missing_center = describe_gated(central, origin, 1.0,
                                    [True, False, True], times, 0.015)
    naive_bridge = describe([central[0], central[2]], origin, 1.0)
    assert naive_bridge["rho_min"] == 1.0
    assert missing_center["reason"] == "missing_or_untrusted_sample"
    assert "metrics" not in missing_center

    # Una pose espuria en el origen fabrica centralidad en una frase periférica.
    spurious = [peripheral[0], origin, peripheral[2]]
    bad_pose = describe_gated(spurious, origin, 1.0,
                              [True, False, True], times, 0.015)
    assert describe(peripheral, origin, 1.0)["rho_min"] == 1.0
    assert describe(spurious, origin, 1.0)["rho_min"] == 0.0
    assert bad_pose["reason"] == "missing_or_untrusted_sample"
    assert "metrics" not in bad_pose

    cases = {
        "complete": valid,
        "untrusted_center": missing_center,
        "untrusted_spurious_pose": bad_pose,
        "large_pts_gap": describe_gated(central, origin, 1.0,
                                        [True] * 3, [0.0, 0.01, 0.03], 0.015),
        "nonmonotonic_pts": describe_gated(central, origin, 1.0,
                                           [True] * 3, [0.0, 0.02, 0.01], 0.015),
        "nonfinite_pts": describe_gated(central, origin, 1.0,
                                        [True] * 3, [0.0, math.nan, 0.02], 0.015),
        "nonfinite_pose": describe_gated([central[0], (math.nan, 0.0, 0.0),
                                          central[2]], origin, 1.0,
                                         [True] * 3, times, 0.015),
        "stationary": describe_gated([origin] * 3, origin, 1.0,
                                     [True] * 3, times, 0.015),
    }
    expected = {"large_pts_gap": "temporal_gap",
                "nonmonotonic_pts": "nonmonotonic_timestamp",
                "nonfinite_pts": "nonfinite_timestamp",
                "nonfinite_pose": "invalid_geometry",
                "stationary": "invalid_geometry"}
    for name, reason in expected.items():
        assert cases[name]["status"] == "invalid"
        assert cases[name]["reason"] == reason
        assert "metrics" not in cases[name]
    print(json.dumps({"kind": "synthetic_quality_gate_only",
                      "naive_bridge_rho_min": naive_bridge["rho_min"],
                      "naive_spurious_rho_min": describe(spurious, origin, 1.0)["rho_min"],
                      "cases": cases}, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
