#!/usr/bin/env python3
"""Video sintético de fase → controles con PTS → PCM offline Weaver/Shaper."""

import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import subprocess
import sys

import numpy as np


def revision(repo: Path) -> str:
    return subprocess.check_output(["git", "-C", str(repo), "rev-parse", "HEAD"], text=True).strip()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--video-repo", type=Path, required=True,
                        help="checkout de la rama de video sintético (PR #26)")
    parser.add_argument("--weaver-repo", type=Path, required=True)
    parser.add_argument("--shaper-repo", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    video_repo, weaver, shaper, out = (p.resolve() for p in
                                        (args.video_repo, args.weaver_repo,
                                         args.shaper_repo, args.output_dir))
    if out.exists():
        parser.error("--output-dir debe ser una ruta nueva")
    if not (video_repo / "research/video_fase_audio_diagnostico.py").is_file():
        parser.error("falta el banco de fase de video de PR #26")
    if not (weaver / "src/harmonic_weaver/lab/evaluation/pcm.py").is_file():
        parser.error("checkout de Weaver sin PCMWriter")
    if not (shaper / "src/harmonic_shaper/audio_engine.py").is_file():
        parser.error("checkout de Shaper sin AudioEngine")

    os.environ["SHAPER_DIR"] = str(shaper)
    sys.path[:0] = [str(weaver / "src"), str(video_repo / "research")]
    import soundfile as sf
    from harmonic_weaver.lab.evaluation.pcm import PCMSettings, PCMWriter, engine_identity
    from video_fase_audio_diagnostico import (
        BASE_HZ, CYCLES, FPS, HZ_PER_RADIAN, decoded_pixel_sha256, from_pixels,
    )

    sources = video_repo / "research/datos_sinteticos_video_ritmo"
    source_manifest = json.loads((sources / "fase_audio_manifest.json").read_text())
    assert source_manifest["source_bank"].startswith("ejecutar_banco_fase_archivo.py")
    out.mkdir(parents=True)
    cases = {}
    recovered = {}
    for name in ("aligned", "opposed"):
        video = sources / f"fase_source_{name}.mp4"
        original = source_manifest["results"][name]
        assert sha256(video) == original["video_sha256"]
        assert decoded_pixel_sha256(video) == original["decoded_pixel_sha256"]
        deltas, times = from_pixels(video)
        assert len(deltas) == len(times) == CYCLES * FPS
        r = abs(sum(complex(math.cos(d), math.sin(d)) for d in deltas)) / len(deltas)
        assert abs(r - original["r_continuous_from_pixels"]) < 1e-12
        recovered[name] = (deltas, times)

    def render(name: str, source_name: str, invalid_frames: tuple[int, int] | None):
        deltas, times = recovered[source_name]
        wav = out / f"{name}.wav"
        writer = PCMWriter(wav, PCMSettings(enabled=True),
                           begin_s=0.0, start_s=0.0, end_s=float(CYCLES))
        frequencies = []
        for i, (time_s, delta) in enumerate(zip(times, deltas)):
            frequency = BASE_HZ + HZ_PER_RADIAN * delta
            assert 100 < frequency < 400
            frequencies.append(frequency)
            valid = invalid_frames is None or not invalid_frames[0] <= i < invalid_frames[1]
            targets = ([dict(id=1, frequency_hz=frequency, gain=0.5,
                             phase_deg=0.0, pan=0.0, shape=0.0, release_s=0.0)]
                       if valid else [])
            writer.feed({"control_time_s": time_s, "targets": targets})
        rendered = writer.finish()
        samples, sample_rate = sf.read(wav, dtype="float32", always_2d=True)
        assert sample_rate == 48000 and samples.shape == (CYCLES * sample_rate, 2)
        frames = [json.loads(line) for line in
                  wav.with_suffix(".voice-frames.jsonl").read_text().splitlines()]
        first_sample = {}
        for frame in frames:
            first_sample.setdefault(frame["control_sequence"], frame["sample_index"])
        assert set(first_sample) == set(range(1, len(times) + 1))
        delays = [first_sample[i + 1] - round(time_s * sample_rate)
                  for i, time_s in enumerate(times)]
        assert all(0 <= delay < 256 for delay in delays)
        silence = None
        if invalid_frames is not None:
            begin = first_sample[invalid_frames[0] + 1]
            end = first_sample[invalid_frames[1] + 1]
            assert begin < end and np.count_nonzero(samples[begin:end]) == 0
            assert np.count_nonzero(samples[:begin]) > 0
            assert np.count_nonzero(samples[end:]) > 0
            silence = {"injected_invalid_frame_interval": invalid_frames,
                       "actual_silent_sample_interval": (begin, end)}
        cases[name] = {
            "source_video": f"fase_source_{source_name}.mp4",
            "source_video_sha256": sha256(sources / f"fase_source_{source_name}.mp4"),
            "frames": len(times), "input_frequency_min_hz": min(frequencies),
            "input_frequency_max_hz": max(frequencies),
            "sample_rate_hz": sample_rate, "samples_per_channel": len(samples),
            "max_control_delay_samples": max(delays),
            "pcm_sha256": rendered["sha256"],
            "voice_frames_sha256": rendered["voice_frames_sha256"],
            "pcm_rms": rendered["rms"], "injected_invalid": silence,
        }

    render("aligned", "aligned", None)
    render("opposed", "opposed", None)
    render("opposed_injected_invalid", "opposed", (90, 120))
    assert cases["aligned"]["input_frequency_max_hz"] - cases["aligned"]["input_frequency_min_hz"] < 1
    assert cases["opposed"]["input_frequency_max_hz"] - cases["opposed"]["input_frequency_min_hz"] > 100
    assert cases["aligned"]["pcm_sha256"] != cases["opposed"]["pcm_sha256"]
    assert abs(cases["aligned"]["pcm_rms"] - cases["opposed"]["pcm_rms"]) / cases["aligned"]["pcm_rms"] < 0.02
    identity = engine_identity()
    report = {"scope": "synthetic_video_phase_to_offline_shaper_pcm",
              "video_repo_commit": revision(video_repo), "weaver_commit": revision(weaver),
              "shaper_commit": revision(shaper),
              "engine_code_sha256": identity["code_sha256"],
              "engine_environment_sha256": identity["environment_sha256"],
              "mapping": f"frequency_hz={BASE_HZ}+{HZ_PER_RADIAN}*(right_phase-left_phase)",
              "control_policy": "current decoded frame PTS, first production block at/after PTS; no future smoothing",
              "invalid_policy": "injected frame invalidity sends empty targets with release_s=0",
              "cases": cases}
    (out / "report.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
