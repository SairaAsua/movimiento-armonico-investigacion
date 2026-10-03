# Primera prueba sobre movimiento humano externo: CMU danza moderna 05_02

Auditoría local del 24 de septiembre de 2026. La [base oficial de captura de movimiento de Carnegie Mellon](http://mocap.cs.cmu.edu/) declara sus datos libres para todos los usos; sus [FAQ](http://mocap.cs.cmu.edu/faqs.php) indican que pueden copiarse, modificarse y redistribuirse sin permiso. La [ficha del sujeto 05](http://mocap.cs.cmu.edu/search.php?subjectnumber=5) clasifica la prueba 02 como danza con brazos expresivos y pirueta, y lista `05_02.c3d`, `05_02.amc` y el esqueleto `05.asf`. Se descargaron **sólo esos tres archivos** en `sources/cmu_mocap/`, dentro del archivo local ignorado por Git. No contienen rope flow de Nico.

## Archivos y reproducción

| Archivo oficial | Bytes | SHA-256 | Uso aquí |
|---|---:|---|---|
| [05_02.c3d](http://mocap.cs.cmu.edu/subjects/05/05_02.c3d) | 2.989.296 | `04bb9be74cd9183eb9f873b26c6eb4dbbf613747af5d6d0ef41f146b859d51d7` | Marcadores 3D y metadatos de la toma |
| [05_02.amc](http://mocap.cs.cmu.edu/subjects/05/05_02.amc) | 893.895 | `a866b7931ba3ca5cd7ca5d154c96d03d447ae4fce870fbfcd1004446cbba6e7e` | Guardado como fuente alternativa de ángulos; **no** se hizo cinemática directa con él |
| [05.asf](http://mocap.cs.cmu.edu/subjects/05/05.asf) | 7.270 | `bbdd4ba5c6807a5c036ebd2e4e23028c6097d36f557cb30a3f49d158aad07aa1` | Esqueleto correspondiente; **no** validó los puntos C3D |

El C3D declara 330 puntos (muchos parecen etiquetas derivadas), 1.123 cuadros, 120 Hz y unidades milimétricas. La duración entre primer y último cuadro es `(1123−1)/120 = 9,350 s`; `1123/120` sería duración de 1.123 intervalos y no la distancia temporal entre extremos. Se leyó con [ezc3d](https://github.com/pyomeca/ezc3d) 1.7.2 y NumPy 2.4.4; el paquete Python `c3d` 0.6.0 rechazó este archivo por metadatos de tasa analógica inconsistentes, de modo que **no** se asumió que todos los lectores aceptan el mismo C3D. El [script local](cmu_danza_05_02_audit.py) verifica hash, dimensiones, unidades y estado residual antes del cálculo.

## Operación geométrica aplicada

Para cada cuadro, el origen es la media de `LFWT` y `RFWT` (dos etiquetas de cintura). El eje lateral va de `RSHO` a `LSHO`; el eje superior va del origen al punto medio de hombros y se ortogonaliza respecto del lateral. El tercer eje es su producto vectorial. Como control de orientación, la proyección de `STRN−RBAC` (esternón menos espalda, según etiquetas) sobre ese tercer eje fue positiva en los 1.123 cuadros, entre 195,9 y 260,9 mm. El ancho entre marcadores de hombros tuvo mediana 302,1 mm y rango 240,2–325,9 mm; se fijó la **mediana de toda la toma** como escala constante `L`. Esto comprueba consistencia interna de la convención para esta toma, no la exactitud anatómica del marco.

Como **proxy de posición de muñeca**, se promedió el par de puntos etiquetados `LWRA/LWRB` o `RWRA/RWRB`. No son el centro articular demostrado ni marcan una soga. Se transformó cada proxy al marco del torso y se calculó la rapidez por diferencia de cuadros. El contraste `C` es rapidez media por arco cuando el proxy está delante (`frente≥0`) menos la misma media cuando está detrás; se pondera cada segmento por su longitud. Los diez marcadores usados por este cálculo se señalaron como presentes por el residual de C3D en todos los cuadros; ese indicador **no certifica** ausencia de error, filtrado o imputación previa.

La escala mediana de hombros usa **toda la toma** y el contraste usa la trayectoria completa: este script es retrospectivo. No constituye un estimador causal listo para Beacon ni un procedimiento que pueda elegir escala después de abrir sesiones reservadas. Para una versión en vivo, escala/calibración deberán quedar fijadas antes de recibir cuadros; el denominador y sus cambios se registrarán.

| Proxy | Recorrido en sala / relativo al torso | Longitud válida delante / detrás | Rapidez por arco delante / detrás | `C` delante−detrás |
|---|---:|---:|---:|---:|
| Izquierdo, media `LWRA/LWRB` | 33,96 / 26,08 `L` | 15,50 / 10,59 `L` | 6,267 / 4,016 `L/s` | **+2,251 `L/s`** |
| Derecho, media `RWRA/RWRB` | 33,63 / 29,02 `L` | 16,30 / 12,71 `L` | 6,901 / 4,126 `L/s` | **+2,775 `L/s`** |

La sensibilidad a la **representación del punto** no es despreciable: usando en su lugar `LWR0` o `RWR0`, el contraste queda +2,451 y +2,437 `L/s`, respectivamente. La distancia mediana entre cada punto adicional y la media del par es 51,2 mm a la izquierda y 46,3 mm a la derecha. Estos puntos proceden del **mismo archivo**, así que el acuerdo de signo no es validación independiente y la diferencia no mide error respecto de una verdad anatómica. Para el piloto de Nico habrá que predefinir qué punto se sigue, su observabilidad y su referencia externa si se hacen inferencias finas.

## Sensibilidad al marco y al espaciado de cuadros

Se calculó además `Q` como distribución de componentes de desplazamiento **ponderada por longitud de arco**, en orden lateral/superior/anterior. Dos operaciones que parecen similares responden preguntas diferentes: (a) desplazamiento de marcador **en sala**, reexpresado en los ejes corporales del comienzo de cada tramo, y (b) diferencia de las coordenadas de muñeca **relativas al torso** entre cuadros. La segunda elimina traslación/rotación globales según el marco estimado; por ello no debe etiquetarse como la primera.

| Proxy | `Q` desplazamiento en sala reexpresado | `Q` cambio relativo al torso |
|---|---|---|
| Izquierdo | 0,284 / 0,183 / 0,533 | 0,357 / 0,243 / 0,400 |
| Derecho | 0,233 / 0,298 / 0,469 | 0,304 / 0,363 / 0,333 |

Cada terna suma 1 por construcción, pero cambia la descripción de la toma: para la izquierda, la componente anterior baja de 0,533 a 0,400 al pasar del desplazamiento en sala al cambio relativo al torso. Es una **elección de pregunta y marco**, no evidencia de que uno sea la verdadera lectura Laban. El marco se deriva de hombros/cintura en cada cuadro y puede introducir ruido o borrar movimiento relevante durante piruetas; el descriptor en sala incorpora traslado y giro del ejecutante. Conservar ambos y su regla de ejes.

La [auditoría adicional del contraste `C` por marco](CMU_MARCOS_C_CONTRASTE.md) mostró que esta elección también puede cambiar el **signo**, no sólo la distribución `Q`: izquierda +2,251 L/s en coordenadas co-rotantes frente a −0,358 L/s al quitar traslado de cintura sin corregir giro, y −0,441 L/s en sala. La mano derecha pasa de +2,775 a −0,035 y +0,013 L/s. Son tres recorridos distintos clasificados con la misma región corporal; no elegir el favorable a la hipótesis después de ver resultados.

Para probar dependencia de muestreo, el script tomó uno de cada 2, 4, 8 o 16 cuadros desde **todos los posibles desplazamientos de inicio**; recalculó `C` con el intervalo temporal correspondiente. Es una decimación **sin filtro antialias**, usada para detectar sensibilidad, no un procesamiento recomendado para video real.

| Muestreo efectivo desde 120 Hz | `C` izquierda, mínimo–mediana–máximo entre fases de decimación | `C` derecha, mínimo–mediana–máximo |
|---:|---:|---:|
| 60 Hz (paso 2) | 2,265–2,292–2,318 `L/s` | 2,659–2,720–2,781 `L/s` |
| 30 Hz (paso 4) | 2,116–2,248–2,277 `L/s` | 2,609–2,784–2,889 `L/s` |
| 15 Hz (paso 8) | 1,937–2,128–2,359 `L/s` | 2,377–2,718–2,937 `L/s` |
| 7,5 Hz (paso 16) | 1,618–2,111–2,320 `L/s` | 2,112–2,637–3,104 `L/s` |

La amplitud entre fases de decimación crece al espaciar cuadros, especialmente a 7,5 Hz. Esa variación no estima el error de las cámaras de Saira: aquí no se cambió exposición, óptica, ruido ni detector, sólo se descartaron muestras de una toma de marcadores. Es otro motivo para comparar descriptores a los **FPS/PTS efectivos** y contra una referencia, sin suponer que interpolar un clip lento reconstruye el acento que no se observó.

Un [banco posterior de situación del recorrido](LABAN_SITUACION_RECORRIDO.md#sensibilidad-a-cantidad-y-fase-de-cuadros) aplica el mismo principio a `rho_min`, `V_r` y `Q` con ventanas y extremos fijos, recorriendo fases de grilla de 60 a 12 Hz. Separa ese efecto de muestreo de los cambios de origen y marco; tampoco estima error de cámaras.

## Control de inversión temporal: una pérdida exacta de información

El script invirtió el orden de los 1.123 cuadros **después** de construir las coordenadas corporales y volvió a calcular `C` y `Q`. Ambos permanecieron iguales hasta tolerancia numérica: `C` izquierda +2,251 y derecha +2,775 `L/s`; las ternas `Q` relativas al torso tampoco cambiaron. Esto no es una propiedad exclusiva de la danza CMU: `C` usa longitudes de tramo, rapidez escalar y región espacial; `Q` usa cuadrados de componentes. Revertir la secuencia conserva esas cantidades por tramo, aunque invierte todos los desplazamientos orientados.

Como control que **sí** retiene sentido, se calculó la suma de incrementos angulares del radio muñeca–cintura proyectado al plano lateral/anterior, con `atan2` y umbral de radio mínimo `0,2 L`. En esta toma ambos radios mínimos superaron `0,62 L` y los saltos por cuadro fueron menores que π, de modo que el cálculo no cruzó singularidades bajo esas reglas. El giro radial neto fue `+0,025` vueltas para la izquierda y `−0,058` para la derecha; en reversa fueron `−0,025` y `+0,058`. Las cantidades positivas/negativas por toda la toma fueron 1,071/1,046 vueltas a la izquierda y 1,149/1,207 a la derecha; se intercambian al invertir el tiempo. **El neto casi se cancela** porque la toma contiene movimientos en ambos sentidos, por lo que un valor agregado cercano a cero tampoco demuestra ausencia de giros o una figura estable.

Consecuencia: para estudiar una **escala o frase orientada** hacen falta dirección firmada, orden de transición, comienzo/fin de figura y reglas de reversa, además de `C` y `Q`. Este giro radial es otro descriptor construido por el proyecto; no se presenta como notación de Laban ni como fase de soga. Su eje y signo dependen del marco corporal validado. Invertir un registro es un control de identificabilidad del descriptor, **no** una actuación humana que pueda valorarse como bella o eficiente.

## Qué cambia para el protocolo

Esta prueba demuestra que el código puede leer una toma humana externa, construir un marco corporal no degenerado en todos sus cuadros y producir el descriptor con trazabilidad de unidades y archivo. También muestra que **elegir “muñeca” sin definición operacional cambia la magnitud**. La prueba no contiene ciclos de rope flow, soga, jueces de belleza, autoinforme, fuerza ni consumo metabólico. Como la toma mezcla brazos expresivos y pirueta, sus cifras agregadas no son una comparación dentro de la **misma figura** ni un resultado predictivo de HIT. La tasa C3D es el reloj del archivo; no se cotejaron PTS absolutos de cámaras ni latencia para Beacon.

La próxima validación real en Nico debe conservar ambos recorridos —sala y cuerpo—, fijar antes el punto de mano/muñeca, medir error y cobertura por región, y analizar figuras/ciclos definidos en vez de sumar toda una sesión diversa. Sólo después se decidirá si `C` entra en un modelo con resultados externos. Esta toma CMU queda como **banco de ingeniería**, no caso de estudio que pruebe la tesis de consonancia.
