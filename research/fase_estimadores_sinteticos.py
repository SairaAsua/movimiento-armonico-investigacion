"""Comparación de fase Hilbert offline y posición-velocidad causal, sin datos humanos.

Señales construidas con fase conocida; numpy solamente. Ejecutar con Python.
"""

import numpy as np


FPS = 120
DURATION = 20.0
OMEGA_REF = 2 * np.pi  # tarea nominal de 1 Hz, fijada antes del test
ENVELOPE_GATE = 0.25
SEED = 20260925


def analytic_signal(x):
    """Señal analítica FFT de serie completa: necesariamente retrospectiva."""
    n = len(x)
    h = np.zeros(n)
    h[0] = 1
    if n % 2 == 0:
        h[1:n // 2] = 2
        h[n // 2] = 1
    else:
        h[1:(n + 1) // 2] = 2
    return np.fft.ifft(np.fft.fft(x) * h)


def wrap(angle):
    return np.angle(np.exp(1j * angle))


def estimate(x, observed):
    # Hilbert recibe relleno lineal offline, pero no se acreditan los huecos.
    indices = np.arange(len(x))
    filled = np.interp(indices, indices[observed], x[observed])
    analytic = analytic_signal(filled - np.mean(filled[observed]))
    hilbert_phase = np.angle(analytic)
    hilbert_valid = observed & (np.abs(analytic) >= ENVELOPE_GATE)

    # Velocidad por diferencia hacia atrás: sin futuro. El dato tras un hueco
    # no usa el último punto anterior como si fuera un tramo de 1/FPS.
    velocity = np.empty_like(x)
    velocity[0] = np.nan
    velocity[1:] = (x[1:] - x[:-1]) * FPS
    pv_phase = np.arctan2(-velocity / OMEGA_REF, x)
    pv_radius = np.hypot(x, velocity / OMEGA_REF)
    pv_valid = observed & np.r_[False, observed[:-1]] & (pv_radius >= ENVELOPE_GATE)
    return {'Hilbert_offline': (hilbert_phase, hilbert_valid),
            'PV_backward': (pv_phase, pv_valid)}


def score(phi, valid, truth, time):
    # Alineación con eventos conocidos en 2–4 s; evaluación sólo en 4–18 s.
    calibration = (time >= 2) & (time < 4) & valid
    evaluation = (time >= 4) & (time < 18)
    if np.sum(calibration) < FPS:
        raise ValueError('Calibración de fase insuficiente')
    offset = np.angle(np.mean(np.exp(1j * (truth[calibration] - phi[calibration]))))
    use = evaluation & valid
    err = np.abs(np.rad2deg(wrap(phi[use] + offset - truth[use])))
    return (float(np.mean(use[evaluation])), float(np.median(err)),
            float(np.percentile(err, 90)), float(offset))


def main():
    rng = np.random.default_rng(SEED)
    time = np.arange(int(DURATION * FPS)) / FPS
    stationary = 2 * np.pi * time
    chirp = 2 * np.pi * (0.8 * time + 0.5 * 0.03 * time ** 2)
    cases = {
        'coseno_limpio': (np.cos(stationary), stationary, np.ones(len(time), bool)),
        'cadencia_0.8_a_1.4Hz': (np.cos(chirp), chirp, np.ones(len(time), bool)),
        'segundo_armonico_0.35': (np.cos(stationary) + 0.35 * np.cos(2 * stationary),
                                  stationary, np.ones(len(time), bool)),
    }
    noise = rng.normal(0, 0.03, len(time))
    cases['ruido_0.03_sin_caida'] = (
        np.cos(stationary) + noise, stationary, np.ones(len(time), bool))
    dropout = np.ones(len(time))
    dropout[(time >= 9) & (time < 10)] = 0.1
    cases['amplitud_0.1_con_ruido'] = (
        dropout * np.cos(stationary) + noise,
        stationary, np.ones(len(time), bool))
    observed = ~((time >= 9) & (time < 9.5))
    cases['hueco_0.5s'] = (np.cos(stationary), stationary, observed)

    print(f'fps={FPS} duracion={DURATION}s semilla={SEED} calibracion=2..4s '
          f'evaluacion=4..18s gate_amplitud={ENVELOPE_GATE}')
    for name, (signal, truth, valid_input) in cases.items():
        for method, (phase, valid) in estimate(signal, valid_input).items():
            coverage, median, p90, offset = score(phase, valid, truth, time)
            near_gap = (time >= 8.5) & (time < 10.5)
            gap_coverage = float(np.mean(valid[near_gap]))
            local = near_gap & valid
            local_error_p90 = float(np.percentile(
                np.abs(np.rad2deg(wrap(phase[local] + offset - truth[local]))), 90))
            low_amplitude = (time >= 9) & (time < 10)
            low_coverage = float(np.mean(valid[low_amplitude]))
            print(f'{name} {method} cobertura={coverage:.3f} '
                  f'error_abs_med/p90={median:.2f}/{p90:.2f}deg '
                  f'cobertura_8.5..10.5s={gap_coverage:.3f} '
                  f'cobertura_9..10s={low_coverage:.3f} '
                  f'error_p90_8.5..10.5s={local_error_p90:.2f}deg '
                  f'offset_cal={np.rad2deg(offset):+.1f}deg')

    # Fuga temporal: dos archivos idénticos hasta 12 s, distinto futuro.
    same_past = np.cos(stationary)
    altered_future = same_past.copy()
    altered_future[(time >= 12) & (time < 13)] *= 0.1
    past = (time >= 11) & (time < 12)
    h0 = np.angle(analytic_signal(same_past))
    h1 = np.angle(analytic_signal(altered_future))
    h_change = np.abs(np.rad2deg(wrap(h1[past] - h0[past])))
    pv0 = estimate(same_past, np.ones(len(time), bool))['PV_backward'][0]
    pv1 = estimate(altered_future, np.ones(len(time), bool))['PV_backward'][0]
    assert np.array_equal(pv0[past], pv1[past])
    assert np.max(h_change) > 40
    print(f'futuro_alterado_12..13s fase_Hilbert_cambia_11..12s '
          f'med/p95/max={np.median(h_change):.2f}/'
          f'{np.percentile(h_change,95):.2f}/{np.max(h_change):.2f}deg '
          f'PV_pasado_identico={np.array_equal(pv0[past], pv1[past])}')


if __name__ == '__main__':
    main()
