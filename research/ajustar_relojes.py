#!/usr/bin/env python3
"""Ajusta relojes de video con eventos comunes anotados; no detecta eventos.

CSV: event_id,camera_id,pts_s (una fila por evento/cámara).
Uso: python3 ajustar_relojes.py eventos.csv --reference cam_a
Requiere al menos tres pares por cámara; no descarta atípicos automáticamente.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path
import statistics
import sys


def fit(xs: list[float], ys: list[float]) -> tuple[float, float, float]:
    """Devuelve origen x, valor predicho en origen y pendiente de y=a+b(x-x0)."""
    x0 = statistics.mean(xs)
    y0 = statistics.mean(ys)
    den = sum((x - x0) ** 2 for x in xs)
    if den <= 0:
        raise ValueError("Los eventos no cubren un intervalo temporal")
    b = sum((x - x0) * (y - y0) for x, y in zip(xs, ys)) / den
    return x0, y0, b


def predict(model: tuple[float, float, float], x: float) -> float:
    x0, y0, b = model
    return y0 + b * (x - x0)


def read_events(path: Path) -> dict[str, dict[str, float]]:
    cameras: dict[str, dict[str, float]] = {}
    with path.open(newline="", encoding="utf-8") as stream:
        reader = csv.DictReader(stream)
        required = {"event_id", "camera_id", "pts_s"}
        if not required.issubset(reader.fieldnames or []):
            raise ValueError(f"CSV requiere columnas: {', '.join(sorted(required))}")
        for row in reader:
            event = (row["event_id"] or "").strip()
            camera = (row["camera_id"] or "").strip()
            try:
                pts = float(row["pts_s"])
            except (TypeError, ValueError):
                raise ValueError("pts_s debe ser un número") from None
            if not event or not camera or not math.isfinite(pts):
                raise ValueError("event_id, camera_id y pts_s finito son obligatorios")
            by_event = cameras.setdefault(camera, {})
            if event in by_event:
                raise ValueError(f"Evento repetido en una cámara: {camera}/{event}")
            by_event[event] = pts
    return cameras


def inspect(cameras: dict[str, dict[str, float]], reference: str) -> dict[str, object]:
    if reference not in cameras:
        raise ValueError("No existe la cámara de referencia en el CSV")
    if len(cameras) < 2:
        raise ValueError("Se requieren al menos dos cámaras")
    ref = cameras[reference]
    results: dict[str, object] = {}
    for camera, events in sorted(cameras.items()):
        if camera == reference:
            continue
        matched = sorted(set(ref) & set(events), key=lambda key: ref[key])
        if len(matched) < 3 or len({events[key] for key in matched}) < 3:
            results[camera] = {
                "error": "Se requieren al menos tres eventos emparejados en tiempos distintos",
                "matched_events": len(matched),
                "unmatched_camera_events": len(set(events) - set(ref)),
                "unmatched_reference_events": len(set(ref) - set(events)),
            }
            continue
        xs = [events[key] for key in matched]
        ys = [ref[key] for key in matched]
        if any(next_time <= previous_time for previous_time, next_time in zip(xs, xs[1:])) or \
                any(next_time <= previous_time for previous_time, next_time in zip(ys, ys[1:])):
            results[camera] = {
                "error": "Los PTS de eventos emparejados deben crecer estrictamente en ambas cámaras",
                "matched_events": len(matched),
                "unmatched_camera_events": len(set(events) - set(ref)),
                "unmatched_reference_events": len(set(ref) - set(events)),
            }
            continue
        model = fit(xs, ys)
        residuals = [predict(model, x) - y for x, y in zip(xs, ys)]
        loo = []
        for index in range(len(xs)):
            x_train = xs[:index] + xs[index + 1:]
            y_train = ys[:index] + ys[index + 1:]
            loo_model = fit(x_train, y_train)
            loo.append(predict(loo_model, xs[index]) - ys[index])
        results[camera] = {
            "matched_events": len(matched),
            "unmatched_camera_events": len(set(events) - set(ref)),
            "unmatched_reference_events": len(set(ref) - set(events)),
            "camera_event_span_s": max(xs) - min(xs),
            "origin_pts_s": model[0],
            "reference_at_origin_s": model[1],
            "slope_reference_per_camera_second": model[2],
            "relative_drift_ppm": (model[2] - 1) * 1_000_000,
            "median_abs_fit_residual_s": statistics.median(abs(v) for v in residuals),
            "max_abs_fit_residual_s": max(abs(v) for v in residuals),
            "median_abs_leave_one_out_residual_s": statistics.median(abs(v) for v in loo),
            "max_abs_leave_one_out_residual_s": max(abs(v) for v in loo),
            "residuals_by_event_s": {key: value for key, value in zip(matched, residuals)},
            "leave_one_out_residuals_by_event_s": {key: value for key, value in zip(matched, loo)},
        }
    return {
        "schema": "ropeflow_clock_alignment_v0.2",
        "reference_camera": reference,
        "reference_event_count": len(ref),
        "cameras": results,
        "notes": [
            "Modelo: t_referencia = reference_at_origin_s + pendiente*(t_camara - origin_pts_s).",
            "Los residuos miden consistencia de eventos anotados, no la exactitud absoluta de exposición.",
            "Un ajuste lineal no corrige irregularidades locales, rolling shutter ni tiempos PTS reescritos.",
            "Se rechazan eventos emparejados cuyo orden PTS no crezca estrictamente en ambas vistas.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv", type=Path)
    parser.add_argument("--reference", required=True)
    args = parser.parse_args()
    try:
        result = inspect(read_events(args.csv), args.reference)
    except (OSError, ValueError) as exc:
        parser.error(str(exc))
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 1 if any("error" in value for value in result["cameras"].values()) else 0


if __name__ == "__main__":
    sys.exit(main())
