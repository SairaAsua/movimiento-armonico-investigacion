"""Exporta una transición invalid→valid de Q sobre C3D CMU al sobre local.

Requiere numpy y ezc3d. Los tiempos son nominales/lógicos, no timestamps
ópticos ni latencia medida. La toma es danza sin soga y no pertenece a Nico.
"""

from collections import deque
import hashlib
import json
from pathlib import Path

from cmu_causal_c_replay import FPS, body_trajectories
from cmu_danza_05_02_audit import EXPECTED_SHA256
from cmu_q_live_replay import MIN_ARC_L, MIN_SEGMENTS, estimate, segments
from validar_research_plane_q import SCHEMA, validate

HERE = Path(__file__).resolve().parent
MANIFEST = HERE / "research_plane_q.cmu05_02_manifest.json"
OUTPUT = HERE / "research_plane_q.cmu05_02.jsonl"


def record(frame_id, window, manifest_hash):
    value = estimate(window)
    arc = sum(item[1] for item in window)
    end_us = round(frame_id * 1_000_000 / FPS)
    last_us = round(window[-1][0] * 1_000_000 / FPS) if window else None
    return {
        "contract_id": "ropeflow.research.plane_q.v0",
        "session_id": "cmu_public_05_02",
        "stream_id": "cmu_05_02_left_wrist_co_rotating",
        "source_frame_id": frame_id,
        "slot_id": 0,
        "signal_name": "plane_normal_Q_live",
        "algorithm_version": "cmu_q_live_replay_v0",
        "input_manifest_sha256": manifest_hash,
        "calibration_version": "median_shoulder_span_frames_0_119_v0",
        "body_frame_version": "shoulder_waist_co_rotating_per_frame_unfiltered_v0",
        "path_definition": "co_rotating",
        "segment_definition": "mean_LWRA_LWRB_minus_waist_midpoint",
        "window_seconds": 1.0,
        "clock": {
            "source_clock_id": "cmu_nominal_120hz_us",
            "source_time_us": end_us,
            "source_time_kind": "sample_index_nominal",
            "clock_map_id": "cmu_index_to_logical_120hz_round_v0",
            "session_clock_id": "cmu_replay_logical_us",
            "feature_window_start_us": end_us - 1_000_000,
            "feature_window_end_us": end_us,
            "last_observation_us": last_us,
            "available_at_us": end_us,
            "availability_time_kind": "logical_replay",
        },
        "coverage": {
            "arc_L": arc,
            "segments": len(window),
            "min_arc_L": MIN_ARC_L,
            "min_segments": MIN_SEGMENTS,
            "max_age_us": 100_000,
        },
        "uncertainty": {
            "status": "not_estimated",
            "max_angle_error_deg": None,
            "length_weight_tv_bound": None,
            "missing_arc_fraction_max": None,
            "q_component_abs_bound": None,
            "validation_profile_id": None,
        },
        "status": "estimated_valid" if value is not None else "invalid",
        "invalid_reason": None if value is not None else "insufficient_arc",
        "q_lateral_up_front": value[0].tolist() if value is not None else None,
    }


def main():
    scale, trajectories = body_trajectories()  # verifica SHA y marcadores
    manifest = {
        "source": "CMU mocap subject 05 trial 02; danza, no rope flow",
        "source_file": "sources/cmu_mocap/05_02.c3d",
        "source_sha256": EXPECTED_SHA256,
        "nominal_fps": FPS,
        "scale_first_second_mm": scale,
        "clock_basis": "índice de muestra / FPS nominal; sin timestamps ópticos ni latencia medida",
        "algorithm": "cmu_q_live_replay.py, segments/estimate, mano izquierda, W=120 cuadros",
    }
    manifest_bytes = (json.dumps(manifest, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode()
    manifest_hash = hashlib.sha256(manifest_bytes).hexdigest()

    past = deque()
    previous = None
    chosen = None
    for item in segments(trajectories["izq"]):
        frame_id = item[0]
        past.append(item)
        while past and past[0][0] <= frame_id - FPS:
            past.popleft()
        current = record(frame_id, list(past), manifest_hash)
        if current["status"] == "estimated_valid":
            if previous is None or previous["status"] != "invalid":
                raise AssertionError("se esperaba primer cruce del umbral")
            chosen = [previous, current]
            break
        previous = current
    if chosen is None:
        raise ValueError("no se halló primera emisión válida")

    schema = json.loads(SCHEMA.read_text())
    for item in chosen:
        validate(item, schema)
    MANIFEST.write_bytes(manifest_bytes)
    OUTPUT.write_text("".join(json.dumps(item, ensure_ascii=False, allow_nan=False,
                                         separators=(",", ":")) + "\n" for item in chosen))
    print(f"OK: CMU SHA-256 {EXPECTED_SHA256}, manifiesto SHA-256 {manifest_hash}")
    print(f"cuadros {chosen[0]['source_frame_id']} inválido → "
          f"{chosen[1]['source_frame_id']} válido; "
          f"Q={chosen[1]['q_lateral_up_front']}")


if __name__ == "__main__":
    main()
