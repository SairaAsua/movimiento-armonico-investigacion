# Información mutua espacio–fase: la medida y el ciclo son parte de la pregunta

Derivación y banco **sintéticos** del 2 de octubre de 2026. El [artículo teórico](../papers/ARTICULO_TEORETICO_METODOLOGICO.md) propone `J_{S,Φ}=I(S;Φ)` para una región espacial `S` y una fase `Φ` de tarea obtenida por una señal independiente. La fórmula de información mutua es correcta **una vez fijada una distribución conjunta**; «distribución ponderada» sola no determina qué observaciones cuentan ni con qué peso. Ningún número de esta nota procede de Nico o de cámaras.

## Dos medidas sobre una misma ejecución

Sean `S(t)` una región predefinida y `Φ(t)` una fase obtenida sin reutilizar la misma etiqueta espacial. Para intervalos válidos `i`, con duración `Δt_i`, arco observado `Δs_i=||x(t_{i+1})−x(t_i)||` y etiquetas en el punto medio, hay al menos dos distribuciones legítimas:

`P_t(k,b) = [Σ_i Δt_i 1{S_i=k,Φ_i=b}]/[Σ_i Δt_i]`,

`P_s(k,b) = [Σ_i Δs_i 1{S_i=k,Φ_i=b}]/[Σ_i Δs_i]`.

`P_t` pregunta **qué fracción del tiempo válido** coincide con cada región y fase; `P_s` pregunta **qué fracción del recorrido válido**. Una pausa visible cuenta en `P_t` y aporta arco cero a `P_s`. Los cuadros duplicados o un FPS variable no deben valer como réplicas nuevas: usar marcas de tiempo y arcos físicos con su incertidumbre, no un conteo bruto de cuadros. Reportar por separado duración, arco, cobertura y exclusiones de cada denominador.

