# Escuchar el sesgo de proyección con el renderer offline de Weaver

**Banco de integración sintético, 3 de octubre de 2026.** Vinculado a la [issue de contrato temporal #9](https://github.com/SairaAsua/movimiento-armonico-investigacion/issues/9) y al [banco MP4 de proyección de PR #26](https://github.com/SairaAsua/movimiento-armonico-investigacion/blob/research/video-misma-curva-ritmo/research/FASE_PROYECCION_OBLICUA.md). El [script reproducible](weaver_video_proyeccion_pcm.py) comprueba hash del video y manifiesto, vuelve a extraer fase **de los píxeles y PTS de un mismo MP4** y entrega dos series de frecuencia a `PCMWriter` de Weaver, que renderiza mediante Shaper. No inicia cámara, servicio, dispositivo de audio ni OSC; no usa el importador de pose R09 ni `beacon-spatial`.

```sh
/tmp/movimiento-audio-venv/bin/python research/weaver_video_proyeccion_pcm.py \
  --video-repo /checkout/de/PR-26 \
  --weaver-repo /checkout/harmonic-weaver \
  --shaper-repo /checkout/harmonic-shaper \
  --output-dir /ruta/nueva/para/salidas
```

La ruta del Python mostrado corresponde al entorno usado aquí; en otra máquina sirve un entorno con NumPy, SoundFile y las dependencias de Weaver/Shaper. El script exige una carpeta de salida **nueva**, fija las revisiones de los tres repositorios, conserva hashes del MP4 y de la versión del motor y deja dos WAV locales con trazas `voice-frames.jsonl`. No publica WAV derivados del motor: el material fuente y sus [dos WAV diagnósticos propios](https://github.com/SairaAsua/movimiento-armonico-investigacion/blob/research/video-misma-curva-ritmo/research/FASE_PROYECCION_OBLICUA.md) ya son revisables en PR #26.

Ambos puntos del video tienen **la misma fase física construida**. El azul se proyecta con factor vertical `0,25`. La condición `raw_image_phase` toma su `atan2` directo; `corrected_known_plane` divide su desplazamiento vertical por `0,25` **porque el generador lo declaró**, no porque el video permita inferirlo. Ambas condiciones usan los mismos 240 cuadros, los mismos PTS, la misma voz Shaper (`gain=0,5`, panorama/timbre/forma fijos), `f=220+20Δφ` Hz y ocho segundos. Sólo cambia la transformación de la coordenada azul **antes** de calcular fase.

| Serie desde el mismo MP4 | `R` desde píxeles | Frecuencia enviada | RMS PCM Shaper | SHA-256 WAV |
|---|---:|---:|---:|---|
| Ángulo crudo | `0,904818` | `207,424–232,576 Hz` | `0,195187891` | `bc16591a58dfd4a88c911e509d8a457617fa1a43615b72dbb13f22a139f5fbd4` |
| Plano sintético rectificado | `0,999898` | `219,312–220,688 Hz` | `0,195188775` | `7204e466e95b38e9d2c5c07ca5263e069267b2cd26874d4931d2cba9bc49a6b8` |

Los controles de los 240 cuadros aparecen en las trazas; el mayor retardo **lógico** PTS→inicio de bloque fue 192 muestras a 48 kHz, es decir 4 ms, bajo el bloque de 256 muestras. No es latencia óptica ni gesto→oído. Los WAV tienen hashes distintos y niveles RMS casi iguales, pero no se evaluó discriminación auditiva ni sonoridad perceptiva. La condición cruda haría sonar como modulación de movimiento una diferencia que este generador produjo **solo por vista**. El caso rectificado demuestra que el software conserva una corrección conocida, no que una cámara real pueda calibrarse desde una trayectoria desconocida.

**Revisiones ejecutadas:** video PR #26 `bb40edc`, Weaver `cc5fb57`, Shaper `f8bfe07`. El reporte local registra SHA del medio, manifiesto, WAV, trazas, código y entorno del motor. Dos ejecuciones completas produjeron reportes idénticos, SHA-256 `e3bb14ec916b5e819b28bd6410e664ed35866183547fc84687c70a4d3f1e90a4`; pasaron compilación Python, enlaces locales y `git diff --check`. El script se ejecutó sobre el MP4 publicado y rechazará un archivo cuyo SHA no coincida. El siguiente gate para un video humano autorizado es fijar o medir el plano de movimiento con referencia independiente y declarar las ventanas donde cambia; sin ello, una fase de imagen puede explorarse como imagen, no etiquetarse como fase intrínseca de mano/soga. Para Beacon live faltan además la ruta OSC, validez por señal y latencia física. Ninguna de estas salidas demuestra Laban, HIT, belleza, eficiencia o conciencia en personas.
