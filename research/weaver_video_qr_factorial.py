#!/usr/bin/env python3
"""MP4 sintéticos 2×2 → Q proyectado y fase → PCM offline Weaver/Shaper."""

import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import subprocess
import sys

import numpy as np


WIDTH, HEIGHT, FPS, CYCLES = 256, 128, 30, 8
LEFT_CENTER, RIGHT_CENTER = (64, 64), (192, 64)
GEOMETRIES = {"eje_x": (48, 24), "eje_y": (24, 48)}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def revision(repo: Path) -> str:
    return subprocess.check_output(["git", "-C", str(repo), "rev-parse", "HEAD"], text=True).strip()


def command(args: list[str], data: bytes | None = None) -> bytes:
    result = subprocess.run(args, input=data, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode:
        raise RuntimeError(f"{args[0]}: {result.stderr.decode(errors='replace')[-800:]}")
    return result.stdout


def draw(frame: np.ndarray, center: tuple[int, int], x: int, y: int, color: tuple[int, int, int]):
    cx, cy = center
    px, py = cx + x, cy - y
    for yy in range(py - 4, py + 5):
        for xx in range(px - 4, px + 5):
            if (xx - px) ** 2 + (yy - py) ** 2 <= 16:
                frame[yy, xx] = color


def render_video(path: Path, axes: tuple[int, int], opposed: bool, angles) -> None:
    frames = bytearray()
    for i in range(CYCLES * FPS):
        left, right = angles(i, opposed)
        frame = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)
        draw(frame, LEFT_CENTER, round(40 * math.cos(left)), round(40 * math.sin(left)), (255, 0, 0))
        draw(frame, RIGHT_CENTER, round(axes[0] * math.cos(right)),
             round(axes[1] * math.sin(right)), (0, 0, 255))
        frames.extend(frame.tobytes())
    command(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
             "-f", "rawvideo", "-pixel_format", "rgb24", "-video_size", f"{WIDTH}x{HEIGHT}",
             "-framerate", str(FPS), "-i", "pipe:0", "-c:v", "libx264rgb", "-crf", "0",
             "-pix_fmt", "rgb24", "-movflags", "+faststart", str(path)], bytes(frames))


