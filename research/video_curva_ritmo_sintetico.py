#!/usr/bin/env python3
"""Two synthetic videos: same circular path and duration, different timing.

The white square is a point marker, not a rope or person. Measurements below
are recovered from decoded pixels and source PTS, never from generation arrays.
Requires FFmpeg/FFprobe; does not use cameras, services or human media.
"""

from __future__ import annotations

import hashlib
import json
import math
import statistics
import struct
import subprocess
import wave
from pathlib import Path

from geometria_tiempo_sintetica import q


HERE = Path(__file__).resolve().parent
OUTPUT = HERE / "datos_sinteticos_video_ritmo"
WIDTH = HEIGHT = 320
FPS = 30
COUNT = 90
CX = CY = 160
RADIUS = 95
MARKER_HALF_WIDTH = 3
SAMPLE_RATE = 24000
TONE_HZ = 220


def run(command: list[str], *, data: bytes | None = None) -> bytes:
    result = subprocess.run(command, input=data, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, check=True)
    return result.stdout


def build_video(kind: str) -> Path:
    if kind not in ("uniforme", "reparametrizado"):
        raise ValueError(kind)
    raw = bytearray()
    for index in range(COUNT):
        t = index / COUNT
        u = t if kind == "uniforme" else q(t)
        x = round(CX + RADIUS * math.cos(2 * math.pi * u))
        y = round(CY + RADIUS * math.sin(2 * math.pi * u))
        frame = bytearray(WIDTH * HEIGHT)
        for row in range(y - MARKER_HALF_WIDTH, y + MARKER_HALF_WIDTH + 1):
            offset = row * WIDTH
            frame[offset + x - MARKER_HALF_WIDTH:
                  offset + x + MARKER_HALF_WIDTH + 1] = b"\xff" * 7
        raw.extend(frame)
    # MP4 retains the 1/30-s timestamps here; Matroska's default millisecond
    # timebase rounds them to 0.033/0.067 s in FFprobe.
    path = OUTPUT / f"circulo_{kind}.mp4"
    run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-f", "rawvideo",
         "-pixel_format", "gray", "-video_size", f"{WIDTH}x{HEIGHT}",
         "-framerate", str(FPS), "-i", "pipe:0", "-c:v", "libx264rgb",
         "-crf", "0", "-pix_fmt", "rgb24", "-movflags", "+faststart",
         "-y", str(path)], data=bytes(raw))
    return path


