#!/usr/bin/env python3
"""Dos acciones con prefijo observado idéntico y destinos posteriores opuestos."""

from math import isclose


def trajectory(time_s: float, destination: int) -> float:
    assert destination in (-1, 1)
    return 0.0 if time_s <= 0.5 else destination * 2.0 * (time_s - 0.5)


def main() -> None:
    times = [i / 20 for i in range(21)]
    left = [trajectory(t, -1) for t in times]
    right = [trajectory(t, 1) for t in times]
    prefix = [i for i, t in enumerate(times) if t <= 0.5]
    assert all(isclose(left[i], right[i]) for i in prefix)
    assert left[-1] == -1.0 and right[-1] == 1.0
    assert left[11] != right[11]
    print("prefijo hasta 0,5 s: idéntico en ambas acciones")
    print("destinos a 1,0 s: izquierda y derecha")
    print("una etiqueta retrospectiva de destino no estaba observada a 0,5 s")


if __name__ == "__main__":
    main()
