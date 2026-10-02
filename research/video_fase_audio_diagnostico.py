#!/usr/bin/env python3
"""Sonify phase difference recovered from the existing synthetic video bank.

The pitch mapping is an offline diagnostic, not Beacon audio or a claim that
zero phase is preferable. No human video, cameras or services are used.
"""

from __future__ import annotations

import hashlib
import json
import math
import struct
import tempfile
import wave
from pathlib import Path

from ejecutar_banco_fase_archivo import (
    CYCLES, FPS, HEIGHT, LEFT_CENTER, RIGHT_CENTER, WIDTH,
    analyze, centroid, pts, render, run,
)


HERE = Path(__file__).resolve().parent
OUTPUT = HERE / "datos_sinteticos_video_ritmo"
SAMPLE_RATE = 24000
BASE_HZ = 220
HZ_PER_RADIAN = 20


def unwrap(angles: list[float]) -> list[float]:
    result = [angles[0]]
    for angle, previous in zip(angles[1:], angles[:-1]):
        step = (angle - previous + math.pi) % (2 * math.pi) - math.pi
        if not 0 < step < math.pi:
            raise ValueError("phase reversal or temporal aliasing in synthetic marker")
        result.append(result[-1] + step)
    return result


def from_pixels(video: Path) -> tuple[list[float], list[float]]:
    times = pts(video)
    count = CYCLES * FPS
    if len(times) != count or any(abs(t - i / FPS) > 0.0005
                                  for i, t in enumerate(times)):
        raise ValueError("unexpected source PTS")
    pixels = run(["ffmpeg", "-v", "error", "-i", str(video), "-f", "rawvideo",
                  "-pix_fmt", "rgb24", "-vcodec", "rawvideo", "pipe:1"])
    frame_size = WIDTH * HEIGHT * 3
    if len(pixels) != count * frame_size:
        raise ValueError("decoded frame count mismatch")
    left_angles, right_angles = [], []
    for index in range(count):
        frame = pixels[index * frame_size:(index + 1) * frame_size]
        lx, ly = centroid(frame, "red")
        rx, ry = centroid(frame, "blue")
        if lx >= WIDTH / 2 or rx <= WIDTH / 2:
            raise ValueError("point identity inconsistent with synthetic fixture")
        left_angles.append(math.atan2(-(ly - LEFT_CENTER[1]), lx - LEFT_CENTER[0]))
        right_angles.append(math.atan2(-(ry - RIGHT_CENTER[1]), rx - RIGHT_CENTER[0]))
    left, right = unwrap(left_angles), unwrap(right_angles)
    return [r - l for l, r in zip(left, right)], times


def decoded_pixel_sha256(video: Path) -> str:
    pixels = run(["ffmpeg", "-v", "error", "-i", str(video), "-f", "rawvideo",
                  "-pix_fmt", "rgb24", "-vcodec", "rawvideo", "pipe:1"])
    return hashlib.sha256(pixels).hexdigest()


def render_audio(deltas: list[float], path: Path) -> dict:
    count = CYCLES * FPS
    if len(deltas) != count:
        raise ValueError("incomplete phase series")
    frequencies = [BASE_HZ + HZ_PER_RADIAN * delta for delta in deltas]
    if not all(100 < frequency < 400 for frequency in frequencies):
        raise ValueError("diagnostic pitch outside declared range")
    samples_per_frame = SAMPLE_RATE // FPS
    total_samples = count * samples_per_frame
    phase = 0.0
    pcm = bytearray()
    sum_sq = 0
    for sample_index in range(total_samples):
        frame = sample_index // samples_per_frame
        frequency = frequencies[frame]  # Current decoded frame; no future-frame smoothing.
        phase += 2 * math.pi * frequency / SAMPLE_RATE
        edge = min(1.0, sample_index / (SAMPLE_RATE * 0.01),
                   (total_samples - 1 - sample_index) / (SAMPLE_RATE * 0.01))
        value = round(10000 * edge * math.sin(phase))
        sum_sq += value * value
        pcm.extend(struct.pack("<h", value))
    with wave.open(str(path), "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(SAMPLE_RATE)
        wav.writeframes(pcm)
    concentration = abs(sum(complex(math.cos(d), math.sin(d)) for d in deltas)) / count
    mean = math.atan2(sum(math.sin(d) for d in deltas),
                      sum(math.cos(d) for d in deltas))
    return {
        "wav_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "duration_s": CYCLES,
        "sample_rate_hz": SAMPLE_RATE,
        "r_continuous_from_pixels": concentration,
        "mean_resultant_angle_rad": mean,
        "mean_angle_note": "resultant direction becomes unstable as R approaches zero; no human threshold set",
        "pitch_min_hz": min(frequencies),
        "pitch_max_hz": max(frequencies),
        "rms_pcm16": math.sqrt(sum_sq / total_samples),
    }


def main() -> None:
    OUTPUT.mkdir(exist_ok=True)
    results = {}
    with tempfile.TemporaryDirectory(prefix="phase-audio-synthetic-") as directory:
        for name, opposed in (("aligned", False), ("opposed", True)):
            intermediate = Path(directory) / f"{name}.mkv"
            render(intermediate, opposed)
            # The FFV1/Matroska source bank can carry variable container metadata.
            # Publish a lossless MP4 with stable hash and exact 1/30-s timestamps.
            video = OUTPUT / f"fase_source_{name}.mp4"
            run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-i",
                 str(intermediate), "-c:v", "libx264rgb", "-crf", "0",
                 "-pix_fmt", "rgb24", "-movflags", "+faststart", "-y", str(video)])
            pixel_hash = decoded_pixel_sha256(intermediate)
            assert decoded_pixel_sha256(video) == pixel_hash
            source_report = analyze(video, opposed)
            deltas, times = from_pixels(video)
            assert len(times) == CYCLES * FPS
            audio = render_audio(deltas, OUTPUT / f"fase_{name}_desde_video.wav")
            assert abs(audio["r_continuous_from_pixels"] -
                       source_report["r_continuous_from_pixels"]) < 1e-12
            results[name] = {"video_sha256": source_report["sha256"],
                             "decoded_pixel_sha256": pixel_hash,
                             "frames": source_report["frames"],
                             "q_projected_xy": source_report["q_projected_xy"],
                             "r_event_only": source_report["r_event_only"],
                             **audio}
    a, b = results["aligned"], results["opposed"]
    assert a["r_continuous_from_pixels"] > 0.99
    assert b["r_continuous_from_pixels"] < 0.15
    assert a["pitch_max_hz"] - a["pitch_min_hz"] < 1
    assert b["pitch_max_hz"] - b["pitch_min_hz"] > 100
    assert abs(a["rms_pcm16"] - b["rms_pcm16"]) / a["rms_pcm16"] < 0.02
    manifest = {
        "kind": "synthetic_video_intracycle_phase_audio_diagnostic",
        "source_bank": "ejecutar_banco_fase_archivo.py; matched-marginal aligned/opposed",
        "review_videos": "lossless MP4 copies of generated FFV1 files; metrics recomputed on published MP4 pixels",
        "mapping": "mono pitch=220+20*(unwrapped right_phase-left_phase) Hz",
        "availability": "current decoded frame after capture/decode; no measured live latency",
        "not": ["Beacon audio", "rope flow", "human phase", "HIT validation",
                "beauty or physiological consonance"],
        "results": results,
    }
    (OUTPUT / "fase_audio_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
