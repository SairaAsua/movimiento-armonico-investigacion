"""Valida el sobre científico Q sintético; no valida pose, OSC ni audio."""

import copy
import json
import math
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SCHEMA = ROOT / "research_plane_q.v0.schema.json"
FIXTURE = ROOT / "research_plane_q.synthetic.jsonl"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def finite(value):
    return type(value) in (int, float) and math.isfinite(value)


def uint(value):
    return type(value) is int and value >= 0


def positive(value):
    return uint(value) and value > 0


def validate(record, schema):
    require(type(record) is dict and set(record) == set(schema["required"]), "claves superiores")
    require(record["contract_id"] == "ropeflow.research.plane_q.v0", "contrato")
    require(record["signal_name"] == "plane_normal_Q_live", "señal")
    for key in ("session_id", "stream_id", "algorithm_version", "calibration_version",
                "body_frame_version", "segment_definition"):
        require(type(record[key]) is str and bool(record[key]), f"{key} vacío")
    for key in ("source_frame_id", "slot_id"):
        require(uint(record[key]), f"{key} inválido")
    require(type(record["input_manifest_sha256"]) is str and
            re.fullmatch(r"[0-9a-f]{64}", record["input_manifest_sha256"]), "hash")
    require(record["path_definition"] in {"co_rotating", "waist_relative_step_body_axes"}, "recorrido")
    require(finite(record["window_seconds"]) and record["window_seconds"] > 0, "ventana")

    clock = record["clock"]
    require(type(clock) is dict and set(clock) ==
            set(schema["properties"]["clock"]["required"]), "claves reloj")
    for key in ("source_clock_id", "clock_map_id", "session_clock_id"):
        require(type(clock[key]) is str and bool(clock[key]), f"{key} vacío")
    require(clock["source_time_kind"] in {"optical_exposure", "media_pts", "software_after_read",
                                          "sample_index_nominal", "synthetic_logical"}, "tiempo fuente")
    require(clock["availability_time_kind"] in {"measured", "logical_replay"}, "disponibilidad")
    for key in ("source_time_us", "feature_window_start_us", "feature_window_end_us", "available_at_us"):
        require(uint(clock[key]), f"{key} inválido")
    last = clock["last_observation_us"]
    require(last is None or uint(last), "última observación")
    start, end, available = (clock[x] for x in
                             ("feature_window_start_us", "feature_window_end_us", "available_at_us"))
    require(start < end <= available, "orden de reloj")
    require(last is None or last <= end, "observación futura")
    require(abs((end - start) / 1e6 - record["window_seconds"]) <= 2e-6, "duración")

    coverage = record["coverage"]
    require(type(coverage) is dict and set(coverage) ==
            set(schema["properties"]["coverage"]["required"]), "claves cobertura")
    require(finite(coverage["arc_L"]) and coverage["arc_L"] >= 0, "arco")
    require(finite(coverage["min_arc_L"]) and coverage["min_arc_L"] > 0, "mínimo arco")
    require(uint(coverage["segments"]) and positive(coverage["min_segments"]), "tramos")
    require(positive(coverage["max_age_us"]), "edad máxima")
    sufficient = (coverage["arc_L"] >= coverage["min_arc_L"] and
                  coverage["segments"] >= coverage["min_segments"])
    fresh = last is not None and start < last <= end and available - last <= coverage["max_age_us"]

    uncertainty = record["uncertainty"]
    require(type(uncertainty) is dict and set(uncertainty) ==
            set(schema["properties"]["uncertainty"]["required"]), "claves incertidumbre")
    fields = ("max_angle_error_deg", "length_weight_tv_bound",
              "missing_arc_fraction_max", "q_component_abs_bound", "validation_profile_id")
    if uncertainty["status"] == "not_estimated":
        require(all(uncertainty[key] is None for key in fields), "incertidumbre ausente con cifras")
    elif uncertainty["status"] == "bounded":
        require(record["status"] == "estimated_valid", "cota en Q inválida")
        for key, maximum in (("max_angle_error_deg", 90), ("length_weight_tv_bound", 1),
                             ("missing_arc_fraction_max", 1), ("q_component_abs_bound", 1)):
            require(finite(uncertainty[key]) and 0 <= uncertainty[key] <= maximum,
                    f"{key} inválido")
        require(type(uncertainty["validation_profile_id"]) is str and
                bool(uncertainty["validation_profile_id"]), "perfil de validación")
        implied = min(1, math.sin(math.radians(uncertainty["max_angle_error_deg"])) +
                      uncertainty["length_weight_tv_bound"] +
                      uncertainty["missing_arc_fraction_max"])
        require(uncertainty["q_component_abs_bound"] + 1e-12 >= implied,
                "cota Q menor que sus componentes")
    else:
        raise ValueError("estado de incertidumbre")

    status = record["status"]
    q = record["q_lateral_up_front"]
    if status == "estimated_valid":
        require(record["invalid_reason"] is None and sufficient and fresh, "Q válida sin soporte")
        require(type(q) is list and len(q) == 3 and all(finite(x) and 0 <= x <= 1 for x in q),
                "vector Q")
        require(math.isclose(sum(q), 1.0, rel_tol=0, abs_tol=1e-6), "Q no normalizada")
    elif status == "invalid":
        require(record["invalid_reason"] in {"insufficient_arc", "occlusion", "frame_unstable",
                                             "calibration_unavailable", "transition", "expired"},
                "razón de invalidez")
        require(q is None, "vector centinela inválido")
        if record["invalid_reason"] == "insufficient_arc":
            require(not sufficient, "arco suficiente marcado insuficiente")
        if record["invalid_reason"] == "expired":
            require(not fresh, "Q fresca marcada vencida")
    else:
        raise ValueError("estado")


