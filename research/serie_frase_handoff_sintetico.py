"""Synthetic, offline handoff for an already-adjudicated phrase descriptor.

This is a research contract fixture, not a HarMoCAP, Weaver or Beacon adapter.
Times, event identities and certification flags are invented. It never reads video.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Phrase:
    phrase_id: str
    revision: int
    context: tuple[str, str, str, str]  # person, stream, clock, calibration
    closed_at_us: int
    available_at_us: int
    expires_at_us: int
    state: str
    certified_word: str | None
    fingerprint: str  # stable digest of the scientific source record


@dataclass(frozen=True)
class Action:
    kind: str
    phrase_id: str | None
    revision: int | None
    reason: str
    at_us: int


class PhraseHandoff:
    def __init__(self) -> None:
        self.active: Phrase | None = None
        self.seen: dict[tuple[tuple[str, str, str, str], str, int], Phrase] = {}

    def _clear(self, at_us: int, reason: str) -> list[Action]:
        if self.active is None:
            return []
        old = self.active
        self.active = None
        return [Action("reset", old.phrase_id, old.revision, reason, at_us)]

    def expire(self, at_us: int) -> list[Action]:
        if self.active is not None and at_us >= self.active.expires_at_us:
            return self._clear(at_us, "expired")
        return []

    def ingest(self, message: Phrase, received_at_us: int,
               transport_status: str = "observed") -> list[Action]:
        out = self.expire(received_at_us)
        if transport_status in {"held", "invalid"}:
            return out + self._clear(received_at_us, f"transport_{transport_status}")
        if transport_status != "observed":
            return out + self._clear(received_at_us, "unknown_transport_status")
        key = (message.context, message.phrase_id, message.revision)
        if key in self.seen:
            if self.seen[key] != message:
                return out + self._clear(received_at_us, "conflicting_revision")
            return out  # replay of exactly the same revision is idempotent

        if message.revision < 1 or not all(message.context) or not message.phrase_id:
            return out + self._clear(received_at_us, "malformed_identity")
        if message.closed_at_us > message.available_at_us or message.available_at_us > received_at_us:
            return out + self._clear(received_at_us, "not_available")
        if message.expires_at_us <= received_at_us:
            return out + self._clear(received_at_us, "stale_on_arrival")

        self.seen[key] = message
        if self.active is not None:
            if message.context != self.active.context or message.phrase_id != self.active.phrase_id:
                out += self._clear(received_at_us, "new_context_or_phrase")
            elif message.revision <= self.active.revision:
                return out
            else:
                out += self._clear(received_at_us, "superseded")

        if message.state != "closed_valid" or message.certified_word is None:
            return out  # partial, aborted or superseded never becomes an audio value
        if not message.certified_word or set(message.certified_word) - {"D", "I"}:
            return out + self._clear(received_at_us, "invalid_word")
        self.active = message
        out.append(Action("publish", message.phrase_id, message.revision, "retrospective", received_at_us))
        return out


def main() -> None:
    gate = PhraseHandoff()
    ctx = ("person_A", "stream_A", "session_clock", "cal_A")

    def m(phrase: str, rev: int, state: str = "closed_valid", word: str | None = "DDII",
          closed: int = 100, available: int = 110, expires: int = 200,
          context: tuple[str, str, str, str] = ctx, fingerprint: str | None = None) -> Phrase:
        return Phrase(phrase, rev, context, closed, available, expires, state, word,
                      fingerprint or f"{phrase}:{rev}:{state}:{word}")

    assert [a.kind for a in gate.ingest(m("p1", 1), 120)] == ["publish"]
    assert gate.ingest(m("p1", 1), 121) == []  # duplicate observed bundle
    assert [a.reason for a in gate.ingest(m("p1", 1, fingerprint="conflict"), 122)] == ["conflicting_revision"]
    assert gate.active is None

    assert [a.kind for a in gate.ingest(m("p2", 1, word="DDI"), 130)] == ["publish"]
    # A later correction invalidates the earlier audio; it cannot undo what was heard.
    assert [a.reason for a in gate.ingest(m("p2", 2, state="closed_partial", word=None), 140)] == ["superseded"]
    assert gate.active is None
    assert gate.ingest(m("p3", 1, state="closed_partial", word=None), 150) == []  # cross-hand tie
    assert gate.ingest(m("p4", 1, state="aborted", word=None), 160) == []  # hidden episode

    assert [a.kind for a in gate.ingest(m("p5", 1), 170)] == ["publish"]
    assert [a.reason for a in gate.ingest(m("p6", 1, available=180), 175)] == ["not_available"]
    assert gate.active is None
    assert [a.kind for a in gate.ingest(m("p7", 1, expires=175), 180)] == []
    assert [a.kind for a in gate.ingest(m("p8", 1, expires=190), 185)] == ["publish"]
    assert [a.reason for a in gate.expire(190)] == ["expired"]

    assert [a.kind for a in gate.ingest(m("p9", 1), 195)] == ["publish"]
    assert [a.reason for a in gate.ingest(m("p9", 1), 196, "held")] == ["transport_held"]
    assert [a.kind for a in gate.ingest(m("p9", 2), 196)] == ["publish"]
    assert [a.reason for a in gate.ingest(m("p9", 2), 196, "invalid")] == ["transport_invalid"]
    assert [a.kind for a in gate.ingest(m("p9", 3), 196)] == ["publish"]
    assert [a.reason for a in gate.ingest(m("p9", 3, expires=201), 196)] == ["conflicting_revision"]
    assert [a.kind for a in gate.ingest(m("p9", 4), 196)] == ["publish"]
    other = ("person_B", "stream_B", "session_clock", "cal_A")
    # Local phrase labels may repeat after a person/stream change.
    assert [a.kind for a in gate.ingest(m("p9", 1, context=other), 196)] == ["reset", "publish"]
    assert [a.kind for a in gate.ingest(m("p11", 1, context=other), 197)] == ["reset", "publish"]
    assert [a.reason for a in gate.ingest(m("p12", 1, state="closed_partial", word=None,
                                           context=other), 198)] == ["new_context_or_phrase"]
    assert gate.active is None
    print("OK: retrospective publish, idempotence, partial/aborted, correction, availability, expiry, context reset")


if __name__ == "__main__":
    main()
