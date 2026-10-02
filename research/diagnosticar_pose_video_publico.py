#!/usr/bin/env python3
"""Diagnóstico agregado de detecciones HarMoCAP sobre video local autorizado.

No escribe cuadros, keypoints, trayectorias ni identificadores por cuadro.
Requiere HarMoCAP instalado, su checkpoint local, OpenCV, NumPy y ffprobe.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import statistics
import subprocess
from collections import Counter
from pathlib import Path

import cv2
import numpy as np
import torch
from harmocap.perception import PoseBackend


JOINTS = {5: "shoulder_l", 6: "shoulder_r", 9: "wrist_l", 10: "wrist_r",
          11: "hip_l", 12: "hip_r", 15: "ankle_l", 16: "ankle_r"}
GATES = {
    "torso": (5, 6, 11, 12),
    "torso_right_wrist": (5, 6, 10, 11, 12),
    "torso_both_wrists": (5, 6, 9, 10, 11, 12),
}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def pts_originales(path: Path) -> np.ndarray:
    raw = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0",
         "-show_entries", "frame=best_effort_timestamp_time", "-of", "csv=p=0", str(path)],
        check=True, capture_output=True,
    ).stdout
    return np.array([float(x) for x in raw.splitlines() if x.strip()], dtype=float)


def resumir(rows: list[dict]) -> dict:
    confs = [p for row in rows for p in row["conf"]]
    gates = {}
    for name, joints in GATES.items():
        valid = [
            row["raw"] == 2 and row["tracked"] == 2
            and len(row["conf"]) == 2
            and all(all(person[j] >= 0.5 for j in joints) for person in row["conf"])
            for row in rows
        ]
        best, current, best_span, run_start = 0, 0, 0.0, 0
        for i, passed in enumerate(valid):
            if passed:
                if current == 0:
                    run_start = i
                current += 1
                if current > best:
                    best = current
                    best_span = rows[i]["pts"] - rows[run_start]["pts"]
            else:
                current = 0
        gates[name] = {
            "person_detections_passing": sum(
                all(person[j] >= 0.5 for j in joints) for person in confs),
            "person_detections_denominator": len(confs),
            "frames_with_two_detections_both_passing": sum(valid),
            "frames_denominator": len(rows),
            "longest_run_processed_samples": best,
            "longest_run_pts_span_s": round(best_span, 3),
        }
    return {
        "sampled_frames": len(rows),
        "raw_detection_count": dict(sorted(Counter(row["raw"] for row in rows).items())),
        "tracked_detection_count": dict(sorted(Counter(row["tracked"] for row in rows).items())),
        "distinct_ephemeral_track_ids": len({i for row in rows for i in row["ids"]}),
        "exploratory_joint_confidence_gate_ge_0p5": gates,
        "joint_model_confidence": {
            name: {
                "detections": len(confs),
                "median": round(float(np.median([p[j] for p in confs])), 4) if confs else None,
                "fraction_ge_0p5": round(sum(p[j] >= 0.5 for p in confs) / len(confs), 4)
                if confs else None,
            }
            for j, name in JOINTS.items()
        },
    }


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("video", type=Path)
    ap.add_argument("checkpoint", type=Path)
    ap.add_argument("--start-pts", type=float, required=True)
    ap.add_argument("--end-pts", type=float, required=True)
    ap.add_argument("--stride", type=int, default=5)
    ap.add_argument("--split-pts", type=float)
    ap.add_argument("--threads", type=int, default=4)
    args = ap.parse_args()
    if args.stride < 1 or args.end_pts <= args.start_pts:
        ap.error("stride positivo e intervalo temporal no vacío requeridos")

    torch.set_num_threads(args.threads)
    pts = pts_originales(args.video)
    if len(pts) < 2 or not np.all(np.diff(pts) > 0):
        raise ValueError("PTS ausentes, repetidos o no monótonos")
    selected = np.flatnonzero((pts >= args.start_pts) & (pts < args.end_pts))
    if not len(selected) or selected[-1] - selected[0] + 1 != len(selected):
        raise ValueError("Intervalo sin cuadros o índices no contiguos")

    cap = cv2.VideoCapture(str(args.video))
    if not cap.isOpened() or not cap.set(cv2.CAP_PROP_POS_FRAMES, int(selected[0])):
        raise RuntimeError("OpenCV no pudo abrir o buscar el cuadro inicial")
    backend = PoseBackend(
        realtime_checkpoint="/nonexistent/harmocap-pose.engine",
        fallback_checkpoint=str(args.checkpoint), device="cpu", imgsz=640,
        conf=0.25, max_det=8, tracker="bytetrack.yaml",
    )
    rows = []
    first_opencv_pos_s = None
    for idx in selected:
        ok, frame = cap.read()
        if not ok or int(cap.get(cv2.CAP_PROP_POS_FRAMES)) != idx + 1:
            raise RuntimeError(f"Decodificación o índice OpenCV inconsistente en {idx}")
        if (idx - selected[0]) % args.stride:
            continue
        if first_opencv_pos_s is None:
            first_opencv_pos_s = float(cap.get(cv2.CAP_PROP_POS_MSEC) / 1000)
        dets, raw_boxes, _, _ = backend.track_frame(frame)
        rows.append({
            "pts": float(pts[idx]), "raw": len(raw_boxes), "tracked": len(dets),
            "ids": [d.track_id for d in dets],
            "conf": [[k[2] for k in d.keypoints_iso] for d in dets],
        })
    cap.release()

    result = {
        "video_sha256": sha256(args.video),
        "checkpoint_sha256": sha256(args.checkpoint),
        "method": "HarMoCAP PoseBackend, CPU, imgsz=640, conf=0.25, max_det=8, ByteTrack; stride declarado",
        "gate_definition": "Exploratorio: cada articulación requerida con confianza de modelo >=0.5; dos detecciones y dos tracks por cuadro; sin referencia anatómica ni garantía de identidad",
        "source_frames_in_interval": len(selected),
        "source_index_first": int(selected[0]),
        "source_index_last": int(selected[-1]),
        "stride": args.stride,
        "sampled_pts_first_s": rows[0]["pts"],
        "sampled_pts_last_s": rows[-1]["pts"],
        "opencv_first_pos_s": first_opencv_pos_s,
        "opencv_minus_original_first_s": round(first_opencv_pos_s - rows[0]["pts"], 6),
        "all": resumir(rows),
    }
    if args.split_pts is not None:
        result["before_split"] = resumir([r for r in rows if r["pts"] < args.split_pts])
        result["after_split"] = resumir([r for r in rows if r["pts"] >= args.split_pts])
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
