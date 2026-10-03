# Puente de tiempo para video: HarMoCAP y Weaver

Revisión de código público al 3-10-2026. Alcance: decidir qué salida sirve para
el primer ensayo de video→movimiento→sonido, sin cámara ni personas. **No es**
una prueba de fase corporal, percepción estética o sincronía audiovisual.

## Dos rutas con propósito distinto

| Ruta | Tiempo y datos disponibles | Uso verificable hoy |
|---|---|---|
| [HarMoCAP `main` `bdeebbf5`](https://github.com/Mar-IA-no/HarMoCAP/tree/bdeebbf5bef4f78d1dc6ff43feb8228e994feb49), webapp | El [procesador offline](https://github.com/Mar-IA-no/HarMoCAP/blob/bdeebbf5bef4f78d1dc6ff43feb8228e994feb49/src/harmocap/webapp/processing.py) usa índice/FPS, exporta 24 features y estados por slot, pero no las articulaciones 2D crudas. | Demostración/mediciones exploratorias cuya cronología irregular todavía no es científicamente utilizable. |
| [HarMoCAP PR #4](https://github.com/Mar-IA-no/HarMoCAP/pull/4), abierto, `e0bdafc` | `ffprobe` PTS/ticks/base, origen del primer cuadro del medio, SHA-256, índice fuente, recorte por PTS, JSONL/CSV y recuentos. Verifica que el archivo no cambie; separa tiempo del medio y reloj monotónico de procesamiento. Rechaza tiempo ausente/no monótono y decodificación con conteo discordante. Sigue exportando **features**, no pose cruda. | Candidato para auditar las features temporales del mismo archivo; no es todavía un conector R09. |
| [Weaver R09](https://github.com/AlterMundi/harmonic-weaver/pull/76), ya integrado | [`MotionFrame`](https://github.com/AlterMundi/harmonic-weaver/blob/7ce7fa3cf356fdc6f73e8ca53a1602d62c2f9060/src/harmonic_weaver/lab/contracts.py) conserva pose COCO-17, `source_pts`, base, origen declarado y tiempo relativo; el [worker](https://github.com/AlterMundi/harmonic-weaver/blob/7ce7fa3cf356fdc6f73e8ca53a1602d62c2f9060/src/harmonic_weaver/lab/perception_worker.py) usa PyAV y el backend de pose de HarMoCAP. Su caché vincula hash de medio/modelo. | Ruta candidata directa para video→pose→sonido de laboratorio. Si el worker cae en `timestamp_origin=index_fps`, ese segmento se excluye del contraste temporal aunque sea reproducible. |
| [Weaver #77](https://github.com/AlterMundi/harmonic-weaver/issues/77), PRs [#86](https://github.com/AlterMundi/harmonic-weaver/pull/86)–[#89](https://github.com/AlterMundi/harmonic-weaver/pull/89) abiertos y apilados | Eventos por slot, IDs, captura/recepción separadas, derivada opcional con reloj de productor y metadata a través de agregadores. | Resuelve progresivamente la ruta **OSC en vivo**; no importa el PTS del archivo de HarMoCAP ni convierte la webapp en fuente R09. |

**Verificación de la punta OSC propuesta:** en PR #89 `013fe914`, 33 pruebas focalizadas del evento/engine/derivada/agregadores y 12 del driver histórico pasaron con el kit de HarMoCAP `e0bdafc` apuntado explícitamente. La [nota de auditoría](WEAVER_LABORATORIO_ESTADO_20261002.md) registra el alcance. Esto no fusiona los PR, no valida el timestamp de exposición ni reemplaza los PTS de los archivos de video.

El [importador CSV R11 #91](https://github.com/AlterMundi/harmonic-weaver/pull/91)
también está abierto, pero su contrato declara canales de neuroseñal, hardware,
frecuencia nominal y reloj propios. Usarlo para rebautizar los CSV de pose de
HarMoCAP sería atribuirles un instrumento y significado que no tienen. No es
un puente de movimiento por mera coincidencia del formato CSV.

## Correspondencia temporal necesaria

El PR #4 define `PTS_i` y `PTS_0` del **primer cuadro decodificado del medio
completo**. Para compararlo con el reloj relativo de la [rama R08 de anotación
de soga](https://github.com/AlterMundi/harmonic-weaver/blob/7ce7fa3cf356fdc6f73e8ca53a1602d62c2f9060/src/harmonic_weaver/lab/research/rope_media.py), el tiempo candidato es

`t_rel_i = (source_pts_ticks_i − source_pts_origin_ticks) × source_time_base`.

No usar `t_s − t_s_del_primer_cuadro_del_recorte`: desplazaría de nuevo el
origen. Tampoco equiparar sin cotejo el `stream.start_time` que el worker R09
resta a `frame.pts` con el primer cuadro decodificado que usa R08/HarMoCAP;
esos orígenes pueden diferir. Para una comparación exacta conservar el PTS
entero y la fracción de base antes de pasar a `float` o microsegundos.

**Control sintético ejecutado.** Con FFmpeg/ffprobe `6.1.1-3ubuntu5`, se
generaron cuatro cuadros FFV1 a 10 fps con `setpts=PTS+2/TB` (CFR) y otros
cuatro con `setpts=PTS+gte(N\,2)*1/TB+2/TB` (hueco VFR). Se corrieron
`probe_video_timeline()` de HarMoCAP `5987e1e` y `rope_media.probe()` de
Weaver `7ce7fa3` sobre **los mismos archivos**. Ambos hashes coincidieron;
las secuencias relativas fueron `0, 0.1, 0.2, 0.3 s` y
`0, 0.1, 1.2, 1.3 s`. La mayor discrepancia por conversión a `float` fue
`2.23e-16 s`. Esto comprueba correspondencia de esos dos probes en dos
fixtures construidos; no la correspondencia de píxeles OpenCV/PyAV en un
video humano, ni las features, ni el audio.

| Campo PR #4 | Destino candidato | Condición |
|---|---|---|
| `source_video_sha256`, `source_frame_index` | Manifiesto de medio y cuadro R09 | Hash idéntico del **original**, mismo orden de decodificación y mismas dimensiones/orientación. |
| `source_pts_ticks`, `source_time_base`, `source_pts_origin_ticks` | `source_pts`, `time_base_num/den`, origen explícito | Verificar igualdad exacta de PTS en cada índice; no asumir que dos backends aceptan idénticos cuadros. |
| `t_us`, `t_s` | Tiempo de cálculo de features | Ambos derivan del PTS del medio. No son reloj de exposición óptica ni `available_monotonic_s`. |
| `persons[].slot`, `feature_states`, `features` | Futuro adaptador **FeatureFrame** de movimiento | Exige segmentar identidad/reinicios de slot y traducir `observed/held/invalid`; el cero centinela inválido no es una observación. |

La webapp no exporta `persons[].joints`, así que no se puede construir un
`MotionFrame` R09 con ella sin volver a correr percepción o ampliar el contrato
de HarMoCAP. Para el primer ensayo sonoro conviene usar la pose del worker R09
y cotejar el tiempo sobre un mismo video; las 24 features de HarMoCAP pueden
compararse como **segunda ruta**, sin afirmar que sean la matemática original
de Laban ni mediciones de energía metabólica.

**La coincidencia PTS no garantiza coincidencia espacial.** En el [banco de rotación con cuatro cuadros](VIDEO_ROTACION_BACKENDS.md), HarMoCAP conservó PTS y OpenCV 5.0.0 entregó píxeles autorrotados, mientras el probe R08 de anotación de soga rechazó el mismo MP4 con matriz de giro. Un derivado sintético con giro incorporado conservó los cuatro PTS, produjo píxeles idénticos a la vista de OpenCV y sí fue aceptado por R08, **con hash nuevo y transformación documentada**. El [control VFR](VIDEO_ROTACION_VFR.md) mostró otro límite: sin `-fps_mode vfr`, esa conversión transformó cuatro cuadros de tiempo irregular en siete regulares y R08 aceptó ambos derivados. El `file_frames()` real de R09, ejecutado con PyAV 16.1.0, coincidió con OpenCV en píxeles/PTS y también consumió los siete cuadros derivados; no se ensayó el modelo de pose. Un estudio mano–soga necesitará comparar **píxeles orientados, número de cuadros y PTS** entre rutas y versionar cualquier vínculo original→derivado.

## Gates antes del video autorizado

1. Con un **fixture sintético** CFR desplazado y otro VFR, producir inventario
   de ambas rutas: hash, `source_frame_index`, PTS entero, base y tiempo
   relativo. Exigir igualdad por cuadro; si no coincide, investigar antes de
   derivar fase o escuchar.
2. En el archivo humano autorizado, repetir el cotejo índice→píxel/PTS en el
   **tramo seleccionado y alrededor de cada hueco**, registrar cuántos cuadros
   fallan y no compartir el material bruto. Congelar SHA de medio, modelo,
   código, configuración y versión de anotación.
3. Para una capa relacional, declarar qué señales independientes se comparan
   (por ejemplo mano–soga), cómo se observó la soga y qué pasa si falta un
   cruce. La webapp sólo mide cuerpo; no inventar fase de soga con `beat_phase`.
4. Guardar WAV realmente renderizado, controles aplicados, reloj de origen y
   exclusiones. El video CFR de vista previa no prueba sincronía; evaluar la
   alineación contra el original/PTS y registrar incertidumbre.

**Decisión:** la [issue de investigación #10](https://github.com/SairaAsua/movimiento-armonico-investigacion/issues/10)
mantiene como primer camino de sonido el laboratorio R09, con controles de
tiempo y calidad. El PR #4 mejora el análisis offline de features y permite un
cotejo independiente, pero no reemplaza ni valida el contrato de video/pose de
Weaver. El trabajo OSC de #77 queda en su propia ruta live.
