#!/usr/bin/env python3
"""Cruza controles rho_min y V_r por separado en el PCM offline Shaper.

Los híbridos son contrafácticos de controles, no trayectorias observadas.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

import numpy as np
import soundfile as sf


SOURCE_KEYS = (
    "lateral_anterior-locked-circle_about_origin",
    "lateral_anterior-locked-circle_shifted_lateral",
)
FREQUENCIES_HZ = (220.0, 330.0, 440.0, 550.0, 660.0)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rms(samples: np.ndarray) -> float:
    return float(np.sqrt(np.mean(np.square(samples.astype(np.float64)))))


def amplitudes(samples: np.ndarray, rate: int) -> list[float]:
    mono = samples[rate // 2:].mean(axis=1)
    spectrum = np.abs(np.fft.rfft(mono)) * 2 / len(mono)
    hz = np.fft.rfftfreq(len(mono), 1 / rate)
    return [float(spectrum[np.argmin(abs(hz - frequency))])
            for frequency in FREQUENCIES_HZ]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-dir", type=Path, required=True)
    parser.add_argument("--weaver-repo", type=Path, required=True)
    parser.add_argument("--shaper-repo", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    source, weaver, shaper, out = (p.resolve() for p in (
        args.input_dir, args.weaver_repo, args.shaper_repo, args.output_dir))
    if out.exists():
        parser.error("--output-dir debe ser una ruta nueva")
    report_path = source / "report.json"
    report = json.loads(report_path.read_text())
    if report.get("scope") != "synthetic_retrospective_qr_situation_to_weaver_shaper_pcm_not_beacon":
        parser.error("reporte de origen incorrecto")
    if not (weaver / "src/harmonic_weaver/lab/evaluation/pcm.py").is_file():
        parser.error("checkout de Weaver sin PCMWriter")
    if not (shaper / "src/harmonic_shaper/audio_engine.py").is_file():
        parser.error("checkout de Shaper sin AudioEngine")
    for key in SOURCE_KEYS:
        if sha256(source / f"{key}.wav") != report["cases"][key]["pcm_sha256"]:
            parser.error(f"WAV de origen no corresponde al reporte: {key}")
    if report["weaver_commit"] != subprocess.check_output(
            ["git", "-C", str(weaver), "rev-parse", "HEAD"], text=True).strip():
        parser.error("revisión Weaver distinta de la fuente")
    if report["shaper_commit"] != subprocess.check_output(
            ["git", "-C", str(shaper), "rev-parse", "HEAD"], text=True).strip():
        parser.error("revisión Shaper distinta de la fuente")

    a, b = (report["cases"][key] for key in SOURCE_KEYS)
    if a["target_gains"][:3] != b["target_gains"][:3]:
        parser.error("Q/R no son iguales en el par de origen")
    os.environ["SHAPER_DIR"] = str(shaper)
    sys.path.insert(0, str(weaver / "src"))
    from harmonic_weaver.lab.evaluation.pcm import PCMSettings, PCMWriter, engine_identity
    identity = engine_identity()
    if identity["code_sha256"] != report["engine_code_sha256"]:
        parser.error("código del motor distinto de la fuente")
    if identity["environment_sha256"] != report["engine_environment_sha256"]:
        parser.error("entorno del motor distinto de la fuente")

    combinations = {
        "rhoA_vA": (a["target_gains"][3], a["target_gains"][4]),
        "rhoB_vA": (b["target_gains"][3], a["target_gains"][4]),
        "rhoA_vB": (a["target_gains"][3], b["target_gains"][4]),
        "rhoB_vB": (b["target_gains"][3], b["target_gains"][4]),
    }
    raw = {}
    with tempfile.TemporaryDirectory(prefix="situacion-ablation-") as tmp:
        for label, (rho_gain, v_gain) in combinations.items():
            gains = (*a["target_gains"][:3], rho_gain, v_gain)
            targets = [dict(id=i + 1, frequency_hz=freq, gain=gain,
                            phase_deg=0.0, pan=0.0, shape=0.0, release_s=0.0)
                       for i, (freq, gain) in enumerate(zip(FREQUENCIES_HZ, gains))]
            wav = Path(tmp) / f"{label}.wav"
            writer = PCMWriter(wav, PCMSettings(enabled=True),
                               begin_s=0.0, start_s=0.0, end_s=1.0)
            writer.feed({"control_time_s": 0.0, "targets": targets})
            writer.finish()
            samples, rate = sf.read(wav, dtype="float32", always_2d=True)
            assert rate == 48000 and samples.shape == (48000, 2)
            raw[label] = samples
    # Los dos extremos deben recuperar exactamente los samples del factorial.
    for label, key in (("rhoA_vA", SOURCE_KEYS[0]), ("rhoB_vB", SOURCE_KEYS[1])):
        previous, _ = sf.read(source / f"{key}.wav", dtype="float32", always_2d=True)
        assert np.array_equal(raw[label], previous)

    target_rms = min(rms(samples) for samples in raw.values())
    out.mkdir(parents=True)
    stimuli = {}
    for label, samples in raw.items():
        before = rms(samples)
        factor = target_rms / before
        adjusted = (samples * factor).astype(np.float32)
        if np.max(np.abs(adjusted)) > 1:
            raise AssertionError("clipping inesperado")
        path = out / f"{label}.wav"
        sf.write(path, adjusted, 48000, subtype="PCM_24")
        reread, rate = sf.read(path, dtype="float32", always_2d=True)
        stimuli[label] = {
            "target_gains": [*a["target_gains"][:3], *combinations[label]],
            "raw_rms": before, "matching_factor": factor,
            "matched_rms": rms(reread), "matched_sha256": sha256(path),
            "matched_bin_amplitudes": amplitudes(reread, rate),
        }
    assert max(v["matched_rms"] for v in stimuli.values()) - min(
        v["matched_rms"] for v in stimuli.values()) < 1e-7
    assert len({v["matched_sha256"] for v in stimuli.values()}) == 4
    for x, y in (("rhoA_vA", "rhoB_vA"), ("rhoA_vB", "rhoB_vB")):
        assert stimuli[x]["target_gains"][4] == stimuli[y]["target_gains"][4]
        assert stimuli[x]["target_gains"][3] != stimuli[y]["target_gains"][3]
    for x, y in (("rhoA_vA", "rhoA_vB"), ("rhoB_vA", "rhoB_vB")):
        assert stimuli[x]["target_gains"][3] == stimuli[y]["target_gains"][3]
        assert stimuli[x]["target_gains"][4] != stimuli[y]["target_gains"][4]
    contrasts = {}
    for name, x, y in (("rho_only", "rhoA_vA", "rhoB_vA"),
                       ("v_only", "rhoA_vA", "rhoA_vB"),
                       ("both", "rhoA_vA", "rhoB_vB")):
        contrasts[name] = [abs(p - q) for p, q in zip(
            stimuli[x]["matched_bin_amplitudes"],
            stimuli[y]["matched_bin_amplitudes"])]
    assert contrasts["rho_only"][3] > 0.01
    assert contrasts["v_only"][4] > 0.01
    manifest = {
        "scope": "synthetic_shaper_situation_control_ablation_not_body_measurement",
        "source_report_sha256": sha256(report_path),
        "engine_code_sha256": identity["code_sha256"],
        "engine_environment_sha256": identity["environment_sha256"],
        "matching": "global_min_stereo_rms_attenuation_then_pcm24",
        "sample_rate_hz": 48000, "frames": 48000,
        "stimuli": stimuli, "contrasts_bin_abs_difference": contrasts,
    }
    (out / "manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    print(json.dumps(manifest, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
