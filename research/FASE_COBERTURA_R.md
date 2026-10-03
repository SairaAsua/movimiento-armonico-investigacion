# Concentración de fase y tramos ocultos: qué permite afirmar `R`

**Nota matemática con [banco sintético reproducible](fase_cobertura_r_sintetica.py), 3 de octubre de 2026.** Complementa la [validación de fase intracíclo](BANCO_FASE_INTRACICLO_CAMARAS.md) y la [auditoría de procedencia](FASE_PROCEDENCIA_CIRCULAR.md). No hay video humano ni estimación de oclusiones de Nico.

## Magnitud y cota

Fijemos **antes** la población de tiempos de un intervalo de tarea en que la fase relativa tendría sentido y una medida normalizada `P_t` sobre él. Si `V` es el tiempo con dos fases observadas y válidas y `M` es el resto, `P_t(M)=m`, definimos el vector observable sin renormalizar `z=∫_V exp(iΔφ(t)) dP_t(t)`. El estadístico publicado sólo sobre válidos es `R_valid_only=|z|/(1−m)` cuando `m<1`. El estadístico de interés para el intervalo completo sería `R_full=|z+v|`, donde `v=∫_M exp(iΔφ(t)) dP_t(t)` es desconocido y `|v|≤m`.

Por desigualdad triangular, **si** existe fase definida en `M` y se conoce `m` respecto del mismo denominador:

`max(0, |z|−m) ≤ R_full ≤ min(1, |z|+m)`.

Estos extremos son alcanzables si la masa faltante puede repartirse entre fases libremente; para una sola muestra discreta de peso `m` la cota inferior puede ser conservadora, porque el vector faltante tiene módulo exactamente `m`. El intervalo es de **identificación**, no de confianza: no incluye error de fase, incertidumbre del reloj ni dependencia entre ciclos. Si cada fase observada tiene un error angular máximo `ε_j`, puede agrandarse conservadoramente el radio de error en `z` por `B=Σ_{j∈V} w_j·2sin(ε_j/2)`; los extremos pasan a `max(0,|ẑ|−m−B)` y `min(1,|ẑ|+m+B)`. Esa cota requiere errores máximos defendibles, no desviaciones estándar tratadas como máximos.

## Contraejemplo exacto

En una unidad temporal sintética, 60 % del tiempo está visible con `Δφ=0`, 15 % visible con `Δφ=π` y 25 % oculto. La cobertura es 75 % y `R_valid_only=|0,60−0,15|/0,75=0,60`. Si toda la fase oculta es `π`, `R_full=0,20`; si es `0`, `R_full=0,70`. Ambos mundos producen exactamente las mismas observaciones válidas. El [script](fase_cobertura_r_sintetica.py) comprueba esos testigos y también que **`R_valid_only=1` con 75 % de cobertura permite `R_full` entre 0,5 y 1**. No es evidencia de que alguna cámara o persona tenga esa tasa de pérdida.

El ángulo medio de la relación también puede variar. Cuando `|z|>m`, un disco de radio `m` alrededor de `z` limita la desviación angular de la resultante completa a `arcsin(m/|z|)`; si `|z|≤m`, la resultante puede anularse y su ángulo deja de estar definido. Con error observado acotado, reemplazar `m` por `m+B` da una cota conservadora. Un `R` pequeño no representa por sí mismo «desarmonía»: puede reflejar fases diversas, mezcla de patrones, o una relación no identificable.

## Decisión para rope flow, HIT y Beacon

- Archivar **duración intentada**, soporte donde la fase de cada señal es válida, masa faltante por patrón/sector de ciclo/giro y el `R_valid_only` junto al intervalo identificable para `R_full`. Un porcentaje de cuadros válidos no equivale necesariamente a la masa temporal si los PTS son irregulares; un porcentaje de ciclos válidos tampoco equivale a masa temporal.
- Si la soga queda oculta, no rellenar su fase copiando la muñeca: la [procedencia](FASE_PROCEDENCIA_CIRCULAR.md) volvería tautológica la relación. Si la tarea pierde periodicidad en una transición, puede **no existir** fase en ese tramo; entonces no hay `R_full` del mismo constructo y se debe separar el episodio, no aplicar estas cotas como si fuera dato faltante ordinario.
- Para el contraste de modelos `base → +Laban → +HIT`, usar las mismas frases y declarar soporte común. El `R_valid_only` de clips con distinta oclusión no es directamente comparable sin esta auditoría; una cota amplia no debe alimentar una conclusión fuerte de HIT. En Beacon, una fase caducada o no identificada invalida la capa sonora correspondiente: no se representa como fase cero ni como consonancia.

Las cotas son más informativas si el protocolo puede medir cobertura alta **en los segmentos relevantes**, sin seleccionar sólo los momentos fáciles. No sustituyen la validación física de cámaras, la referencia de eventos ni la valoración independiente de belleza, experiencia y costo energético.
