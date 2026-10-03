"""Check continuity of proposed Q_live research records across a stream.

This checks a synthetic research envelope, not HarMoCAP, Weaver, OSC, or
beacon-spatial. A per-record schema cannot see a mixed-definition window.
"""

import copy
import json
from pathlib import Path

from validar_research_plane_q import SCHEMA, FIXTURE, validate


SEMANTIC_FIELDS = (
    "algorithm_version",
    "input_manifest_sha256",
    "calibration_version",
    "body_frame_version",
    "path_definition",
    "segment_definition",
    "window_seconds",
)
CLOCK_FIELDS = (
    "source_clock_id",
    "source_time_kind",
    "clock_map_id",
    "session_clock_id",
    "availability_time_kind",
)


def fingerprint(record):
    return tuple(record[key] for key in SEMANTIC_FIELDS) + tuple(
        record["clock"][key] for key in CLOCK_FIELDS
    )


class QStreamGate:
    def __init__(self, schema):
        self.schema = schema
        self.states = {}

    def accept(self, record):
        validate(record, self.schema)
        key = tuple(record[name] for name in (
            "session_id", "stream_id", "slot_id", "signal_name"
        ))
        clock = record["clock"]
        current = fingerprint(record)
        previous = self.states.get(key)
        boundary = None
        if previous is not None:
            if clock["session_clock_id"] != previous["session_clock_id"]:
                raise ValueError("session_clock_id cambió dentro de la sesión")
            if record["source_frame_id"] <= previous["source_frame_id"]:
                raise ValueError("source_frame_id repetido o retrocedido")
            if clock["available_at_us"] < previous["available_at_us"]:
                raise ValueError("disponibilidad retrocedida")
            if clock["feature_window_end_us"] < previous["feature_window_end_us"]:
                raise ValueError("ventana retrocedida")
            if current == previous["fingerprint"] and (
                clock["source_time_us"] <= previous["source_time_us"]
            ):
                raise ValueError("tiempo fuente repetido o retrocedido")
            if current != previous["fingerprint"] and not (
                record["status"] == "invalid"
                and record["invalid_reason"] == "transition"
            ):
                raise ValueError("cambio semántico sin emisión invalid/transition")
            boundary = previous["reset_boundary_us"]
            if record["status"] == "estimated_valid" and boundary is not None:
                if clock["feature_window_start_us"] < boundary:
                    raise ValueError("ventana válida cruza un reset anterior")
                boundary = None
        if record["status"] == "invalid":
            # Use the moment the reset becomes available, not an older sample's
            # window end. This deliberately requires a fresh post-reset window.
            boundary = clock["available_at_us"]
        self.states[key] = {
            "fingerprint": current,
            "source_frame_id": record["source_frame_id"],
            "session_clock_id": clock["session_clock_id"],
            "source_time_us": clock["source_time_us"],
            "feature_window_end_us": clock["feature_window_end_us"],
            "available_at_us": clock["available_at_us"],
            "reset_boundary_us": boundary,
        }
        return "reset_candidate" if record["status"] == "invalid" else "value_candidate"


def shifted(record, frame_id, end_us):
    result = copy.deepcopy(record)
    result["source_frame_id"] = frame_id
    result["clock"]["source_time_us"] = end_us
    result["clock"]["feature_window_start_us"] = end_us - 1_000_000
    result["clock"]["feature_window_end_us"] = end_us
    result["clock"]["last_observation_us"] = end_us
    result["clock"]["available_at_us"] = end_us + 1_000
    return result


def fixture():
    schema = json.loads(Path(SCHEMA).read_text())
    base = json.loads(Path(FIXTURE).read_text().splitlines()[0])
    changed = shifted(base, 121, 1_008_333)
    changed["path_definition"] = "waist_relative_step_body_axes"
    transition = copy.deepcopy(changed)
    transition["status"] = "invalid"
    transition["invalid_reason"] = "transition"
    transition["q_lateral_up_front"] = None
    transition["coverage"]["arc_L"] = 0.0
    transition["coverage"]["segments"] = 0
    recovered = shifted(changed, 242, 2_010_000)
    recovered["clock"]["feature_window_start_us"] = transition["clock"]["available_at_us"]
    recovered["clock"]["feature_window_end_us"] = recovered["clock"]["feature_window_start_us"] + 1_000_000
    recovered["clock"]["source_time_us"] = recovered["clock"]["feature_window_end_us"]
    recovered["clock"]["last_observation_us"] = recovered["clock"]["feature_window_end_us"]
    recovered["clock"]["available_at_us"] = recovered["clock"]["feature_window_end_us"] + 1_000
    return schema, base, changed, transition, recovered


def run_sequence(schema, records):
    gate = QStreamGate(schema)
    return [gate.accept(record) for record in records]


def main():
    schema, base, changed, transition, recovered = fixture()
    good = run_sequence(schema, [base, transition, recovered])
    assert good == ["value_candidate", "reset_candidate", "value_candidate"]
    stale_recovery = copy.deepcopy(recovered)
    stale_recovery["clock"]["feature_window_start_us"] = transition["clock"]["feature_window_end_us"]
    stale_recovery["clock"]["feature_window_end_us"] = stale_recovery["clock"]["feature_window_start_us"] + 1_000_000
    stale_recovery["clock"]["source_time_us"] = stale_recovery["clock"]["feature_window_end_us"]
    stale_recovery["clock"]["last_observation_us"] = stale_recovery["clock"]["feature_window_end_us"]
    stale_recovery["clock"]["available_at_us"] = stale_recovery["clock"]["feature_window_end_us"] + 1_000
    wrong_clock = copy.deepcopy(transition)
    wrong_clock["clock"]["session_clock_id"] = "another_time_domain"
    adversarial = {
        "path_change_without_reset": ([base, changed], "cambio semántico"),
        "recovery_with_old_window": ([base, transition, stale_recovery], "cruza un reset"),
        "duplicate_source_frame": ([base, shifted(base, 120, 1_008_333)], "source_frame_id"),
        "session_clock_switch": ([base, wrong_clock], "session_clock_id cambió"),
    }
    rejected = []
    for name, (records, expected_message) in adversarial.items():
        # Ensure every adversarial item is individually schema-valid. Only
        # sequence-level validation should reject it.
        for record in records:
            validate(record, schema)
        try:
            run_sequence(schema, records)
        except ValueError as error:
            if expected_message not in str(error):
                raise AssertionError(f"rechazo inesperado en {name}: {error}") from error
            rejected.append(name)
        else:
            raise AssertionError(f"secuencia adversa aceptada: {name}")
    print(json.dumps({
        "scope": "synthetic_research_envelope_sequence_gate_not_live_audio",
        "accepted_actions": good,
        "rejected_sequences": rejected,
        "reset_boundary_us": transition["clock"]["available_at_us"],
        "recovered_window_start_us": recovered["clock"]["feature_window_start_us"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
