"""Synthetic, offline handoff for an already-adjudicated phrase descriptor.

This is a research contract fixture, not a HarMoCAP, Weaver or Beacon adapter.
Times, event identities and certification flags are invented. It never reads video.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Adjudication:
    event_ids: tuple[str, ...]
    possible_words: tuple[str, ...]
    cross_leader_tie_possible: bool
    episodes_complete: bool
    continuity_verified: bool
    hard_bounds_audited: bool


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
    adjudication: Adjudication
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

        if message.state != "closed_valid":
            return out  # partial, aborted or superseded never becomes an audio value
        proof = message.adjudication
        if (not proof.episodes_complete or not proof.continuity_verified
                or not proof.hard_bounds_audited or proof.cross_leader_tie_possible
                or not proof.event_ids or len(set(proof.event_ids)) != len(proof.event_ids)
                or len(proof.possible_words) != 1
                or message.certified_word != proof.possible_words[0]
                or not message.certified_word
                or set(message.certified_word) - {"D", "I"}
                or len(message.certified_word) != len(proof.event_ids)):
            return out + self._clear(received_at_us, "adjudication_not_certified")
        self.active = message
        out.append(Action("publish", message.phrase_id, message.revision, "retrospective", received_at_us))
        return out


def main() -> None:
    gate = PhraseHandoff()
    ctx = ("person_A", "stream_A", "session_clock", "cal_A")

    def m(phrase: str, rev: int, state: str = "closed_valid", word: str | None = "DDII",
          closed: int = 100, available: int = 110, expires: int = 200,
          context: tuple[str, str, str, str] = ctx, fingerprint: str | None = None,
          possible_words: tuple[str, ...] | None = None, tie: bool = False,
          complete: bool = True, continuity: bool = True,
          bounds_audited: bool = True) -> Phrase:
        proof = Adjudication(tuple(f"e{i}" for i in range(len(word or ""))),
                             possible_words if possible_words is not None else ((word,) if word else ()),
                             tie, complete, continuity, bounds_audited)
        return Phrase(phrase, rev, context, closed, available, expires, state, word, proof,
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
    assert gate.ingest(m("p4b", 1, tie=True), 161) == []  # a false closed_valid does not publish
    assert gate.ingest(m("p4c", 1, possible_words=("DDII", "DIDI")), 162) == []
    assert gate.ingest(m("p4d", 1, complete=False), 163) == []
    assert gate.ingest(m("p4e", 1, continuity=False), 164) == []
    assert gate.ingest(m("p4f", 1, bounds_audited=False), 165) == []

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
    print("OK: retrospective publish, adjudication gate, idempotence, partial/aborted, correction, availability, expiry, context reset")


if __name__ == "__main__":
    main()
