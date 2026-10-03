"""Prepare a local, blinded ABX playlist from the synthetic Shaper ablation.

No participant responses are collected here. Keep the coordinator key private.
"""

import argparse
import csv
import hashlib
import json
import random
import shutil
import wave
from pathlib import Path


PAIRS = {
    "rho_only": ("rhoA_vA", "rhoB_vA"),
    "v_only": ("rhoA_vA", "rhoA_vB"),
    "both": ("rhoA_vA", "rhoB_vB"),
}


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def check_inputs(directory):
    manifest_path = directory / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("scope") != "synthetic_shaper_situation_control_ablation_not_body_measurement":
        raise ValueError("unexpected source scope")
    if set(manifest.get("stimuli", {})) != set().union(*(set(p) for p in PAIRS.values())):
        raise ValueError("unexpected source stimuli")
    source_hashes = {}
    for name, info in manifest["stimuli"].items():
        path = directory / f"{name}.wav"
        actual_hash = sha256(path)
        if actual_hash != info["matched_sha256"]:
            raise ValueError(f"source hash mismatch: {name}")
        with wave.open(str(path), "rb") as audio:
            if (audio.getnchannels(), audio.getsampwidth(), audio.getframerate(), audio.getnframes()) != (
                2, 3, 48000, 48000
            ):
                raise ValueError(f"unexpected PCM format: {name}")
        source_hashes[name] = actual_hash
    levels = [entry["matched_rms"] for entry in manifest["stimuli"].values()]
    if max(levels) - min(levels) >= 1e-7:
        raise ValueError("RMS matching outside declared tolerance")
    return sha256(manifest_path), source_hashes


def make_schedule(repetitions, rng):
    if repetitions < 4 or repetitions % 4:
        raise ValueError("repetitions per contrast must be a positive multiple of four")
    schedule = []
    for contrast, (left, right) in PAIRS.items():
        for _ in range(repetitions // 4):
            for swapped in (False, True):
                for x_is_left in (False, True):
                    a, b = (right, left) if swapped else (left, right)
                    x = left if x_is_left else right
                    schedule.append((contrast, a, b, x))
    rng.shuffle(schedule)
    return schedule


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--seed", type=int, required=True, help="store only with the private key")
    parser.add_argument("--repetitions", type=int, default=8, help="per contrast, divisible by four")
    args = parser.parse_args()

    source_manifest_sha, source_hashes = check_inputs(args.input_dir)
    rng = random.Random(args.seed)
    schedule = make_schedule(args.repetitions, rng)
    output = args.output_dir
    output.mkdir(parents=True, exist_ok=False)
    public = output / "para_oyente"
    private = output / "solo_coordinacion"
    stimuli = public / "audio"
    stimuli.mkdir(parents=True)
    private.mkdir()

    rows = []
    key_rows = []
    used_names = set()
    for index, (contrast, a, b, x) in enumerate(schedule, 1):
        trial_id = f"T{index:03d}"
        files = {}
        for role, source in (("A", a), ("B", b), ("X", x)):
            while True:
                filename = f"{rng.getrandbits(64):016x}.wav"
                if filename not in used_names:
                    used_names.add(filename)
                    break
            shutil.copyfile(args.input_dir / f"{source}.wav", stimuli / filename)
            files[role] = f"audio/{filename}"
        rows.append({"trial_id": trial_id, "A": files["A"], "B": files["B"], "X": files["X"]})
        key_rows.append({
            "trial_id": trial_id,
            "contrast": contrast,
            "answer": "A" if x == a else "B",
            "sources": {"A": a, "B": b, "X": x},
            "files": files,
        })

    trials_path = public / "ensayos.csv"
    with trials_path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=("trial_id", "A", "B", "X"))
        writer.writeheader()
        writer.writerows(rows)
    (public / "LEER.txt").write_text(
        "Prueba técnica ABX de sonidos sintéticos. En cada fila escuchá A, B y X; "
        "registrá si X coincide con A o con B, sin mirar nombres de origen ni hashes. "
        "Podés repetir los tres clips el mismo número de veces por ensayo. "
        "La tarea sólo pregunta si se distingue el sonido; no muestra movimiento ni "
        "pregunta qué posición espacial representa. El coordinador debe fijar antes "
        "equipo, volumen, orden de personas, instrucciones y registro de respuestas.\n",
        encoding="utf-8",
    )
    key = {
        "scope": "synthetic_offline_shaper_abx_preparation_not_human_results",
        "source_manifest_sha256": source_manifest_sha,
        "source_wav_sha256": source_hashes,
        "seed": args.seed,
        "repetitions_per_contrast": args.repetitions,
        "public_trials_sha256": sha256(trials_path),
        "trials": key_rows,
    }
    (private / "clave.json").write_text(json.dumps(key, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"trials": len(rows), "per_contrast": args.repetitions, "output": str(output)}))


if __name__ == "__main__":
    main()
