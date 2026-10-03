"""Check finite-window phase concentration for uncoupled constant rates."""

from __future__ import annotations

from math import cos, pi, sin


def analytic_r(detuning_hz: float, seconds: float) -> float:
    x = pi * detuning_hz * seconds
    return 1.0 if x == 0 else abs(sin(x) / x)


def sampled_r(detuning_hz: float, seconds: float, samples: int = 100_000) -> float:
    # Midpoint quadrature approximates a uniform time integral, not independent cycles.
    real = 0.0
    imag = 0.0
    for n in range(samples):
        phase = 2 * pi * detuning_hz * seconds * (n + 0.5) / samples
        real += cos(phase)
        imag += sin(phase)
    return (real * real + imag * imag) ** 0.5 / samples


def main() -> None:
    assert analytic_r(0, 10) == 1
    for detuning, seconds in ((0.02, 1), (0.02, 5), (0.02, 10), (0.02, 50),
                              (0.1, 1), (0.1, 5), (0.1, 10)):
        exact = analytic_r(detuning, seconds)
        numeric = sampled_r(detuning, seconds)
        assert abs(exact - numeric) < 1e-8, (detuning, seconds, exact, numeric)
        print(f"detuning={detuning:.2f} Hz, T={seconds:g} s, R={exact:.6f}")


if __name__ == "__main__":
    main()
