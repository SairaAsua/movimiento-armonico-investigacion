#!/usr/bin/env python3
"""Contract regression probe for the public HarMoCAP reference receiver.

Usage: python probar_gating_harmocap.py /path/to/harmocap-nico-kit
Uses only synthetic public fixture data; no sockets, camera, model or audio.
Exit 1 means the receiver violates the documented frame handshake gate.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


def main(kit: Path) -> int:
    sys.path.insert(0, str(kit.resolve()))
    import osc_receiver_example  # type: ignore[import-not-found]
    import replay  # type: ignore[import-not-found]

    fixture = kit / "examples/fixtures/calibration.jsonl"
    frames = [json.loads(line) for line in fixture.read_text().splitlines()]
    first = frames[0]
    next_generation = next(d for d in frames if d["calibration_generation"] != first["calibration_generation"])

    class Receiver(osc_receiver_example.ContractReceiver):
        def __init__(self) -> None:
            super().__init__(quiet=True)
            self.applied: list[tuple[int, str, int]] = []

        def on_movement(self, slot: int, person: dict, meta: list) -> None:
            self.applied.append((meta[1], meta[5], meta[6]))

        def on_absent(self, slot: int) -> None:
            pass

    rx = Receiver()
    for packet in replay.handshake_bytes(first):
        rx.handle_datagram(packet)

    seq = 0

    def send_frame(frame: dict) -> None:
        nonlocal seq
        packets = replay.frame_to_wire(frame, seq + 1, 0)
        for packet in packets:
            rx.handle_datagram(packet)
        seq += len(packets)

    send_frame(first)  # valid under generation 1
    send_frame(next_generation)  # invalid until generation-2 handshake
    wrong_contract = dict(next_generation)
    wrong_contract["contract_id"] = "0" * 32
    wrong_contract["captured_frame_id"] = next_generation["captured_frame_id"] + 1
    send_frame(wrong_contract)  # invalid regardless of generation

    for packet in replay.handshake_bytes(next_generation):
        rx.handle_datagram(packet)
    good_after_handshake = dict(next_generation)
    good_after_handshake["captured_frame_id"] = next_generation["captured_frame_id"] + 2
    send_frame(good_after_handshake)  # valid under generation 2

    expected = [first["captured_frame_id"], good_after_handshake["captured_frame_id"]]
    observed = [frame_id for frame_id, _, _ in rx.applied]
    print("expected_applied_frame_ids", expected)
    print("observed_applied_frame_ids", observed)
    print("reference_receiver_stats", rx.stats)
    if observed != expected:
        print("FAIL: el receptor aplicó frames sin handshake del frame coincidente")
        return 1
    print("PASS: gating coincide con la especificación")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: python probar_gating_harmocap.py /path/to/harmocap-nico-kit")
    raise SystemExit(main(Path(sys.argv[1])))
