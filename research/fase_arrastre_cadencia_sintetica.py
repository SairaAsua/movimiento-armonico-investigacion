"""Retardo mecánico ideal y concentración de fase bajo cambio de cadencia.

Ejecutar: python research/fase_arrastre_cadencia_sintetica.py
Fases oráculo sintéticas; no hay video, estimación de fase ni datos humanos.
"""

from cmath import exp
from math import pi, sin


def phase(time, f0, acceleration):
    return 2 * pi * (f0 * time + acceleration * time * time / 2)


def concentration(f0, acceleration, delay, duration, samples=10000):
    offsets = (phase((i + 0.5) * duration / samples, f0, acceleration)
               - phase((i + 0.5) * duration / samples - delay, f0, acceleration)
               for i in range(samples))
    return abs(sum(exp(1j * offset) for offset in offsets) / samples)


def main():
    duration = 8.0
    delay = 0.25
    f0 = 1.5
    acceleration = 0.25  # Hz/s: 1,5 → 3,5 Hz durante ocho segundos.
    constant = concentration(f0, 0.0, delay, duration)
    changing = concentration(f0, acceleration, delay, duration)
    half_span = pi * acceleration * delay * duration
    analytic = abs(sin(half_span) / half_span)
    assert abs(constant - 1.0) < 1e-12
    assert abs(changing - analytic) < 1e-8
    assert abs(changing - 2 / pi) < 1e-8
    print(f"retardo={delay:.2f}s, duración={duration:.1f}s")
    print(f"cadencia constante: R={constant:.6f}")
    print(f"cadencia 1.5→3.5 Hz: R={changing:.6f}")
    print(f"valor analítico de referencia={analytic:.6f}")


if __name__ == "__main__":
    main()
