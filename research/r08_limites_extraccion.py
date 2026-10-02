#!/usr/bin/env python3
"""Construct adversarial image candidates for Weaver R08 mask/path proposals.

Usage: python research/r08_limites_extraccion.py /path/to/harmonic-weaver
These are in-memory synthetic pictures, not video or human rope motion.
"""

from __future__ import annotations

import argparse
import hashlib
import sys
from pathlib import Path

from r08_sonido_diagnostico import HEIGHT, WIDTH, projected_tensor


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("weaver_checkout", type=Path)
    args = parser.parse_args()
    source = args.weaver_checkout / "src"
    if not source.is_dir():
        parser.error("Weaver checkout must contain src/")
    sys.path.insert(0, str(source))

    import numpy as np
    from harmonic_weaver.lab.research.rope_mask import propose as propose_mask
    from harmonic_weaver.lab.research.rope_path import propose as propose_path

    def candidate(image: np.ndarray, label: str) -> dict:
        result = propose_mask(image, {
            "target_rgb": [255, 255, 255], "distance_rgb": 40,
            "min_component_px": 100, "max_components": 4,
        })
        result.update(media_sha256=hashlib.sha256(image.tobytes()).hexdigest(),
                      frame_index=0, time_s=0.0)
        print(label, [(c["component_id"], c["area_px"])
                      for c in result["candidate_components"]])
        return result

    def path(result: dict, component_id: int, start: tuple, stop: tuple) -> dict:
        return propose_path(result, {
            "component_id": component_id,
            "start": {"x": start[0] / WIDTH, "y": start[1] / HEIGHT},
            "stop": {"x": stop[0] / WIDTH, "y": stop[1] / HEIGHT},
        })

    # A filled, non-rope object passes the color, connectivity and path gates.
    rectangle = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)
    rectangle[500:560, 400:700] = 255
    proposed = candidate(rectangle, "non-rope rectangle:")
    assert proposed["components_detected"] == 1
    rectangle_path = path(proposed, proposed["candidate_components"][0]["component_id"],
                          (450.5, 530.5), (650.5, 530.5))
    assert rectangle_path["supported"]
    tensor = projected_tensor({"state": "observed",
                               "visible_segments": [rectangle_path["points"]]})
    assert tensor is not None and abs(tensor["m_xx"] - 1.0) < 1e-12
    print("non-rope rectangle: seeded path supported, M2 xx=1")

    # The largest white region is a distractor; candidate rank is not identity.
    distractor = np.zeros_like(rectangle)
    distractor[100:140, 100:300] = 255  # 8000 px
    distractor[538:542, 768:1152] = 255  # 1536 px: target-like line
    proposed = candidate(distractor, "larger distractor:")
    assert [c["area_px"] for c in proposed["candidate_components"]] == [8000, 1536]
    first = path(proposed, proposed["candidate_components"][0]["component_id"],
                 (770.5, 539.5), (1149.5, 539.5))
    assert not first["supported"] and first["cause"] == "seed_outside_selected_component"
    second = path(proposed, proposed["candidate_components"][1]["component_id"],
                  (770.5, 539.5), (1149.5, 539.5))
    assert second["supported"]
    print("larger distractor: largest-component choice fails; explicit second choice works")

    # A dark occlusion splits one drawn line. The path tool does not bridge it.
    split = np.zeros_like(rectangle)
    split[538:542, 768:1152] = 255
    split[538:542, 950:970] = 0
    proposed = candidate(split, "20-px gap:")
    assert proposed["components_detected"] == 2
    assert sorted(c["area_px"] for c in proposed["candidate_components"]) == [728, 728]
    bridged = path(proposed, proposed["candidate_components"][0]["component_id"],
                   (770.5, 539.5), (1149.5, 539.5))
    assert not bridged["supported"] and bridged["cause"] == "seed_outside_selected_component"
    print("20-px gap: two components; no supported path between sides")

    print("Candidate support proves only a path in selected white pixels, not rope identity.")


if __name__ == "__main__":
    main()
