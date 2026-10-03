#!/usr/bin/env python3
"""Control mínimo del render PCM offline de Weaver/Shaper; no usa video ni audio físico."""

import argparse
import json
import os
from pathlib import Path
import subprocess
import sys

import numpy as np


def revision(repo: Path) -> str:
    return subprocess.check_output(
        ["git", "-C", str(repo), "rev-parse", "HEAD"], text=True
    ).strip()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--weaver-repo", type=Path, required=True)
    parser.add_argument("--shaper-repo", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    weaver, shaper = args.weaver_repo.resolve(), args.shaper_repo.resolve()
    out = args.output_dir.resolve()
    if out.exists():
        parser.error("--output-dir debe ser una ruta nueva para no sobrescribir evidencia")
    if not (weaver / "src/harmonic_weaver/lab/evaluation/pcm.py").is_file():
        parser.error("Weaver no contiene el renderer PCM esperado")
    if not (shaper / "src/harmonic_shaper/audio_engine.py").is_file():
        parser.error("Shaper no contiene el motor esperado")

    os.environ["SHAPER_DIR"] = str(shaper)
    sys.path.insert(0, str(weaver / "src"))
    import soundfile as sf
    from harmonic_weaver.lab.evaluation.pcm import PCMSettings, PCMWriter, engine_identity

    identity = engine_identity()
    out.mkdir(parents=True)
    controls = {"silence": None, "a": 220.0, "a_repeat": 220.0, "b": 330.0}
    results = {}
    for name, frequency in controls.items():
        path = out / f"{name}.wav"
        voice = [] if frequency is None else [dict(
            id=1, frequency_hz=frequency, gain=0.5, phase_deg=0.0,
            pan=0.0, shape=0.0, release_s=0.0,
        )]
        writer = PCMWriter(path, PCMSettings(enabled=True),
                           begin_s=0.0, start_s=0.0, end_s=0.1)
        writer.feed({"control_time_s": 0.0, "targets": voice})
        rendered = writer.finish()
        samples, sample_rate = sf.read(path, dtype="float32", always_2d=True)
        assert sample_rate == 48000 and samples.shape == (4800, 2)
        mono = samples.mean(axis=1)
        spectrum = np.abs(np.fft.rfft(mono))
        peak_frequency = float(np.fft.rfftfreq(len(mono), 1 / sample_rate)[np.argmax(spectrum)])
        results[name] = {
            "control_frequency_hz": frequency,
            "sha256": rendered["sha256"],
            "voice_frames_sha256": rendered["voice_frames_sha256"],
            "samples": rendered["samples"],
            "rms": rendered["rms"],
            "peak": rendered["peak"],
            "fft_peak_hz": peak_frequency if frequency is not None else None,
        }
        if frequency is None:
            assert np.count_nonzero(samples) == 0
        else:
            assert np.count_nonzero(samples) > 0
            assert abs(peak_frequency - frequency) <= 10.0

    assert results["a"]["sha256"] == results["a_repeat"]["sha256"]
    assert results["a"]["voice_frames_sha256"] == results["a_repeat"]["voice_frames_sha256"]
    assert results["a"]["sha256"] != results["b"]["sha256"]
    report = {
        "scope": "synthetic_offline_pcm_control_only",
        "weaver_commit": revision(weaver),
        "shaper_commit": revision(shaper),
        "engine_code_sha256": identity["code_sha256"],
        "engine_environment_sha256": identity["environment_sha256"],
        "controls": results,
    }
    report_path = out / "report.json"
    report_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
