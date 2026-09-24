#!/usr/bin/env python3
"""Adversarial synthetic video checks for the offline phase-file fixture."""

from __future__ import annotations

import json

from ejecutar_banco_fase_archivo import OUT, analyze, render


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    cases = {
        "missing_frame": ({"skip_frame": 91}, "missing or unexpected frame PTS"),
        "identity_swap": ({"swap_colors_frame": 91}, "point identity inconsistent"),
        "tiny_orbit": ({"orbit_radius": 3, "dot_radius": 1},
                       "angular precision below fixture requirement"),
    }
    results = {}
    for name, (kwargs, expected_reason) in cases.items():
        path = OUT / f"stress_{name}.mkv"
        render(path, opposed=True, **kwargs)
        try:
            analyze(path, opposed=True)
        except ValueError as exc:
            reason = str(exc)
            if expected_reason not in reason:
                raise AssertionError(f"{name}: unexpected rejection: {reason}") from exc
            results[name] = {"outcome": "rejected", "reason": reason}
        else:
            raise AssertionError(f"{name}: invalid file was accepted")
    (OUT / "stress_report.json").write_text(json.dumps(results, indent=2) + "\n")
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
