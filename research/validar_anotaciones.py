#!/usr/bin/env python3
"""Chequeos estructurales para el CSV piloto; no valida juicios Laban ni video."""

import argparse
import csv
import re
import sys
from pathlib import Path


FIELDS = (
    "annotation_id", "action_id", "clip_id", "media_bundle_id", "view_ids", "coder_id",
    "guide_version", "unit_type", "target", "start_us", "end_us",
    "time_uncertainty_us", "coordinate_frame", "layer", "feature",
    "value", "certainty", "cannot_code_reason", "scope", "evidence_note",
)
ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]*$")
UNITS = {"phrase", "segment", "event"}
FRAMES = {"camera", "room", "body", "unspecified"}
CERTAINTY = {"high", "medium", "low", "unknown"}
SCOPES = {"whole", "transition", "instant", "arrival"}


def validate(path: Path) -> tuple[int, list[str]]:
    errors: list[str] = []
    seen: set[str] = set()
    action_context: dict[str, tuple[str, str, str, str]] = {}
    count = 0
    with path.open(newline="", encoding="utf-8-sig") as stream:
        reader = csv.DictReader(stream)
        if tuple(reader.fieldnames or ()) != FIELDS:
            return 0, ["header: debe coincidir exactamente con el esquema de la guía"]
        for line, row in enumerate(reader, start=2):
            count += 1
            prefix = f"fila {line}"
            if None in row:
                errors.append(f"{prefix}: columnas adicionales")
                continue
            row = {key: (value or "").strip() for key, value in row.items()}
            for key in FIELDS[:-1]:
                if not row[key] and key not in {"action_id", "cannot_code_reason"}:
                    errors.append(f"{prefix}: falta {key}")
            if any(not row[key] for key in ("annotation_id", "clip_id", "media_bundle_id", "coder_id", "guide_version")):
                continue
            for key in ("annotation_id", "clip_id", "media_bundle_id", "coder_id", "guide_version"):
                if not ID.fullmatch(row[key]):
                    errors.append(f"{prefix}: {key} requiere un ID seudónimo sin espacios")
            if row["annotation_id"] in seen:
                errors.append(f"{prefix}: annotation_id duplicado")
            seen.add(row["annotation_id"])
            if row["action_id"]:
                if not ID.fullmatch(row["action_id"]):
                    errors.append(f"{prefix}: action_id requiere un ID seudónimo sin espacios")
                context = (row["clip_id"], row["media_bundle_id"], row["coder_id"], row["guide_version"])
                previous = action_context.setdefault(row["action_id"], context)
                if previous != context:
                    errors.append(f"{prefix}: action_id reutilizado entre clip/bundle/codificador/guía distintos")
            views = row["view_ids"].split("|")
            if not views or any(not ID.fullmatch(view) for view in views) or len(set(views)) != len(views):
                errors.append(f"{prefix}: view_ids deben ser IDs únicos separados por |")
            if row["coordinate_frame"] == "camera" and len(views) != 1:
                errors.append(f"{prefix}: marco camera requiere una sola view_id")
            for key, allowed in (("unit_type", UNITS), ("coordinate_frame", FRAMES),
                                 ("certainty", CERTAINTY), ("scope", SCOPES)):
                if row[key] not in allowed:
                    errors.append(f"{prefix}: {key} inválido: {row[key]!r}")
            if row["layer"] not in {"0", "1", "2"}:
                errors.append(f"{prefix}: layer debe ser 0, 1 o 2")
            times: dict[str, int] = {}
            for key in ("start_us", "end_us", "time_uncertainty_us"):
                try:
                    times[key] = int(row[key])
                    if times[key] < 0:
                        errors.append(f"{prefix}: {key} negativo")
                except ValueError:
                    errors.append(f"{prefix}: {key} debe ser entero en microsegundos")
            if len(times) == 3:
                start, end = times["start_us"], times["end_us"]
                if row["unit_type"] == "event" and (start != end or row["scope"] != "instant"):
                    errors.append(f"{prefix}: evento requiere inicio=fin y scope=instant")
                if row["unit_type"] in {"phrase", "segment"} and (start >= end or row["scope"] == "instant"):
                    errors.append(f"{prefix}: frase/tramo requiere duración positiva y scope no instant")
                if row["scope"] == "arrival" and row["unit_type"] != "segment":
                    errors.append(f"{prefix}: scope=arrival requiere unit_type=segment")
                if row["scope"] == "arrival" and not row["action_id"]:
                    errors.append(f"{prefix}: scope=arrival requiere action_id")
            if (row["value"] == "no_codable") != bool(row["cannot_code_reason"]):
                errors.append(f"{prefix}: no_codable y cannot_code_reason deben aparecer juntos")
            if row["value"] == "no_codable" and row["certainty"] != "unknown":
                errors.append(f"{prefix}: no_codable requiere certainty=unknown")
    if count == 0:
        errors.append("el CSV no contiene anotaciones")
    return count, errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv_path", type=Path)
    args = parser.parse_args()
    try:
        count, errors = validate(args.csv_path)
    except (OSError, UnicodeError, csv.Error) as exc:
        print(f"No se pudo leer el CSV: {exc}", file=sys.stderr)
        return 2
    for error in errors:
        print(error, file=sys.stderr)
    if errors:
        print(f"INVÁLIDO: {count} filas, {len(errors)} errores", file=sys.stderr)
        return 1
    print(f"VÁLIDO: {count} filas; sólo estructura, no observación ni fidelidad Laban")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
