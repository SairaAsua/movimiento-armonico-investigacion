"""Comprobaciones sintéticas de ciclo y fase para rope flow.

Ejecutar: python fase_sintetica.py
Biblioteca estándar; no contiene medidas humanas ni valida HIT.
"""

from bisect import bisect_right
from cmath import phase
from math import cos, pi, sin
from random import Random


TAU = 2 * pi


def periodic_peak_count(values):
    """Cuenta máximos locales de una señal periódica muestreada sin extremos."""
    n = len(values)
    return sum(
        values[i] >= values[(i - 1) % n]
        and values[i] >= values[(i + 1) % n]
        and (values[i] > values[(i - 1) % n]
             or values[i] > values[(i + 1) % n])
        for i in range(n)
    )


def event_phase(t, events, invalid_intervals=()):
    """Interpola entre eventos anotados sólo si el intervalo es válido."""
    assert all(a < b for a, b in zip(events, events[1:]))
    k = bisect_right(events, t) - 1
    if k < 0 or k >= len(events) - 1:
        return None
    start, end = events[k], events[k + 1]
    if (start, end) in invalid_intervals:
        return None
    return TAU * (t - start) / (end - start)


def phase_relation(phases_i, phases_j, p, q):
    """f_i/f_j = p/q; devuelve concentración y desfase circular medio."""
    assert len(phases_i) == len(phases_j) and phases_i
    z = sum(complex(cos(q * a - p * b), sin(q * a - p * b))
            for a, b in zip(phases_i, phases_j)) / len(phases_i)
    return abs(z), phase(z)


def pearson(xs, ys):
    """Correlación descriptiva de residuos de evento, sin inferencia estadística."""
    assert len(xs) == len(ys) and len(xs) > 1
    mx, my = sum(xs) / len(xs), sum(ys) / len(ys)
    numerator = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    denominator = (
        sum((x - mx) ** 2 for x in xs)
        * sum((y - my) ** 2 for y in ys)
    ) ** 0.5
    assert denominator > 0
    return numerator / denominator


def phrase_repair_control(shared_residual):
    """Control de residuos por frases emparejadas dentro de tarea ficticia.

    Preserva orden de los 16 ciclos y distribución de cada señal/frase. Rompe
    la coincidencia entre señales de frases distintas del mismo patrón.
    """
    rng = Random(781)
    phrases = []
    for phrase_id in range(24):
        pattern = phrase_id // 12
        a, b_independent = 0.0, 0.0
        left, right = [], []
        for _ in range(16):
            a = 0.6 * a + rng.gauss(0, 1)
            b_independent = 0.6 * b_independent + rng.gauss(0, 1)
            left.append(a)
            right.append(0.8 * a + 0.3 * b_independent if shared_residual
                         else b_independent)
        phrases.append((pattern, left, right))

    matched_left = [x for _, left, _ in phrases for x in left]
    matched_right = [x for _, _, right in phrases for x in right]
    original = pearson(matched_left, matched_right)
    # Dentro de cada patrón, asociar cada frase con la siguiente (cierre
    # circular); los 16 residuos permanecen en su orden dentro de la frase.
    repaired_right = []
    for i, (pattern, _, _) in enumerate(phrases):
        next_i = pattern * 12 + ((i - pattern * 12 + 1) % 12)
        repaired_right.extend(phrases[next_i][2])
    surrogate = pearson(matched_left, repaired_right)
    return original, surrogate


