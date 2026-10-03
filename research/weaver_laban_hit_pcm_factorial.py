#!/usr/bin/env python3
"""Replay sonoro 2×2 de Q/R sintéticos con el PCM offline real de Weaver/Shaper."""

import argparse
import json
import os
from pathlib import Path
import subprocess
import sys

import numpy as np

from laban_hit_factorial_sintetico import arc_weighted_q, relative_phase_r, trajectory


FREQUENCIES_HZ = (220.0, 330.0, 440.0)
PLANES = ("lateral_anterior", "lateral_vertical")
TIMINGS = ("locked", "drift")


def revision(repo: Path) -> str:
    return subprocess.check_output(["git", "-C", str(repo), "rev-parse", "HEAD"], text=True).strip()


def gains_from(q: tuple[float, float, float], r: float) -> tuple[float, float, float]:
    # Propuesta diagnóstica de capas; no es una fórmula histórica de Laban.
    return (0.2 + 0.8 * q[1], 0.2 + 0.8 * q[2], 0.2 + 0.8 * r)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--weaver-repo", type=Path, required=True)
    parser.add_argument("--shaper-repo", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    weaver, shaper, out = (p.resolve() for p in
                           (args.weaver_repo, args.shaper_repo, args.output_dir))
    if out.exists():
        parser.error("--output-dir debe ser una ruta nueva")
    if not (weaver / "src/harmonic_weaver/lab/evaluation/pcm.py").is_file():
        parser.error("checkout de Weaver sin PCMWriter")
    if not (shaper / "src/harmonic_shaper/audio_engine.py").is_file():
        parser.error("checkout de Shaper sin AudioEngine")

    os.environ["SHAPER_DIR"] = str(shaper)
    sys.path.insert(0, str(weaver / "src"))
    import soundfile as sf
    from harmonic_weaver.lab.evaluation.pcm import PCMSettings, PCMWriter, engine_identity

    out.mkdir(parents=True)
    results = {}
    for plane in PLANES:
        for timing in TIMINGS:
            points, phases = trajectory(plane, timing)
            q, _ = arc_weighted_q(points)
            r = relative_phase_r(phases)
            gains = gains_from(q, r)
            assert all(0 < gain <= 1 for gain in gains)
            targets = [dict(id=i + 1, frequency_hz=freq, gain=gain,
                            phase_deg=0.0, pan=0.0, shape=0.0, release_s=0.0)
                       for i, (freq, gain) in enumerate(zip(FREQUENCIES_HZ, gains))]
            key = f"{plane}-{timing}"
            wav = out / f"{key}.wav"
            writer = PCMWriter(wav, PCMSettings(enabled=True),
                               begin_s=0.0, start_s=0.0, end_s=1.0)
            writer.feed({"control_time_s": 0.0, "targets": targets})
            rendered = writer.finish()
            samples, rate = sf.read(wav, dtype="float32", always_2d=True)
            assert rate == 48000 and samples.shape == (48000, 2)
            # Los últimos 0,5 s evitan el ataque del primer bloque.
            mono = samples[24000:].mean(axis=1)
            spectrum = np.abs(np.fft.rfft(mono)) * 2 / len(mono)
            bins = np.fft.rfftfreq(len(mono), 1 / rate)
            amplitudes = [float(spectrum[np.argmin(abs(bins - freq))])
                          for freq in FREQUENCIES_HZ]
            results[key] = {"Q": q, "R": r, "target_gains": gains,
                            "carrier_hz": FREQUENCIES_HZ,
                            "pcm_bin_amplitudes": amplitudes,
                            "pcm_rms": rendered["rms"], "pcm_sha256": rendered["sha256"],
                            "voice_frames_sha256": rendered["voice_frames_sha256"]}

    for plane in PLANES:
        a, b = (results[f"{plane}-{timing}"] for timing in TIMINGS)
        assert np.allclose(a["Q"], b["Q"], atol=1e-4)
        assert np.allclose(a["target_gains"][:2], b["target_gains"][:2], atol=1e-4)
        assert abs(a["R"] - b["R"]) > 0.4
        assert abs(a["pcm_bin_amplitudes"][2] - b["pcm_bin_amplitudes"][2]) > 0.05
    for timing in TIMINGS:
        a, b = (results[f"{plane}-{timing}"] for plane in PLANES)
        assert abs(a["R"] - b["R"]) < 1e-12
        assert abs(a["target_gains"][2] - b["target_gains"][2]) < 1e-12
        assert abs(a["pcm_bin_amplitudes"][0] - b["pcm_bin_amplitudes"][0]) > 0.05
        assert abs(a["pcm_bin_amplitudes"][1] - b["pcm_bin_amplitudes"][1]) > 0.05
    assert len({row["pcm_sha256"] for row in results.values()}) == 4
    report = {"scope": "synthetic_retrospective_qr_to_offline_pcm",
              "weaver_commit": revision(weaver), "shaper_commit": revision(shaper),
              "engine_code_sha256": engine_identity()["code_sha256"],
              "engine_environment_sha256": engine_identity()["environment_sha256"],
              "cases": results}
    (out / "report.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
