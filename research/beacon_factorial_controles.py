"""Fixture numérico de controles para el contrato real de beacon-spatial.

No ejecuta Weaver, OSC, SuperCollider ni audio. Las ganancias son un mapeo
diagnóstico propuesto, no una calibración perceptual o fisiológica.
"""

import hashlib
import json
from math import isclose
from pathlib import Path

from laban_hit_factorial_sintetico import arc_weighted_q, relative_phase_r, trajectory

HERE = Path(__file__).resolve().parent
CONTRACT = HERE / "sources/beacon_spatial.contract.de2768c3.json"
EXPECTED_SHA256 = "84383e254cd19f520eb5e19c7d6dedb0af93c95ad8b226aeb4c7694bde936dbb"
BANDS = (4, 5, 6)


def control_vector(q, r):
    # Dos componentes de Q determinan la tercera porque suma uno.
    spatial = (0.0, 0.0) if q is None else (0.2 + 0.8 * q[1], 0.2 + 0.8 * q[2])
    temporal = 0.0 if r is None else 0.2 + 0.8 * r
    return (*spatial, temporal)


def main():
    raw = CONTRACT.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == EXPECTED_SHA256
    contract = json.loads(raw)
    assert contract["instrument"]["instrument_id"] == "beacon-spatial"
    gain = next(c for c in contract["capabilities"] if c["name"] == "band_gain")
    lower, upper = gain["arguments"][0]["range"]
    n_lower, n_upper = gain["parameters"]["N"]["bounds"]
    assert gain["address_pattern"] == "/beacon/gain/{N}"
    assert all(n_lower <= band <= n_upper for band in BANDS)
    assert lower <= 0 <= upper

    results = {}
    for plane in ("lateral_anterior", "lateral_vertical"):
        for timing in ("locked", "drift"):
            points, phases = trajectory(plane, timing)
            q, _ = arc_weighted_q(points)
            r = relative_phase_r(phases)
            controls = control_vector(q, r)
            assert all(lower <= number <= upper for number in controls)
            results[(plane, timing)] = controls
            print(f'{plane:18s} {timing:6s} '
                  + ' '.join(f'/beacon/gain/{band}={number:.6f}'
                             for band, number in zip(BANDS, controls)))

    # Cambiar plano afecta sólo bandas 4/5; cambiar fase afecta sólo banda 6.
    for timing in ("locked", "drift"):
        a = results[("lateral_anterior", timing)]
        b = results[("lateral_vertical", timing)]
        assert a[:2] != b[:2] and abs(a[2] - b[2]) < 1e-12
    for plane in ("lateral_anterior", "lateral_vertical"):
        a = results[(plane, "locked")]
        b = results[(plane, "drift")]
        assert all(abs(x - y) < 1e-12 for x, y in zip(a[:2], b[:2]))
        assert abs(a[2] - b[2]) > 0.4
    assert len(set(results.values())) == 4
    q_demo = (0.5, 0.5, 0.0)
    assert control_vector(None, 1.0) == (0.0, 0.0, 1.0)
    partial = control_vector(q_demo, None)
    assert all(isclose(a, b, abs_tol=1e-12) for a, b in zip(partial, (0.6, 0.2, 0.0)))
    assert control_vector(None, None) == (0.0, 0.0, 0.0)
    print('Q invalid → bandas 4/5=0; R invalid → banda 6=0; ambos invalid → 4/5/6=0')
    print('OK: cuatro vectores únicos dentro del contrato; sin prueba de audio')


if __name__ == '__main__':
    main()
