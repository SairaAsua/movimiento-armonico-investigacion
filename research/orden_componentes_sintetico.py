#!/usr/bin/env python3
"""Exploratory signed component orders; not a decoder of Laban's original signs."""

from __future__ import annotations

from itertools import permutations, product

from margen_orientacion import margins_deg, unit

AXES = ("lateral", "vertical", "sagital")
# Cyclic orders described in Longstaff's table 2 for each octant. This maps
# only rank order, not the precise historical angular regions or vector signs.
NOMINAL_ORDERS = {(0, 1, 2), (1, 2, 0), (2, 0, 1)}


def classify(
    vector: tuple[float, float, float],
    *,
    angular_bound_deg: float,
    direction_identified: bool,
) -> dict[str, object]:
    """Return a class only when a *hard* angular bound clears every border.

    A statistical 95% interval must not be supplied as a hard bound. The caller
    must independently establish that the displacement/axis is identifiable.
    """
    if not 0 <= angular_bound_deg < 90:
        raise ValueError("angular_bound_deg must be in [0, 90)")
    u = unit(vector)
    oct_margin, dominant_margin, full_margin = margins_deg(vector)
    result: dict[str, object] = {
        "vector": u,
        "margins_deg": (oct_margin, dominant_margin, full_margin),
        "coarse_24": None,
        "order_48": None,
        "table2_candidate": "indeterminado",
    }
    if not direction_identified:
        return result
    signs = tuple(1 if x > 0 else -1 for x in u)
    sizes = tuple(abs(x) for x in u)
    ranking = tuple(sorted(range(3), key=lambda i: sizes[i], reverse=True))
    if angular_bound_deg < min(oct_margin, dominant_margin):
        result["coarse_24"] = (signs, ranking[0])
    if angular_bound_deg < min(oct_margin, full_margin):
        result["order_48"] = (signs, ranking)
        result["table2_candidate"] = (
            "orden_nominal_candidato"
            if ranking in NOMINAL_ORDERS
            else "sin_correspondencia_en_tabla_2"
        )
    return result


def main() -> None:
    counts = {"nominal": 0, "other": 0}
    for signs in product((-1, 1), repeat=3):
        for ranking in permutations(range(3)):
            values = [0.0, 0.0, 0.0]
            for rank, axis in enumerate(ranking):
                values[axis] = signs[axis] * (3 - rank)
            result = classify(tuple(values), angular_bound_deg=0, direction_identified=True)
            assert result["order_48"] == (signs, ranking)
            counts["nominal" if ranking in NOMINAL_ORDERS else "other"] += 1
    assert counts == {"nominal": 24, "other": 24}

    clear = classify((0.8, 0.5, 0.3), angular_bound_deg=3, direction_identified=True)
    assert clear["coarse_24"] is not None and clear["order_48"] is not None
    # A cone can clear the dominant-axis border but cross the smaller-to-middle border.
    partial = classify((0.8, 0.35, 0.3), angular_bound_deg=3, direction_identified=True)
    assert partial["coarse_24"] is not None and partial["order_48"] is None
    undefined = classify((0.8, 0.5, 0.3), angular_bound_deg=0, direction_identified=False)
    assert undefined["coarse_24"] is None and undefined["order_48"] is None
    borderline = classify((0.8, 0.5, 0.3), angular_bound_deg=clear["margins_deg"][2], direction_identified=True)
    assert borderline["order_48"] is None
    print("cells=48 nominal_order_candidates=24 other_orders=24")
    print("hard_bound_abstention=ok direction_gate=ok")


if __name__ == "__main__":
    main()
