#!/usr/bin/env python3
"""Stage A: render two synthetic videos and recover phase from decoded pixels.

Requires ffmpeg/ffprobe; uses no human/camera footage or third-party Python packages.
Outputs are local ignored research artifacts, not evidence about a physical camera.
"""

from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path
import subprocess

from laban_hit_marginales_igualados import CYCLES, SWING, phase_and_speed

WIDTH, HEIGHT, FPS = 256, 128, 30
RADIUS, DOT_RADIUS = 40, 4
LEFT_CENTER, RIGHT_CENTER = (64, 64), (192, 64)
OUT = Path(__file__).parent / "sources" / "phase_bench_synthetic"


def run(args: list[str], *, input_bytes: bytes | None = None) -> bytes:
    result = subprocess.run(args, input=input_bytes, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, check=False)
    if result.returncode:
        raise RuntimeError(f"{args[0]} failed: {result.stderr.decode(errors='replace')[-1000:]}")
    return result.stdout


def angles(frame: int, opposed: bool) -> tuple[float, float]:
    cycle, step = divmod(frame, FPS)
    u = step / FPS
    left_swing = SWING if cycle % 2 == 0 else -SWING
    right_swing = -left_swing if opposed else left_swing
    left, _ = phase_and_speed(cycle, u, left_swing)
    right, _ = phase_and_speed(cycle, u, right_swing)
    return left, right


def dot(frame: bytearray, center: tuple[int, int], phase: float,
        color: tuple[int, int, int], orbit_radius: int, dot_radius: int) -> None:
    cx = round(center[0] + orbit_radius * math.cos(phase))
    cy = round(center[1] - orbit_radius * math.sin(phase))
    for y in range(cy - dot_radius, cy + dot_radius + 1):
        for x in range(cx - dot_radius, cx + dot_radius + 1):
            if (x - cx) ** 2 + (y - cy) ** 2 <= dot_radius ** 2:
                start = 3 * (y * WIDTH + x)
                frame[start:start + 3] = bytes(color)


def render(path: Path, opposed: bool, *, orbit_radius: int = RADIUS,
           dot_radius: int = DOT_RADIUS, skip_frame: int | None = None,
           swap_colors_frame: int | None = None) -> None:
    command = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo",
               "-pixel_format", "rgb24", "-video_size", f"{WIDTH}x{HEIGHT}",
               "-framerate", str(FPS), "-i", "pipe:0", "-c:v", "ffv1", str(path)]
    proc = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL,
                            stderr=subprocess.PIPE)
    assert proc.stdin is not None
    try:
        for i in range(CYCLES * FPS):
            if i == skip_frame:
                continue
            frame = bytearray(WIDTH * HEIGHT * 3)
            left, right = angles(i, opposed)
            swapped = i == swap_colors_frame
            dot(frame, LEFT_CENTER, left, (0, 0, 255) if swapped else (255, 0, 0),
                orbit_radius, dot_radius)
            dot(frame, RIGHT_CENTER, right, (255, 0, 0) if swapped else (0, 0, 255),
                orbit_radius, dot_radius)
            proc.stdin.write(frame)
    finally:
        proc.stdin.close()
    error = proc.stderr.read() if proc.stderr else b""
    if proc.wait() != 0:
        raise RuntimeError(f"ffmpeg render failed: {error.decode(errors='replace')[-1000:]}")


def pts(path: Path) -> list[float]:
    raw = run(["ffprobe", "-v", "error", "-select_streams", "v:0",
               "-show_entries", "frame=best_effort_timestamp_time", "-of", "json", str(path)])
    frames = json.loads(raw)["frames"]
    return [float(f["best_effort_timestamp_time"]) for f in frames]


def centroid(rgb: bytes, channel: str) -> tuple[float, float]:
    sx = sy = count = 0
    for y in range(HEIGHT):
        for x in range(WIDTH):
            idx = 3 * (y * WIDTH + x)
            r, g, b = rgb[idx:idx + 3]
            match = r > 200 and g < 30 and b < 30 if channel == "red" else (
                b > 200 and r < 30 and g < 30
            )
            if match:
                sx += x
                sy += y
                count += 1
    if not count:
        raise ValueError(f"missing {channel} point")
    return sx / count, sy / count


