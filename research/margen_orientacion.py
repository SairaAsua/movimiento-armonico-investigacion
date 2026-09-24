#!/usr/bin/env python3
"""Synthetic angular margins for a proposed 24-bin orientation descriptor.

This is project mathematics, not a transcription of Laban's vector signs.
No human/camera data are loaded.
"""

from __future__ import annotations

import math


def unit(v: tuple[float, float, float]) -> tuple[float, float, float]:
    length = math.sqrt(sum(x * x for x in v))
    if not length or not math.isfinite(length):
        raise ValueError("orientation must have finite, nonzero length")
    result = tuple(x / length for x in v)
    if not all(math.isfinite(x) for x in result):
        raise ValueError("orientation must have finite components")
    return result  # type: ignore[return-value]


def signature(v: tuple[float, float, float]) -> tuple[tuple[int, int, int], int]:
    u = unit(v)
    if any(x == 0 for x in u):
        raise ValueError("orientation is on an octant boundary")
    sizes = [abs(x) for x in u]
    strongest = max(range(3), key=sizes.__getitem__)
    if sizes.count(sizes[strongest]) > 1:
        raise ValueError("orientation is on a dominant-axis boundary")
    signs = tuple(1 if x > 0 else -1 for x in u)
    return signs, strongest  # type: ignore[return-value]


def margins_deg(v: tuple[float, float, float]) -> tuple[float, float, float]:
    """Exact spherical angles to octant, dominant-axis, full-order boundaries."""
    u = unit(v)
    a = sorted((abs(x) for x in u), reverse=True)
    octant = math.asin(a[-1])
    dominant = math.asin((a[0] - a[1]) / math.sqrt(2))
    full_order = min(
        math.asin((a[0] - a[1]) / math.sqrt(2)),
        math.asin((a[1] - a[2]) / math.sqrt(2)),
    )
    return tuple(math.degrees(x) for x in (octant, dominant, full_order))  # type: ignore[return-value]


def main() -> None:
    cone_deg = 3.0  # illustrative hard angular bound, not a measured camera error
    scenarios = {
        "separado": (0.8, 0.5, 0.3),
        "casi_empate": (0.71, 0.69, 0.14),
        "casi_plano_de_signo": (0.99, 0.1, 0.01),
    }
    for label, v in scenarios.items():
        o, d, f = margins_deg(v)
        print(
            f"{label}: margen_octante={o:.2f}°, "
            f"margen_eje_dominante={d:.2f}°, "
            f"margen_orden_completo={f:.2f}°, "
            f"clase_24_estable_bajo_{cone_deg:g}°={cone_deg < min(o, d)}"
        )

    assert signature((0.8, 0.5, 0.3)) == ((1, 1, 1), 0)
    assert margins_deg((1.0, 1.0, 0.1))[1] == 0.0
    assert margins_deg((1.0, 0.1, 0.0))[0] == 0.0
    # A mirror change reverses the octant but preserves all angular margins.
    assert margins_deg((0.8, 0.5, 0.3)) == margins_deg((-0.8, 0.5, 0.3))
    print("sanity_checks=ok")


if __name__ == "__main__":
    main()
