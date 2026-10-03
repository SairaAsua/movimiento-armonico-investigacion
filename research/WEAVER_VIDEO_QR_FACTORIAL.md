# Geometría proyectada × fase: cuatro MP4 y audio Shaper

**Banco sintético de método, 2 de octubre de 2026; coordinación de la [issue #9](https://github.com/SairaAsua/movimiento-armonico-investigacion/issues/9).** El [script reproducible](weaver_video_qr_factorial.py) genera cuatro MP4 sin pérdida de dos puntos de color, recupera trayectorias y PTS **desde los píxeles decodificados**, calcula `Q_xy` proyectado y concentración de fase `R`, y controla tres voces del renderer offline de Weaver/Shaper. Reutiliza sólo la ley de fase del [banco #26](https://github.com/SairaAsua/movimiento-armonico-investigacion/pull/26); las elipses y los cuatro MP4 se generan aquí. No hay cámaras, personas, soga, OSC ni audio físico.

El marcador izquierdo recorre un círculo de referencia; el derecho recorre una elipse de radios de imagen `(48,24)` o `(24,48)` píxeles, durante ocho vueltas en ocho segundos. Se cruza con la relación temporal `aligned/opposed` del banco previo. Intercambiar radios cambia la distribución de direcciones **en la imagen**, sin cambiar la longitud de la elipse continua; no es una reconstrucción 3D ni una categoría histórica de plano Laban. `Q_xy` es nuestra fórmula de recorrido ponderado por arco aplicada a las posiciones del marcador azul. `R=|promedio exp(iΔφ)|` se calcula con las fases recuperadas de ambos puntos; `R=1` puede ser fase cero o antifase estable y no significa consonancia estética.

```sh
python research/weaver_video_qr_factorial.py \
  --phase-repo /checkout/de/PR-26 \
  --weaver-repo /checkout/harmonic-weaver \
  --shaper-repo /checkout/harmonic-shaper \
  --output-dir /ruta/nueva/para/salidas
```

Requiere FFmpeg/FFprobe, NumPy, Pydantic y SoundFile. Cada video tiene 240 cuadros a 30 fps; cada WAV, ocho segundos estéreo a 48 kHz. No se suben MP4 ni WAV generados. El reporte local fija hashes de videos, audio, trazas, commits y entorno. El checkout de fase fue `80a47c1`, Weaver `cc5fb57` y Shaper `f8bfe07`; dos ejecuciones completas produjeron `report.json` idénticos byte por byte.

| Geometría / relación | `Q_xy` desde MP4 | `R` desde MP4 | Ganancias espaciales objetivo | Frecuencia temporal objetivo | RMS PCM |
|---|---|---:|---|---|---:|
| Eje x / aligned | 0,739796 / 0,260204 | 0,999942 | 0,791837 / 0,408163 | 439,526–440,474 Hz | 0,123245 |
| Eje x / opposed | 0,739796 / 0,260204 | 0,077713 | 0,791837 / 0,408163 | 367,938–512,062 Hz | 0,123427 |
| Eje y / aligned | 0,265137 / 0,734863 | 0,999927 | 0,412110 / 0,787890 | 439,605–440,395 Hz | 0,122838 |
| Eje y / opposed | 0,264893 / 0,735107 | 0,076296 | 0,411915 / 0,788085 | 368,439–511,561 Hz | 0,123215 |

Una referencia numérica de 10.000 tramos para la elipse continua da `Q=(0,739770,0,260230)` o su intercambio. El mayor error absoluto de `Q` observado desde el MP4 fue **0,004907** (condición eje y); la diferencia entre `Q` de `aligned/opposed` dentro de la misma geometría fue como máximo 0,000244. La concentración ideal de la ley temporal muestreada es `R=1` o `0,077246`; los valores recuperados se muestran arriba. El máximo error de ángulo de cualquiera de los puntos frente a la animación fue **1,193°**. Esto cuantifica el costo del muestreo y la rasterización en este fixture, no un error de cámara o de pose humana.

El mapeo sonoro es explícito y diagnóstico: voces fijas de 220 y 330 Hz reciben ganancia `0,2+0,8 Q_x` y `0,2+0,8 Q_y`; una tercera voz recibe ganancia 0,3 y frecuencia instantánea `440+20Δφ(t)` Hz. `Q` requiere toda la trayectoria de ocho segundos y por eso las dos ganancias espaciales son **replay retrospectivo**; la tercera voz usa la fase recuperada en cada PTS. Los controles se aplican en el primer bloque de Shaper que comienza después de ese PTS, con máximo observado de 192 muestras = 4 ms en reloj lógico. No es latencia de captura ni feedback en vivo. Los cuatro WAV tienen hashes distintos; su RMS parecido no demuestra sonoridad perceptiva igualada ni separación perfecta de capas acústicas. El [banco de Shaper con `Q/R` estáticos](WEAVER_LABAN_HIT_PCM_FACTORIAL.md) ya mostró una pequeña interacción entre componentes en el PCM final.

Este ensayo prueba que una medida espacial **proyectada** y una relación temporal pueden cruzarse en videos fabricados, recuperarse con error explícito y llegar al instrumento offline. No verifica si un gesto de danza real se etiqueta según Laban, si el movimiento de Nico tiene esa relación, si HIT mejora una predicción independiente, ni belleza, eficiencia o conciencia. Para el primer video humano hace falta permiso de uso, identidad y articulaciones revisadas contra una referencia independiente, PTS conservados y estados inválidos por señal; el [candidato público exploratorio](https://github.com/SairaAsua/movimiento-armonico-investigacion/pull/27) aún no tiene esas referencias y su licencia no reemplaza consentimiento de participación.
