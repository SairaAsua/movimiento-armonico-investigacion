#!/usr/bin/env python3
"""Replay de fase 2D cruda/rectificada del mismo MP4 en Weaver/Shaper."""

import argparse
import json
import math
import os
from pathlib import Path
import sys

from weaver_video_fase_pcm import revision, sha256


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--video-repo", type=Path, required=True)
    parser.add_argument("--weaver-repo", type=Path, required=True)
    parser.add_argument("--shaper-repo", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    video_repo, weaver, shaper, out = (p.resolve() for p in
                                        (args.video_repo, args.weaver_repo,
                                         args.shaper_repo, args.output_dir))
    if out.exists():
        parser.error("--output-dir debe ser una ruta nueva")
    os.environ["SHAPER_DIR"] = str(shaper)
    sys.path[:0] = [str(weaver / "src"), str(video_repo / "research")]
    import soundfile as sf
    from harmonic_weaver.lab.evaluation.pcm import PCMSettings, PCMWriter, engine_identity
    from ejecutar_banco_fase_archivo import CYCLES, FPS, pts
    from video_fase_audio_diagnostico import BASE_HZ, HZ_PER_RADIAN
    from video_fase_plano_oblicuo import phase_from_video

    sources = video_repo / "research/datos_sinteticos_video_ritmo"
    video = sources / "fase_plano_oblicuo.mp4"
    source_manifest = json.loads((sources / "fase_plano_oblicuo_manifest.json").read_text())
    assert sha256(video) == source_manifest["video_sha256"]
    raw, corrected, pts_error = phase_from_video(video)
    times = pts(video)
    assert len(raw) == len(corrected) == len(times) == CYCLES * FPS
    assert abs(pts_error - source_manifest["max_pts_grid_error_ms"]) < 1e-12
    out.mkdir(parents=True)

    cases = {}
    for name, deltas in (("raw_image_phase", raw),
                         ("corrected_known_plane", corrected)):
        wav = out / f"{name}.wav"
        writer = PCMWriter(wav, PCMSettings(enabled=True),
                           begin_s=0, start_s=0, end_s=float(CYCLES))
        frequencies = []
        for time_s, delta in zip(times, deltas):
            frequency = BASE_HZ + HZ_PER_RADIAN * delta
            assert 100 < frequency < 400
            frequencies.append(frequency)
            writer.feed({"control_time_s": time_s,
                         "targets": [dict(id=1, frequency_hz=frequency, gain=0.5,
                                          phase_deg=0.0, pan=0.0, shape=0.0,
                                          release_s=0.0)]})
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
        r = abs(sum(complex(math.cos(d), math.sin(d)) for d in deltas)) / len(deltas)
        assert abs(r - source_manifest["raw" if name == "raw_image_phase"
                                       else "corrected"]["r_continuous_from_pixels"]) < 1e-12
        cases[name] = {
            "r_from_pixels": r,
            "input_frequency_min_hz": min(frequencies),
            "input_frequency_max_hz": max(frequencies),
            "max_control_delay_samples": max(delays),
            "pcm_sha256": rendered["sha256"],
            "voice_frames_sha256": rendered["voice_frames_sha256"],
            "pcm_rms": rendered["rms"],
        }

    assert cases["raw_image_phase"]["pcm_sha256"] != cases["corrected_known_plane"]["pcm_sha256"]
    assert abs(cases["raw_image_phase"]["pcm_rms"] -
               cases["corrected_known_plane"]["pcm_rms"]) < 0.01
    identity = engine_identity()
    report = {
        "scope": "synthetic_projection_bias_to_offline_weaver_shaper_pcm",
        "video_repo_commit": revision(video_repo),
        "weaver_commit": revision(weaver),
        "shaper_commit": revision(shaper),
        "source_video_sha256": sha256(video),
        "source_manifest_sha256": sha256(sources / "fase_plano_oblicuo_manifest.json"),
        "engine_code_sha256": identity["code_sha256"],
        "engine_environment_sha256": identity["environment_sha256"],
        "mapping": f"frequency_hz={BASE_HZ}+{HZ_PER_RADIAN}*(right_phase-left_phase)",
        "correction_provenance": "known synthetic y factor 0.25; not inferred from video",
        "clock": "source PTS from same MP4, applied in first render block at/after PTS",
        "not": ["physical camera calibration", "Beacon OSC", "human movement", "HIT validation"],
        "cases": cases,
    }
    (out / "report.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
