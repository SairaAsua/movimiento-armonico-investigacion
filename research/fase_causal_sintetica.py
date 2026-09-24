#!/usr/bin/env python3
"""Causal event-phase examples for rope flow; synthetic, standard library only.

The live estimator sees only past task events. This is project mathematics,
not a validated phase estimator for Nico or a HarMoCAP feature.
"""

from __future__ import annotations

import math


def wrap_degrees(deg: float) -> float:
    return (deg + 180.0) % 360.0 - 180.0


def live_phase_deg(t: float, past_events: list[float], max_age_cycles: float = 1.5) -> tuple[str, float | None]:
    """Predict current phase from the last complete, accepted interval."""
    if len(past_events) < 2:
        return "warmup", None
    if any(a >= b for a, b in zip(past_events, past_events[1:])):
        raise ValueError("past events must be strictly increasing")
    if past_events[-1] > t:
        raise ValueError("future event leaked into live estimator")
    period = past_events[-1] - past_events[-2]
    age = t - past_events[-1]
    if age > max_age_cycles * period:
        return "expired", None
    return "estimated", (360.0 * age / period) % 360.0


def offline_phase_deg(t: float, start: float, end: float) -> float:
    if not start <= t < end:
        raise ValueError("time must be inside complete offline cycle")
    return 360.0 * (t - start) / (end - start)


def circle_angle_deg(t: float, start: float, microtiming_amplitude_rad: float) -> float:
    """Ideal circular kinematic angle; not an estimator from video."""
    tau = t - start
    if not 0 <= tau <= 1:
        raise ValueError("synthetic cycle is one second long")
    theta = 2 * math.pi * tau + microtiming_amplitude_rad * math.sin(2 * math.pi * tau)
    return math.degrees(theta) % 360.0


def main() -> None:
    stable_state, stable_live = live_phase_deg(2.5, [0.0, 1.0, 2.0])
    stable_offline = offline_phase_deg(2.5, 2.0, 3.0)
    assert stable_state == "estimated" and math.isclose(stable_live, stable_offline)

    # The next event at 2.8 s is used only for retrospective comparison.
    # It is deliberately absent from the live estimator's input at t=2.4 s.
    accel_state, accel_live = live_phase_deg(2.4, [0.0, 1.0, 2.0])
    accel_offline = offline_phase_deg(2.4, 2.0, 2.8)
    accel_error = wrap_degrees(accel_live - accel_offline)  # type: ignore[operator]
    assert accel_state == "estimated" and math.isclose(accel_error, -36.0, abs_tol=1e-12)

    missing_state, missing_live = live_phase_deg(3.6, [0.0, 1.0, 2.0])
    assert missing_state == "expired" and missing_live is None
    warm_state, warm_live = live_phase_deg(0.4, [0.0])
    assert warm_state == "warmup" and warm_live is None
    try:
        live_phase_deg(2.4, [0.0, 1.0, 2.0, 2.8])
    except ValueError as error:
        assert "future event" in str(error)
    else:
        raise AssertionError("a future event must be rejected")

    # Same prior events and future endpoint, different motion *inside* a cycle.
    micro_state, shared_task_phase = live_phase_deg(2.25, [0.0, 1.0, 2.0])
    angle_a = circle_angle_deg(2.25, 2.0, 0.0)
    angle_b = circle_angle_deg(2.25, 2.0, 0.5)
    assert micro_state == "estimated"
    assert math.isclose(shared_task_phase, 90.0)  # type: ignore[arg-type]
    assert math.isclose(wrap_degrees(angle_b - angle_a), math.degrees(0.5))
    assert math.isclose(circle_angle_deg(3.0, 2.0, 0), circle_angle_deg(3.0, 2.0, 0.5))

    print(f"cadencia_constante: live={stable_live:.1f}°, offline={stable_offline:.1f}°")
    print(f"aceleracion: live={accel_live:.1f}°, offline={accel_offline:.1f}°, error={accel_error:.1f}°")
    print(f"cruce_ausente: estado={missing_state}, fase={missing_live}")
    print(f"un_solo_evento: estado={warm_state}, fase={warm_live}")
    print(f"microtiempo_t=2.25: fase_tarea_live={shared_task_phase:.1f}° para A/B; "
          f"angulo_cinematico_A={angle_a:.2f}°, B={angle_b:.2f}°")
    print("future_event_guard=ok")


if __name__ == "__main__":
    main()
