#!/usr/bin/env python3
"""Replay the proposed pair gate through Weaver's isolated recording transport.

Usage: python research/replay_par_espacial_weaver.py /path/to/harmonic-weaver
No camera, OSC, beacon-spatial process or audio is used.
"""

import json
import subprocess
import sys
from pathlib import Path

from par_espacial_live_sintetico import demo_events


def main():
    if len(sys.argv) != 2:
        raise SystemExit("usage: replay_par_espacial_weaver.py WEAVER_CHECKOUT")
    root = Path(sys.argv[1]).resolve()
    if not (root / "src/harmonic_weaver/engine/core.py").is_file():
        raise SystemExit("WEAVER_CHECKOUT does not contain the engine source")
    commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True).strip()
    sys.path[:0] = [str(root / "src"), str(root / "tests")]
    from engine_fixtures import ready_engine, route, scene
    from harmonic_weaver.engine import INVALID, OBSERVED

    engine, recorder, source, _instrument = ready_engine(channels={"distance": (0.0, 2.0)})
    mapping = route(
        "pair-distance", channel="sensor.distance", voice=0,
        transforms=[{"type": "scale_range", "in": [0.0, 2.0],
                     "out": [0.0, 1.0], "clamp": True}],
        validity={"held": "reject", "min_confidence": 0.0, "invalid": "reset"},
    )
    engine.upsert_scene(scene(routes=[mapping]), engine.stage_revision)
    engine.switch_scene("main", 1, engine.stage_revision)
    recorder.clear()
    events = demo_events()
    for sequence, event in enumerate(events):
        valid = event["state"] == "eligible_numeric"
        value = event["distance"] if valid else 0.0  # Sentinel is ignored on invalid.
        accepted = engine.ingest_source_frame(
            "sensor", "0000000000000001", source["contract_id"], sequence,
            {"distance": (value, OBSERVED if valid else INVALID,
                          1.0 if valid else 0.0)}, now_us=event["at_us"],
        )
        assert accepted
    records = [(item.reason, item.value, item.sent_at_us) for item in recorder.records]
    assert [(reason, value) for reason, value, _ in records] == [
        ("route", 0.5), ("route_reset", 0.0),
    ] * 4
    assert [sent_at_us for _, _, sent_at_us in records] == [
        event["at_us"] for event in events
    ]
    print(json.dumps({"weaver_commit": commit,
                      "source_events": len(events),
                      "recorded_controls": [
                          {"event": event.get("reason", event["state"]),
                           "reason": reason, "value": value, "sent_at_us": sent_at_us}
                          for event, (reason, value, sent_at_us) in zip(events, records)
                      ]}, sort_keys=True))


if __name__ == "__main__":
    main()
