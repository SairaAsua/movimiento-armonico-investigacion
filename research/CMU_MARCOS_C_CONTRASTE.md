# La elección de marco puede invertir el contraste de rapidez

Fecha: 24 de septiembre de 2026. Se reutiliza exactamente la [toma humana externa CMU 05_02](CMU_DANZA_BANCO_REAL.md) y el [script con hash fijado](cmu_danza_05_02_audit.py). Es un banco de ingeniería, no una observación de Nico ni prueba de estética, eficiencia, HIT o una regla histórica de Laban.

## Tres recorridos, una sola clasificación espacial

Para mantener comparable la pregunta «¿delante o detrás del torso?», todos los cálculos clasifican el tramo por el **punto medio de sus dos posiciones en el marco corporal**: signo de la coordenada anterior. La escala `L` es la mediana del ancho de hombros sobre la toma completa (302,1 mm), igual que en la auditoría original. Sólo cambia qué longitud de tramo determina la rapidez:

- **Co-rotante**: `b_t = R_tᵀ(w_t−p_t)/L`; `ds = ||b_t−b_{t−1}||`. `w` es el proxy de muñeca, `p` el centro de cintura y `R` los ejes del torso. Describe cambio de posición de la mano respecto del marco que gira con el torso.
- **Cintura centrada sin corregir giro**: `ds = ||(w_t−p_t)−(w_{t−1}−p_{t−1})||/L`. Quita el traslado de la cintura, pero **conserva** el recorrido debido al giro global del brazo/torso en la sala. Su norma no depende de reexpresar el vector resultante en ejes corporales.
- **Sala**: `ds = ||w_t−w_{t−1}||/L`. Conserva traslado y giro globales además del cambio relativo.

En cada caso `v=ds·120 Hz` y se calcula la misma media de rapidez ponderada por longitud de arco para los tramos delanteros y traseros. Por eso las tres cifras son contrastes de recorridos **distintos**, no tres estimadores intercambiables de una verdad única. La diferencia co-rotante menos cintura centrada incluye giro real y posible error de estimación del marco que cambia entre cuadros.

| Mano | `C` co-rotante | `C` cintura centrada, sin corregir giro | `C` sala | Mediana / p90 de `|v_co−v_cintura|` por tramo |
|---|---:|---:|---:|---:|
| Izquierda | +2,251 L/s | −0,358 L/s | −0,441 L/s | 0,239 / 3,620 L/s |
| Derecha | +2,775 L/s | −0,035 L/s | +0,013 L/s | 0,242 / 2,704 L/s |

El signo izquierdo se invierte al quitar sólo el traslado; el derecho pasa de un contraste positivo marcado a casi cero. La diferencia de rapidez no es uniforme: la mediana entre marcos es pequeña frente al percentil 90, de modo que unos tramos de giro/marco podrían pesar mucho. Este agregado de 9,35 s mezcla figuras y pirueta; no dice en qué frase surge la divergencia ni cuál marco predice una respuesta independiente.

## Decisión metodológica

El primer estudio con Nico debe conservar **ambos** recorridos (co-rotante y cintura centrada) junto al de sala y separar frases, patrones y giros. No se seleccionará el marco por el signo de `C` ni por el mejor ajuste retrospectivo a belleza o consumo. La pregunta primaria «acento de mano respecto al torso» puede justificar el co-rotante, pero la reconstrucción de `R_t` tendrá que superar una prueba de estabilidad/error angular, y la misma operación no debe llamarse automáticamente dirección de Laban: su frente convencional puede ser más estable que el torso instantáneo ([matemática y fuentes](LABAN_MATEMATICA.md)). El contraste en sala responde a otra pregunta: dónde cae el acento del gesto observado desde un marco fijo.

El [control Monte Carlo siguiente](CMU_ORIENTACION_RUIDO.md) perturbó **sólo la orientación** del marco, sin alterar el marcador de muñeca, y mostró que jitter cuadro a cuadro importa más que un sesgo angular constante de igual tamaño. No suavizó la orientación observada ni midió su error real. La validez con cámaras propias deberá cotejar `R_t` contra una referencia física y reportar el error de cada recorrido por región, incluida la latencia de cualquier filtro. El [replay causal previo](ACOPLE_CAUSAL_REPLAY.md) usó sólo la versión co-rotante y una escala fijada en el primer segundo; sus porcentajes no se deben transferir a las otras dos definiciones.