def points_from_video(path: Path) -> tuple[list[float], list[tuple[float, float]], list[tuple[float, float]]]:
    raw_pts = command(["ffprobe", "-v", "error", "-select_streams", "v:0",
                       "-show_entries", "frame=best_effort_timestamp_time", "-of", "json", str(path)])
    times = [float(frame["best_effort_timestamp_time"])
             for frame in json.loads(raw_pts)["frames"]]
    assert len(times) == CYCLES * FPS
    assert max(abs(t - i / FPS) for i, t in enumerate(times)) < 0.0005
    raw = command(["ffmpeg", "-v", "error", "-i", str(path), "-f", "rawvideo",
                   "-pix_fmt", "rgb24", "-vcodec", "rawvideo", "pipe:1"])
    pixels = np.frombuffer(raw, dtype=np.uint8)
    assert pixels.size == CYCLES * FPS * HEIGHT * WIDTH * 3
    pixels = pixels.reshape(CYCLES * FPS, HEIGHT, WIDTH, 3)
    left_points, right_points = [], []
    for frame in pixels:
        for channel, collection in (("red", left_points), ("blue", right_points)):
            if channel == "red":
                mask = (frame[:, :, 0] > 200) & (frame[:, :, 1] < 30) & (frame[:, :, 2] < 30)
            else:
                mask = (frame[:, :, 2] > 200) & (frame[:, :, 0] < 30) & (frame[:, :, 1] < 30)
            ys, xs = np.nonzero(mask)
            if not len(xs):
                raise ValueError(f"marcador {channel} ausente")
            collection.append((float(xs.mean()), float(ys.mean())))
    return times, left_points, right_points


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phase-repo", type=Path, required=True,
                        help="checkout del banco de fase #26")
    parser.add_argument("--weaver-repo", type=Path, required=True)
    parser.add_argument("--shaper-repo", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    phase_repo, weaver, shaper, out = (p.resolve() for p in
                                        (args.phase_repo, args.weaver_repo,
                                         args.shaper_repo, args.output_dir))
    if out.exists():
        parser.error("--output-dir debe ser una ruta nueva")
    if not (phase_repo / "research/ejecutar_banco_fase_archivo.py").is_file():
        parser.error("falta el banco de fase #26")
    if not (weaver / "src/harmonic_weaver/lab/evaluation/pcm.py").is_file():
        parser.error("checkout de Weaver sin PCMWriter")
    if not (shaper / "src/harmonic_shaper/audio_engine.py").is_file():
        parser.error("checkout de Shaper sin AudioEngine")

    os.environ["SHAPER_DIR"] = str(shaper)
    sys.path[:0] = [str(weaver / "src"), str(phase_repo / "research")]
    import soundfile as sf
    from ejecutar_banco_fase_archivo import angles, q_projected
    from video_fase_audio_diagnostico import unwrap
    from harmonic_weaver.lab.evaluation.pcm import PCMSettings, PCMWriter, engine_identity

    out.mkdir(parents=True)
    cases = {}
    for geometry, axes in GEOMETRIES.items():
        for timing, opposed in (("aligned", False), ("opposed", True)):
            key = f"{geometry}-{timing}"
            mp4 = out / f"{key}.mp4"
            render_video(mp4, axes, opposed, angles)
            times, left, right = points_from_video(mp4)
            assert all(lx < WIDTH / 2 < rx for (lx, _), (rx, _) in zip(left, right))
            qx, qy = q_projected(right)
            left_phase = unwrap([math.atan2(-(y - LEFT_CENTER[1]) / 40,
                                                 (x - LEFT_CENTER[0]) / 40) for x, y in left])
            right_phase = unwrap([math.atan2(-(y - RIGHT_CENTER[1]) / axes[1],
                                                  (x - RIGHT_CENTER[0]) / axes[0]) for x, y in right])
            delta = [r - l for l, r in zip(left_phase, right_phase)]
            r = abs(sum(complex(math.cos(d), math.sin(d)) for d in delta)) / len(delta)
            q_ideal = q_projected([
                (axes[0] * math.cos(2 * math.pi * i / 10000),
                 axes[1] * math.sin(2 * math.pi * i / 10000))
                for i in range(10001)
            ])
            truth = [angles(i, opposed) for i in range(CYCLES * FPS)]
            r_ideal = abs(sum(complex(math.cos(right_true - left_true),
                                      math.sin(right_true - left_true))
                              for left_true, right_true in truth)) / len(truth)
            phase_error_deg = max(math.degrees(abs(math.atan2(
                math.sin(observed - expected), math.cos(observed - expected))))
                for (left_true, right_true), left_obs, right_obs
                in zip(truth, left_phase, right_phase)
                for observed, expected in ((left_obs, left_true), (right_obs, right_true)))
            assert max(abs(qx - q_ideal[0]), abs(qy - q_ideal[1])) < 0.01
            assert abs(r - r_ideal) < 0.01 and phase_error_deg < 2
            gains = (0.2 + 0.8 * qx, 0.2 + 0.8 * qy)
            frequencies = [440 + 20 * d for d in delta]
            assert all(350 < f < 530 for f in frequencies)

            wav = out / f"{key}.wav"
            writer = PCMWriter(wav, PCMSettings(enabled=True),
                               begin_s=0.0, start_s=0.0, end_s=float(CYCLES))
            for time_s, temporal_hz in zip(times, frequencies):
                voices = [dict(id=i + 1, frequency_hz=f, gain=g,
                               phase_deg=0.0, pan=0.0, shape=0.0, release_s=0.0)
                          for i, (f, g) in enumerate(((220.0, gains[0]),
                                                       (330.0, gains[1]),
                                                       (temporal_hz, 0.3)))]
                writer.feed({"control_time_s": time_s, "targets": voices})
            rendered = writer.finish()
            audio, sample_rate = sf.read(wav, dtype="float32", always_2d=True)
            assert sample_rate == 48000 and audio.shape == (CYCLES * sample_rate, 2)
            frames = [json.loads(line) for line in
                      wav.with_suffix(".voice-frames.jsonl").read_text().splitlines()]
            first = {}
            for frame in frames:
                first.setdefault(frame["control_sequence"], frame["sample_index"])
            assert set(first) == set(range(1, CYCLES * FPS + 1))
            delays = [first[i + 1] - round(t * sample_rate) for i, t in enumerate(times)]
            assert all(0 <= delay < 256 for delay in delays)
            cases[key] = {"mp4_sha256": sha256(mp4), "wav_sha256": rendered["sha256"],
                          "voice_frames_sha256": rendered["voice_frames_sha256"],
                          "Q_projected_xy": (qx, qy), "Q_ideal_xy": q_ideal,
                          "R_from_pixels": r, "R_ideal_at_frames": r_ideal,
                          "max_phase_error_deg": phase_error_deg,
                          "spatial_target_gains": gains,
                          "temporal_frequency_range_hz": (min(frequencies), max(frequencies)),
                          "pcm_rms": rendered["rms"],
                          "max_control_delay_samples": max(delays)}

    for geometry in GEOMETRIES:
        a, b = (cases[f"{geometry}-{timing}"] for timing in ("aligned", "opposed"))
        assert max(abs(x - y) for x, y in zip(a["Q_projected_xy"], b["Q_projected_xy"])) < 0.01
        assert a["R_from_pixels"] > 0.98 and b["R_from_pixels"] < 0.15
        assert a["temporal_frequency_range_hz"][1] - a["temporal_frequency_range_hz"][0] < 2
        assert b["temporal_frequency_range_hz"][1] - b["temporal_frequency_range_hz"][0] > 100
    for timing in ("aligned", "opposed"):
        a, b = (cases[f"{geometry}-{timing}"] for geometry in GEOMETRIES)
        assert abs(a["R_from_pixels"] - b["R_from_pixels"]) < 0.01
        assert a["Q_projected_xy"][0] - b["Q_projected_xy"][0] > 0.4
    assert len({case["wav_sha256"] for case in cases.values()}) == 4
    identity = engine_identity()
    report = {"scope": "synthetic_projected_geometry_x_phase_video_to_shaper_pcm",
              "phase_repo_commit": revision(phase_repo), "weaver_commit": revision(weaver),
              "shaper_commit": revision(shaper),
              "engine_code_sha256": identity["code_sha256"],
              "engine_environment_sha256": identity["environment_sha256"],
              "geometry": "right-marker ellipse with swapped image axes; Q is projected 2D",
              "temporal_mapping": "third voice frequency_hz=440+20*unwrapped_phase_difference",
              "spatial_mapping": "two constant gains=0.2+0.8*Qx/Qy, retrospective eight-second descriptor",
              "cases": cases}
    (out / "report.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
