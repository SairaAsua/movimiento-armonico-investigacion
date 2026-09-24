# Acople espacio–tiempo: replay causal antes de Beacon

Fecha: 24 de septiembre de 2026. Este es un ensayo computacional **offline** sobre una toma humana externa, no una prueba de HarMoCAP, del instrumento Beacon, de Nico ni de rope flow. Su objetivo es averiguar si el contraste `C` propuesto en [el acople espacio–tiempo](ACOPLE_ESPACIO_TIEMPO.md) puede existir en una ventana retrospectiva sin conocer el resto de la toma.

## Entrada y operación disponible en cada instante

El [banco CMU 05_02](CMU_DANZA_BANCO_REAL.md) documenta procedencia, licencia, SHA-256 y límites de los diez marcadores de torso y muñecas que se usan. El [script reproducible](cmu_causal_c_replay.py) verifica el hash `04bb9be74cd9183eb9f873b26c6eb4dbbf613747af5d6d0ef41f146b859d51d7`, 1.123 cuadros a 120 Hz y unidades mm. Usa `numpy` y `ezc3d`; se ejecutó con `PYTHONPATH=/tmp/ropeflow-ezc3d python cmu_causal_c_replay.py` (`ezc3d` 1.7.2 en el entorno aislado). No reetiqueta marcadores como articulaciones anatómicas.

Los cuadros 0–119 calibran la escala fija: mediana del ancho entre marcadores de hombros = **303,532 mm**. Ningún valor se emite antes del cuadro 120 (1,000 s). En cada cuadro nuevo, el origen es el punto medio de la cintura y los ejes son lateral de hombros, superior ortogonalizado y anterior por producto vectorial. La mano es el promedio de dos marcadores de muñeca; el tramo nuevo utiliza los dos cuadros ya llegados. Se conserva si el punto medio del tramo cae delante o detrás del plano coronal, y su longitud y rapidez en unidades de longitud de hombros por segundo.

Para una ventana retrospectiva `(t−W,t]`, `C` es la rapidez media ponderada por longitud de arco **delante menos detrás**. El umbral exploratorio exige al menos **0,5 longitudes de hombro de recorrido y dos tramos en cada región**; si falta una región, la salida es `insufficient_region`, sin número nuevo. El umbral es una regla instrumental creada aquí, no un límite de Laban, HIT ni fisiológico. El script compara cada valor de la cola retrospectiva con un cálculo por lote sobre exactamente los mismos tramos y exige acuerdo a 1e−12. Además, trunca el archivo en los cuadros 240, 600 y 960 y exige que las emisiones anteriores no cambien. El código lee un archivo completo para simular la llegada cuadro a cuadro: estas pruebas establecen **dependencia temporal lógica**, no latencia de cómputo, transmisión ni audio en tiempo real.

| Mano | W | Cuadros válidos tras calibrar | Primera emisión válida desde inicio | `C` mínimo / mediana / máximo, L/s |
|---|---:|---:|---:|---:|
| Izquierda | 0,5 s | 122/1003 (12,2 %) | 4,408 s | −0,019 / 1,707 / 2,620 |
| Izquierda | 1,0 s | 314/1003 (31,3 %) | 4,408 s | −0,473 / 2,003 / 3,194 |
| Izquierda | 2,0 s | 521/1003 (51,9 %) | 4,408 s | 1,075 / 1,953 / 3,910 |
| Derecha | 0,5 s | 205/1003 (20,4 %) | 2,958 s | −1,829 / 1,879 / 5,325 |
| Derecha | 1,0 s | 445/1003 (44,4 %) | 2,958 s | −2,602 / 1,759 / 3,889 |
| Derecha | 2,0 s | 671/1003 (66,9 %) | 2,958 s | −1,273 / 1,999 / 4,884 |

