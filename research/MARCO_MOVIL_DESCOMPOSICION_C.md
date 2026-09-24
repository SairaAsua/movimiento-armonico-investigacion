# Qué añade el marco corporal móvil a `C`

Análisis del 24 de septiembre de 2026 sobre la [toma pública CMU 05_02](CMU_DANZA_BANCO_REAL.md), con [código reproducible](cmu_descomponer_marco_c.py). Es danza sin soga; no representa a Nico, el error de las cámaras de Saira, una categoría histórica de Laban ni una respuesta estética. Complementa la [comparación de tres recorridos](CMU_MARCOS_C_CONTRASTE.md), que empleó una escala de hombros distinta (mediana de toda la toma). Aquí se usa la **escala causal fijada con el primer segundo**, `303,532 mm`, igual que el [replay `C`](ACOPLE_CAUSAL_REPLAY.md) y el [exportador al contrato](CONTRATO_C_LIVE_V0.md). Por eso las cifras agregadas no deben confundirse con las del contraste anterior.

Sea `r_t=(w_t−p_t)/L`, mano menos centro de cintura en ejes de sala y unidades de hombro; `R_t` tiene como columnas los ejes lateral, superior y anterior estimados del torso. La posición co-rotante es `b_t=R_tᵀr_t`. Para cada par de cuadros, con todos los términos expresados en los ejes del **cuadro actual**:

```text
Δb_t = R_tᵀ(r_t−r_{t−1}) + (R_tᵀ−R_{t−1}ᵀ)r_{t−1}
     = desplazamiento relativo  + cambio de marco
```

La igualdad es exacta a tiempo discreto y pasó comprobación numérica por cuadro a `1e−12`. También se comprobó `||Δb||²=||a||²+||f||²+2a·f`. Así, **las longitudes de arco y el contraste `C` no se suman**: un giro de ejes puede aumentar o cancelar el movimiento relativo según su dirección. El segundo término recoge tanto el giro corporal observado como el error/jitter de la orientación estimada; este archivo no permite separarlos.

Para las **mismas regiones** delante/detrás —clasificadas por el punto medio en marco corporal—, se calculó `C` de la norma de cada término por separado sólo como diagnóstico, sin sumarlos:

| Mano e intervalo | `C` co-rotante | `C` de desplazamiento relativo | `C` sólo de cambio de marco | Tramos donde `||f|| > 0,5||Δb||` |
|---|---:|---:|---:|---:|
| Izquierda, toma completa | +2,241 L/s | −0,356 L/s | −4,174 L/s | 43,8 % |
| Derecha, toma completa | +2,762 L/s | −0,035 L/s | −5,711 L/s | 30,6 % |
| Izquierda, ventana causal que termina en cuadro 529 | +2,964 L/s | +2,252 L/s | −1,354 L/s | 34,2 % |
| Derecha, misma ventana | +1,997 L/s | +1,637 L/s | +0,480 L/s | 4,2 % |

En la ventana de la primera emisión izquierda válida, el recorrido co-rotante acumula sólo `0,518 L` delante y `3,876 L` detrás; por eso el umbral exploratorio de `0,5 L` delante se supera por poco. Una pequeña perturbación de marco, segmentación o escala podría devolver esa salida a `invalid`, aun si el número condicional `+2,964` parece preciso. El signo agregado izquierdo cambia entre definiciones, pero esta tabla **no** demuestra que una sea correcta y la otra falsa: describen preguntas diferentes. El porcentaje de tramos no es un porcentaje de energía ni una atribución causal al giro.

La decisión para el piloto de Nico es conservar `path_definition` y, para cada emisión candidata, los recorridos co-rotante y cintura centrada, más la calidad angular y latencia del marco. Antes de sonificar `C`, evaluar por patrón/giro si su diferencia supera el error instrumental y si la salida sigue válida bajo la perturbación realista de marco. Un `C` que cambia de signo o estado por una elección de ejes no debe presentarse al oyente como «consonancia» o «desconexión» corporal. Si la pregunta es la dirección de Laban, además hace falta el frente de referencia y la línea/segmento pertinentes: la descomposición cinemática no asigna una etiqueta coreútica.
