"""Una órbita uniforme vista oblicua tiene fase angular 2D no uniforme."""

from __future__ import annotations

import cmath
import math


def medir(aplanamiento: float, muestras: int = 120_000) -> tuple[float, float, float]:
    if not 0 < aplanamiento <= 1:
        raise ValueError("aplanamiento debe estar en (0, 1]")
    z = 0j
    for j in range(muestras):
        theta = 2 * math.pi * (j + 0.5) / muestras
        # Una órbita circular 3D rotada hacia la cámara proyecta una elipse.
        fase_imagen = math.atan2(aplanamiento * math.sin(theta), math.cos(theta))
        z += cmath.exp(1j * (fase_imagen - theta))
    # d fase_imagen / d theta = c / (cos²(theta)+c² sin²(theta)).
    minimo = aplanamiento
    maximo = 1 / aplanamiento
    return abs(z / muestras), minimo, maximo


def main() -> None:
    for c in (1.0, 0.5, 0.25):
        r, minimo, maximo = medir(c)
        print(f"c={c:.2f} R_2D={r:.6f} ")
        print(f"  rapidez_angular_aparente/real=[{minimo:.2f}, {maximo:.2f}]")
        if c == 1:
            assert math.isclose(r, 1, abs_tol=1e-12)
        if c == 0.25:
            assert math.isclose(r, 0.9027799278, abs_tol=1e-6)
            assert math.isclose(maximo / minimo, 16, abs_tol=1e-12)


if __name__ == "__main__":
    main()
