"""Mismo círculo, distinta cadencia: Q espacial vs directness de 300 ms.

Sólo biblioteca estándar sin argumentos. Con --harmocap-root se ejercita además
el FeatureExtractor real del checkout indicado (dependencias de HarMoCAP).
"""
from __future__ import annotations

import argparse
import json
import math
import subprocess
import sys
from pathlib import Path

FPS = 120
RADIUS = 0.04
WINDOW_S = 0.3
FREQUENCIES_HZ = (1.0, 2.0)


def path(frequency_hz: float):
    n = round(FPS / frequency_hz)
    return [(i / FPS, RADIUS * math.cos(2 * math.pi * frequency_hz * i / FPS),
             RADIUS * math.sin(2 * math.pi * frequency_hz * i / FPS))
            for i in range(n + 1)]


def q_and_directness(points, window_s):
    dxs = [b[1] - a[1] for a, b in zip(points, points[1:])]
    dys = [b[2] - a[2] for a, b in zip(points, points[1:])]
    ds = [math.hypot(dx, dy) for dx, dy in zip(dxs, dys)]
    length = sum(ds)
    q = [sum(d * (v / d) ** 2 for d, v in zip(ds, axis)) / length
         for axis in (dxs, dys)]
    t_last = points[-1][0]
    window = [p for p in points if t_last - p[0] <= window_s + 1e-10]
    chord = math.dist(window[0][1:], window[-1][1:])
    arc = sum(math.dist(a[1:], b[1:]) for a, b in zip(window, window[1:]))
    return q, chord / arc, len(window)


BASE_POSE = {
    0: (.50, .18), 1: (.48, .165), 2: (.52, .165),
    3: (.46, .18), 4: (.54, .18), 5: (.40, .34), 6: (.60, .34),
    7: (.37, .48), 8: (.63, .48), 9: (.36, .61), 10: (.64, .61),
    11: (.425, .62), 12: (.575, .62), 13: (.43, .78), 14: (.57, .78),
    15: (.435, .95), 16: (.565, .95),
}


def actual_harmocap(frequency_hz: float, root: Path):
    sys.path.insert(0, str(root / "src"))
    import yaml
    from harmocap.features import CalibrationManager, FeatureExtractor
    from harmocap.schema import FEATURE_ORDER, KpState

    cfg = yaml.safe_load((root / "configs/features.yaml").read_text())
    calib = CalibrationManager(cfg["calibration"]["fallback"],
                               period_ms=60_000)
    extractor = FeatureExtractor(cfg["windows"], calib)
    k = FEATURE_ORDER.index("laban_space_proxy")
    for t, x, y in path(frequency_hz):
        pose = []
        for i in range(17):
            px, py = BASE_POSE[i]
            if i == 9:
                px, py = .35 + x, .60 + y
            elif i == 10:
                px, py = .65 + x, .60 + y
            pose.append((px, py, .9, int(KpState.OBSERVED), 0, 0))
        values, states = extractor.extract(pose, round(t * 1_000_000))
    assert states[k] == int(KpState.OBSERVED)
    return values[k]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--harmocap-root", type=Path)
    args = parser.parse_args()
    result = {"fixture": "one full wrist circle per condition",
              "fps_synthetic": FPS, "window_s": WINDOW_S,
              "frequency_conditions": []}
    if args.harmocap_root:
        root = args.harmocap_root.resolve()
        result["harmocap_sha"] = subprocess.check_output(
            ["git", "-C", str(root), "rev-parse", "HEAD"], text=True).strip()
    for frequency in FREQUENCIES_HZ:
        points = path(frequency)
        q, directness, n_window = q_and_directness(points, WINDOW_S)
        _, by_cycle, n_cycle = q_and_directness(points, 0.3 / frequency)
        phi = math.pi * frequency * WINDOW_S
        row = {"frequency_hz": frequency, "duration_s": 1 / frequency,
               "q_by_arc_xy": q, "directness_300ms_discrete": directness,
               "directness_300ms_continuous": abs(math.sin(phi) / phi),
               "window_samples": n_window,
               "directness_30pct_cycle_discrete": by_cycle,
               "cycle_fraction_samples": n_cycle}
        assert all(abs(value - 0.5) < 1e-12 for value in q)
        if args.harmocap_root:
            row["harmocap_laban_space_proxy"] = actual_harmocap(frequency, root)
            assert abs(row["harmocap_laban_space_proxy"] - directness) < 1e-6
        result["frequency_conditions"].append(row)
    slow, fast = result["frequency_conditions"]
    assert slow["directness_300ms_discrete"] - fast["directness_300ms_discrete"] > 0.3
    assert abs(slow["directness_30pct_cycle_discrete"] -
               fast["directness_30pct_cycle_discrete"]) < 0.001
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
