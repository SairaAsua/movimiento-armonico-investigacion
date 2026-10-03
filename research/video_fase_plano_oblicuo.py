#!/usr/bin/env python3
"""Video sintético: fase de imagen oblicua cruda y rectificada, con audio."""

from __future__ import annotations

import hashlib
import json
import math
import subprocess
from pathlib import Path

from ejecutar_banco_fase_archivo import (
    CYCLES, FPS, HEIGHT, LEFT_CENTER, RIGHT_CENTER, WIDTH, centroid, pts, run,
)
from video_fase_audio_diagnostico import OUTPUT, render_audio, unwrap


RADIUS = 40
DOT_RADIUS = 4
FLATTENING = 0.25


def draw(frame: bytearray, x_center: int, y_center: int,
         color: tuple[int, int, int]) -> None:
    for y in range(y_center - DOT_RADIUS, y_center + DOT_RADIUS + 1):
        for x in range(x_center - DOT_RADIUS, x_center + DOT_RADIUS + 1):
            if (x - x_center) ** 2 + (y - y_center) ** 2 <= DOT_RADIUS ** 2:
                offset = 3 * (y * WIDTH + x)
                frame[offset:offset + 3] = bytes(color)


def generate_video(path: Path) -> None:
    command = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo",
               "-pixel_format", "rgb24", "-video_size", f"{WIDTH}x{HEIGHT}",
               "-framerate", str(FPS), "-i", "pipe:0", "-c:v", "libx264rgb",
               "-crf", "0", "-pix_fmt", "rgb24", "-movflags", "+faststart", str(path)]
    proc = subprocess.Popen(command, stdin=subprocess.PIPE,
                            stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    assert proc.stdin is not None
    try:
        for index in range(CYCLES * FPS):
            angle = 2 * math.pi * index / FPS
            frame = bytearray(WIDTH * HEIGHT * 3)
            draw(frame,
                 round(LEFT_CENTER[0] + RADIUS * math.cos(angle)),
                 round(LEFT_CENTER[1] - RADIUS * math.sin(angle)), (255, 0, 0))
            draw(frame,
                 round(RIGHT_CENTER[0] + RADIUS * math.cos(angle)),
                 round(RIGHT_CENTER[1] - RADIUS * FLATTENING * math.sin(angle)),
                 (0, 0, 255))
            proc.stdin.write(frame)
    finally:
        proc.stdin.close()
    error = proc.stderr.read() if proc.stderr else b""
    if proc.wait() != 0:
        raise RuntimeError(error.decode(errors="replace")[-1000:])


def phase_from_video(path: Path) -> tuple[list[float], list[float], float]:
    times = pts(path)
    expected = CYCLES * FPS
    if len(times) != expected or any(abs(t - i / FPS) > 0.0005
                                          for i, t in enumerate(times)):
        raise ValueError("PTS/frame count differs from synthetic reference")
    pixels = run(["ffmpeg", "-v", "error", "-i", str(path), "-f", "rawvideo",
                  "-pix_fmt", "rgb24", "-vcodec", "rawvideo", "pipe:1"])
    frame_size = WIDTH * HEIGHT * 3
    if len(pixels) != expected * frame_size:
        raise ValueError("decoded pixel count differs from frame count")
    left, raw_right, corrected_right = [], [], []
    for index in range(expected):
        frame = pixels[index * frame_size:(index + 1) * frame_size]
        lx, ly = centroid(frame, "red")
        rx, ry = centroid(frame, "blue")
        if lx >= WIDTH / 2 or rx <= WIDTH / 2:
            raise ValueError("synthetic marker identity failed")
        left.append(math.atan2(-(ly - LEFT_CENTER[1]), lx - LEFT_CENTER[0]))
        raw_right.append(math.atan2(-(ry - RIGHT_CENTER[1]), rx - RIGHT_CENTER[0]))
        corrected_right.append(math.atan2(-(ry - RIGHT_CENTER[1]) / FLATTENING,
                                          rx - RIGHT_CENTER[0]))
    l, raw, corrected = map(unwrap, (left, raw_right, corrected_right))
    return ([r - x for x, r in zip(l, raw)],
            [r - x for x, r in zip(l, corrected)],
            max(abs(t - i / FPS) * 1000 for i, t in enumerate(times)))


def main() -> None:
    OUTPUT.mkdir(exist_ok=True)
    video = OUTPUT / "fase_plano_oblicuo.mp4"
    generate_video(video)
    raw, corrected, pts_error = phase_from_video(video)
    raw_audio = render_audio(raw, OUTPUT / "fase_plano_oblicuo_cruda.wav")
    corrected_audio = render_audio(corrected, OUTPUT / "fase_plano_oblicuo_rectificada.wav")
    assert 0.88 < raw_audio["r_continuous_from_pixels"] < 0.93
    assert corrected_audio["r_continuous_from_pixels"] > 0.995
    assert raw_audio["pitch_max_hz"] - raw_audio["pitch_min_hz"] > 20
    assert corrected_audio["pitch_max_hz"] - corrected_audio["pitch_min_hz"] < 10
    manifest = {
        "kind": "synthetic_oblique_projection_phase_audio_diagnostic",
        "video_sha256": hashlib.sha256(video.read_bytes()).hexdigest(),
        "frames": CYCLES * FPS,
        "fps": FPS,
        "max_pts_grid_error_ms": pts_error,
        "geometry": "left circle frontoparallel, right identical physical phase projected with y factor 0.25",
        "correction": "right image y divided by known synthetic factor 0.25 before atan2",
        "mapping": "mono pitch=220+20*(right-left unwrapped image phase) Hz",
        "availability": "offline after frame decode; no measured live latency",
        "not": ["physical camera", "generic homography validation", "Beacon audio",
                "Nico movement", "human HIT result"],
        "raw": raw_audio,
        "corrected": corrected_audio,
    }
    output = OUTPUT / "fase_plano_oblicuo_manifest.json"
    output.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"raw": raw_audio, "corrected": corrected_audio},
                     ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
