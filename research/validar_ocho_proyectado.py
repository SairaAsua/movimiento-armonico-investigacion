#!/usr/bin/env python3
"""Valida estructura y coherencia de un resumen de ocho 2D; no inspecciona video."""

import argparse
import json
import math
import re
import sys
from pathlib import Path


ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]*$")
FIELDS = {
    "schema_version", "material", "clip_id", "media_bundle_id", "view_id",
    "media_id", "track_id", "target", "coordinate_convention",
    "image_transform_id", "clock_map_id", "crossing_times_us",
    "uncertainty_method_id", "lobes",
}
LOBE_FIELDS = {
    "lobe_id", "start_us", "end_us", "signed_area", "area_error_bound",
    "orientation",
}


def validate(record):
    errors = []
    if not isinstance(record, dict) or set(record) != FIELDS:
        return ["campos raíz ausentes o adicionales"]
    if record["schema_version"] != "figure8_projected_measurement_v0":
        errors.append("schema_version desconocida")
    if record["material"] not in {"synthetic", "human_private"}:
        errors.append("material desconocido")
    for key in (
        "clip_id", "media_bundle_id", "view_id", "media_id", "track_id",
        "target", "image_transform_id", "clock_map_id", "uncertainty_method_id",
    ):
        if not isinstance(record[key], str) or not ID.fullmatch(record[key]):
            errors.append(f"{key} requiere ID sin espacios")
    if record["coordinate_convention"] != "x_right_y_up":
        errors.append("se requiere convención x derecha, y arriba")
    if (record["material"] == "human_private"
            and isinstance(record["uncertainty_method_id"], str)
            and record["uncertainty_method_id"].startswith("synthetic_")):
        errors.append("incertidumbre sintética no sirve para video humano")
    crossings = record["crossing_times_us"]
    if (not isinstance(crossings, list) or len(crossings) != 3
            or any(type(t) is not int or t < 0 for t in crossings)):
        errors.append("crossing_times_us requiere tres tiempos enteros no negativos")
        crossings = None
    elif not (crossings[0] < crossings[1] < crossings[2]):
        errors.append("los tres cruces deben ser estrictamente crecientes")
    lobes = record["lobes"]
    if not isinstance(lobes, list) or len(lobes) != 2:
        return errors + ["lobes requiere exactamente dos objetos"]
    for index, lobe in enumerate(lobes, start=1):
        if not isinstance(lobe, dict) or set(lobe) != LOBE_FIELDS:
            errors.append(f"lóbulo {index}: campos ausentes o adicionales")
            continue
        if type(lobe["lobe_id"]) is not int or lobe["lobe_id"] != index:
            errors.append(f"lóbulo {index}: lobe_id incorrecto")
        if crossings and (lobe["start_us"], lobe["end_us"]) != (crossings[index - 1], crossings[index]):
            errors.append(f"lóbulo {index}: tiempos no enlazan los cruces")
        area = lobe["signed_area"]
        bound = lobe["area_error_bound"]
        if (type(area) not in {int, float} or not math.isfinite(area)
                or type(bound) not in {int, float} or not math.isfinite(bound) or bound < 0):
            errors.append(f"lóbulo {index}: área/cota no finita o inválida")
            continue
        expected = ("counterclockwise" if area > 0 else "clockwise") if abs(area) > bound else "undetermined"
        if lobe["orientation"] != expected:
            errors.append(f"lóbulo {index}: orientación no respaldada por área y cota")
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("json_path", type=Path)
    args = parser.parse_args()
    try:
        record = json.loads(args.json_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        print(f"No se pudo leer el JSON: {exc}", file=sys.stderr)
        return 2
    errors = validate(record)
    for error in errors:
        print(error, file=sys.stderr)
    if errors:
        print(f"INVÁLIDO: {len(errors)} errores; sólo contrato estructural", file=sys.stderr)
        return 1
    print("VÁLIDO: sólo estructura y coherencia; no video, error físico ni Laban")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
