#!/usr/bin/env python3
"""Generate a tiny synthetic MP4 and schema-shaped R08 test annotation.

The video and points are programmatically constructed; method=manual is only
the required R08 v1 schema token, never a claim of a human annotation. The
black gap tests unavailable support; it is not a physical occlusion model.
"""

from __future__ import annotations

import hashlib
import json
import math
import subprocess
from pathlib import Path

from r08_sonido_diagnostico import FPS, HEIGHT, OUTPUT, WIDTH, synthetic_annotation


VIDEO = OUTPUT / "curva_proyectada_sintetica.mp4"
ANNOTATION = OUTPUT / "annotation_sintetica_test.json"


def generate() -> tuple[Path, Path]:
    OUTPUT.mkdir(exist_ok=True)
    duration = 75 / FPS
    video_filter = (
        "drawbox=x=768:y=538:w=384:h=4:color=white:t=fill:enable='between(n,0,29)',"
        "drawbox=x=958:y=348:w=4:h=384:color=white:t=fill:enable='between(n,45,74)'"
    )
    subprocess.run([
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-f", "lavfi", "-i",
        f"color=c=black:s={WIDTH}x{HEIGHT}:r={FPS}:d={duration}",
        "-vf", video_filter, "-c:v", "libx264", "-preset", "veryfast",
        "-crf", "24", "-pix_fmt", "yuv420p", "-movflags", "+faststart",
        "-y", str(VIDEO),
    ], check=True, capture_output=True)
    probed = subprocess.run([
        "ffprobe", "-v", "error", "-select_streams", "v:0", "-show_frames",
        "-show_entries", "frame=best_effort_timestamp_time", "-of", "json",
        str(VIDEO),
    ], check=True, capture_output=True, text=True)
    pts = [float(frame["best_effort_timestamp_time"])
           for frame in json.loads(probed.stdout)["frames"]]
    assert len(pts) == 75 and all(math.isfinite(value) for value in pts)
    times = [value - pts[0] for value in pts]
    assert all(b > a for a, b in zip(times, times[1:]))
    annotation = synthetic_annotation()
    annotation["media_sha256"] = hashlib.sha256(VIDEO.read_bytes()).hexdigest()
    for frame, time_s in zip(annotation["frames"], times):
        frame["time_s"] = time_s
    # Keep one decoded frame per line so a review does not bury the contract.
    header = [
        f"  {json.dumps(key)}: {json.dumps(value, ensure_ascii=False)}"
        for key, value in annotation.items() if key != "frames"
    ]
    frame_lines = [
        "    " + json.dumps(frame, ensure_ascii=False, sort_keys=True,
                             separators=(",", ":"))
        for frame in annotation["frames"]
    ]
    ANNOTATION.write_text(
        "{\n" + ",\n".join(header) + ',\n  "frames": [\n'
        + ",\n".join(frame_lines) + "\n  ]\n}\n", encoding="utf-8"
    )
    return VIDEO, ANNOTATION


if __name__ == "__main__":
    print(*generate(), sep="\n")
