# `Q_live` depende de qué recorrido corporal se define

Comparación del 24-09-2026 sobre la [toma CMU 05_02](CMU_DANZA_BANCO_REAL.md), con [script reproducible](cmu_q_marcos_live.py). Es una persona bailando **sin soga**, no Nico ni un ensayo de cámaras/Beacon. Se usan la misma muñeca, cintura, escala fijada con el primer segundo, ejes corporales y ventana de llegada que en el [replay causal de `Q`](CMU_Q_CAUSAL_PLANOS.md). La única decisión que cambia es el significado del desplazamiento:

- `co`: diferencia de posiciones muñeca–cintura expresadas cada una en los ejes corporales de **su** cuadro; incluye el cambio de esos ejes.
- `rel`: cambio físico de muñeca respecto de cintura en sala, expresado en los ejes corporales del **cuadro actual**; excluye el término debido sólo al cambio de ejes.

La identidad exacta `Δco = Δrel + Δmarco` se verifica en cada cuadro ([derivación](MARCO_MOVIL_DESCOMPOSICION_C.md)). Después se calcula el mismo `Q=diag(M)` de cada ventana con gate exploratorio de `0,5 L` de arco y dos tramos. Se comparan `Q` sólo donde **ambas** definiciones pasan el gate; los valores de los tramos no comunes no se imputan.

| Mano | Ventana | `co` válido / 1003 | `rel` válido / 1003 | Ambos válidos | Distancia `||Q_co−Q_rel||₁` mediana / p90 / máximo |
|---|---:|---:|---:|---:|---:|
| Izquierda | 0,5 s | 737 | 719 | 719 | 0,147 / 0,828 / 1,236 |
| Izquierda | 1,0 s | 875 | 865 | 865 | 0,137 / 0,789 / 1,076 |
| Izquierda | 2,0 s | 886 | 881 | 881 | 0,137 / 0,604 / 0,668 |
| Derecha | 0,5 s | 820 | 848 | 820 | 0,121 / 0,688 / 1,110 |
| Derecha | 1,0 s | 938 | 940 | 938 | 0,102 / 0,730 / 0,813 |
| Derecha | 2,0 s | 938 | 940 | 938 | 0,108 / 0,657 / 0,722 |

La distancia L1 entre dos vectores `Q` normalizados puede ir de 0 a 2. En este caso, la diferencia de definición es pequeña en la mediana pero grande en parte de las ventanas: para 1 s, el p90 es **0,789** en la izquierda y **0,730** en la derecha. También cambia qué ventanas superan el umbral de arco. No es error del algoritmo ni evidencia de que un recorrido sea «verdadero»: `co` pregunta por la trayectoria de una posición relativa **en el cuerpo que gira**; `rel` pregunta por desplazamiento muñeca–cintura sin contar el giro de los ejes. El segundo aún usa ejes instantáneos para expresar cada incremento y no constituye trayectoria en un marco fijo único.

Si `Q_live` llega a controlar tres ganancias Beacon con `g_k=0,2+0,4Q_k`, el p90 de la **suma de diferencias absolutas de control** sería 0,316/0,292 para izquierda/derecha a 1 s, antes de toda ruta OSC o audio. Eso sólo dimensiona sensibilidad numérica; no demuestra diferencia audible. Por tanto el contrato científico y el paper deberán declarar `path_definition` junto a `Q`, no sólo `window=1s`, y escoger definición primaria en desarrollo según el constructo Laban concreto y la validación de orientación. Una ambigüedad de marco comparable o mayor que la diferencia espacial que se pretende escuchar impide llamar al sonido «calibrado al movimiento» sin acotar su alcance.

Esta comparación **no** separa giro corporal real de ruido angular del marcador, ni estima error de las cámaras de Saira. El [banco estático/dinámico sin persona](PAQUETE_CAPTURA_NICO_V0.md) debe medir ese componente antes de fijar un gate para Nico. `Q` sigue sin codificar signo, secuencia, fase HIT, fuerza o costo energético.

Ejecutar: `uv run --no-project --with numpy --with ezc3d python docs/beacon-contexto-local/ropeflow-consonancia/cmu_q_marcos_live.py`.
