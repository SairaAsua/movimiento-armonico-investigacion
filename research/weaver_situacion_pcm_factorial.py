#!/usr/bin/env python3
"""Render retrospectivo de ocho controles Q/R/situación con Weaver y Shaper.

Consume el fixture numérico de la PR de situación; no ejecuta Beacon live.
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import subprocess
import sys

import numpy as np


FREQUENCIES_HZ = (220.0, 330.0, 440.0, 550.0, 660.0)
BANDS = (4, 5, 6, 7, 8)


def revision(repo: Path) -> str:
    return subprocess.check_output(["git", "-C", str(repo), "rev-parse", "HEAD"],
                                   text=True).strip()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--situation-repo", type=Path, required=True)
    parser.add_argument("--weaver-repo", type=Path, required=True)
    parser.add_argument("--shaper-repo", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    situation, weaver, shaper, out = (p.resolve() for p in (
        args.situation_repo, args.weaver_repo, args.shaper_repo, args.output_dir))
    if out.exists():
        parser.error("--output-dir debe ser una ruta nueva")
    fixture_script = situation / "research/beacon_situacion_controles.py"
    if not fixture_script.is_file():
        parser.error("checkout de situación sin fixture de controles")
    if not (weaver / "src/harmonic_weaver/lab/evaluation/pcm.py").is_file():
        parser.error("checkout de Weaver sin PCMWriter")
    if not (shaper / "src/harmonic_shaper/audio_engine.py").is_file():
        parser.error("checkout de Shaper sin AudioEngine")

    fixture = json.loads(subprocess.check_output([sys.executable, str(fixture_script)],
                                             text=True))
    assert fixture["kind"] == "synthetic_controls_no_osc_no_audio"
    assert fixture["band_addresses"] == [f"/beacon/gain/{b}" for b in BANDS]
    assert len(fixture["cases"]) == 8

    os.environ["SHAPER_DIR"] = str(shaper)
    sys.path.insert(0, str(weaver / "src"))
    import soundfile as sf
    from harmonic_weaver.lab.evaluation.pcm import PCMSettings, PCMWriter, engine_identity

    out.mkdir(parents=True)
    results = {}
    for case in fixture["cases"]:
        key = "-".join(case[k] for k in ("plane", "timing", "situation"))
        gains = tuple(case["gains_by_band"][str(b)] for b in BANDS)
        assert all(0 < g <= 1 for g in gains)
        targets = [dict(id=i + 1, frequency_hz=freq, gain=gain,
                        phase_deg=0.0, pan=0.0, shape=0.0, release_s=0.0)
                   for i, (freq, gain) in enumerate(zip(FREQUENCIES_HZ, gains))]
        wav = out / f"{key}.wav"
        writer = PCMWriter(wav, PCMSettings(enabled=True),
                           begin_s=0.0, start_s=0.0, end_s=1.0)
        writer.feed({"control_time_s": 0.0, "targets": targets})
        rendered = writer.finish()
        samples, rate = sf.read(wav, dtype="float32", always_2d=True)
        assert rate == 48000 and samples.shape == (48000, 2)
        mono = samples[24000:].mean(axis=1)
        spectrum = np.abs(np.fft.rfft(mono)) * 2 / len(mono)
        bins = np.fft.rfftfreq(len(mono), 1 / rate)
        amplitudes = tuple(float(spectrum[np.argmin(abs(bins - freq))])
                           for freq in FREQUENCIES_HZ)
        results[key] = {
            "plane": case["plane"], "timing": case["timing"],
            "situation": case["situation"], "Q": case["Q"],
            "R_1to1": case["R_1to1"], "rho_min": case["rho_min"],
            "V_r": case["V_r"], "target_gains": gains,
            "carrier_hz": FREQUENCIES_HZ, "pcm_bin_amplitudes": amplitudes,
            "pcm_rms": rendered["rms"], "pcm_sha256": rendered["sha256"],
            "voice_frames_sha256": rendered["voice_frames_sha256"],
        }

    def row(plane: str, timing: str, situation_name: str) -> dict:
        return results[f"{plane}-{timing}-{situation_name}"]

    contrast = []
    for plane in ("lateral_anterior", "lateral_vertical"):
        for timing in ("locked", "drift"):
            a = row(plane, timing, "circle_about_origin")
            b = row(plane, timing, "circle_shifted_lateral")
            assert a["target_gains"][:3] == b["target_gains"][:3]
            assert a["target_gains"][3:] != b["target_gains"][3:]
            assert a["pcm_sha256"] != b["pcm_sha256"]
            delta = tuple(abs(x - y) for x, y in zip(
                a["pcm_bin_amplitudes"], b["pcm_bin_amplitudes"]))
            contrast.append({"plane": plane, "timing": timing,
                             "pcm_bin_abs_difference": delta,
                             "rms_abs_difference": abs(a["pcm_rms"] - b["pcm_rms"])})
    assert len({v["pcm_sha256"] for v in results.values()}) == 8
    assert all(c["pcm_bin_abs_difference"][3] > 0.01 for c in contrast)
    assert all(c["pcm_bin_abs_difference"][4] > 0.01 for c in contrast)
    report = {
        "scope": "synthetic_retrospective_qr_situation_to_weaver_shaper_pcm_not_beacon",
        "situation_commit": revision(situation),
        "situation_contract_sha256": fixture["contract_sha256"],
        "weaver_commit": revision(weaver), "shaper_commit": revision(shaper),
        "engine_code_sha256": engine_identity()["code_sha256"],
        "engine_environment_sha256": engine_identity()["environment_sha256"],
        "cases": results, "situation_contrasts": contrast,
    }
    (out / "report.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
