#!/usr/bin/env python3
"""Check the synthetic audio frames against a local Weaver R08 checkout.

Usage: python research/r08_contrato_smoke.py /path/to/harmonic-weaver
Requires Weaver's Python dependencies; no media, services or cameras are used.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from r08_sonido_diagnostico import OUTPUT, projected_tensor, synthetic_frame


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("weaver_checkout", type=Path)
    args = parser.parse_args()
    source = args.weaver_checkout / "src"
    if not source.is_dir():
        parser.error("Weaver checkout must contain src/")
    sys.path.insert(0, str(source))

    from harmonic_weaver.lab.research.rope_annotations import Annotation, report
    from harmonic_weaver.lab.research.rope_media import bind

    import json

    fixture = json.loads((OUTPUT / "annotation_sintetica_test.json").read_text())
    video = OUTPUT / "curva_proyectada_sintetica.mp4"
    checked = Annotation.model_validate(fixture)
    media = bind(checked, video)
    assert len(media["frame_times_s"]) == 75
    rows = report(checked)["rows"]
    assert len(rows) == 75
    assert all(row["visible_projected_length_px"] is None for row in rows[30:45])
    assert all(abs(row["visible_projected_length_px"] - 384) < 1e-9
               for row in rows[:30] + rows[45:])
    assert all(projected_tensor(fixture["frames"][i]) is None for i in range(30, 45))

    wrong_clock = {**fixture, "frames": [dict(frame) for frame in fixture["frames"]]}
    wrong_clock["frames"][45]["time_s"] += 0.01
    try:
        bind(wrong_clock, video)
    except ValueError:
        pass
    else:
        raise AssertionError("R08 accepted an annotation shifted off source PTS")

    wrong_media = {**fixture, "media_sha256": "0" * 64}
    try:
        bind(wrong_media, video)
    except ValueError:
        pass
    else:
        raise AssertionError("R08 accepted an annotation bound to another media hash")

    bad = {**fixture, "frames": [{
        "frame_index": 0, "time_s": 0,
        **{**synthetic_frame("horizontal"), "state": "unidentifiable",
           "causes": ["occlusion"]},
    }]}
    try:
        Annotation.model_validate(bad)
    except ValueError:
        pass
    else:
        raise AssertionError("R08 accepted a visible curve in an unidentifiable frame")
    print("R08 schema/bind/report: 75 synthetic video frames accepted")
    print("Invalid curve, shifted PTS and wrong media hash rejected")
    print("method=manual is a synthetic test sentinel, not human provenance")


if __name__ == "__main__":
    main()
