"""Valida el fixture científico sintético sin dependencias externas.

No valida un flujo HarMoCAP ni relojes físicos: sólo el sobre y sus invariantes.
"""

import copy
import json
import math
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SCHEMA = ROOT / "research_spacetime_c.v0.schema.json"
FIXTURE = ROOT / "research_spacetime_c.synthetic.jsonl"


def require(condition, explanation):
    if not condition:
        raise ValueError(explanation)


def finite_number(value):
    return type(value) in (int, float) and math.isfinite(value)


def positive_int(value, allow_zero=False):
    return type(value) is int and value >= (0 if allow_zero else 1)


def nonempty(value):
    return isinstance(value, str) and bool(value)


def validate(record, schema):
    require(type(record) is dict, "el registro debe ser objeto")
    require(set(record) == set(schema["required"]), "claves de nivel superior incorrectas")
    require(record["contract_id"] == "ropeflow.research.spacetime_c.v0", "contrato ajeno")
    require(record["signal_name"] == "spacetime_c_live", "señal ajena")
    for name in ("session_id", "stream_id", "algorithm_version", "calibration_version", "body_frame_version", "segment_definition"):
        require(nonempty(record[name]), f"{name} vacío")
    require(positive_int(record["source_frame_id"], allow_zero=True), "source_frame_id inválido")
    require(positive_int(record["slot_id"], allow_zero=True), "slot_id inválido")
    require(isinstance(record["input_manifest_sha256"], str) and bool(re.fullmatch(r"[0-9a-f]{64}", record["input_manifest_sha256"])), "SHA-256 inválido")
    require(record["path_definition"] in ("co_rotating", "waist_centered_uncompensated_rotation", "world"), "ruta sin definición")
    require(record["region_definition"] == "body_front_back_midpoint_v0", "regiones sin definición")
    require(finite_number(record["window_seconds"]) and record["window_seconds"] > 0, "ventana inválida")

    clock = record["clock"]
    require(type(clock) is dict and set(clock) == set(schema["properties"]["clock"]["required"]), "claves de reloj incorrectas")
    for name in ("source_clock_id", "clock_map_id", "session_clock_id"):
        require(nonempty(clock[name]), f"{name} vacío")
    require(clock["source_time_kind"] in ("optical_exposure", "media_pts", "software_after_read", "sample_index_nominal", "synthetic_logical"), "clase de tiempo fuente desconocida")
    require(clock["availability_time_kind"] in ("measured", "logical_replay"), "disponibilidad sin base temporal")
    for name in ("source_time_us", "feature_window_start_us", "feature_window_end_us", "available_at_us"):
        require(positive_int(clock[name], allow_zero=True), f"{name} inválido")
    require(clock["feature_window_start_us"] < clock["feature_window_end_us"] <= clock["available_at_us"], "orden temporal imposible")
    require(abs((clock["feature_window_end_us"] - clock["feature_window_start_us"]) / 1e6 - record["window_seconds"]) <= 2e-6, "duración de ventana incoherente")

    coverage = record["coverage"]
    require(type(coverage) is dict and set(coverage) == set(schema["properties"]["coverage"]["required"]), "claves de cobertura incorrectas")
    for name in ("front_arc_L", "rear_arc_L"):
        require(finite_number(coverage[name]) and coverage[name] >= 0, f"{name} inválido")
    for name in ("front_segments", "rear_segments"):
        require(positive_int(coverage[name], allow_zero=True), f"{name} inválido")
    require(finite_number(coverage["min_arc_L"]) and coverage["min_arc_L"] > 0, "min_arc_L inválido")
    require(positive_int(coverage["min_segments"]), "min_segments inválido")
    sufficient = all(coverage[f"{side}_arc_L"] >= coverage["min_arc_L"] and coverage[f"{side}_segments"] >= coverage["min_segments"] for side in ("front", "rear"))
    for side in ("front", "rear"):
        speed = coverage[f"{side}_speed_arc_weighted_L_per_s"]
        require(speed is None or (finite_number(speed) and speed >= 0), "rapidez inválida")

    status = record["status"]
    require(status in ("estimated_valid", "invalid"), "estado desconocido")
    if status == "estimated_valid":
        require(record["invalid_reason"] is None and sufficient, "salida válida sin cobertura o con razón de invalidez")
        front = coverage["front_speed_arc_weighted_L_per_s"]
        rear = coverage["rear_speed_arc_weighted_L_per_s"]
        value = record["value_L_per_s"]
        require(front is not None and rear is not None and finite_number(value), "rapidez o valor ausente")
        require(math.isclose(value, front - rear, rel_tol=1e-9, abs_tol=1e-9), "C != delante - detrás")
    else:
        require(record["invalid_reason"] in ("insufficient_region", "occlusion", "frame_unstable", "calibration_unavailable", "transition", "expired"), "razón inválida")
        require(record["value_L_per_s"] is None, "valor numérico en estado inválido")
        if record["invalid_reason"] == "insufficient_region":
            require(not sufficient, "invalidez por región sin déficit")


def main():
    schema = json.loads(SCHEMA.read_text())
    records = [json.loads(line) for line in FIXTURE.read_text().splitlines() if line.strip()]
    require(len(records) == 2, "fixture incompleto")
    seen = set()
    for record in records:
        validate(record, schema)
        key = (record["session_id"], record["stream_id"], record["source_frame_id"], record["slot_id"], record["signal_name"])
        require(key not in seen, "emisión duplicada para cuadro y persona")
        seen.add(key)

    # Mutaciones adversas comprueban que fallos importantes no pasen en silencio.
    mutations = []
    bad = copy.deepcopy(records[0]); bad["coverage"]["rear_arc_L"] = 0.1; mutations.append(bad)
    bad = copy.deepcopy(records[0]); bad["value_L_per_s"] = 2.0; mutations.append(bad)
    bad = copy.deepcopy(records[1]); bad["value_L_per_s"] = 0.0; mutations.append(bad)
    bad = copy.deepcopy(records[0]); bad["clock"]["available_at_us"] = 999999; mutations.append(bad)
    bad = copy.deepcopy(records[0]); bad["path_definition"] = "unspecified"; mutations.append(bad)
    bad = copy.deepcopy(records[0]); bad["coverage"]["front_speed_arc_weighted_L_per_s"] = float("nan"); mutations.append(bad)
    for index, bad in enumerate(mutations, 1):
        try:
            validate(bad, schema)
        except ValueError:
            continue
        raise AssertionError(f"mutación adversa {index} aceptada")
    print(f"OK: {len(records)} registros sintéticos válidos, {len(mutations)} mutaciones rechazadas")


if __name__ == "__main__":
    main()