La primera salida válida tarda mucho más que `W` porque la mano permanece en una región o no alcanza el recorrido mínimo en la otra. Una ventana mayor aumenta cobertura, pero mezcla más fases/frases; por ejemplo, el signo mínimo de la mano izquierda cambia entre ventanas. No hay motivo para elegir 2 s sólo por cobertura. La toma no tiene soga ni tarea repetida, así que estos porcentajes no predicen cuánto estará disponible `C` durante el patrón de Nico.

## Sensibilidad al umbral elegido

Con `W=1,0 s` y al menos dos tramos por región, se repitió el replay variando **sólo** el arco mínimo por región. El denominador sigue siendo 1.003 cuadros tras calibrar.

| Arco mínimo por región | Izquierda válida | Derecha válida | Primera izquierda / derecha |
|---:|---:|---:|---:|
| 0,10 L | 393 (39,2 %) | 510 (50,8 %) | 4,367 / 2,900 s |
| 0,25 L | 367 (36,6 %) | 486 (48,5 %) | 4,383 / 2,925 s |
| 0,50 L | 314 (31,3 %) | 445 (44,4 %) | 4,408 / 2,958 s |
| 1,00 L | 187 (18,6 %) | 327 (32,6 %) | 4,467 / 3,092 s |

La cobertura de la mano izquierda cae de 39,2 % a 18,6 % al exigir diez veces más recorrido; la derecha de 50,8 % a 32,6 %. Los valores de `C` en cuadros que pasan **ambos** umbrales son idénticos porque el umbral decide emisión, no cambia la fórmula. Los cuadros extra admitidos por una regla laxa podrían tener mayor error relativo si el recorrido es pequeño frente al error de reconstrucción, pero esta toma no proporciona un error de cámara propia ni una referencia para cuantificarlo. La elección del umbral requiere medir ruido, sesgo y estabilidad en el montaje real, y fijarla antes de contrastar experiencia o eficiencia. Maximizar cobertura sobre esta toma sería optimizar la regla con el mismo caso que se usa para ilustrarla.

Con `W=1,0 s` y umbral 0,50 L, la izquierda forma cuatro rachas válidas de **106, 86, 97 y 25 cuadros** (0,883, 0,717, 0,808 y 0,208 s); la derecha, cuatro de **99, 150, 97 y 99 cuadros** (0,825, 1,250, 0,808 y 0,825 s). Hay huecos internos inválidos de 23, 64 y 193 cuadros a la izquierda; de 25, 19 y 217 a la derecha. Por tanto un control sonoro sin estado de expiración reaparecería en ráfagas separadas por tramos sin valor descriptivo, aunque el archivo de marcadores no tenga huecos de captura. Esto es un problema de **cobertura geométrica**, distinto de pérdida de video. La política de reset/fade y la audibilidad de esas rachas siguen sin probarse.

## Consecuencia para el contrato futuro

Una eventual señal `spacetime_c` precisa `source_frame_id`, `feature_window_start/end`, `available_at`, `scale_calibration_end`, `window_seconds`, marcador/proxy usado, arco y número de tramos por región, unidades, calidad y estado. En este replay `available_at` lógico es la llegada del cuadro terminal; **no** se midió una marca de reloj de pared. Si la condición regional caduca, Beacon debería recibir un estado inválido y aplicar un `reset` o política de supresión comprobada, [no sostener el último timbre como si aún describiera el movimiento](BEACON_TRANSICIONES_Y_RESET.md). La pérdida de metadatos de captura en [la ruta HarMoCAP→Weaver auditada](RUTA_HARMOCAP_WEAVER_BEACON.md) impide por ahora verificar esa procedencia en el instrumento.

Antes de diseñar sonificación o un modelo de belleza/eficiencia, el banco de cámaras propio debe medir cobertura y sesgo por patrón, mano, región y ventana; repetir el cálculo con error 3D y oclusiones observados; y comparar la salida causal con una referencia independiente. `C` sólo detecta **dónde cae un acento de rapidez** respecto al cuerpo. No mide energía metabólica, esfuerzo, sensualidad, conciencia ni “consonancia” en sentido valorativo.
