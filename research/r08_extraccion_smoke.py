#!/usr/bin/env python3
"""Audit Weaver pixel candidates on the synthetic R08 video.

Usage: python research/r08_extraccion_smoke.py /path/to/harmonic-weaver
The seeds are taken from the known synthetic drawing, not found automatically.
No human video, cameras, live services, or accepted rope annotations are used.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from io import BytesIO
from pathlib import Path

from r08_sonido_diagnostico import HEIGHT, OUTPUT, WIDTH, projected_tensor


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("weaver_checkout", type=Path)
    args = parser.parse_args()
    source = args.weaver_checkout / "src"
    if not source.is_dir():
        parser.error("Weaver checkout must contain src/")
    sys.path.insert(0, str(source))

    import numpy as np
    from PIL import Image
    from harmonic_weaver.lab.research.rope_mask import propose as propose_mask
    from harmonic_weaver.lab.research.rope_media import frame_png, probe
    from harmonic_weaver.lab.research.rope_path import propose as propose_path

    video = OUTPUT / "curva_proyectada_sintetica.mp4"
    fixture = json.loads((OUTPUT / "annotation_sintetica_test.json").read_text())
    media = probe(video)
    assert media["media_sha256"] == hashlib.sha256(video.read_bytes()).hexdigest()
    assert fixture["media_sha256"] == media["media_sha256"]
    assert (fixture["width_px"], fixture["height_px"]) == (WIDTH, HEIGHT)

    assert len(media["frame_times_s"]) == len(fixture["frames"]) == 75
    candidates_by_frame = {}
    for index in range(75):
        assert abs(media["frame_times_s"][index] - fixture["frames"][index]["time_s"]) < 1e-6
        rgb = np.asarray(Image.open(BytesIO(frame_png(
            video, index, media["media_sha256"]
        ))).convert("RGB"))
        candidates = propose_mask(rgb, {
            "target_rgb": [255, 255, 255], "distance_rgb": 40,
            "min_component_px": 100, "max_components": 4,
        })
        expected_gap = 30 <= index < 45
        assert candidates["components_detected"] == (0 if expected_gap else 1)
        assert [component["area_px"] for component in candidates["candidate_components"]] == (
            [] if expected_gap else [1536]
        )
        if index in (0, 37, 45):
            candidates_by_frame[index] = candidates
    print("75 decoded frames: 60 with one 1536-px white candidate; "
          "15 gap frames with none")

    # These positions are supplied from the drawing recipe. An operator would
    # have to select and independently review analogous seeds for real footage.
    cases = (
        (0, "horizontal", (770.5, 539.5), (1149.5, 539.5), 540.0),
        (37, "unidentifiable", None, None, None),
        (45, "vertical", (959.5, 350.5), (959.5, 729.5), 960.0),
    )
    for index, kind, start, stop, reference_axis in cases:
        candidates = candidates_by_frame[index]
        if kind == "unidentifiable":
            assert candidates["components_detected"] == 0
            assert candidates["candidate_components"] == []
            assert projected_tensor(fixture["frames"][index]) is None
            print(f"frame {index}: no white candidate; no curve or tensor")
            continue

        assert candidates["components_detected"] == 1
        component = candidates["candidate_components"][0]
        assert component["area_px"] == 1536
        candidates.update(media_sha256=media["media_sha256"],
                          frame_index=index, time_s=media["frame_times_s"][index])
        settings = {
            "component_id": component["component_id"],
            "start": {"x": start[0] / WIDTH, "y": start[1] / HEIGHT},
            "stop": {"x": stop[0] / WIDTH, "y": stop[1] / HEIGHT},
        }
        proposal = propose_path(candidates, settings)
        assert proposal["supported"] and len(proposal["points"]) == 380
        xy = np.array([[point["x"] * WIDTH, point["y"] * HEIGHT]
                       for point in proposal["points"]])
        transverse = xy[:, 1] if kind == "horizontal" else xy[:, 0]
        max_perpendicular_error = float(np.max(np.abs(transverse - reference_axis)))
        assert max_perpendicular_error == 0.5
        assert np.allclose(xy[0], start) and np.allclose(xy[-1], stop)

        # M2 is computed from the candidate path, then compared to the
        # separately specified orientation of the drawn synthetic line.
        candidate_tensor = projected_tensor({
            "state": "observed", "visible_segments": [proposal["points"]]
        })
        assert candidate_tensor is not None
        expected_xx = 1.0 if kind == "horizontal" else 0.0
        assert abs(candidate_tensor["m_xx"] - expected_xx) < 1e-12
        assert abs(candidate_tensor["m_xy"]) < 1e-12
        assert abs(candidate_tensor["visible_length_px"] - 379.0) < 1e-9
        print(f"frame {index}: one {component['area_px']}-px candidate; "
              f"seeded path {len(xy)} points / 379 px; "
              f"perpendicular error {max_perpendicular_error:.1f} px; "
              f"M2 xx={candidate_tensor['m_xx']:.0f}")

    print("Candidate paths require synthetic truth seeds and manual review; "
          "the existing WAV is generated from the fixture annotation, not these paths.")


if __name__ == "__main__":
    main()
