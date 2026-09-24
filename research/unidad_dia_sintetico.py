"""Contraejemplo sintético: ponderar clips y ponderar días responde preguntas distintas."""

from collections import defaultdict


def mean(values):
    return sum(values) / len(values)


# Diferencia pareada de pérdida: positivo favorece base+Laban.
# Son días ficticios, no ratings de Nico ni estimaciones de tamaño de efecto.
rows = [
    *(('dia_a', 1.0, 0.9) for _ in range(100)),
    *(('dia_b', 1.0, 1.5) for _ in range(5)),
]
by_day = defaultdict(list)
for day, base_loss, laban_loss in rows:
    by_day[day].append(base_loss - laban_loss)

paired_days = {day: mean(differences) for day, differences in by_day.items()}
clip_weighted = mean([difference for values in by_day.values() for difference in values])
day_weighted = mean(list(paired_days.values()))

assert abs(paired_days['dia_a'] - 0.1) < 1e-12
assert abs(paired_days['dia_b'] + 0.5) < 1e-12
assert abs(clip_weighted - 1 / 14) < 1e-12  # +0.071428...
assert abs(day_weighted + 0.2) < 1e-12
print(f"clips_pooled={clip_weighted:+.6f}; dias_equilibrados={day_weighted:+.6f}")