Una región radial puede definirse **en cada tramo** como `S_i=1{||q_i||/R≤a}`, con origen, escala, umbral `a` y regla para cruces de frontera declarados antes del contraste. No sustituir `S_i` por el `rho_min` o la fracción de arco **resumidos para toda la frase**: una etiqueta constante dentro de esa frase da `H(S)=J=0` por definición y no pregunta en qué fase ocurrió la cercanía. El [banco de ocupación radial del PR #28](https://github.com/SairaAsua/movimiento-armonico-investigacion/pull/28) muestra por qué es útil conservar la distribución dentro del recorrido, aunque todavía no valida ninguna región Laban. Los puntos cercanos al umbral con incertidumbre que cruza la frontera requieren estado incierto o análisis de sensibilidad; no se convierten en etiquetas seguras por redondeo.

### El máximo de `J` depende de cuánta curva ocupa cada región

Para regiones binarias, `J=I(S;Φ)≤H(S)=−p ln p−(1−p)ln(1−p)`, donde `p=P(S=1)` bajo la **medida elegida**. En el par sintético del [banco de ocupación radial](https://github.com/SairaAsua/movimiento-armonico-investigacion/pull/28), la fracción de **arco** cerca del centro (`a=0,4`) es `p=0,625` o `p=0,125`. Sus techos matemáticos para `J_s` son respectivamente `0,661563` y `0,376770` nats; con dos tablas diagonales hipotéticas de correspondencia perfecta `S=Φ`, los valores de `J` **alcanzan** esos techos diferentes. Las tablas son un límite algebraico, no fases medidas ni evidencia HIT. Si `Φ` tiene una marginal fijada distinta, el techo alcanzable puede ser incluso menor.

Así, comparar dos números brutos de `J` entre frases con ocupaciones distintas puede confundir **capacidad informativa marginal** con una relación espacio–fase diferente. Archivar `P(S,Φ)`, `P(S)`, `P(Φ)`, `H(S)` y `H(Φ)` por ciclo, además de `J`, y evaluar el valor incremental frente al patrón/cadencia en días reservados. Dividir por `H(S)` tampoco resuelve por sí solo el problema: puede explotar cuando una región es rara y la estimación tiene poco soporte. La fase debe provenir de eventos o señales independientes y pasar los controles de reloj común descritos abajo.

El [banco ejecutable](j_espacio_fase_sintetico.py) usa una vuelta monótona de la misma circunferencia, parametrizada por `q(t)=t+0,8t(1−t)`, `0≤t≤1`. `S=0` para la primera mitad espacial `q<1/2` y `S=1` para la otra; un reloj externo independiente da `Φ=0` si `t<1/2` y `Φ=1` después. `q` alcanza `1/2` en `t≈0,32460947`; por ello la primera mitad de la curva termina antes de la mitad del tiempo. Las tablas exactas (filas `S`, columnas `Φ`) son:

| Medida | `P(0,0)` | `P(0,1)` | `P(1,0)` | `P(1,1)` | `J`, nats |
|---|---:|---:|---:|---:|---:|
| Tiempo `P_t` | 0,32460947 | 0 | 0,17539053 | 0,5 | 0,306330845 |
| Arco `P_s` | 0,5 | 0 | 0,2 | 0,3 | 0,274358469 |

El recorrido, su sentido, la fase externa y sus cortes son **idénticos**; sólo cambia la medida sobre la ejecución. Ambas respuestas son válidas para preguntas diferentes. Ninguna es por sí sola un valor de consonancia ni un test de HIT.

## Control nulo: asociación creada por una vuelta y el reloj común

Incluso con rapidez uniforme `q(t)=t`, las mismas definiciones `S=1{q≥1/2}` y `Φ=1{t≥1/2}` producen `P_t=P_s=[[1/2,0],[0,1/2]]` y `J_t=J_s=ln 2` nats: la **asociación binaria máxima**. No se introdujo una relación extraordinaria entre dos sistemas; ambas etiquetas son funciones de la progresión monótona de una sola vuelta. En el ejemplo no uniforme anterior `J_t` baja a `0,3063` aunque la curva y el sentido siguen iguales. Por tanto, leer `J` alto como «más consonancia» premiaría una regularidad de tarea construida por el reloj y los cortes. Que la fase provenga de una señal medida por separado evita copiar literalmente `S`, pero **no** elimina un impulsor común como el avance del ciclo, música o consigna.

El control del estudio debe fijar antes de ver los resultados un modelo de la **progresión esperada de la tarea** (patrón, sentido, cadencia y fase/eventos disponibles) y preguntar si la asociación espacio–fase predice algo externo *más allá* de esa base en días reservados. Un surrogate puede desplazar una fase medida respecto de la trayectoria **sólo si** conserva el soporte, la estructura dentro del ciclo y el significado del evento; desplazar etiquetas por cuadros arbitrarios puede crear un nulo mecánicamente imposible. Si `S` es una función casi determinista de la propia fase de tarea, el estimando `J` describe el ciclo pero no ofrece un contraste independiente de HIT. Esta comprobación se añade a los controles de [proveniencia circular](FASE_PROCEDENCIA_CIRCULAR.md) y [ritmo común](CONTROLES_RITMO_COMUN.md); no se resuelve eligiendo después el binning que reduzca el problema.

### Control exacto con progreso de tarea separado

El [mismo banco sintético](j_espacio_fase_sintetico.py) incluye ahora tres etiquetas binarias deliberadamente abstractas: progreso de tarea `T`, región `S` y fase de **otra señal** `Φ`. Si ambas observaciones siguen `T` con errores Bernoulli independientes de probabilidad `1/4`, la asociación **bruta** `I(S;Φ)=0,031584` nats es positiva, pero la asociación **condicionada** `I(S;Φ|T)=0`: conocer `Φ` no añade información sobre `S` después de conocer `T`. En una alternativa con un residuo compartido `E`, `S=T⊕E` y `Φ=T⊕E`, la asociación condicionada pasa a `H(E)=0,562335` nats. Las marginales de `S`, `Φ` y `T` son equilibradas en ambos casos. Esta construcción comprueba una distinción de análisis; el residuo común también podría proceder de un tercer factor no medido, de modo que **ni `I(S;Φ|T)>0` demuestra acoplamiento causal**.

En video real, `T` tendría que ser una referencia de progreso/cadencia de tarea definida y medida **sin copiar `Φ` ni `S`**; si se condiciona en `T=Φ`, la información condicional es cero por identidad y el control carece de sentido. Con pocos ciclos y bins, un estimador de información condicional puede tener sesgo considerable; no se adoptará una prueba numérica por ver estos números exactos. La decisión confirmatoria sigue siendo predefinir señales y tarea, contrastar modelos predictivos sobre las mismas unidades/días reservados y reportar cobertura y controles de ritmo común. El ejemplo justifica preguntar si hay **aporte adicional**, no imponer `I(S;Φ|T)` como la métrica principal del piloto.

## Mezclar ciclos puede borrar una relación presente en cada uno

Con dos regiones y dos bins de fase, imaginemos dos ciclos de igual peso. El primero tiene tabla `[[0.5,0],[0,0.5]]`: región y fase coinciden. El segundo tiene `[[0,0.5],[0.5,0]]`: la relación se invierte. En **cada ciclo** `J=ln 2≈0,693147181` nats, pero al mezclar las dos tablas antes del cálculo se obtiene `[[0.25,0.25],[0.25,0.25]]` y `J_pool=0`. Además, `J` no distingue por sí solo coincidencia de inversión: las dos tablas individuales tienen el mismo valor. Es un hecho de las distribuciones construidas, no evidencia de que Nico alterne esas relaciones.

Por ello conservar `P_ciclo(k,b)`, duración, arco, etiquetas, fase circular original y orden de los ciclos. Si la pregunta es **consistencia entre ciclos**, resumir valores y patrones por ciclo con igual peso por ciclo o una regla predeclarada; no reemplazarlos por un único `J` agrupado. Si la pregunta es asociación en el tiempo total del bloque, el agrupamiento es otro estimando y debe nombrarse. Una fase inferida del mismo cruce espacial que define `S` crea asociación por construcción; requerimos eventos o señales independientes y un control que rompa la relación preservando los marginales pertinentes.

## Decisión para el piloto y el paper

`J` permanece **exploratorio** hasta fijar en desarrollo: región, marco, origen independiente de fase, bins, medida `t` o `s`, unidad ciclo/frase/bloque, pausa, cobertura mínima y regla para ciclos inválidos. Para un contraste HIT de fase temporal, `J_t` con resultados por ciclo es el candidato inicial; `J_s` responde a la pregunta complementaria de asociación a lo largo del camino. La selección se hace antes de abrir días reservados y sin mirar juicios de belleza o costo. Si no hay fase identificable o la cámara no recupera con fiabilidad los tramos y el frente, `J` es `no_identificable`, no cero.

La [separación geometría–tiempo](GEOMETRIA_VS_TIEMPO_TRAYECTORIA.md) ya demostró que promediar por cuadros puede mezclar velocidad y forma. Esta nota extiende esa cautela al descriptor conjunto; el [contraste regional de rapidez](ACOPLE_ESPACIO_TIEMPO.md) es otro estimando y no debe renombrarse `J`. Para un futuro Beacon, cualquier sonificación de la asociación necesitaría declarar la medida, la ventana causal, la fase disponible, la calidad y la latencia; estas tablas retrospectivas no prueban aún que eso pueda hacerse en vivo.

Reproducir: `python research/j_espacio_fase_sintetico.py` desde la raíz del repositorio.
