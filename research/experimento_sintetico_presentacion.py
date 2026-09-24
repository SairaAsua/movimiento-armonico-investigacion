#!/usr/bin/env python3
"""Fixture reproducible de geometría, fase y sonificación diagnóstica.

No simula biomecánica, belleza, gasto metabólico ni conciencia.
"""

from __future__ import annotations

import csv
import hashlib
import json
import math
import struct
import wave
from pathlib import Path

ROOT = Path(__file__).resolve().parent / "datos_sinteticos_presentacion"
FPS = 30
SECONDS = 8
N = FPS * SECONDS
SWING = 1.8


def state(plane: str, opposed: bool, t: float):
    cycle = min(int(t), SECONDS - 1)
    u = t - cycle
    swing_l = SWING if cycle % 2 == 0 else -SWING
    swing_r = -swing_l if opposed else swing_l
    theta_l = 2 * math.pi * t + swing_l * math.sin(math.pi * u) ** 2
    theta_r = 2 * math.pi * t + swing_r * math.sin(math.pi * u) ** 2
    left = (math.cos(theta_l), math.sin(theta_l), 0.0)
    right = (math.cos(theta_r), math.sin(theta_r), 0.0) if plane == "lateral_anterior" else (math.cos(theta_r), 0.0, math.sin(theta_r))
    vel_l = 2 * math.pi + swing_l * math.pi * math.sin(2 * math.pi * u)
    vel_r = 2 * math.pi + swing_r * math.pi * math.sin(2 * math.pi * u)
    return left, right, theta_l, theta_r, vel_l, vel_r


def q_arc(points):
    accum = [0.0, 0.0, 0.0]
    length = 0.0
    for a, b in zip(points[:-1], points[1:]):
        delta = [b[k] - a[k] for k in range(3)]
        ds = math.sqrt(sum(d * d for d in delta))
        if ds:
            length += ds
            for k in range(3):
                accum[k] += delta[k] ** 2 / ds
    return [x / length for x in accum], length


def r_phase(rows):
    z = sum(complex(math.cos(r["delta_rad"]), math.sin(r["delta_rad"])) for r in rows)
    return abs(z) / len(rows)


def make_audio(path: Path, rows: list[dict], plane: str):
    """Two separate diagnostic channels: plane colour and phase deviation.

    Left has a steady tone selected by plane; right is frequency-modulated by
    instantaneous phase difference. This is a fixture, not Beacon audio.
    """
    sample_rate = 22050
    plane_hz = 220 if plane == "lateral_anterior" else 294
    samples = bytearray()
    phase_r = 0.0
    for i in range(sample_rate * SECONDS):
        t = i / sample_rate
        row = rows[min(int(t * FPS), len(rows) - 1)]
        deviation = (1 - math.cos(row["delta_rad"])) / 2
        right_hz = 330 + 90 * deviation
        phase_r += 2 * math.pi * right_hz / sample_rate
        fade = min(1.0, t / 0.04, (SECONDS - t) / 0.04)
        left = int(11000 * fade * math.sin(2 * math.pi * plane_hz * t))
        right = int(11000 * fade * math.sin(phase_r))
        samples.extend(struct.pack("<hh", left, right))
    with wave.open(str(path), "wb") as wav:
        wav.setnchannels(2)
        wav.setsampwidth(2)
        wav.setframerate(sample_rate)
        wav.writeframes(samples)


