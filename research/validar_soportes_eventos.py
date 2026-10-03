#!/usr/bin/env python3
"""Validate claimed hard event-time supports against annotations and lineage.

Structural only: does not prove that an interval contains the physical event,
that camera clocks are calibrated, or that the cited frames show the event.
"""

import argparse
import csv
import json
import re
import sys
from pathlib import Path

from validar_linaje import validate_lineage


FIELDS = ("annotation_id", "earliest_us", "latest_us", "available_at_us",
          "clock_domain", "source_frame_ids", "bound_kind", "bound_basis")
FRAME_ID = re.compile(r"^([A-Za-z0-9][A-Za-z0-9_.-]*):([0-9]+)$")


def validate(supports_path: Path, annotations_path: Path, manifest_path: Path) -> list[str]:
    errors = validate_lineage(annotations_path, manifest_path)
    if errors:
        return errors
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    clips = {c["clip_id"]: c for c in manifest["clips"]}
    bundles = {b["media_bundle_id"]: b for b in manifest["bundles"]}
    with annotations_path.open(newline="", encoding="utf-8-sig") as stream:
        annotations = {row["annotation_id"]: row for row in csv.DictReader(stream)}
    seen = set()
    with supports_path.open(newline="", encoding="utf-8-sig") as stream:
        reader = csv.DictReader(stream)
        if tuple(reader.fieldnames or ()) != FIELDS:
            return ["soportes: encabezado distinto del esquema"]
        for line, row in enumerate(reader, start=2):
            prefix = f"soportes fila {line}"
            if None in row or any(row.get(field) is None for field in FIELDS):
                errors.append(f"{prefix}: cantidad de columnas incorrecta")
                continue
            row = {key: value.strip() for key, value in row.items()}
            aid = row["annotation_id"]
            if aid in seen:
                errors.append(f"{prefix}: annotation_id repetido")
            seen.add(aid)
            a = annotations.get(aid)
            if a is None or a["unit_type"] != "event" or a["value"] == "no_codable":
                errors.append(f"{prefix}: requiere anotación de evento codificable existente")
                continue
            if row["clock_domain"] != "session" or row["bound_kind"] != "claimed_hard":
                errors.append(f"{prefix}: se exige reloj session y bound_kind=claimed_hard")
            if not row["bound_basis"]:
                errors.append(f"{prefix}: falta base de la cota")
            try:
                lo, hi, available = (int(row[key]) for key in
                                     ("earliest_us", "latest_us", "available_at_us"))
            except ValueError:
                errors.append(f"{prefix}: tiempos deben ser enteros en microsegundos")
                continue
            nominal = int(a["start_us"])
            clip = clips[a["clip_id"]]
            if not (clip["start_us"] <= lo <= nominal <= hi <= clip["end_us"]):
                errors.append(f"{prefix}: soporte fuera de clip o no contiene tiempo nominal")
            if available < hi:
                errors.append(f"{prefix}: disponibilidad anterior al fin del soporte")
            media_ids = {v["media_id"] for v in bundles[a["media_bundle_id"]]["views"]
                         if v["view_id"] in a["view_ids"].split("|")}
            frame_ids = row["source_frame_ids"].split("|")
            if not frame_ids or len(set(frame_ids)) != len(frame_ids) or any(
                (match := FRAME_ID.fullmatch(fid)) is None or match.group(1) not in media_ids
                for fid in frame_ids
            ):
                errors.append(f"{prefix}: cuadros fuente inválidos o ajenos a las vistas anotadas")
    if not seen:
        errors.append("soportes: no hay eventos")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("supports", type=Path)
    parser.add_argument("annotations", type=Path)
    parser.add_argument("manifest", type=Path)
    args = parser.parse_args()
    try:
        errors = validate(args.supports, args.annotations, args.manifest)
    except (OSError, UnicodeError, csv.Error, json.JSONDecodeError) as exc:
        print(f"No se pudo leer el paquete: {exc}", file=sys.stderr)
        return 2
    for error in errors:
        print(error, file=sys.stderr)
    if errors:
        print(f"SOPORTES INVÁLIDOS: {len(errors)} errores", file=sys.stderr)
        return 1
    print("SOPORTES ESTRUCTURALMENTE VÁLIDOS; cotas físicas no verificadas")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
