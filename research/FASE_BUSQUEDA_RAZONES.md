# Buscar la mejor razón `p:q` también encuentra azar

**Control analítico y sintético, sin personas ni video.** Pertenece a la [Issue #7](https://github.com/SairaAsua/movimiento-armonico-investigacion/issues/7). La [especificación de fase](FASE_ROPEFLOW.md) pide fijar la relación desde la tarea antes de evaluar HIT; aquí cuantificamos el costo de no hacerlo. En este proyecto `Rₚ:q=|K⁻¹Σₖ exp(i[qφ_A,k−pφ_B,k])|` es una **concentración circular**, no un índice de belleza, metabolismo o conciencia. La fuente de HIT propone razones armónicas como hipótesis, pero no autoriza elegir el mayor `R` de un catálogo después de ver los mismos datos.

## Dos decisiones estadísticas diferentes

1. **Pregunta confirmatoria:** el patrón de tarea y los eventos observables justifican, por ejemplo, `1:1` entre señales independientes. Se congelan señales, origen/signo de fase, `p:q`, ventana, estado inválido, unidad de resumen, resultado externo y regla de incertidumbre **antes** de las sesiones reservadas.
2. **Búsqueda exploratoria:** se prueban varias razones. Si se informa `max_{p,q} Rₚ:q`, el estadístico es ese **máximo**, no el `R` de la razón ganadora tomado como si hubiese sido la única candidata. El catálogo, los filtros, la selección de ventana y cualquier búsqueda de señal/par se registran. Una nueva sesión reservada puede evaluar una razón descubierta, pero no convierte en confirmatorio el mismo material que la eligió. Usamos pares coprimos para nombrar razones fundamentales; `2:2` y `1:1` comparten razón de frecuencias, pero **sus concentraciones no son iguales**: la primera calcula el segundo armónico del desfase y sería otra prueba si se incluyera.

Para un nulo ideal de `K` pares de fases **independientes y uniformes entre ciclos**, `E[Rₚ:q²]=1/K` para cada razón fija: al expandir el cuadrado, los términos diagonales aportan `K`, y los cruzados tienen media cero. Esto no hace a las once razones independientes entre sí ni justifica contar cuadros como `K`; la [identidad de Vinck y el contraejemplo de cuadros copiados](FASE_SESGO_MUESTRAL.md) explican por qué la unidad importa. El máximo de muchas razones no conserva la distribución de una razón preespecificada.

## Banco reproducible

El [script](fase_busqueda_razones_sintetica.py) usa `p,q∈{1,2,3,4}` coprimos: **11** razones, incluidos `1:1`, `1:2` y `2:1`. En 10 000 réplicas por condición, semilla `20261003`, sortea cada fase de A y B independientemente para cada ciclo. Calcula el `R` de `1:1` prefijado y el máximo de las once razones **sobre los mismos datos**.

| Ciclos independientes construidos | Media `R₁:₁` | Media `max R` | Percentil 95 de `R₁:₁` | Percentil 95 de `max R` | Fracción de máximos que supera el percentil 95 de `R₁:₁` |
|---:|---:|---:|---:|---:|---:|
| 8 | 0,3153 | 0,5899 | 0,5964 | 0,7734 | 0,4486 |
| 32 | 0,1570 | 0,3001 | 0,3067 | 0,4036 | 0,4251 |

La simulación también obtuvo `E[R₁:₁²]=0,12416` con `K=8` y `0,03147` con `K=32`, cerca de `1/K=0,125` y `0,03125`; es un chequeo interno del nulo ideal. Los números del máximo dependen del catálogo de once razones, de `K` y de la semilla; **no son umbrales para Nico** ni estimaciones de falsos positivos de sus cámaras. Incluso en este nulo favorable, reutilizar el umbral de una sola razón para el máximo de once lo superó en alrededor del 43–45 % de las réplicas.

## Regla para el estudio y Beacon

El contraste principal de HIT debe fijar una relación por patrón que tenga una interpretación de eventos verificable. `1:1` no es una preferencia estética; puede ser simplemente la periodicidad impuesta por una figura. Si una búsqueda de razones es necesaria, calibrar **todo el procedimiento de selección**, incluida la elección de ventanas y pares, con desarrollo y sesiones posteriores separadas. Un nulo empírico tendrá que preservar la estructura de cada señal, cadencia, música, soga y entradas comunes pertinentes: las fases uniformes independientes de este banco no representan ese mundo. Desplazar circularmente una serie periódica puede conservar una relación espuria y no es por sí solo un control suficiente ([control de ritmo común](CONTROLES_RITMO_COMUN.md)).

Reportar valor y ángulo de la razón fijada, cobertura, número de ciclos válidos, dependencia por día y el catálogo explorado. No dar once oportunidades de activar una capa musical y después llamar «señal armónica» al control ganador: para Beacon se llevaría sólo un descriptor con procedencia y validez establecidas, con elección de mapeo auditivo evaluada aparte. Una `R` alta bajo selección no demuestra la cadena de conjeturas HIT de recurrencia útil, menor carga correctiva y experiencia; cada escalón necesita un resultado externo independiente ([predicciones escalonadas](HIT_PREDICCIONES_ESCALONADAS.md)).