def main():
    schema = json.loads(SCHEMA.read_text())
    records = [json.loads(line) for line in FIXTURE.read_text().splitlines() if line.strip()]
    require(len(records) == 3, "fixture incompleto")
    seen = set()
    for record in records:
        validate(record, schema)
        key = tuple(record[x] for x in ("session_id", "stream_id", "source_frame_id", "slot_id"))
        require(key not in seen, "emisión duplicada")
        seen.add(key)

    mutations = []
    bad = copy.deepcopy(records[0]); bad["q_lateral_up_front"] = [0, 0, 0]; mutations.append(bad)
    bad = copy.deepcopy(records[0]); bad["q_lateral_up_front"] = [0.5, float("nan"), 0.5]; mutations.append(bad)
    bad = copy.deepcopy(records[0]); bad["path_definition"] = "unspecified"; mutations.append(bad)
    bad = copy.deepcopy(records[0]); bad["coverage"]["arc_L"] = 0.1; mutations.append(bad)
    bad = copy.deepcopy(records[0]); bad["clock"]["available_at_us"] = 3_000_000; mutations.append(bad)
    bad = copy.deepcopy(records[1]); bad["q_lateral_up_front"] = [0, 0, 0]; mutations.append(bad)
    bad = copy.deepcopy(records[2]); bad["clock"]["last_observation_us"] = 2_000_000; mutations.append(bad)
    bad = copy.deepcopy(records[0]); bad["uncertainty"]["status"] = "bounded"; mutations.append(bad)
    bad = copy.deepcopy(records[0]); bad["uncertainty"]["q_component_abs_bound"] = 0.0; mutations.append(bad)
    bounded = copy.deepcopy(records[0])
    bounded["uncertainty"] = {
        "status": "bounded", "max_angle_error_deg": 5.0,
        "length_weight_tv_bound": 0.02, "missing_arc_fraction_max": 0.1,
        "q_component_abs_bound": 0.21,
        "validation_profile_id": "synthetic_arithmetic_only",
    }
    validate(bounded, schema)
    bad = copy.deepcopy(bounded); bad["uncertainty"]["q_component_abs_bound"] = 0.20; mutations.append(bad)
    bad = copy.deepcopy(bounded); bad["status"] = "invalid"; bad["invalid_reason"] = "occlusion"; bad["q_lateral_up_front"] = None; mutations.append(bad)
    for i, bad in enumerate(mutations, 1):
        try:
            validate(bad, schema)
        except ValueError:
            continue
        raise AssertionError(f"mutación adversa {i} aceptada")
    print(f"OK: {len(records)} registros Q sintéticos y cota aritmética; "
          f"{len(mutations)} mutaciones rechazadas")


if __name__ == "__main__":
    main()
