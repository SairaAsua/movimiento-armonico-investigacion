"""Exporta dos emisiones de C del replay CMU al sobre científico propuesto.

Requiere numpy y ezc3d. Los tiempos son lógicos por índice/FPS, no exposición
óptica ni latencia real. La toma pública CMU es danza, no rope flow ni Nico.
"""

from collections import deque
import hashlib
import json
from pathlib import Path

from cmu_causal_c_replay import (
    FPS, MIN_ARC_PER_REGION, MIN_SEGMENTS_PER_REGION, body_trajectories,
    segments, value,
)
from cmu_danza_05_02_audit import EXPECTED_SHA256
from validar_research_spacetime_c import SCHEMA, validate

HERE = Path(__file__).resolve().parent
MANIFEST = HERE / "research_spacetime_c.cmu05_02_manifest.json"
OUTPUT = HERE / "research_spacetime_c.cmu05_02.jsonl"


def summary(window):
    regions = {True: {"arc": 0.0, "numerator": 0.0, "segments": 0},
               False: {"arc": 0.0, "numerator": 0.0, "segments": 0}}
    for _, front, ds, speed_numerator in window:
        region = regions[front]
        region["arc"] += ds
        region["numerator"] += speed_numerator
        region["segments"] += 1
    result = {}
    for name, flag in (("front", True), ("rear", False)):
        region = regions[flag]
        result[f"{name}_arc_L"] = region["arc"]
        result[f"{name}_segments"] = region["segments"]
        result[f"{name}_speed_arc_weighted_L_per_s"] = (
            region["numerator"] / region["arc"] if region["arc"] > 0 else None
        )
    result["min_arc_L"] = MIN_ARC_PER_REGION
    result["min_segments"] = MIN_SEGMENTS_PER_REGION
    return result


def record(frame_id, window, manifest_hash):
    coverage = summary(window)
    c = value(window)
    end_us = round(frame_id * 1_000_000 / FPS)
    return {
        "contract_id": "ropeflow.research.spacetime_c.v0",
        "session_id": "cmu_public_05_02",
        "stream_id": "cmu_05_02_left_wrist",
        "source_frame_id": frame_id,
        "slot_id": 0,
        "signal_name": "spacetime_c_live",
        "algorithm_version": "cmu_causal_c_replay_v0",
        "input_manifest_sha256": manifest_hash,
        "calibration_version": "median_shoulder_span_frames_0_119_v0",
        "body_frame_version": "shoulder_waist_co_rotating_per_frame_unfiltered_v0",
        "path_definition": "co_rotating",
        "region_definition": "body_front_back_midpoint_v0",
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
            "available_at_us": end_us,
            "availability_time_kind": "logical_replay",
        },
        "coverage": coverage,
        "status": "estimated_valid" if c is not None else "invalid",
        "invalid_reason": None if c is not None else "insufficient_region",
        "value_L_per_s": c,
    }


def main():
    scale, trajectories = body_trajectories()  # verifica hash y marcadores
    manifest = {
        "source": "CMU mocap subject 05 trial 02; danza, no rope flow",
        "source_file": "sources/cmu_mocap/05_02.c3d",
        "source_sha256": EXPECTED_SHA256,
        "nominal_fps": FPS,
        "scale_first_second_mm": scale,
        "clock_basis": "índice de muestra / FPS nominal; sin timestamps ópticos ni latencia medida",
        "algorithm": "cmu_causal_c_replay.py, segments/value, mano izquierda, W=120 cuadros",
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
        current = record(frame_id, past, manifest_hash)
        if current["status"] == "estimated_valid":
            if previous is None or previous["status"] != "invalid":
                raise AssertionError("se esperaba el primer cruce del umbral")
            chosen = [previous, current]
            break
        previous = current
    if chosen is None:
        raise ValueError("la toma no contiene primera emisión válida")

    schema = json.loads(SCHEMA.read_text())
    for item in chosen:
        validate(item, schema)
    MANIFEST.write_bytes(manifest_bytes)
    OUTPUT.write_text("".join(json.dumps(item, ensure_ascii=False, allow_nan=False, separators=(",", ":")) + "\n" for item in chosen))
    print(f"OK: CMU SHA-256 {EXPECTED_SHA256}, manifiesto SHA-256 {manifest_hash}")
    print(f"cuadros {chosen[0]['source_frame_id']} inválido → {chosen[1]['source_frame_id']} válido; C={chosen[1]['value_L_per_s']:.6f} L/s")


if __name__ == "__main__":
    main()