def main():
    ROOT.mkdir(exist_ok=True)
    results = []
    all_rows = []
    for plane in ("lateral_anterior", "lateral_vertical"):
        for opposed in (False, True):
            condition = f"{plane}__{'opposed' if opposed else 'aligned'}"
            rows = []
            for frame in range(N):
                t = frame / FPS
                left, right, theta_l, theta_r, vl, vr = state(plane, opposed, t)
                row = {"condition": condition, "frame": frame, "t_s": t,
                       "left_x": left[0], "left_y": left[1], "left_z": left[2],
                       "right_x": right[0], "right_y": right[1], "right_z": right[2],
                       "theta_left_rad": theta_l, "theta_right_rad": theta_r,
                       "speed_left_rad_s": vl, "speed_right_rad_s": vr,
                       "delta_rad": theta_r - theta_l,
                       "event_only_delta_rad": 0.0}
                rows.append(row)
            # Close the path for arc integration, without adding a data frame.
            _, end_right, *_ = state(plane, opposed, SECONDS)
            q, length = q_arc([(r["right_x"], r["right_y"], r["right_z"]) for r in rows] + [end_right])
            r = r_phase(rows)
            make_audio(ROOT / f"{condition}.wav", rows, plane)
            results.append({"condition": condition, "plane": plane,
                            "timing": "opposed" if opposed else "aligned",
                            "frames": N, "Q_lateral": q[0], "Q_anterior": q[1],
                            "Q_vertical": q[2], "R_continuous": r,
                            "R_event_only": 1.0, "path_length": length,
                            "audio": f"{condition}.wav"})
            all_rows.extend(rows)
    csv_path = ROOT / "trayectorias.csv"
    with csv_path.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(all_rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(all_rows)
    by = {r["condition"]: r for r in results}
    for plane in ("lateral_anterior", "lateral_vertical"):
        a = by[f"{plane}__aligned"]
        b = by[f"{plane}__opposed"]
        assert abs(a["R_continuous"] - 1) < 1e-12
        assert 0 < b["R_continuous"] < 0.2
        assert max(abs(a[k] - b[k]) for k in ("Q_lateral", "Q_anterior", "Q_vertical")) < 1e-12
        assert abs(a["path_length"] - b["path_length"]) < 1e-12
    for timing in ("aligned", "opposed"):
        a = by[f"lateral_anterior__{timing}"]
        b = by[f"lateral_vertical__{timing}"]
        assert abs(a["R_continuous"] - b["R_continuous"]) < 1e-12
        assert abs(a["Q_vertical"] - b["Q_vertical"]) > 0.4
    assert len(all_rows) == 960
    # Adversarial control: concentration alone cannot rank a phase relation.
    # A perfectly stable anti-phase has the same R as perfect in-phase.
    anti_phase = [math.pi] * N
    in_phase = [0.0] * N
    uniform = [2 * math.pi * k / N for k in range(N)]
    def concentration(deltas):
        return abs(sum(complex(math.cos(d), math.sin(d)) for d in deltas)) / len(deltas)
    negative_controls = {
        "in_phase": {"R": concentration(in_phase), "mean_delta_rad": 0.0},
        "anti_phase": {"R": concentration(anti_phase), "mean_delta_rad": math.pi},
        "uniform_phase": {"R": concentration(uniform), "mean_delta_rad": None},
    }
    assert abs(negative_controls["in_phase"]["R"] - 1) < 1e-12
    assert abs(negative_controls["anti_phase"]["R"] - 1) < 1e-12
    assert negative_controls["uniform_phase"]["R"] < 1e-12
    manifest = {"type": "synthetic_fixture_not_human_evidence", "version": 1,
                "fps": FPS, "seconds_per_condition": SECONDS,
                "formula": "theta=2*pi*t+sign*1.8*sin(pi*u)^2; opposed flips right sign",
                "axes": "lateral, anterior, vertical; unit radius",
                "rows": len(all_rows), "conditions": results,
                "negative_controls": negative_controls,
                "sha256_csv": hashlib.sha256(csv_path.read_bytes()).hexdigest(),
                "limitations": ["no rope physics", "no human movement", "no aesthetic labels",
                                "no metabolic variables", "no consciousness labels",
                                "diagnostic audio is not live Beacon output"]}
    (ROOT / "resultados.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps({"csv": str(csv_path), "rows": len(all_rows),
                      "conditions": results}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
