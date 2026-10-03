"""Cotas de R temporal con fase faltante; ejemplo exacto, sin personas."""

from __future__ import annotations

import math


def cotas_r(vector_observado: complex, masa_faltante: float) -> tuple[float, float]:
    """R total posible si la fase no vista puede tener cualquier distribución."""
    if not 0 <= masa_faltante <= 1:
        raise ValueError("masa_faltante debe estar entre 0 y 1")
    if abs(vector_observado) > 1 - masa_faltante + 1e-12:
        raise ValueError("resultante observada incompatible con masa válida")
    return (
        max(0.0, abs(vector_observado) - masa_faltante),
        min(1.0, abs(vector_observado) + masa_faltante),
    )


def vector(*masas_y_fases: tuple[float, float]) -> complex:
    return sum((masa * complex(math.cos(fase), math.sin(fase))
                for masa, fase in masas_y_fases), 0j)


def main() -> None:
    # La distribución visible pesa 0,75: 0,60 en fase 0 y 0,15 en fase pi.
    observado = vector((0.60, 0.0), (0.15, math.pi))
    perdido = 0.25
    inferior, superior = cotas_r(observado, perdido)
    testigos = [
        ("falta en antifase", vector((0.60, 0), (0.15, math.pi), (perdido, math.pi))),
        ("falta en fase", vector((0.60, 0), (0.15, math.pi), (perdido, 0))),
    ]
    assert math.isclose(abs(observado) / (1 - perdido), 0.6, abs_tol=1e-12)
    assert math.isclose(inferior, 0.2, abs_tol=1e-12)
    assert math.isclose(superior, 0.7, abs_tol=1e-12)
    assert math.isclose(abs(testigos[0][1]), inferior, abs_tol=1e-12)
    assert math.isclose(abs(testigos[1][1]), superior, abs_tol=1e-12)
    print(f"cobertura={1-perdido:.2f} R_valid_only={abs(observado)/(1-perdido):.2f} ")
    print(f"R_total_posible=[{inferior:.2f}, {superior:.2f}]")
    for nombre, resultado in testigos:
        print(f"{nombre}: R_total={abs(resultado):.2f}")

    # Incluso un R_valid_only perfecto con 75 % observado no fija R_total.
    perfecto = vector((0.75, 0))
    assert cotas_r(perfecto, 0.25) == (0.5, 1.0)
    print("R_valid_only=1.00 con cobertura=0.75 permite R_total=[0.50, 1.00]")


if __name__ == "__main__":
    main()
