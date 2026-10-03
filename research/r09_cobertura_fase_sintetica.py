"""Audit R09 aggregate coverage against externally defined task-phase bins.

Requires an audited harmonic-weaver checkout and Pydantic v2. No video,
camera, service, OSC, audio, or human data are used.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path


AUDITED_SHA256 = {
    "spatial_adapter.py": "3072e4245faa653eebcc222ecbf57528ba0154ab2b2f73ff363ad084da8ec422",
    "spatial_observations.py": "c6f8f5365058680506949377a9f88d7c005f319b86f568fe6b219a50e8726381",
}


def audited_convert(checkout: Path):
    research = checkout / "src/harmonic_weaver/lab/research"
    for name, expected in AUDITED_SHA256.items():
        actual = hashlib.sha256((research / name).read_bytes()).hexdigest()
        if actual != expected:
            raise RuntimeError(f"{name} differs from audited R09 source: {actual}")
    sys.path.insert(0, str(checkout / "src"))
    from harmonic_weaver.lab.research.spatial_adapter import convert
    return convert


def request(missing_phase: int) -> dict:
    frames = []
    for index in range(8):
        phase = index // 4  # External synthetic task annotation, not an R09 field.
        joints = [
            {"index": joint, "position": [0.2 + 0.01 * joint, 0.3 + 0.01 * index],
             "confidence": 0.9, "state": "observed"}
            for joint in range(17)
        ]
        if phase == missing_phase:
            joints[0] = {"index": 0, "position": None, "confidence": 0, "state": "missing"}
        if index == 1:
            joints[1] = {"index": 1, "position": [0.21, 0.31],
                         "confidence": 0.9, "state": "held"}
        frames.append({
            "source_id": "synthetic", "stream_id": "s1", "sequence": index,
            "source_time_s": 0.1 * index, "available_monotonic_s": 10 + 0.1 * index,
            "timestamp_origin": "synthetic", "width": 640, "height": 480,
            "persons": [{"person_id": "slot1-gen1", "joints": joints}],
        })
    return {"frames": frames, "person_id": "slot1-gen1",
            "clock": {"source_clock": "synthetic", "common_clock": "synthetic",
                      "rate": 1.0, "offset_s": 0.0, "uncertainty_s": 0.0,
                      "method": "declared_assumption"}}


def joint0_by_phase(stream: dict) -> dict:
    report = {"phase_0": {"observed": 0, "missing": 0},
              "phase_1": {"observed": 0, "missing": 0}}
    for frame in stream["frames"]:
        phase = f"phase_{frame['index'] // 4}"  # Supplied separately from R09.
        state = next(point["state"] for point in frame["points"]
                     if point["label"] == "joint-0")
        report[phase][state] += 1
    return report


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--weaver-repo", type=Path, required=True)
    args = parser.parse_args()
    checkout = args.weaver_repo.resolve()
    convert = audited_convert(checkout)
    cases = {}
    for missing_phase in (0, 1):
        result = convert(request(missing_phase))
        stream = result["stream"]
        assert all("phase" not in frame for frame in stream["frames"])
        assert "phase" not in stream
        assert stream["frames"][1]["points"][1]["state"] == "held"
        cases[f"missing_in_phase_{missing_phase}"] = {
            "R09_aggregate_coverage": result["coverage"],
            "external_joint0_by_phase": joint0_by_phase(stream),
        }

    first, second = cases.values()
    assert first["R09_aggregate_coverage"] == second["R09_aggregate_coverage"]
    assert first["R09_aggregate_coverage"] == {
        "observed": 131, "held": 1, "inferred": 0, "missing": 4}
    assert first["external_joint0_by_phase"] == {
        "phase_0": {"observed": 0, "missing": 4},
        "phase_1": {"observed": 4, "missing": 0}}
    assert second["external_joint0_by_phase"] == {
        "phase_0": {"observed": 4, "missing": 0},
        "phase_1": {"observed": 0, "missing": 4}}

    revision = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=checkout, text=True).strip()
    print(json.dumps({"kind": "synthetic_R09_phase_coverage_audit",
                      "weaver_revision": revision, "cases": cases,
                      "limit": "R09 retains point states; task phase is external. No camera or human inference."},
                     ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
