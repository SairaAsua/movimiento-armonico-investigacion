"""Dos historias causales con exactamente las mismas señales observadas."""

from math import sin


def drive(t):
    # Señal no periódica: oscilación, deriva y dos eventos breves.
    return sin(0.19 * t) + 0.002 * t + (1 if t == 31 else 0) - (0.7 if t == 73 else 0)


delay_pelvis, delay_hand, delay_rope = 2, 5, 9
times = range(20, 120)

common = [
    (drive(t - delay_pelvis), drive(t - delay_hand), drive(t - delay_rope))
    for t in times
]

# Historia alternativa: pelvis recibe la señal; mano sigue a pelvis;
# soga sigue a mano. Los retardos incrementales son 3 y 4 muestras.
def pelvis(t):
    return drive(t - delay_pelvis)


def hand_from_pelvis(t):
    return pelvis(t - (delay_hand - delay_pelvis))


def rope_from_hand(t):
    return hand_from_pelvis(t - (delay_rope - delay_hand))


chain = [(pelvis(t), hand_from_pelvis(t), rope_from_hand(t)) for t in times]
assert common == chain
assert len({row[0] for row in common}) > 50
print("OK: causa común y cadena producen 100 tripletas idénticas")
