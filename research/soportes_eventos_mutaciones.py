#!/usr/bin/env python3
"""Adversarial structural cases for the proposed event-support sidecar."""

import csv
import json
import tempfile
from pathlib import Path

from validar_soportes_eventos import FIELDS, validate


HERE = Path(__file__).resolve().parent
SOURCE = HERE / "soportes_eventos_ejemplo_sintetico.csv"
ANNOTATIONS = HERE / "anotaciones_ejemplo_sintetico.csv"
MANIFEST = HERE / "manifiesto_ejemplo_sintetico.json"


def run_case(name, change):
    with SOURCE.open(newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream))
    change(rows)
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "supports.csv"
        with path.open("w", newline="", encoding="utf-8") as stream:
            writer = csv.DictWriter(stream, fieldnames=FIELDS)
            writer.writeheader()
            writer.writerows(rows)
        errors = validate(path, ANNOTATIONS, MANIFEST)
    assert errors, f"{name}: mutated case was accepted"
    return {"case": name, "errors": errors}


def main():
    assert validate(SOURCE, ANNOTATIONS, MANIFEST) == []
    mutations = (
        ("nominal_outside", lambda r: r[0].update(earliest_us="1700001")),
        ("reversed", lambda r: r[0].update(earliest_us="1720000")),
        ("availability_before_support", lambda r: r[0].update(available_at_us="1700000")),
        ("wrong_media", lambda r: r[0].update(source_frame_ids="media_other:50")),
        ("uncodable_event", lambda r: r[0].update(annotation_id="a04")),
        ("duplicate", lambda r: r[1].update(annotation_id="a07")),
        ("wrong_clock", lambda r: r[0].update(clock_domain="camera")),
        ("no_basis", lambda r: r[0].update(bound_basis="")),
    )
    results = [run_case(name, mutate) for name, mutate in mutations]
    print(json.dumps({"valid_fixture": True, "rejected": len(results),
                      "cases": [r["case"] for r in results]}, sort_keys=True))


if __name__ == "__main__":
    main()
