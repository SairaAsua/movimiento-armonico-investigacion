#!/usr/bin/env python3
"""Check the synthetic audio frames against a local Weaver R08 checkout.

Usage: python research/r08_contrato_smoke.py /path/to/harmonic-weaver
Requires Weaver's Python dependencies; no media, services or cameras are used.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from r08_sonido_diagnostico import projected_tensor, synthetic_annotation, synthetic_frame


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("weaver_checkout", type=Path)
    args = parser.parse_args()
    source = args.weaver_checkout / "src"
    if not source.is_dir():
        parser.error("Weaver checkout must contain src/")
    sys.path.insert(0, str(source))

    from harmonic_weaver.lab.research.rope_annotations import Annotation, report

    fixture = synthetic_annotation()
    checked = Annotation.model_validate(fixture)
    rows = report(checked)["rows"]
    assert len(rows) == 75
    assert all(row["visible_projected_length_px"] is None for row in rows[30:45])
    assert all(abs(row["visible_projected_length_px"] - 384) < 1e-9
               for row in rows[:30] + rows[45:])
    assert all(projected_tensor(fixture["frames"][i]) is None for i in range(30, 45))

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
    print("R08 schema/report: 75 synthetic frames accepted; invalid curve rejected")
    print("No media binding: synthetic hash and required method=manual are test sentinels")


if __name__ == "__main__":
    main()