def decoded_measurements(path: Path) -> tuple[dict, list[float]]:
    info = json.loads(run([
        "ffprobe", "-v", "error", "-select_streams", "v:0", "-show_frames",
        "-show_entries", "frame=best_effort_timestamp_time", "-of", "json",
        str(path),
    ]))
    pts = [float(frame["best_effort_timestamp_time"])
           for frame in info["frames"]]
    assert len(pts) == COUNT and all(b > a for a, b in zip(pts, pts[1:]))
    pts = [value - pts[0] for value in pts]
    assert all(abs(value - index / FPS) < 1e-6 for index, value in enumerate(pts))
    raw = run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-i",
               str(path), "-f", "rawvideo", "-pix_fmt", "gray", "pipe:1"])
    frame_size = WIDTH * HEIGHT
    assert len(raw) == COUNT * frame_size

    positions = []
    for index in range(COUNT):
        frame = raw[index * frame_size:(index + 1) * frame_size]
        pixels = [offset for offset, value in enumerate(frame) if value > 128]
        assert len(pixels) == 49  # 7×7 decoded marker, no segmentation loss.
        x = sum(offset % WIDTH for offset in pixels) / len(pixels)
        y = sum(offset // WIDTH for offset in pixels) / len(pixels)
        positions.append((x, y))

    angles = [math.atan2(y - CY, x - CX) for x, y in positions]
    unwrapped = [angles[0]]
    for angle in angles[1:]:
        delta = (angle - unwrapped[-1] + math.pi) % (2 * math.pi) - math.pi
        assert 0 < delta < math.pi  # No reversal or half-turn aliasing.
        unwrapped.append(unwrapped[-1] + delta)
    start = unwrapped[0]
    phase = [angle - start for angle in unwrapped]
    durations = [pts[i + 1] - pts[i] for i in range(COUNT - 1)]
    lengths = [math.dist(positions[i], positions[i + 1])
               for i in range(COUNT - 1)]
    in_first_half = [(phase[i] + phase[i + 1]) / 2 < math.pi
                     for i in range(COUNT - 1)]
    time_fraction = sum(dt for dt, selected in zip(durations, in_first_half)
                        if selected) / sum(durations)
    arc_fraction = sum(ds for ds, selected in zip(lengths, in_first_half)
                       if selected) / sum(lengths)
    radial_errors = [math.hypot(x - CX, y - CY) - RADIUS for x, y in positions]
    summary = {
        "video_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "frames": COUNT,
        "first_pts_s": pts[0],
        "last_pts_s": pts[-1],
        "nominal_duration_s": COUNT / FPS,
        "decoded_marker_pixels_per_frame": 49,
        "radial_rmse_px": math.sqrt(sum(e * e for e in radial_errors) / COUNT),
        "observed_path_length_px": sum(lengths),
        "first_semicircle_time_fraction": time_fraction,
        "first_semicircle_arc_fraction": arc_fraction,
        "phase_covered_rad_without_closure": phase[-1],
    }
    speeds = [distance / duration for distance, duration in zip(lengths, durations)]
    return summary, speeds


def render_speed_audio(speeds: list[float], baseline_speed: float,
                       output: Path) -> dict:
    """Fixed-carrier amplitude from measured speed; last unsupported frame fades out."""
    assert len(speeds) == COUNT - 1 and baseline_speed > 0
    gains = [min(0.9, 0.45 * speed / baseline_speed) for speed in speeds] + [0.0]
    samples = bytearray()
    thirds: list[list[int]] = [[], [], []]
    samples_per_frame = SAMPLE_RATE // FPS
    ramp_samples = SAMPLE_RATE // 100  # 10 ms ramp after each frame boundary.
    for sample_index in range(COUNT * samples_per_frame):
        frame_index, frame_sample = divmod(sample_index, samples_per_frame)
        current = gains[frame_index]
        previous = gains[frame_index - 1] if frame_index else 0.0
        ramp = min(1.0, frame_sample / ramp_samples)
        gain = previous + (current - previous) * ramp
        carrier = math.sin(2 * math.pi * TONE_HZ * sample_index / SAMPLE_RATE)
        value = round(16000 * gain * carrier)
        thirds[frame_index // 30].append(value)
        samples.extend(struct.pack("<h", value))
    with wave.open(str(output), "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(SAMPLE_RATE)
        wav.writeframes(samples)
    rms = [math.sqrt(sum(value * value for value in third) / len(third))
           for third in thirds]
    return {
        "wav_sha256": hashlib.sha256(output.read_bytes()).hexdigest(),
        "sample_rate_hz": SAMPLE_RATE,
        "tone_hz": TONE_HZ,
        "mapping": "gain=min(0.9,0.45*measured_speed/baseline_speed)",
        "availability": "speed for interval i requires decoded frame i+1; offline alignment, not live output",
        "boundary_ramp_ms": 10,
        "last_frame": "no next observed position; target gain zero",
        "rms_pcm16_by_second": rms,
    }


def main() -> None:
    OUTPUT.mkdir(exist_ok=True)
    decoded = {
        kind: decoded_measurements(build_video(kind))
        for kind in ("uniforme", "reparametrizado")
    }
    measurements = {kind: result[0] for kind, result in decoded.items()}
    a, b = measurements["uniforme"], measurements["reparametrizado"]
    assert a["radial_rmse_px"] < 0.5 and b["radial_rmse_px"] < 0.5
    assert abs(a["first_semicircle_time_fraction"] - 0.5) < 0.02
    assert b["first_semicircle_time_fraction"] < 0.36
    assert a["first_semicircle_time_fraction"] - b["first_semicircle_time_fraction"] > 0.12
    assert abs(a["first_semicircle_arc_fraction"] - 0.5) < 0.03
    assert abs(b["first_semicircle_arc_fraction"] - 0.5) < 0.03
    assert abs(a["first_semicircle_arc_fraction"] - b["first_semicircle_arc_fraction"]) < 0.03
    baseline_speed = statistics.median(decoded["uniforme"][1])
    audio = {
        kind: render_speed_audio(speeds, baseline_speed,
                                 OUTPUT / f"sonido_rapidez_{kind}.wav")
        for kind, (_, speeds) in decoded.items()
    }
    a_rms = audio["uniforme"]["rms_pcm16_by_second"]
    b_rms = audio["reparametrizado"]["rms_pcm16_by_second"]
    assert 0.9 < a_rms[0] / a_rms[2] < 1.1
    assert b_rms[0] / b_rms[2] > 1.8
    assert b_rms[0] > a_rms[0] and b_rms[2] < a_rms[2]
    manifest = {
        "kind": "synthetic_video_same_path_different_timing",
        "source": "generated point marker; no rope or human motion",
        "construction": "theta_A=2*pi*t; theta_B=2*pi*(t+0.8*t*(1-t))",
        "analysis": "decoded white-pixel centroid and source PTS; 89 observed intervals",
        "audio": "offline diagnostic amplitude from frame speed; fixed carrier; not Beacon",
        "baseline_speed_px_s": baseline_speed,
        "not": ["Laban category", "HIT validation", "rope tracking",
                "energy or aesthetic measurement", "Beacon audio"],
        "measurements": measurements,
        "audio_measurements": audio,
    }
    (OUTPUT / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps({"measurements": measurements,
                      "audio_measurements": audio}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
