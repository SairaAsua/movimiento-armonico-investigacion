# Filtrar el marco corporal: menos jitter, más atraso en los giros

Fecha: 24 de septiembre de 2026. Seguimiento del [ensayo de ruido angular](CMU_ORIENTACION_RUIDO.md) en la misma toma CMU 05_02. [Código ejecutable](cmu_filtro_marco_causal.py), `numpy` y `ezc3d`; el archivo C3D se verifica por SHA-256. No se ha probado HarMoCAP, Beacon, las cámaras de Saira ni rope flow. Los ejes derivados de marcadores CMU son una **referencia interna nominal**, no verdad anatómica libre de error.

## Cálculo

Se conservan muñeca, cintura y escala fijada con el primer segundo (303,532 mm). A cada marco nominal `R_t` se agrega una rotación aleatoria independiente entre cuadros con error angular RMS hipotético de **1°**, igual para ambas manos en cada réplica. Semilla `20260925`, 60 réplicas. El filtro toma sólo los últimos `W=1,3,5,9` marcos recibidos, promedia sus matrices y proyecta el promedio a una rotación válida mediante SVD. Se calcula también el filtro del marco nominal **sin ruido añadido**: su diferencia respecto de `R_t` representa el costo de suavizar giros registrados. Para cada `W`, la edad media de muestras en régimen estable es `(W−1)/(2·120)` segundos; no es una medición de latencia de procesamiento/audio.

El script verifica que el resultado emitido antes de los cuadros 250, 600 y 900 no cambie al truncar el futuro. Verifica asimismo determinante 1 para las rotaciones reconstruidas. El contraste `C` usa el recorrido co-rotante completo de la toma y la misma clasificación delante/detrás que el banco previo. Baseline nominal: izquierda **+2,241 L/s**, derecha **+2,762 L/s**.

| W cuadros | Edad media | Error angular p90 al filtrar el nominal | Error angular p90 con ruido y filtro | `C` izquierda: sólo filtro / mediana con ruido | `C` derecha: sólo filtro / mediana con ruido |
|---:|---:|---:|---:|---:|---:|
| 1 | 0 ms | 0,000° | 1,446° | +2,241 / +3,034 | +2,762 / +2,072 |
| 3 | 8,3 ms | 1,818° | 1,834° | +2,316 / +2,594 | +2,803 / +2,873 |
| 5 | 16,7 ms | 3,676° | 3,637° | +2,397 / +2,539 | +2,810 / +2,907 |
| 9 | 33,3 ms | 7,252° | 7,265° | +2,474 / +2,536 | +2,795 / +2,860 |

El promedio de tres cuadros reduce la desviación mediana de `C` respecto del baseline de 0,794 a 0,353 L/s a la izquierda y de 0,690 a 0,111 L/s a la derecha. Con cinco o nueve cuadros ya domina también el cambio producido **sin ruido añadido**: el `C` izquierdo pasa de +2,241 a +2,397 y +2,474 L/s respectivamente. En giros, el filtro se aleja del marco nominal; su p90 angular sube hasta 7,252° a nueve cuadros. Por eso una salida aparentemente estable puede estar atrasada o describir otra trayectoria, y ninguna ventana gana por una métrica única.

Las cifras no demuestran que el marco nominal sea exacto ni que el ruido real sea independiente de un cuadro al siguiente. El filtro puede mejorar o empeorar una medición física: aquí sólo se conoce su diferencia respecto de los marcadores de esta toma. La prueba tampoco cuantifica error temporal de eventos o percepción sonora. Para Nico, el [piloto de video](PILOTO_VALIDACION_VIDEO.md) debe comparar orientación cruda y filtrada con una referencia externa durante giros, registrar marcas `captured_at`/`available_at` y medir tanto estabilidad de `C` como retraso de dirección y fase. La ventana se congelará por tarea y descriptor antes de usar ratings o autoinformes.
