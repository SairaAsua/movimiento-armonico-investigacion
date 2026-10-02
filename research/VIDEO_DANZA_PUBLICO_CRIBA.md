# Criba de video público de danza para la issue #10

**2 de octubre de 2026 · exploración técnica, no datos del estudio.** La [issue #10](https://github.com/SairaAsua/movimiento-armonico-investigacion/issues/10) pide un original autorizado, pose con calidad, canales validados y audio offline de Weaver/Beacon. Esta criba busca un material puente entre los bancos sintéticos y la futura grabación consentida de Nico. No cumple esos criterios de aceptación ni incorpora videos, cuadros o trayectorias de personas al repositorio.

## Regla de elección

Antes de calcular Laban o HIT, exigir: movimiento visible en cuadros sucesivos; cuerpo y extremidades identificables durante un intervalo continuo; PTS del original conservados; cámara y cortes caracterizados; permiso de uso compatible con el análisis; y una referencia independiente para cualquier afirmación de error anatómico. Registrar también los candidatos descartados, para no escoger sólo el fragmento que produce una figura atractiva. Una licencia de copyright del archivo no documenta por sí sola el consentimiento de quien aparece para participar en este estudio ni habilita inferencias sobre su experiencia, eficiencia o estado de conciencia.

## Tres originales revisados

| Archivo y procedencia | Inspección local del original | Decisión |
|---|---|---|
| [«Las primeras segundas de Danza Negra»](https://commons.wikimedia.org/wiki/File:Video-output-5043687D-0BB7-47C6-A884-4BCAA317BFB0.webm), marcado CC0 por quien lo subió | WebM VP9, 2160 × 2160, 15,533 s, **466** cuadros a 30 fps con PTS monótonos. Las muestras a 0, 3, 6, 9 y 12 s muestran la misma fotografía con firma; no hay cuerpo en movimiento visible. SHA-256 del original descargado: `81925ccd2e5bf108886cbeaaf421339199b8bc03a08c63d5a9906c1a006a5a58`. | **Descartar como video de danza**. Es un falso positivo que título, licencia y metadatos temporales no detectan. |
| [«Otra expresión artística, danza»](https://commons.wikimedia.org/wiki/File:Otra_expresi%C3%B3n_art%C3%ADstica,_danza.webm), CC BY-SA 4.0 según Commons | WebM VP8, 1080 × 1920, 10,843 s, **271** cuadros a 25 fps; PTS monótonos e intervalo máximo observado de 40 ms. Las muestras cada 2 s muestran danza real, pero cámara móvil, varias personas, cruces y oclusiones. SHA-256: `28649496f17af54dadee5c6e77aad9646ac2548fa05953e1a6abfbdc94485b38`. | **Reservar como prueba de estrés** de identidad/visibilidad y movimiento de cámara. No usar para validar trayectorias corporales, fase entre personas ni una relación belleza–medida. |
| [«Persona dance rehearsal»](https://commons.wikimedia.org/wiki/File:Persona_dance_rehearsal.webm), CC BY-SA 4.0 según Commons | WebM VP8, 852 × 480 según decodificador, 1039,547 s. Hay **25.967** cuadros con PTS monótonos, desde 0,827 s hasta 1039,547 s; el mayor intervalo observado es 120 ms pese a los 25 fps nominales. Las muestras a intervalos de 180 s y las de los primeros 24 s muestran dos intérpretes, contacto/solapamiento y al menos un cambio de encuadre aparente; todavía no se hizo auditoría completa de cortes, escala ni calidad de pose. SHA-256: `573ac41a261d71fc59fbf890d129964061f3c9346bcf6fcf5b4cecb3217e05aa`. | **Candidato exploratorio condicionado** a hallar un tramo continuo y auditar todas sus pérdidas de visibilidad. No declarar cámara fija ni señal 2D válida con la muestra actual. |

Los nombres y licencias anteriores proceden de las páginas de los archivos en Wikimedia Commons; las propiedades del medio y la inspección de cuadros proceden de los originales descargados localmente. Las observaciones visuales describen **sólo los cuadros muestreados**, salvo los conteos de PTS indicados expresamente. No se redistribuyen medios de terceros ni se publican contactos visuales.

La [auditoría reproducible](auditar_video_fuente.py) coteja el número de cuadros decodificados con sus PTS, calcula SHA-256 y resume el cambio medio absoluto entre cuadros grises reducidos a 64 × 64 píxeles. En los tres originales, la mediana de ese cambio normalizado fue respectivamente `0,0000019`, `0,0424` y `0,0155`; los máximos fueron `0,00072`, `0,123` y `0,162`. Esto ayuda a detectar el archivo casi estático y señala saltos visuales para revisión. **No separa movimiento corporal de cámara, iluminación, compresión o corte**, ni califica danza. El primer conteo manual con `awk` omitió el primer cuadro de cada archivo; se corrigió cotejando decodificación y PTS en el mismo programa.

### Preselección de un intervalo del ensayo

Se revisó una cuadrícula de cuadros cada 10 s a lo largo del ensayo y, alrededor de un encuadre más abierto, cuadros cada 2 s entre 150 y 174 s. **152 ≤ PTS < 174 s** contiene 550 cuadros, del 152,027 al 173,987 s, con intervalo máximo de 40 ms y ningún salto mayor de 60 ms. El encuadre en las muestras de ese tramo muestra dos cuerpos generalmente enteros; al comienzo se superponen y después alternan desplazamientos y pausas. Justo antes aparece un cambio de escala/encuadre. La detección automática con `select='gt(scene,0.1)'` no marcó saltos internos posteriores al borde inicial, pero ese umbral no demuestra que no haya cortes, paneos o identidades perdidas.

**Decisión:** 152–174 s es un **precandidato para ensayar rechazo y cobertura de pose 2D**, no un clip ya apto para estimar una geometría corporal de referencia, fase HIT o sonido Beacon. La muestra temporal no sustituye la revisión de todos los cuadros ni una anotación independiente; la superposición entre intérpretes es precisamente una razón para esperar estados `invalid`. La licencia pública del archivo tampoco convierte a las intérpretes en participantes del estudio. Si una prueba futura usa este tramo, debe conservar los PTS del original y reportar los 550 cuadros en el denominador, incluidos los que no permitan seguir un cuerpo.

### Frontera actual con HarMoCAP

Se leyó el código de `Mar-IA-no/HarMoCAP` en el commit [`bdeebbf`](https://github.com/Mar-IA-no/HarMoCAP/tree/bdeebbf5bef4f78d1dc6ff43feb8228e994feb49). Su [procesador web de archivos](https://github.com/Mar-IA-no/HarMoCAP/blob/bdeebbf5bef4f78d1dc6ff43feb8228e994feb49/src/harmocap/webapp/processing.py#L506) convierte inicio/fin a índices mediante FPS y asigna `t_us = (src_i - 1) / fps`, sin leer PTS del medio ni guardar el índice fuente en su JSONL. La [ruta `LatchingCamera`](https://github.com/Mar-IA-no/HarMoCAP/blob/bdeebbf5bef4f78d1dc6ff43feb8228e994feb49/src/harmocap/capture.py#L91) simula un archivo a 1/FPS, le asigna reloj monotónico de ejecución y puede descartar cuadros por *latest-frame*. Son rutas útiles para visualización o simulación en vivo, pero todavía no producen una cronología científica offline del archivo.

En este original, `(25.967−1)/25 = 1038,640 s` difiere del último PTS `1039,547 s`; la diferencia incluye el origen `0,827 s` y al menos un hueco temporal. En el salto máximo observado, `120 ms` de medio se convertirían en `40 ms` por FPS; una derivada calculada a través de ese salto podría triplicarse artificialmente. El tramo 152–174 s no presenta ese hueco, pero aún necesita un enlace explícito entre cada detección y su PTS antes de usarse en una comparación de fase. Se abrió [HarMoCAP #3](https://github.com/Mar-IA-no/HarMoCAP/issues/3) para conservar PTS, procedencia y denominadores; el receptor Weaver tiene además [su issue #77](https://github.com/AlterMundi/harmonic-weaver/issues/77).

### Prueba local de percepción, sin validación anatómica

Se ejecutó [este diagnóstico agregado](diagnosticar_pose_video_publico.py) con el `PoseBackend` del commit HarMoCAP `bdeebbf`, el checkpoint oficial `models-v1/harmocap-m-pose-ft2.pt` (SHA-256 `80eae9b99ab5710ec6c0bd366acefa0e116482e98c9bba3803b62bf984fc0bcc`), CPU, imagen de inferencia 640, `conf=0,25`, `max_det=8` y ByteTrack. Entorno local: Python 3.12.3, PyTorch 2.14.1+cpu, Ultralytics 8.4.99 y OpenCV 5.0.0.93. El script coteja índice decodificado con PTS obtenidos de `ffprobe` y **sólo imprime conteos y confianza agregados**. Comando, con rutas locales propias:

```bash
python research/diagnosticar_pose_video_publico.py VIDEO_ORIGINAL.webm CHECKPOINT.pt \
  --start-pts 152 --end-pts 174 --stride 1 --split-pts 160
```

| Pasada | Cuadros procesados / denominador | 2 detecciones / 1 detección | Confianza de muñeca izquierda ≥ 0,5 entre detecciones |
|---|---:|---:|---:|
| Muestreo sistemático, 1 de cada 5 | 110 / 550 | 106 / 4 | 58,33 % de 216 detecciones |
| Todos los cuadros | **550 / 550** | **542 / 8** | **59,07 % de 1092 detecciones** |
| Todos, 152–160 s | 200 / 200 | 200 / 0 | 41,00 % de 400 detecciones |
| Todos, 160–174 s | 350 / 350 | 342 / 8 | 69,51 % de 692 detecciones |

En la pasada completa el modelo produjo tres IDs efímeros para una escena que las muestras visuales muestran con dos intérpretes: hay que auditar continuidad de identidad antes de derivar relaciones entre personas. La menor confianza de muñeca izquierda en 152–160 s coincide con las muestras donde hay mayor cruce, **sin probar que el cruce sea la causa**. Un umbral exploratorio de confianza `0,5` no es una probabilidad calibrada ni una referencia anatómica: dos detecciones no prueban que se hayan seguido correctamente dos cuerpos, y 550 cuadros procesados no implican 550 cuadros con muñecas utilizables. No se guardaron ni publicaron cuadros, poses o IDs por tiempo.

Para comprobar **coincidencia temporal** de señales, se repitió la pasada completa con tres compuertas fijadas antes de ver los nuevos agregados. `torso` exige ambos hombros y ambas caderas con confianza ≥ 0,5; las otras añaden muñeca derecha o ambas muñecas. Una fila pasa sólo si aparecen **dos** detecciones con track y las dos cumplen todos los puntos requeridos. La racha se cuenta en cuadros procesados consecutivos (`stride=1`); la columna de segundos es la distancia PTS entre el primer y último cuadro de esa racha.

| Compuerta exploratoria, dos personas | Cuadros que pasan / 550 | Racha más larga | Tramo 152–160 s / 200 |
|---|---:|---:|---:|
| Torso | 542 | 328 cuadros; 13,08 s de span PTS | 200 |
| Torso + muñeca derecha | 467 | 285 cuadros; 11,36 s | 166 |
| Torso + ambas muñecas | **141** | **63 cuadros; 2,48 s** | **33** |

Estas son **salidas de confianza del modelo**, no cobertura anatómica validada. Un cálculo bilateral o de fase entre personas no puede tratar los 550 cuadros como si contuvieran cuatro muñecas observadas: ni siquiera este gate permisivo los conserva, y no se ha demostrado continuidad de identidad. El clip puede servir para probar políticas de `invalid`/reset y la auditoría de anotación; no permite todavía atribuir consonancia, planitud o coordinación real. La diferencia entre la compuerta unilateral y bilateral tampoco autoriza cambiar el objetivo del estudio de rope flow a una sola mano: señala una exigencia instrumental para captar bien la soga y ambas manos en el caso principal.

La primera posición que informó OpenCV para esta ventana fue `152,000 s`, mientras que el PTS original del mismo índice fue `152,827 s`: **−0,827 s** de discrepancia de origen. Este diagnóstico de percepción no calcula velocidad, fase, `Q`, belleza ni audio. Para avanzar hará falta una anotación independiente de identidad/keypoints sobre una muestra predefinida, un gate por señal y la corrección de PTS de HarMoCAP #3. El diagnóstico usa ByteTrack sobre la secuencia completa o muestreada; no equivale a validar la configuración `duo` de la interfaz web ni el receptor Beacon.

La [muestra y guía de referencia 2D](REFERENCIA_POSE_VIDEO_PUBLICO.md) ya quedaron preparadas para esa anotación independiente: 40 cuadros sorteados por bins temporales en dos estratos y plantilla privada para A/B, hombros, muñecas y caderas. El paquete no contiene predicciones ni se publica; todavía no hay coordenadas de referencia ni error anatómico medido.

El enlace índice↔PTS usado en ese diagnóstico se cotejó con un [verificador separado de decodificadores](verificar_cuadros_video.py): **los 550/550 cuadros** del intervalo 152–174 s produjeron exactamente los mismos píxeles BGR en OpenCV y FFmpeg (`MAE = 0`). En esos mismos 550 cuadros, `PTS_original − CAP_PROP_POS_MSEC/1000 = 0,827 s` con variación menor a un microsegundo de la representación decimal. Se cotejaron además, por separado, el cuadro inicial y los dos que rodean el hueco al final del original: también coincidieron píxel por píxel; la posición temporal relativa que devuelve OpenCV sí conserva allí el salto de 120 ms. **La pérdida de ese salto ocurre en el cálculo `frame/FPS` de HarMoCAP, no en la decodificación OpenCV de este archivo.** Esta propiedad se verificó en este original/backend, no se generaliza a otros contenedores o implementaciones sin repetir el cotejo.

## Reproducción y siguiente puerta

Conservar en un archivo privado el original exacto y su hash. Para repetir la inspección técnica: `python research/auditar_video_fuente.py <archivo>` y `ffprobe -v error -show_entries format=duration,size:stream=codec_name,width,height,r_frame_rate,avg_frame_rate -of json <archivo>`; muestrear cuadros de toda la duración y después revisar **cada cuadro** del intervalo candidato para cortes, identidades, pies/manos visibles y cambios de escala. Anotar exclusiones con duración y motivo. Sólo entonces ejecutar pose y comparar contra anotación independiente en ese intervalo. Un descriptor que no supere su referencia queda `invalid`, no se rellena ni se transforma en sonido de «consonancia».

Para la issue #10 sigue faltando un clip con permiso apropiado al estudio, una escena versionada, calidad por señal y la traza real de controles aplicados a Weaver/Beacon con audio registrado. El ensayo escénico puede servir como diagnóstico técnico externo; el caso principal sigue siendo el material autorizado de Nico. El audio de un video ajeno, si se ensaya, deberá identificarse como exploración de mediciones observables y no como prueba de HIT, placer, belleza o eficiencia.
