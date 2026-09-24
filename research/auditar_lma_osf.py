#!/usr/bin/env python3
"""Audita categorías R1/R2 del depósito público de Bernardet et al. (2019).

No reproduce su alfa: sólo calcula frecuencias descriptivas de las respuestas
Q2 (primera categoría) y Q22 (segunda categoría), con hashes fijados.
"""

import csv
import hashlib
import json
import statistics
from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path

BASE = Path(__file__).parent / "sources" / "lma_reliability_2019"
CATEGORIES = {"Effort", "Space", "Shape", "Phrasing"}


def parse_file(path):
    rows = list(csv.reader(path.read_text(encoding="utf-8-sig").splitlines()))
    assert rows[0][0].startswith("# Participant Id:")
    participant = rows[0][0].split(":", 1)[1].strip().lower()
    records = defaultdict(dict)
    for row in rows[1:]:
        assert len(row) == 7, (path, row)
        pair = (row[0].strip("'"), row[2].strip("'"))
        question = row[4].split(":", 1)[0]
        answer = row[5].split(":", 1)[1].strip("'")
        if question in ("Q1", "Q2", "Q11", "Q22"):
            assert question not in records[pair], (path, pair, question)
            records[pair][question] = answer
    return participant, records


def main():
    manifest = json.loads((BASE / "MANIFEST.json").read_text())
    by_pair = defaultdict(dict)
    all_by_pair = defaultdict(dict)
    participants = set()
    for entry in manifest["files"]:
        path = BASE / entry["name"]
        data = path.read_bytes()
        assert len(data) == entry["bytes"]
        assert hashlib.sha256(data).hexdigest() == entry["sha256"]
        participant, records = parse_file(path)
        assert participant not in participants, participant
        participants.add(participant)
        for pair, answers in records.items():
            all_by_pair[pair][participant] = answers
            if answers.get("Q2"):
                assert answers["Q2"] in CATEGORIES, (participant, pair)
                if "Q22" in answers:
                    assert answers["Q22"] in CATEGORIES, (participant, pair)
                by_pair[pair][participant] = answers

    first_counts = Counter()
    second_counts = Counter()
    exact_first = 0
    shared_either = 0
    compared = 0
    first_question = Counter()
    q1_comparisons = 0
    q1_matches = 0
    q1_stimulus_agreement = []
    for ratings in all_by_pair.values():
        for answers in ratings.values():
            first_question[answers.get("Q1", "missing")] += 1
            if answers.get("Q1") == "No":
                assert "Q2" not in answers
        valid_q1 = [a["Q1"] for a in ratings.values() if a.get("Q1") in {"Yes", "No"}]
        q1_pairs = list(combinations(valid_q1, 2))
        if q1_pairs:
            q1_stimulus_agreement.append(sum(a == b for a, b in q1_pairs) / len(q1_pairs))
        for a, b in q1_pairs:
            q1_comparisons += 1
            q1_matches += a == b
    first_stimulus_agreement = []
    first_stimuli_single_rater = 0
    for ratings in by_pair.values():
        for answers in ratings.values():
            first_counts[answers["Q2"]] += 1
            if "Q22" in answers:
                second_counts[answers["Q22"]] += 1
        rating_pairs = list(combinations(ratings.values(), 2))
        if rating_pairs:
            first_stimulus_agreement.append(
                sum(a["Q2"] == b["Q2"] for a, b in rating_pairs) / len(rating_pairs)
            )
        else:
            first_stimuli_single_rater += 1
        for a, b in rating_pairs:
            compared += 1
            exact_first += a["Q2"] == b["Q2"]
            shared_either += bool(
                {a["Q2"], *([a["Q22"]] if "Q22" in a else [])}
                & {b["Q2"], *([b["Q22"]] if "Q22" in b else [])}
            )

    print(json.dumps({
        "files": len(manifest["files"]),
        "unique_participants": len(participants),
        "rated_pairs_all": len(all_by_pair),
        "rated_units_all": sum(first_question.values()),
        "change_question_counts": dict(sorted(first_question.items())),
        "q1_pairwise_comparisons": q1_comparisons,
        "q1_pairwise_agreement": round(q1_matches / q1_comparisons, 6),
        "q1_mean_agreement_per_stimulus": round(statistics.mean(q1_stimulus_agreement), 6),
        "pairs_with_Q2": len(by_pair),
        "q2_stimuli_with_at_least_two_raters": len(first_stimulus_agreement),
        "q2_stimuli_with_one_rater": first_stimuli_single_rater,
        "first_category_counts": dict(sorted(first_counts.items())),
        "second_category_counts": dict(sorted(second_counts.items())),
        "pairwise_comparisons": compared,
        "exact_first_fraction": round(exact_first / compared, 6),
        "exact_first_mean_per_stimulus": round(statistics.mean(first_stimulus_agreement), 6),
        "exact_first_per_stimulus_range": [
            round(min(first_stimulus_agreement), 6),
            round(max(first_stimulus_agreement), 6),
        ],
        "shared_either_fraction_exploratory": round(shared_either / compared, 6),
        "caveat": "Respuesta Q2/Q22 solamente; sin alfa, jerarquía fina ni validez en rope flow."
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