def q_projected(points: list[tuple[float, float]]) -> tuple[float, float]:
    accum_x = accum_y = total = 0.0
    for (ax, ay), (bx, by) in zip(points, points[1:]):
        dx, dy = bx - ax, by - ay
        length = math.hypot(dx, dy)
        if length:
            total += length
            accum_x += dx * dx / length
            accum_y += dy * dy / length
    if not total:
        raise ValueError("zero observed path")
    return accum_x / total, accum_y / total


def analyze(path: Path, opposed: bool) -> dict[str, object]:
    timestamps = pts(path)
    expected = CYCLES * FPS
    # Matroska in this ffmpeg build stores a 1 ms timebase: 1/30 s is rounded.
    if len(timestamps) != expected or any(abs(t - i / FPS) > 0.0005
                                          for i, t in enumerate(timestamps)):
        raise ValueError("missing or unexpected frame PTS")
    pts_grid_error_ms = max(abs(t - i / FPS) * 1000 for i, t in enumerate(timestamps))
    pixels = run(["ffmpeg", "-v", "error", "-i", str(path), "-f", "rawvideo",
                  "-pix_fmt", "rgb24", "-vcodec", "rawvideo", "pipe:1"])
    frame_size = WIDTH * HEIGHT * 3
    if len(pixels) != expected * frame_size:
        raise ValueError("decoded frame count mismatch")
    observed_deltas, truth_deltas, angular_errors = [], [], []
    right_points = []
    for i in range(expected):
        frame = pixels[i * frame_size:(i + 1) * frame_size]
        lx, ly = centroid(frame, "red")
        rx, ry = centroid(frame, "blue")
        if lx >= WIDTH / 2 or rx <= WIDTH / 2:
            raise ValueError(f"point identity inconsistent with fixture at frame {i}")
        right_points.append((rx, ry))
        left_angle = math.atan2(-(ly - LEFT_CENTER[1]), lx - LEFT_CENTER[0])
        right_angle = math.atan2(-(ry - RIGHT_CENTER[1]), rx - RIGHT_CENTER[0])
        true_left, true_right = angles(i, opposed)
        observed_deltas.append(right_angle - left_angle)
        truth_deltas.append(true_right - true_left)
        for observed, truth in ((left_angle, true_left), (right_angle, true_right)):
            angular_errors.append(abs(math.atan2(math.sin(observed - truth),
                                                  math.cos(observed - truth))))
    def concentration(values: list[float]) -> float:
        return math.hypot(sum(math.cos(v) for v in values),
                          sum(math.sin(v) for v in values)) / len(values)
    r_truth, r_observed = concentration(truth_deltas), concentration(observed_deltas)
    q = q_projected(right_points)
    if abs(r_truth - r_observed) >= 0.02:
        raise ValueError("R differs from generated reference")
    if max(angular_errors) >= math.radians(2):
        raise ValueError("angular precision below fixture requirement")
    if max(abs(v - 0.5) for v in q) >= 0.02:
        raise ValueError("projected Q differs from generated reference")
    if (not opposed and r_observed <= 0.98) or (opposed and r_observed >= 0.15):
        raise ValueError("fixture relational condition not distinguishable")
    return {"file": path.name, "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "frames": expected, "fps": FPS, "q_projected_xy": q,
            "r_continuous_truth": r_truth, "r_continuous_from_pixels": r_observed,
            "r_event_only": 1.0, "max_pixel_phase_error_deg": math.degrees(max(angular_errors)),
            "pts_first_s": timestamps[0], "pts_last_s": timestamps[-1],
            "max_pts_grid_error_ms": pts_grid_error_ms}


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    results = {}
    for name, opposed in (("aligned", False), ("opposed", True)):
        path = OUT / f"{name}.mkv"
        render(path, opposed)
        results[name] = analyze(path, opposed)
    (OUT / "report.json").write_text(json.dumps(results, indent=2) + "\n")
    print(json.dumps({name: {"r_truth": value["r_continuous_truth"],
                             "r_pixels": value["r_continuous_from_pixels"],
                             "q": value["q_projected_xy"],
                             "max_angle_error_deg": value["max_pixel_phase_error_deg"]}
                      for name, value in results.items()}, indent=2))
    print(f"report={OUT / 'report.json'}")


if __name__ == "__main__":
    main()
