#!/usr/bin/env python3
"""Iguala RMS de un par sintético Shaper sin modificar su espectro relativo.

Prepara estímulos exploratorios A/B; no ejecuta una prueba perceptiva.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
import soundfile as sf


KEYS = (
    "lateral_anterior-locked-circle_about_origin",
    "lateral_anterior-locked-circle_shifted_lateral",
)
FREQUENCIES_HZ = (550.0, 660.0)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rms(samples: np.ndarray) -> float:
    return float(np.sqrt(np.mean(np.square(samples.astype(np.float64)))))


def bins(samples: np.ndarray, sample_rate: int) -> list[float]:
    mono = samples[sample_rate // 2:].mean(axis=1)
    spectrum = np.abs(np.fft.rfft(mono)) * 2 / len(mono)
    hz = np.fft.rfftfreq(len(mono), 1 / sample_rate)
    return [float(spectrum[np.argmin(abs(hz - freq))]) for freq in FREQUENCIES_HZ]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    source, out = args.input_dir.resolve(), args.output_dir.resolve()
    if out.exists():
        parser.error("--output-dir debe ser una ruta nueva")
    report = json.loads((source / "report.json").read_text())
    if report.get("scope") != "synthetic_retrospective_qr_situation_to_weaver_shaper_pcm_not_beacon":
        parser.error("reporte de origen no corresponde al factorial de situación")

    originals = []
    for key in KEYS:
        wav = source / f"{key}.wav"
        if sha256(wav) != report["cases"][key]["pcm_sha256"]:
            parser.error(f"hash del WAV no coincide con el reporte: {key}")
        samples, rate = sf.read(wav, dtype="float32", always_2d=True)
        if rate != 48000 or samples.shape != (48000, 2) or not np.isfinite(samples).all():
            parser.error(f"PCM inesperado: {key}")
        originals.append(samples)

    levels = [rms(samples) for samples in originals]
    if min(levels) <= 0:
        parser.error("no se puede igualar un PCM silencioso")
    target = min(levels)  # sólo atenuar; ningún clip se amplifica.
    out.mkdir(parents=True)
    rows = []
    matched = []
    for label, key, samples, before in zip(("A", "B"), KEYS, originals, levels):
        factor = target / before
        adjusted = (samples * factor).astype(np.float32)
        if np.max(np.abs(adjusted)) > 1:
            raise AssertionError("normalización produjo clipping")
        path = out / f"{label}.wav"
        # WAV float de libsndfile inserta un timestamp en PEAK; PCM_24 evita
        # ese metadato variable y permite comparar artefactos byte a byte.
        sf.write(path, adjusted, 48000, subtype="PCM_24")
        reread, rate = sf.read(path, dtype="float32", always_2d=True)
        assert rate == 48000 and reread.shape == (48000, 2)
        rows.append({"label": label, "source_case": key,
                     "source_sha256": report["cases"][key]["pcm_sha256"],
                     "source_rms": before, "linear_factor": factor,
                     "matched_rms": rms(reread), "matched_sha256": sha256(path),
                     "matched_tail_bin_amplitudes": bins(reread, rate)})
        matched.append(reread)
    assert abs(rows[0]["matched_rms"] - rows[1]["matched_rms"]) < 1e-7
    assert rows[0]["matched_sha256"] != rows[1]["matched_sha256"]
    residual = [abs(a - b) for a, b in zip(
        rows[0]["matched_tail_bin_amplitudes"],
        rows[1]["matched_tail_bin_amplitudes"])]
    assert all(difference > 0.01 for difference in residual)
    manifest = {
        "scope": "synthetic_shaper_rms_matched_ab_no_listener_test",
        "source_report_sha256": sha256(source / "report.json"),
        "source_engine_code_sha256": report["engine_code_sha256"],
        "sample_rate_hz": 48000, "frames": 48000,
        "matching": "stereo_whole_clip_linear_rms_attenuation_only_then_pcm24",
        "target_rms": target, "stimuli": rows,
        "matched_tail_bin_abs_difference_550_660_hz": residual,
    }
    (out / "manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    print(json.dumps(manifest, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
