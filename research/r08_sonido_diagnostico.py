#!/usr/bin/env python3
"""Synthetic image-plane rope geometry to a diagnostic stereo WAV.

This is neither an R08 media/annotation validator nor Beacon/Shaper audio.
There are no cameras, participant data, biomechanical frequencies or ratings.
"""

from __future__ import annotations

import hashlib
import json
import math
import struct
import wave
from pathlib import Path


HERE = Path(__file__).resolve().parent
OUTPUT = HERE / "datos_sinteticos_r08"
WIDTH, HEIGHT = 1920, 1080
FPS = 30
SAMPLE_RATE = 22050
TONE_HZ = 220
PEAK = 10000
SEGMENTS = (("horizontal", 30), ("invalid", 15), ("vertical", 30))


def synthetic_frame(kind: str) -> dict:
    if kind == "invalid":
        return {"state": "unidentifiable", "visible_segments": [],
                "causes": ["occlusion"]}
    if kind == "horizontal":
        points = [{"x": 0.4, "y": 0.5}, {"x": 0.6, "y": 0.5}]
    elif kind == "vertical":
        half_height = 192 / HEIGHT
        points = [{"x": 0.5, "y": 0.5 - half_height},
                  {"x": 0.5, "y": 0.5 + half_height}]
    else:
        raise ValueError(kind)
    return {"state": "observed", "visible_segments": [points], "causes": []}


def synthetic_annotation() -> dict:
    """Schema-shaped test input; 'manual' and hash are synthetic sentinels."""
    kinds = [kind for kind, count in SEGMENTS for _ in range(count)]
    return {
        "schema_version": 1,
        "media_sha256": hashlib.sha256(b"SYNTHETIC_NO_MEDIA").hexdigest(),
        "width_px": WIDTH,
        "height_px": HEIGHT,
        "method": "manual",  # Required by R08 v1; not human provenance here.
        "coordinate_frame": "image_normalized",
        "frames": [
            {"frame_index": index, "time_s": index / FPS, **synthetic_frame(kind)}
            for index, kind in enumerate(kinds)
        ],
    }


def projected_tensor(frame: dict) -> dict | None:
    """Length-weighted, signless 2D line tensor on visible polylines only."""
    if frame["state"] in ("absent", "unidentifiable"):
        return None
    m_xx = m_xy = m_yy = length = 0.0
    for polyline in frame["visible_segments"]:
        for a, b in zip(polyline, polyline[1:]):
            dx = (b["x"] - a["x"]) * WIDTH
            dy = (b["y"] - a["y"]) * HEIGHT
            ds = math.hypot(dx, dy)
            if ds == 0:
                continue
            length += ds
            m_xx += dx * dx / ds
            m_xy += dx * dy / ds
            m_yy += dy * dy / ds
    if length == 0:
        return None
    xx = min(1.0, max(0.0, m_xx / length))
    return {"m_xx": xx, "m_xy": m_xy / length,
            "m_yy": 1.0 - xx, "visible_length_px": length,
            "support": frame["state"]}


def rms(values: list[int]) -> float:
    return math.sqrt(sum(value * value for value in values) / len(values))


