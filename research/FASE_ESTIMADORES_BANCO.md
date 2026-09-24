# Qué fase se recupera de una señal: Hilbert y posición–velocidad

Fecha: 24 de septiembre de 2026. El [protocolo de fase](FASE_ROPEFLOW.md) pedía comparar estimadores antes de usar relaciones HIT o una fase sonora. Este [banco ejecutable](fase_estimadores_sinteticos.py) usa **sólo NumPy y señales construidas**, con fase fundamental conocida; no hay datos de Nico ni prueba de la soga. Complementa el [banco de ciclos y relaciones p:q](FASE_BANCO_SINTETICO.md), que empezaba con fases exactas en vez de estimarlas.

## Dos estimadores que no comparten disponibilidad

Serie a 120 Hz durante 20 s. La señal básica es `x(t)=cos(θ(t))`; en un caso `θ=2πt`, en otro la cadencia sube linealmente de 0,8 a 1,4 Hz. **Hilbert offline** obtiene la señal analítica mediante FFT de los 20 s completos; donde falta una muestra, interpola usando ambos lados, pero el hueco se marca inválido. La fase de **posición–velocidad causal** es `atan2(−v/2π,x)` con `v=(x_t−x_{t−1})·120`, sin cuadros futuros; usa una frecuencia nominal fija de 1 Hz. Es una implementación deliberadamente simple, no el mejor estimador posible. Ambos tienen gate de amplitud/radio `≥0,25`. Un desfase constante se calibra con la fase conocida de 2–4 s —análogo a eventos de referencia independientes— y se evalúa sólo en 4–18 s. El gate y la calibración son decisiones ilustrativas, no umbrales para rope flow.

| Caso | Hilbert: cobertura; error absoluto med/p90 | Posición–velocidad: cobertura; error absoluto med/p90 | Lectura |
|---|---:|---:|---|
| Coseno limpio 1 Hz | 100 %; 0,00/0,00° | 100 %; 0,53/0,74° | Control positivo ideal. |
| Cadencia 0,8→1,4 Hz | 100 %; 0,01/0,04° | 100 %; 1,82/5,86° | La frecuencia fija de `PV` deforma la fase al acelerar. |
| Segundo armónico de amplitud 0,35 | 100 %; 14,28/20,18° | 100 %; 18,51/42,24° | La fase fundamental construida no se recupera sin sesgo de una forma de onda asimétrica. |
| Ruido gaussiano `σ=0,03`, sin caída | 100 %; 1,20/2,83° | 98,1 %; 16,57/58,32° | Derivar por cuadro amplifica ruido. |
| Mismo ruido, amplitud 0,1 entre 9–10 s | 94,0 %; 1,25/3,08° | 96,3 %; 17,67/67,22° | El gate de `PV` acepta 74,2 % del segundo débil; el de Hilbert, 15,8 %. Los errores resumidos excluyen cuadros inválidos. |
| Hueco de observación 9–9,5 s | 96,4 %; 0,03/0,15° | 96,4 %; 0,52/0,74° | Ambos excluyen el hueco. La cifra global diluye la distorsión local vecina. |

En el caso de hueco, aunque se excluyen los 0,5 s ausentes, la fase Hilbert en los **cuadros observados** de 8,5–10,5 s tiene error p90 **2,08°** y máximo **7,59°**; la fase causal por diferencia hacia atrás tiene p90 **0,74°** allí y descarta el primer tramo tras la reaparición. Este ejemplo es una señal ideal muy simple: no autoriza afirmar que la segunda será mejor con video ruidoso; la fila de ruido muestra justamente lo contrario.

La caída de amplitud ilustra por qué también hay que informar **error local entre los cuadros que pasan el gate**: en 8,5–10,5 s, el p90 es **50,10°** para Hilbert y **123,29°** para posición–velocidad, aunque el p90 global de los cuadros válidos es 3,08° y 67,22° respectivamente. En el segundo débil, Hilbert declara inválido 84,2 % de los cuadros; posición–velocidad sólo 25,8 %, porque la derivada del ruido puede inflar su radio. El gate numérico `0,25` no demuestra identificabilidad de fase cuando la señal baja de amplitud.

## Prueba directa de fuga del futuro

Dos series son idénticas hasta `t=12 s`; sólo en una se reduce la amplitud entre `12–13 s`. La FFT de los 20 s cambia la fase Hilbert que asigna a **11–12 s**: diferencia absoluta mediana **0,76°**, p95 **15,63°** y máxima **48,17°**. La fase posición–velocidad de 11–12 s permanece exactamente igual en ambos archivos. El script lo verifica. Por tanto Hilbert global puede ser un descriptor retrospectivo con etiqueta `available_at` posterior al bloque; **no** se puede reproducir hacia atrás como si Beacon lo hubiera conocido a las 11 s. Si se desea una fase analítica live, hace falta otro filtro causal, otro error y otra prueba de latencia.

## Decisiones para la investigación

1. La fase de tarea definida por eventos de soga, la fase continua de una mano y la fase de una señal analítica siguen siendo entidades distintas. Una relación HIT requiere fuentes independientes y ventanas simultáneamente válidas; no declarar coordinación porque un estimador entregue ángulos suaves.
2. El repertorio de Nico debe aportar eventos visibles y sentidos, una referencia de fase dentro de ciclo y clips con aceleración, figura asimétrica, pausa, amplitud pequeña y oclusión. En desarrollo se evaluarán error angular **y cobertura**, por patrón. Una fase válida sólo en gestos fáciles no responde a la hipótesis artística completa.
3. El primer comparador live puede ser una fase cinemática causal por patrón con radio y calidad medidos, pero esta versión `PV_backward` no queda aprobada: su derivada cruda falló con ruido leve simulado. Cualquier suavizado exige repetir el análisis de atraso del [banco de filtrado del marco](CMU_FILTRO_MARCO_CAUSAL.md).
4. Para el paper, usar Hilbert sólo con ventanas y disponibilidad retrospectivas declaradas. El contraste base→Laban→HIT debe mantener los mismos episodios válidos por modelo y reservar sesiones completas; este banco no valida la teoría HIT ni cuantifica conciencia, placer o metabolismo.