def main():
    # Cinco ciclos de posición senoidal; rapidez tiene dos picos por ciclo.
    samples_per_cycle, cycles = 100, 5
    speed = [abs(cos(TAU * i / samples_per_cycle))
             for i in range(samples_per_cycle * cycles)]
    peaks = periodic_peak_count(speed)
    annotated_cycles = len(list(range(cycles + 1))) - 1
    assert peaks == 2 * annotated_cycles == 10

    # Un evento ausente no autoriza interpolar a través de una pausa/transición.
    events = [0, 1, 2, 4, 5]
    assert abs(event_phase(1.5, events) - pi) < 1e-12
    assert event_phase(3, events, {(2, 4)}) is None

    # Relación 2:1 bajo cadencia variable: la velocidad instantánea cambia,
    # pero ambas fases siguen exactamente la relación definida.
    t = [8 * i / 800 for i in range(800)]
    base = [TAU * (0.8 * x + 0.5 * 0.08 * x * x) for x in t]
    twice = [2 * x + 0.3 for x in base]
    locked_r, locked_angle = phase_relation(twice, base, 2, 1)
    assert abs(locked_r - 1) < 1e-12
    assert abs(locked_angle - 0.3) < 1e-12

    # La misma cadencia variable con un desajuste de 0,125 Hz completa una
    # vuelta de diferencia en ocho segundos: concentración casi nula.
    detuned = [2 * x + TAU * 0.125 * ti + 0.3 for x, ti in zip(base, t)]
    detuned_r, _ = phase_relation(detuned, base, 2, 1)
    assert detuned_r < 1e-10

    # Alternancia 1:1: concentración perfecta con desfase de media vuelta.
    opposite = [x + pi for x in base]
    anti_r, anti_angle = phase_relation(opposite, base, 1, 1)
    assert abs(anti_r - 1) < 1e-12
    assert abs(abs(anti_angle) - pi) < 1e-12

    # Un retardo fijo sesga la fase media sin disminuir su concentración.
    frequency_hz, lag_s = 2.0, 0.02
    ref = [TAU * frequency_hz * x for x in t]
    delayed = [TAU * frequency_hz * (x - lag_s) for x in t]
    lag_r, lag_angle = phase_relation(ref, delayed, 1, 1)
    expected_lag_degrees = 360 * frequency_hz * lag_s
    assert abs(lag_r - 1) < 1e-12
    assert abs(lag_angle * 180 / pi - expected_lag_degrees) < 1e-10

    # Dos señales pueden seguir exactamente el mismo metrónomo sin que sus
    # variaciones ciclo a ciclo estén relacionadas entre sí.
    n_cycles = 16
    residual_i = [0.02 * (-1) ** k for k in range(n_cycles)]
    residual_j = [0.02 * (-1) ** (k // 2) for k in range(n_cycles)]
    event_i = [k + 0.1 + residual_i[k] for k in range(n_cycles)]
    event_j = [k + 0.3 + residual_j[k] for k in range(n_cycles)]
    common_r, _ = phase_relation(
        [TAU * x for x in event_i],
        [TAU * x for x in event_j], 1, 1,
    )
    residual_r = pearson(residual_i, residual_j)
    assert common_r > 0.98
    assert abs(residual_r) < 1e-12

    # Un desplazamiento circular de una señal periódica pura cambia su ángulo
    # relativo pero deja R=1: no sirve como nulo para sincronía en esta tarea.
    pure_i = [TAU * k / 100 for k in range(800)]
    pure_j = [x + 0.4 for x in pure_i]
    shifted_j = pure_j[23:] + pure_j[:23]
    shifted_r, _ = phase_relation(pure_i, shifted_j, 1, 1)
    assert abs(shifted_r - 1) < 1e-12

    # Dos ciclos internamente bloqueados pero con fase opuesta. El ciclo lento
    # pesa tres veces más en tiempo; promediar módulos por ciclo borra el cambio.
    cycle_vectors = [complex(cos(a), sin(a)) for a in (0.0, pi)]
    time_vector = (cycle_vectors[0] + 3 * cycle_vectors[1]) / 4
    equal_cycle_vector = sum(cycle_vectors) / 2
    mean_cycle_strength = sum(abs(z) for z in cycle_vectors) / 2
    assert abs(abs(time_vector) - 0.5) < 1e-12
    assert abs(equal_cycle_vector) < 1e-12
    assert abs(mean_cycle_strength - 1) < 1e-12

    null_matched, null_repaired = phrase_repair_control(False)
    shared_matched, shared_repaired = phrase_repair_control(True)
    assert abs(null_matched) < 0.15 and abs(null_repaired) < 0.15
    assert shared_matched > 0.9 and abs(shared_repaired) < 0.15

    print(f"picos de rapidez={peaks}; ciclos anotados={annotated_cycles}")
    print("intervalo de transición sin fase:", event_phase(3, events, {(2, 4)}))
    print(f"2:1 variable bloqueada: R={locked_r:.6f}, ángulo={locked_angle:.6f} rad")
    print(f"2:1 desajustada: R={detuned_r:.6f}")
    print(f"1:1 alternada: R={anti_r:.6f}, ángulo={anti_angle:.6f} rad")
    print(f"retardo fijo: R={lag_r:.6f}, sesgo={expected_lag_degrees:.1f}°")
    print(f"ritmo común: R={common_r:.6f}, correlación de residuos={residual_r:.6f}")
    print(f"desplazamiento circular de señal periódica: R={shifted_r:.6f}")
    print(f"ciclos 1s/3s opuestos: R_t={abs(time_vector):.6f}, "
          f"R_c={abs(equal_cycle_vector):.6f}, "
          f"promedio R_por_ciclo={mean_cycle_strength:.6f}")
    print(f"reemparejamiento de frases: nulo residuos original/control="
          f"{null_matched:.6f}/{null_repaired:.6f}; "
          f"residuo compartido original/control={shared_matched:.6f}/"
          f"{shared_repaired:.6f}")


if __name__ == "__main__":
    main()
