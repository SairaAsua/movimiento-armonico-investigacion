"""Escenarios de resolución temporal y desenfoque, sin datos de cámaras reales.

Ejecutar: python presupuesto_camara.py
Biblioteca estándar. Los valores impresos son ejemplos, no recomendaciones.
"""

from math import sqrt


def half_frame_ms(fps):
    assert fps > 0
    return 500 / fps


def phase_degrees(frequency_hz, timing_error_ms):
    assert frequency_hz >= 0 and timing_error_ms >= 0
    return 360 * frequency_hz * timing_error_ms / 1000


def blur_pixels(pixel_speed_per_s, exposure_s):
    assert pixel_speed_per_s >= 0 and exposure_s >= 0
    return pixel_speed_per_s * exposure_s


def samples_per_cycle_fraction(fps, cycle_hz, fraction):
    assert fps > 0 and cycle_hz > 0 and 0 < fraction <= 1
    return fps * fraction / cycle_hz


def second_difference_noise(pixel_sd, fps):
    """SD of central second-difference error for independent position errors."""
    assert pixel_sd >= 0 and fps > 0
    return sqrt(6) * pixel_sd * fps**2


def main():
    for fps in (30, 60, 120):
        uncertainty_ms = half_frame_ms(fps)
        phases = [phase_degrees(f, uncertainty_ms) for f in (1, 2, 3)]
        print(f"{fps} fps: medio cuadro={uncertainty_ms:.3f} ms; "
              f"fase a 1/2/3 Hz={phases[0]:.1f}/{phases[1]:.1f}/{phases[2]:.1f}°")

    for exposure_denom in (60, 250, 1000):
        blur = blur_pixels(500, 1 / exposure_denom)
        print(f"500 px/s, exposición 1/{exposure_denom} s: "
              f"desenfoque aproximado={blur:.2f} px")

    for fps in (30, 60, 120):
        print(f"{fps} fps a 2 Hz hipotéticos: "
              f"{samples_per_cycle_fraction(fps, 2, 1):.0f} cuadros/vuelta, "
              f"{samples_per_cycle_fraction(fps, 2, 0.1):.1f} en 10 % de vuelta; "
              f"ruido SD de segunda diferencia con σ=1 px="
              f"{second_difference_noise(1, fps):.0f} px/s²")

    assert abs(phase_degrees(2, 10) - 7.2) < 1e-12
    assert abs(half_frame_ms(60) - 8.333333333333334) < 1e-12
    assert abs(blur_pixels(500, 1 / 250) - 2) < 1e-12
    assert abs(samples_per_cycle_fraction(60, 2, 0.1) - 3) < 1e-12
    assert abs(second_difference_noise(1, 60) - sqrt(6) * 3600) < 1e-12


if __name__ == "__main__":
    main()
