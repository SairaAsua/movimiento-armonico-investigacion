"""Exact selection example for space–phase MI; no human/camera inference."""

from __future__ import annotations

import json

from j_espacio_fase_sintetico import mutual_information


def main() -> None:
    truth = [[0.25, 0.25], [0.25, 0.25]]
    observed = [[0.25, 0.125], [0.125, 0.25]]
    missing_by_phase = [0.125, 0.125]
    complete_independent = [[0.25, 0.25], [0.25, 0.25]]
    complete_aligned = [[0.375, 0.125], [0.125, 0.375]]
    coverage = sum(map(sum, observed))
    phase_coverage = [
        sum(observed[s][phi] for s in range(2)) / 0.5
        for phi in range(2)
    ]
    j_observed = mutual_information(observed)
    j_independent = mutual_information(complete_independent)
    j_aligned = mutual_information(complete_aligned)
    assert mutual_information(truth) == 0
    assert coverage == 0.75 and phase_coverage == [0.75, 0.75]
    assert abs(j_observed - 0.056633012265132426) < 1e-12
    assert j_independent == 0
    assert abs(j_aligned - 0.13081203594113697) < 1e-12
    assert all(
        sum(complete_independent[s][phi] - observed[s][phi] for s in range(2))
        == missing_by_phase[phi]
        for phi in range(2)
    )
    assert all(
        sum(complete_aligned[s][phi] - observed[s][phi] for s in range(2))
        == missing_by_phase[phi]
        for phi in range(2)
    )
    print(json.dumps({
        "kind": "synthetic_phase_region_selection",
        "coverage_total": coverage,
        "coverage_by_phase": phase_coverage,
        "J_true_independent_nats": 0.0,
        "J_valid_only_nats": j_observed,
        "J_possible_completion_independent_nats": j_independent,
        "J_possible_completion_aligned_nats": j_aligned,
        "limit": "Constructed probability masses, not camera missingness rates",
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