def render_diagnostic_wav(tensors: list[dict | None], wav_path: Path) -> list[dict]:
    """Render the fixed stereo M2 diagnostic; return RMS by synthetic segment.

    The caller declares tensor provenance. This renderer does not validate an
    R08 annotation or identify a rope, and its 220 Hz carrier is arbitrary.
    """
    assert len(tensors) == sum(count for _, count in SEGMENTS) == 75
    samples = bytearray()
    left_values: list[list[int]] = [[] for _ in SEGMENTS]
    right_values: list[list[int]] = [[] for _ in SEGMENTS]
    boundaries = (0, 30, 45, 75)
    for sample_index in range(len(tensors) * SAMPLE_RATE // FPS):
        frame_index = sample_index * FPS // SAMPLE_RATE
        region = next(i for i in range(len(SEGMENTS)) if frame_index < boundaries[i + 1])
        tensor = tensors[frame_index]
        if tensor is None:
            left = right = 0
        else:
            local_time = sample_index / SAMPLE_RATE - boundaries[region] / FPS
            remaining = boundaries[region + 1] / FPS - sample_index / SAMPLE_RATE
            fade = max(0.0, min(1.0, local_time / 0.02, remaining / 0.02))
            carrier = math.sin(2 * math.pi * TONE_HZ * sample_index / SAMPLE_RATE)
            left = round(PEAK * fade * tensor["m_xx"] * carrier)
            right = round(PEAK * fade * tensor["m_yy"] * carrier)
        left_values[region].append(left)
        right_values[region].append(right)
        samples.extend(struct.pack("<hh", left, right))

    wav_path.parent.mkdir(exist_ok=True)
    with wave.open(str(wav_path), "wb") as wav:
        wav.setnchannels(2)
        wav.setsampwidth(2)
        wav.setframerate(SAMPLE_RATE)
        wav.writeframes(samples)
    assert rms(left_values[0]) > 6000 and rms(right_values[0]) == 0
    assert rms(left_values[1]) == rms(right_values[1]) == 0
    assert rms(left_values[2]) == 0 and rms(right_values[2]) > 6000
    return [
        {"kind": kind, "frames": count, "duration_s": count / FPS,
         "left_rms_pcm16": rms(left_values[i]),
         "right_rms_pcm16": rms(right_values[i])}
        for i, (kind, count) in enumerate(SEGMENTS)
    ]


def main() -> None:
    # Generate and read the exact synthetic video-bound annotation before audio.
    from r08_video_sintetico import generate

    video_path, annotation_path = generate()
    annotation = json.loads(annotation_path.read_text(encoding="utf-8"))
    assert annotation["media_sha256"] == hashlib.sha256(video_path.read_bytes()).hexdigest()
    assert (annotation["width_px"], annotation["height_px"]) == (WIDTH, HEIGHT)
    horizontal = projected_tensor(synthetic_frame("horizontal"))
    vertical = projected_tensor(synthetic_frame("vertical"))
    invalid = projected_tensor(synthetic_frame("invalid"))
    assert horizontal is not None and vertical is not None and invalid is None
    assert abs(horizontal["visible_length_px"] - 384) < 1e-9
    assert abs(vertical["visible_length_px"] - 384) < 1e-9
    assert abs(horizontal["m_xx"] - 1) < 1e-12 and horizontal["m_yy"] == 0
    assert vertical["m_xx"] == 0 and abs(vertical["m_yy"] - 1) < 1e-12

    # Reversing vertex order cannot change a signless line descriptor.
    reversed_frame = synthetic_frame("horizontal")
    reversed_frame["visible_segments"][0].reverse()
    assert projected_tensor(reversed_frame) == horizontal

    # A partial annotation keeps two visible fragments separate; no gap bridge.
    partial = {"state": "partial", "causes": ["occlusion"],
               "visible_segments": [
                   [{"x": 0.2, "y": 0.5}, {"x": 0.3, "y": 0.5}],
                   [{"x": 0.7, "y": 0.5}, {"x": 0.8, "y": 0.5}],
               ]}
    partial_result = projected_tensor(partial)
    assert partial_result is not None
    assert abs(partial_result["visible_length_px"] - 384) < 1e-9
    assert partial_result["support"] == "partial"

    # Equal changes in normalized x/y are not a 45-degree pixel direction.
    diagonal = {"state": "observed", "causes": [], "visible_segments": [[
        {"x": 0.4, "y": 0.4}, {"x": 0.5, "y": 0.5},
    ]]}
    diagonal_result = projected_tensor(diagonal)
    assert diagonal_result is not None
    assert abs(diagonal_result["m_xx"] - 192**2 / (192**2 + 108**2)) < 1e-12

    frames = annotation["frames"]
    tensors = [projected_tensor(frame) for frame in frames]
    OUTPUT.mkdir(exist_ok=True)
    wav_path = OUTPUT / "curva_proyectada_gap.wav"
    segments = render_diagnostic_wav(tensors, wav_path)

    manifest = {
        "kind": "synthetic_projected_rope_audio_diagnostic",
        "not": ["human R08 annotation", "geometric validation from pixels",
                "HarMoCAP audio", "Weaver audio", "Beacon audio",
                "human movement", "Laban validation", "HIT validation"],
        "image_px": [WIDTH, HEIGHT], "fps": FPS,
        "video_sha256": annotation["media_sha256"],
        "annotation_sha256": hashlib.sha256(annotation_path.read_bytes()).hexdigest(),
        "annotation_provenance": "programmatic synthetic fixture; method=manual is R08 v1 schema token",
        "sample_rate_hz": SAMPLE_RATE, "tone_hz": TONE_HZ,
        "mapping": "left_gain=m_xx; right_gain=m_yy; invalid=both_zero",
        "segments": segments,
        "horizontal": horizontal, "vertical": vertical,
        "partial_visible_only": partial_result,
        "diagonal": diagonal_result,
        "wav_sha256": hashlib.sha256(wav_path.read_bytes()).hexdigest(),
    }
    (OUTPUT / "manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(wav_path)


if __name__ == "__main__":
    main()
