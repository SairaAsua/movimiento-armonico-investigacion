# Presupuesto geométrico de error para situación del recorrido

Derivación **del equipo de Harmonic Beacon** para las medidas candidatas de [situación](LABAN_SITUACION_RECORRIDO.md), no fórmula atribuida a Laban ni precisión medida de las cámaras. El [banco reproducible](situacion_error_sintetico.py) comprueba casos construidos; la [issue #4](https://github.com/SairaAsua/movimiento-armonico-investigacion/issues/4) conserva la validación pendiente.

## Condiciones necesarias

Sean `q_i=p_i−o_i` los puntos relativos verdaderos de una **misma definición de origen** y `q̂_i` los estimados en el mismo marco 3D y en los mismos tiempos. Supongamos una **cota dura simultánea** `‖q̂_i−q_i‖≤δ` para todos los `n+1` puntos de la frase. Si posición y origen elegido tienen respectivamente cotas duras `ε_p` y `ε_o`, basta tomar `δ=ε_p+ε_o`; la desigualdad triangular no exige que sus errores sean independientes. La incertidumbre del marco ya debe estar incluida al expresar ambos recorridos en coordenadas comunes. No valen para esta derivación cambios de identidad, oclusiones rellenadas, muestras ausentes, relojes sin correspondencia, un cambio deliberado de cintura a otro origen ni una escala elegida de la propia frase.

Sean `R` el alcance verdadero fijado para esa tarea y `R̂` su estimación, con `|R−R̂|≤ε_R<R̂`. Esta última también es **cota dura**, no desviación estándar. Denotemos por `m` y `M` las distancias mínima y máxima no normalizadas de la polilínea al origen. Como cada segmento verdadero y estimado está a distancia como máximo `δ` punto a punto bajo la misma interpolación, sus mínimos difieren a lo sumo `δ`; lo mismo ocurre con los máximos. Por tanto, para `d̂∈{m̂,M̂}`:

```text
max(0, d̂−δ)/(R̂+ε_R) ≤ d/R ≤ (d̂+δ)/(R̂−ε_R).
```

Con `ε_R=0`, esto recupera `|rho_min verdadero−rho_min observado|≤δ/R` y da la misma forma para `rho_max`. Si `R̂≤ε_R`, no hay denominador inferior positivo y **no se emite un intervalo finito**. Dos intervalos de condiciones cuya diferencia sea menor que su incertidumbre conjunta no autorizan afirmar que una situación es más central. Un error de definición del origen se explora por sensibilidad, no se esconde en `ε_o`.

## Por qué `V_r` exige mucho más

Para cada segmento, sea `N_i=r_i+r_{i+1}−2m_i` su variación radial; `N=ΣN_i`, `L=Σ‖q_{i+1}−q_i‖` y `V_r=N/L`. Cada radio extremo y cada mínimo de segmento cambian como máximo `δ`, así que `|N̂−N|≤4nδ`. Cada longitud de segmento cambia como máximo `2δ`, de donde `|L̂−L|≤2nδ`. Como la distancia al origen es 1-Lipschitz sobre cada segmento, `0≤N≤L` y `0≤N̂≤L̂`. Para `L,L̂>0`, dos formas simétricas de la desigualdad triangular dan:

```text
|V̂_r−V_r| ≤ min(1, 6nδ/max(L,L̂)).
```

Es una **cota conservadora**, no un intervalo de confianza. Se vuelve trivial (`1`) si hay muchos segmentos cortos frente a `δ`: subir FPS no garantiza una medida más precisa de variación radial si el error posicional no baja. Tampoco cubre el cambio de polilínea causado por descartar cuadros; esa sensibilidad se estudia [por separado en CMU](CMU_DANZA_BANCO_REAL.md). El [script sintético](situacion_error_sintetico.py) probó 1000 parejas aleatorias con perturbaciones acotadas y dos círculos poligonales. Con error máximo construido `δ=0,01` y `R̂=1,02±0,02`, el círculo de 32 segmentos tuvo `|ΔV_r|=0,004355` y cota `0,305979`; el de 128 tuvo `|ΔV_r|=0,065722` y cota trivial `1`. Son **números de un generador**, no rendimiento de Reolink, «logicam», Moto G, HarMoCAP o Nico.

El [cálculo sobre CMU 05_02](CMU_SITUACION_PRECISION_VR.md) aplica esta desigualdad a nueve ventanas reales de danza y grillas decimadas. Muestra cuán exigente puede resultar la **garantía peor caso**; no convierte ese umbral suficiente en especificación de compra, ni estima error de cámara.

Una [perturbación temporal controlada del mismo C3D](CMU_SITUACION_ERROR_TEMPORAL.md) compara desplazamiento constante, deriva suave y jitter con **igual norma de error por punto**. La respuesta de `V_r` cambia mucho: el piloto deberá caracterizar la estructura temporal del error, además de su magnitud.

## Qué medir antes de usar la cota

El banco instrumental debe producir error por punto y por origen contra referencia dinámica independiente, con dominio de vista, volumen, giro, rapidez, oclusión y día. Una distribución de errores o un percentil no se puede sustituir por una cota dura sin cambiar el tipo de afirmación. Hay que estimar además error de escala y del marco, y registrar qué frases quedan inválidas; evaluar sólo frases detectadas puede ocultar sesgo de cobertura. Fijar después, en desarrollo y antes de sesiones reservadas, qué diferencia geométrica mínima necesita distinguir el contraste HIT o la capa sonora. Si las cotas cubren esa diferencia, el resultado se reporta como no identificable con ese montaje.

El [sobre experimental](CONTRATO_SITUACION_V0.md) conserva por ahora `uncertainty.status=not_estimated`. Una versión `bounded` requerirá perfil de validación, intervalo derivado por frase y evidencia privada auditable; no basta calcular las fórmulas sobre una supuesta confianza de pose. No se deduce de estas cotas belleza, eficiencia, placer o estado de conciencia.
