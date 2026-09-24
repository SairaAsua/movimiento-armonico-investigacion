#!/usr/bin/env python3
"""Valida enlaces estructurales anotación→clip→bundle→original; no lee video.

Uso: python validar_linaje.py anotaciones.csv manifiesto.json
El manifiesto de ejemplo es enteramente sintético y privado para este diseño.
"""

import argparse
import csv
import json
import re
import sys
from pathlib import Path

from validar_anotaciones import validate as validate_annotations


ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]*$")
HASH = re.compile(r"^[0-9a-f]{64}$")


def check_id(value, field, errors):
    if not isinstance(value, str) or not ID.fullmatch(value):
        errors.append(f"{field}: ID seudónimo inválido")


def check_interval(start, end, field, errors):
    if (isinstance(start, bool) or isinstance(end, bool)
            or not isinstance(start, int) or not isinstance(end, int)
            or start < 0 or end <= start):
        errors.append(f"{field}: intervalo inválido")


def validate_lineage(annotation_path: Path, manifest_path: Path) -> list[str]:
    _, errors = validate_annotations(annotation_path)
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if not isinstance(manifest, dict) or manifest.get("schema_version") != "0.1":
        return errors + ["manifest: schema_version debe ser 0.1"]
    clips, bundles = manifest.get("clips"), manifest.get("bundles")
    if not isinstance(clips, list) or not isinstance(bundles, list) or not clips or not bundles:
        return errors + ["manifest: clips y bundles deben ser listas no vacías"]

    bundle_by_id = {}
    for b in bundles:
        if not isinstance(b, dict):
            errors.append("bundle: objeto requerido")
            continue
        bid = b.get("media_bundle_id")
        check_id(bid, "media_bundle_id", errors)
        if not isinstance(bid, str):
            continue
        if bid in bundle_by_id:
            errors.append(f"bundle duplicado: {bid}")
        bundle_by_id[bid] = b
        for field in ("session_id", "attempt_id"):
            check_id(b.get(field), f"{bid}.{field}", errors)
        views = b.get("views")
        if not isinstance(views, list) or not views:
            errors.append(f"{bid}: views vacío/inválido")
            continue
        seen_views, seen_media = set(), set()
        for v in views:
            if not isinstance(v, dict):
                errors.append(f"{bid}: view debe ser objeto")
                continue
            vid, mid = v.get("view_id"), v.get("media_id")
            for field, value in (("view_id", vid), ("media_id", mid),
                                 ("sync_version", v.get("sync_version")),
                                 ("calibration_version", v.get("calibration_version"))):
                check_id(value, f"{bid}.{field}", errors)
            if not isinstance(vid, str) or not isinstance(mid, str):
                continue
            if vid in seen_views or mid in seen_media:
                errors.append(f"{bid}: view_id o media_id duplicado")
            seen_views.add(vid)
            seen_media.add(mid)
            if not isinstance(v.get("sha256"), str) or not HASH.fullmatch(v["sha256"]):
                errors.append(f"{bid}.{vid}: sha256 debe tener 64 caracteres hexadecimales")
            clock = v.get("clock")
            if not isinstance(clock, dict):
                errors.append(f"{bid}.{vid}: falta clock")
                continue
            slope = clock.get("slope_session_per_pts")
            offset = clock.get("offset_us")
            residual = clock.get("max_residual_us")
            if (not isinstance(slope, (int, float)) or isinstance(slope, bool)
                    or not 0 < slope < 10):
                errors.append(f"{bid}.{vid}: slope inválido")
            if not isinstance(offset, int) or isinstance(offset, bool):
                errors.append(f"{bid}.{vid}: offset_us inválido")
            if not isinstance(residual, int) or isinstance(residual, bool) or residual < 0:
                errors.append(f"{bid}.{vid}: max_residual_us inválido")
            check_interval(clock.get("valid_start_pts_us"),
                           clock.get("valid_end_pts_us"), f"{bid}.{vid}.clock", errors)

    clip_by_id = {}
    for c in clips:
        if not isinstance(c, dict):
            errors.append("clip: objeto requerido")
            continue
        cid = c.get("clip_id")
        check_id(cid, "clip_id", errors)
        if not isinstance(cid, str):
            continue
        if cid in clip_by_id:
            errors.append(f"clip duplicado: {cid}")
        clip_by_id[cid] = c
        for field in ("session_id", "attempt_id", "media_bundle_id"):
            check_id(c.get(field), f"{cid}.{field}", errors)
        check_interval(c.get("start_us"), c.get("end_us"), cid, errors)
        bundle_id = c.get("media_bundle_id")
        b = bundle_by_id.get(bundle_id) if isinstance(bundle_id, str) else None
        if b is None:
            errors.append(f"{cid}: bundle ausente")
        elif (c.get("session_id"), c.get("attempt_id")) != (b.get("session_id"), b.get("attempt_id")):
            errors.append(f"{cid}: session_id/attempt_id difieren del bundle")
        if b is not None and isinstance(c.get("start_us"), int) and isinstance(c.get("end_us"), int):
            for v in b.get("views") or []:
                if not isinstance(v, dict) or not isinstance(v.get("clock"), dict):
                    continue
                clock = v["clock"]
                try:
                    offset = clock["offset_us"]
                    slope = clock["slope_session_per_pts"]
                    first = clock["valid_start_pts_us"]
                    last = clock["valid_end_pts_us"]
                    residual = clock["max_residual_us"]
                    if (not isinstance(offset, int) or isinstance(offset, bool)
                            or not isinstance(slope, (int, float)) or isinstance(slope, bool)
                            or not 0 < slope < 10 or not isinstance(first, int)
                            or not isinstance(last, int) or not isinstance(residual, int)):
                        continue
                    if c["start_us"] < offset + slope * first - residual or c["end_us"] > offset + slope * last + residual:
                        errors.append(f"{cid}: fuera del rango temporal mapeado de {v.get('view_id')}")
                except KeyError:
                    continue  # Ya se informó que faltan campos de reloj.

    with annotation_path.open(newline="", encoding="utf-8-sig") as stream:
        for line, row in enumerate(csv.DictReader(stream), start=2):
            cid, bid = row.get("clip_id"), row.get("media_bundle_id")
            c = clip_by_id.get(cid)
            if c is None:
                errors.append(f"fila {line}: clip_id ausente del manifiesto")
                continue
            if bid != c.get("media_bundle_id"):
                errors.append(f"fila {line}: bundle no pertenece al clip")
                continue
            b = bundle_by_id.get(bid)
            if b is None:
                continue
            valid_views = {v["view_id"] for v in b.get("views") or []
                           if isinstance(v, dict) and isinstance(v.get("view_id"), str)}
            requested = set((row.get("view_ids") or "").split("|"))
            if not requested <= valid_views:
                errors.append(f"fila {line}: view_ids no pertenecen al bundle")
            try:
                start, end = int(row["start_us"]), int(row["end_us"])
                if start < c["start_us"] or end > c["end_us"]:
                    errors.append(f"fila {line}: tiempo fuera del clip en reloj de sesión")
            except (ValueError, TypeError, KeyError):
                pass  # El validador básico informa valores no enteros.
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("annotations", type=Path)
    parser.add_argument("manifest", type=Path)
    args = parser.parse_args()
    try:
        errors = validate_lineage(args.annotations, args.manifest)
    except (OSError, UnicodeError, csv.Error, json.JSONDecodeError) as exc:
        print(f"No se pudo leer el paquete: {exc}", file=sys.stderr)
        return 2
    for error in errors:
        print(error, file=sys.stderr)
    if errors:
        print(f"LINAJE INVÁLIDO: {len(errors)} errores", file=sys.stderr)
        return 1
    print("LINAJE VÁLIDO: sólo estructura; hashes, relojes y video no comprobados")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
