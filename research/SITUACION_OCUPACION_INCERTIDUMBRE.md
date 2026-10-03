# Cuándo es defendible una ocupación radial

**Derivación y banco sintéticos, sin video ni validación de Nico.** La [ocupación por arco](SITUACION_OCUPACION_ARCO.md) `F_arc(a)` distingue dos recorridos que comparten `Q`, extremos y `V_r`. Pero el número obtenido al fijar un umbral `a` es frágil si muchos segmentos están cerca de la esfera de radio `aR`. Una fracción grande no es automáticamente una categoría central de Laban ni una señal apta para Beacon.

## Banda geométrica conservadora

Sean dos polilíneas 3D `P=(p₀,…,pₙ)` y `P'=(p'₀,…,p'ₙ)` con **correspondencia de vértices**, mismo origen, marco, escala `R>0` y regla de segmentación. Supongamos una cota simultánea `||pᵢ−p'ᵢ||≤δ` para todos los vértices. Si el origen también tiene error acotado, sumarlo a `δ` por desigualdad triangular; un cambio conceptual de origen o de marco **no** es ese error. Sobre los segmentos lineales correspondientes, la posición a igual parámetro difiere como máximo `δ`, porque es una combinación convexa de los errores en los extremos.

Escribamos `L=Σℓᵢ` para el largo de `P`, `N(a)=L·F_arc(a)` para el largo dentro de la esfera y `D=Σ|ℓ'ᵢ−ℓᵢ|`. Si sólo se conocen cotas de error por vértice, `D≤2nδ`; una referencia dinámica puede dar una cota menor. Para `L>D`, la ocupación de `P'` está dentro de:

```text
inferior = max(0, [N(max(0,a−δ/R))−D] / [L+D])
superior = min(1, [N(a+δ/R)+D] / [L−D]).
```

Si `a−δ/R<0`, tomar `N=0`: no hay esfera de radio negativo. Si `L≤D`, la cota sólo permite `[0,1]`. **Prueba:** en cada segmento, todo punto perturbado que cae dentro de `aR` proviene de uno que cae dentro de `(aR+δ)`; todo punto original dentro de `(aR−δ)` sigue dentro de `aR`. Integrar esas inclusiones sobre el parámetro de cada segmento y acotar la diferencia de pesos de longitud por `D` da `N(a−δ/R)−D ≤ N'(a) ≤ N(a+δ/R)+D`. El largo nuevo satisface `L−D≤L'≤L+D`; dividir da el intervalo.

Es una **cota condicional**, no una incertidumbre ya medida. Requiere una cota física simultánea para todos los puntos y el origen, el mismo número/correspondencia de segmentos y una escala fijada independientemente de la frase. No incluye excursiones entre cuadros, cambios de identidad, error de sincronía, oclusiones, efecto del filtro ni sesgo de selección de frases válidas. El [presupuesto de situación](PRESUPUESTO_ERROR_SITUACION.md) y la [ambigüedad entre cuadros](MUESTREO_SITUACION_ENTRE_CUADROS.md) siguen siendo necesarios.

## Contraejemplo cercano al umbral

El [script reproducible](situacion_ocupacion_incertidumbre_sintetica.py) aproxima el mismo círculo con 720 segmentos, una vez a radio `0,99R` y otra a `1,01R`. Cada vértice cambia sólo `0,02R`; la primera polilínea está por completo dentro de la esfera `a=1` y la segunda por completo fuera. Por ello `F_arc(1)` cambia de `1` a `0`, aunque forma angular, orden, cantidad de muestras y desplazamiento relativo apenas cambian. Al elegir radios `1±ε` y aumentar la densidad de muestreo puede hacerse `ε` arbitrariamente pequeño: **sin un margen radial, un umbral único carece de estabilidad uniforme**. El ejemplo es geométrico, no una estimación de error de las cámaras disponibles.

La cota básica `D≤2nδ` suele ser enorme al densificar una polilínea, aunque la curva visual parezca casi igual. Esto muestra por qué más FPS y una confianza de pose no bastan para certificar ocupación; harían falta error correlacionado/temporal medido, un límite de longitud o una referencia dinámica. Una banda estrecha en el cálculo sintético no sustituiría esa evidencia.

Como control de la fórmula, el mismo script desplaza una línea de `x=0,1…0,9` a `x=0,11…0,91`, con `δ=0,01`, `D≤0,02` y umbral `a=0,5`. La ocupación desplazada es `0,4875` y cae dentro de la banda calculada `[0,4512; 0,5513]`. En cambio, para los 720 segmentos circulares `2nδ=28,8R` supera el largo `6,22R` y la cota básica queda `[0,1]`: el ejemplo enseña tanto un caso informativo como uno donde el error disponible no alcanza.

## Decisión para el piloto y HIT

Conservar la **curva radial de ocupación** o unos pocos cuantiles/rangos elegidos antes de las sesiones reservadas, junto con la masa de arco que cae en la banda de incertidumbre alrededor de cada umbral. Reportar proporción de frases computables, error de posición/origen, marco, FPS efectivo y robustez frente a umbrales vecinos; si la banda permite tanto `0` como `1`, el descriptor queda no identificable para esa comparación. La ocupación por **tiempo** responde otra pregunta y necesita PTS/pausas válidos; no sustituir `F_arc` por promedio de cuadros. Para un contraste con HIT, usar la misma frase y reloj, controlar ritmo, y conservar separados ocupación espacial, permanencia temporal y fase de tarea. No usar un umbral ajustado tras ver juicios estéticos o escuchar una sonificación.
