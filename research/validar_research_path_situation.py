#!/usr/bin/env python3
"""Valida invariantes del sobre sintético; no valida pose ni calibración."""

from __future__ import annotations

import copy
import json
import math
from pathlib import Path

from situacion_recorrido_sintetica import describe_gated


FIXTURE = Path(__file__).with_name("research_path_situation.synthetic.jsonl")
REASONS = {"insufficient_samples", "missing_or_untrusted_sample",
           "nonfinite_timestamp", "nonmonotonic_timestamp", "temporal_gap",
           "invalid_geometry"}


def finite_number(value: object) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def nonempty(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def validate(record: dict) -> None:
    require(isinstance(record, dict), "record")
    require(record.get("kind") == "path_situation_geometry", "kind")
    require(record.get("schema_version") == "0.1-synthetic", "schema_version")
    for key in ("session_id", "stream_id", "algorithm_version", "source_clock_id",
                "session_clock_id", "clock_map_id"):
        require(nonempty(record.get(key)), key)
    require(isinstance(record.get("source_frame_id"), int)
            and not isinstance(record["source_frame_id"], bool)
            and record["source_frame_id"] >= 0, "source_frame_id")
    require(isinstance(record.get("person_slot"), int)
            and not isinstance(record["person_slot"], bool)
            and record["person_slot"] >= 0, "person_slot")
    digest = record.get("input_manifest_sha256")
    require(isinstance(digest, str) and len(digest) == 64
            and all(c in "0123456789abcdef" for c in digest), "input_manifest_sha256")
    require(record.get("source_time_kind") == "synthetic"
            and record.get("availability_time_kind") == "logical_replay"
            and record["source_clock_id"] == record["session_clock_id"], "synthetic clock")
    times = [record.get(k) for k in ("window_start_us", "window_end_us",
                                        "source_time_us", "available_at_us")]
    require(all(isinstance(t, int) and not isinstance(t, bool) for t in times)
            and times[0] < times[1] == times[2] <= times[3], "window/clock order")

    definition = record.get("definition")
    require(isinstance(definition, dict), "definition")
    for key in ("point_id", "origin_id", "frame_id"):
        require(nonempty(definition.get(key)), "definition." + key)
    require(definition.get("path_definition") == "3d_polyline", "path_definition")
    require(finite_number(definition.get("reach_L")) and definition["reach_L"] > 0,
            "reach_L")

    quality = record.get("quality")
    require(isinstance(quality, dict), "quality")
    count, trusted = quality.get("samples"), quality.get("trusted_samples")
    require(isinstance(count, int) and not isinstance(count, bool) and count >= 0
            and isinstance(trusted, int) and not isinstance(trusted, bool)
            and 0 <= trusted <= count, "sample counts")
    max_gap, seen_gap = quality.get("max_gap_us"), quality.get("observed_max_gap_us")
    require(isinstance(max_gap, int) and not isinstance(max_gap, bool) and max_gap > 0
            and isinstance(seen_gap, int) and not isinstance(seen_gap, bool)
            and seen_gap >= 0, "gap")

    uncertainty = record.get("uncertainty")
    require(uncertainty == {"status": "not_estimated", "rho_min_abs_bound": None},
            "uncertainty")
    status, metrics, reason = record.get("status"), record.get("metrics"), record.get("reason")
    if status == "computed_candidate":
        require(reason is None and count >= 2 and count == trusted
                and 0 < seen_gap <= max_gap, "valid gate")
        require(isinstance(metrics, dict), "valid metrics")
        for key in ("rho_min", "rho_max", "radial_variation_over_path_length",
                    "path_length_L"):
            require(finite_number(metrics.get(key)), key)
        require(0 <= metrics["rho_min"] <= metrics["rho_max"]
                and 0 <= metrics["radial_variation_over_path_length"] <= 1.000001
                and metrics["path_length_L"] > 0, "metric bounds")
    else:
        require(status == "invalid" and reason in REASONS and metrics is None,
                "invalid must have reason and null metrics")
        if reason == "missing_or_untrusted_sample":
            require(trusted < count, "missing reason without missing samples")
        if reason == "temporal_gap":
            require(seen_gap > max_gap, "temporal reason without gap")
        if reason == "insufficient_samples":
            require(count < 2, "insufficient reason without low count")


def main() -> None:
    records = [json.loads(line) for line in FIXTURE.read_text().splitlines() if line.strip()]
    require(len(records) == 2, "fixture count")
    keys = set()
    for record in records:
        validate(record)
        key = (record["session_id"], record["stream_id"], record["source_frame_id"],
               record["person_slot"], record["kind"])
        require(key not in keys, "duplicate source identity")
        keys.add(key)

    curve = [(-1.0, 1.0, 0.0), (0.0, 0.0, 0.0), (1.0, 1.0, 0.0)]
    result = describe_gated(curve, (0.0, 0.0, 0.0), 1.0,
                            [True] * 3, [0.0, 0.01, 0.02], 0.015)
    expected = dict(result["metrics"])
    expected.pop("Q")  # Q viaja por un canal independiente.
    expected["path_length_L"] = expected.pop("path_length")
    require(expected == records[0]["metrics"], "fixture does not match geometry")
    missing = describe_gated(curve, (0.0, 0.0, 0.0), 1.0,
                             [True, False, True], [0.01, 0.02, 0.03], 0.015)
    require(records[1]["status"] == missing["status"]
            and records[1]["reason"] == missing["reason"], "invalid fixture mismatch")

    mutation_count = 0
    for edit in (
        lambda r: r["quality"].update(trusted_samples=2),
        lambda r: r["quality"].update(observed_max_gap_us=16000),
        lambda r: r["metrics"].update(rho_min=2.0),
        lambda r: r["metrics"].update(rho_min=float("nan")),
        lambda r: r.update(available_at_us=19000),
        lambda r: r["definition"].update(reach_L=0),
        lambda r: r["uncertainty"].update(rho_min_abs_bound=0.01),
    ):
        mutated = copy.deepcopy(records[0])
        edit(mutated)
        try:
            validate(mutated)
        except ValueError:
            mutation_count += 1
        else:
            raise AssertionError("a malformed candidate passed validation")
    invalid_with_value = copy.deepcopy(records[1])
    invalid_with_value["metrics"] = records[0]["metrics"]
    try:
        validate(invalid_with_value)
    except ValueError:
        mutation_count += 1
    else:
        raise AssertionError("invalid record carried metrics")
    print(json.dumps({"kind": "synthetic_contract_validation_only",
                      "records": len(records), "rejected_mutations": mutation_count}))


if __name__ == "__main__":
    main()
