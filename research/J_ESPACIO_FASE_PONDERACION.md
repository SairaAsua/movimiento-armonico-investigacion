# Información mutua espacio–fase: la medida y el ciclo son parte de la pregunta

Derivación y banco **sintéticos** del 2 de octubre de 2026. El [artículo teórico](../papers/ARTICULO_TEORETICO_METODOLOGICO.md) propone `J_{S,Φ}=I(S;Φ)` para una región espacial `S` y una fase `Φ` de tarea obtenida por una señal independiente. La fórmula de información mutua es correcta **una vez fijada una distribución conjunta**; «distribución ponderada» sola no determina qué observaciones cuentan ni con qué peso. Ningún número de esta nota procede de Nico o de cámaras.

## Dos medidas sobre una misma ejecución

Sean `S(t)` una región predefinida y `Φ(t)` una fase obtenida sin reutilizar la misma etiqueta espacial. Para intervalos válidos `i`, con duración `Δt_i`, arco observado `Δs_i=||x(t_{i+1})−x(t_i)||` y etiquetas en el punto medio, hay al menos dos distribuciones legítimas:

`P_t(k,b) = [Σ_i Δt_i 1{S_i=k,Φ_i=b}]/[Σ_i Δt_i]`,

`P_s(k,b) = [Σ_i Δs_i 1{S_i=k,Φ_i=b}]/[Σ_i Δs_i]`.

`P_t` pregunta **qué fracción del tiempo válido** coincide con cada región y fase; `P_s` pregunta **qué fracción del recorrido válido**. Una pausa visible cuenta en `P_t` y aporta arco cero a `P_s`. Los cuadros duplicados o un FPS variable no deben valer como réplicas nuevas: usar marcas de tiempo y arcos físicos con su incertidumbre, no un conteo bruto de cuadros. Reportar por separado duración, arco, cobertura y exclusiones de cada denominador.

El [banco ejecutable](j_espacio_fase_sintetico.py) usa una vuelta monótona de la misma circunferencia, parametrizada por `q(t)=t+0,8t(1−t)`, `0≤t≤1`. `S=0` para la primera mitad espacial `q<1/2` y `S=1` para la otra; un reloj externo independiente da `Φ=0` si `t<1/2` y `Φ=1` después. `q` alcanza `1/2` en `t≈0,32460947`; por ello la primera mitad de la curva termina antes de la mitad del tiempo. Las tablas exactas (filas `S`, columnas `Φ`) son:

| Medida | `P(0,0)` | `P(0,1)` | `P(1,0)` | `P(1,1)` | `J`, nats |
|---|---:|---:|---:|---:|---:|
| Tiempo `P_t` | 0,32460947 | 0 | 0,17539053 | 0,5 | 0,306330845 |
| Arco `P_s` | 0,5 | 0 | 0,2 | 0,3 | 0,274358469 |

El recorrido, su sentido, la fase externa y sus cortes son **idénticos**; sólo cambia la medida sobre la ejecución. Ambas respuestas son válidas para preguntas diferentes. Ninguna es por sí sola un valor de consonancia ni un test de HIT.

## Mezclar ciclos puede borrar una relación presente en cada uno

Con dos regiones y dos bins de fase, imaginemos dos ciclos de igual peso. El primero tiene tabla `[[0.5,0],[0,0.5]]`: región y fase coinciden. El segundo tiene `[[0,0.5],[0.5,0]]`: la relación se invierte. En **cada ciclo** `J=ln 2≈0,693147181` nats, pero al mezclar las dos tablas antes del cálculo se obtiene `[[0.25,0.25],[0.25,0.25]]` y `J_pool=0`. Además, `J` no distingue por sí solo coincidencia de inversión: las dos tablas individuales tienen el mismo valor. Es un hecho de las distribuciones construidas, no evidencia de que Nico alterne esas relaciones.

Por ello conservar `P_ciclo(k,b)`, duración, arco, etiquetas, fase circular original y orden de los ciclos. Si la pregunta es **consistencia entre ciclos**, resumir valores y patrones por ciclo con igual peso por ciclo o una regla predeclarada; no reemplazarlos por un único `J` agrupado. Si la pregunta es asociación en el tiempo total del bloque, el agrupamiento es otro estimando y debe nombrarse. Una fase inferida del mismo cruce espacial que define `S` crea asociación por construcción; requerimos eventos o señales independientes y un control que rompa la relación preservando los marginales pertinentes.

## Decisión para el piloto y el paper

`J` permanece **exploratorio** hasta fijar en desarrollo: región, marco, origen independiente de fase, bins, medida `t` o `s`, unidad ciclo/frase/bloque, pausa, cobertura mínima y regla para ciclos inválidos. Para un contraste HIT de fase temporal, `J_t` con resultados por ciclo es el candidato inicial; `J_s` responde a la pregunta complementaria de asociación a lo largo del camino. La selección se hace antes de abrir días reservados y sin mirar juicios de belleza o costo. Si no hay fase identificable o la cámara no recupera con fiabilidad los tramos y el frente, `J` es `no_identificable`, no cero.

La [separación geometría–tiempo](GEOMETRIA_VS_TIEMPO_TRAYECTORIA.md) ya demostró que promediar por cuadros puede mezclar velocidad y forma. Esta nota extiende esa cautela al descriptor conjunto; el [contraste regional de rapidez](ACOPLE_ESPACIO_TIEMPO.md) es otro estimando y no debe renombrarse `J`. Para un futuro Beacon, cualquier sonificación de la asociación necesitaría declarar la medida, la ventana causal, la fase disponible, la calidad y la latencia; estas tablas retrospectivas no prueban aún que eso pueda hacerse en vivo.

Reproducir: `python research/j_espacio_fase_sintetico.py` desde la raíz del repositorio.
