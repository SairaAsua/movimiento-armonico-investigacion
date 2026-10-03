# Un proxy «espacial» puede cambiar sólo por la velocidad

Banco sintético del 3-10-2026; [código reproducible](laban_proxy_ventana_sintetica.py).
El objetivo es auditar el significado de una variable que **existe** en
HarMoCAP, no puntuar a Nico ni validar categorías históricas de Laban.

## La comparación

La implementación [HarMoCAP `FeatureExtractor`](https://github.com/Mar-IA-no/HarMoCAP/blob/bdeebbf5bef4f78d1dc6ff43feb8228e994feb49/src/harmocap/features.py)
calcula `laban_space_proxy` como desplazamiento neto dividido por longitud del
recorrido de las muñecas en una [ventana causal de 300 ms](https://github.com/Mar-IA-no/HarMoCAP/blob/bdeebbf5bef4f78d1dc6ff43feb8228e994feb49/configs/features.yaml).
La [documentación del productor](https://github.com/Mar-IA-no/HarMoCAP/blob/bdeebbf5bef4f78d1dc6ff43feb8228e994feb49/docs/FEATURES.md)
lo declara proxy de directness, con `1=directo`; no es un Effort Space
histórico medido por un experto.

Construimos una muñeca que completa **una vuelta** de la misma circunferencia
de radio `0,04` en coordenadas de imagen, una vez a 1 Hz y otra a 2 Hz.
La forma, radio, sentido y longitud total del recorrido son iguales; duran
1 s y 0,5 s respectivamente. Se muestrean a 120 cuadros/s ideales, con PTS
exactos, sin ruido ni oclusión. El cuerpo de prueba es un esqueleto sintético
fijo salvo ambas muñecas; no pretende ser una ejecución biomecánica posible.

Para velocidad angular constante `ω=2πf`, en una ventana `w≤1/f` el cociente
geométrico continuo es

`D(w,f) = cuerda/arco = |sin(πfw)|/(πfw)`.

El descriptor de distribución de tangentes por arco propuesto **por este
proyecto**, `Q=(∫u_x²ds/L, ∫u_y²ds/L)`, da `(0,5; 0,5)` en ambas vueltas. `Q`
describe el recorrido en estos ejes proyectados; no es «la ecuación de Laban».

| Una vuelta | `Q` por arco `(x,y)` | Directness 300 ms continuo | HarMoCAP real `laban_space_proxy` | Directness en 30 % del ciclo, alternativa sintética |
|---|---|---:|---:|---:|
| 1 Hz, 1 s | (0,500; 0,500) | 0,858394 | **0,858492** | 0,858492 |
| 2 Hz, 0,5 s | (0,500; 0,500) | 0,504551 | **0,504782** | 0,858786 |

El script ejecutó el `FeatureExtractor` real en el checkout HarMoCAP
`e0bdafc16485770739576ed8a910796da6727bf0` (misma fórmula que el
`main` auditado), con la configuración real de ventanas y calibración
fallback. Los estados del proxy fueron `observed` en ambos casos. La pequeña
diferencia respecto de la fórmula continua procede de aproximar el arco con
segmentos a 120 Hz. Sin `--harmocap-root`, el script corre con la biblioteca
estándar y reproduce las columnas geométricas; con esa opción coteja el
productor real.

## Qué cambia en el diseño del estudio

`laban_space_proxy` responde a **geometría local dentro de 300 ms**. Si se
duplica la cadencia manteniendo la misma curva completa, la ventana abarca
60 % en vez de 30 % de la vuelta y el valor cae. Eso no es un bug del
extractor: es una consecuencia de elegir una ventana de tiempo fijo. Tampoco
quiere decir que una ejecución sea menos directa en el sentido cualitativo
de Effort Space. Con una vuelta cerrada y ventana de ciclo entero, el cociente
sería cero incluso para una órbita fluida.

Para el contraste `base → +Laban → +HIT`, no clasificar esta señal como
**geometría pura**. Conservarla con nombre, ventana y unidades como descriptor
cinemático mixto; incluir cadencia/duración en la base o hacer un análisis de
sensibilidad que la excluya. Para la pregunta espacial primaria, preferir
`Q` por arco u otra descripción validada que no cambie al reparametrizar el
mismo recorrido, más una capa temporal separada. Una ventana de fracción de
ciclo puede quitar este efecto en el círculo ideal, pero necesita fase/ciclo
identificables; derivarla de la misma relación HIT filtraría información al
bloque «Laban». Si se ensaya, congelar el detector de tarea y su procedencia
antes de comparar modelos.

Esto sólo demuestra una propiedad matemática y de software. No mide soga,
fuerza, gasto energético, belleza ni conciencia. La validación espacial en
Nico sigue necesitando tarea, marcos, cámaras y anotaciones independientes
según [issue #4](https://github.com/SairaAsua/movimiento-armonico-investigacion/issues/4).
