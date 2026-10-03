# Fase recuperada de video sintético → PCM offline Weaver/Shaper

**Banco de integración, 2 de octubre de 2026.** Esta prueba enlaza el [banco de video y fase del PR #26](https://github.com/SairaAsua/movimiento-armonico-investigacion/pull/26) con el renderer offline de [Weaver `cc5fb57`](https://github.com/AlterMundi/harmonic-weaver/tree/cc5fb57df815a2657eb06cbaa94fa8ad64d6ad2f) y [Shaper `f8bfe07`](https://github.com/AlterMundi/harmonic-shaper/tree/f8bfe07017d17da1d71e5370c437dd929d9dc997). Los MP4 son **marcadores sintéticos**, no personas ni soga. El [script reproducible](weaver_video_fase_pcm.py) los lee desde el checkout de PR #26, verifica hash de archivo y de píxeles decodificados contra su manifest, recupera fase de los dos puntos desde píxeles y PTS, y alimenta `PCMWriter` cuadro por cuadro. No inicia cámara, audio físico, servicio ni OSC.

El par `aligned/opposed` conserva las distribuciones individuales de rapidez por construcción, pero cambia cómo se emparejan temporalmente los dos marcadores. El [banco origen](https://github.com/SairaAsua/movimiento-armonico-investigacion/blob/research/video-misma-curva-ritmo/research/video_fase_audio_diagnostico.py) informa `R_cont=1,0000` frente a `0,0769`; usar sólo cierres de vuelta daría `R_eventos=1` en ambos. Aquí **no** se sonifica el `R` retrospectivo de ocho segundos: cada cuadro aporta su diferencia de fase recuperada `Δφ(t)` y controla una sola voz mediante `f(t)=220+20Δφ(t)` Hz, con ganancia 0,5 y timbre/pan fijos. Esto es una asignación diagnóstica arbitraria, no una frecuencia medida en el cuerpo ni una ecuación de Laban o HIT.

```sh
python research/weaver_video_fase_pcm.py \
  --video-repo /checkout/de/PR-26 \
  --weaver-repo /checkout/harmonic-weaver \
  --shaper-repo /checkout/harmonic-shaper \
  --output-dir /ruta/nueva/para/salidas
```

Requiere FFmpeg/FFprobe, NumPy, Pydantic y SoundFile. Produce tres WAV estéreo float de ocho segundos a 48 kHz, sus registros `voice-frames.jsonl` y un `report.json` local con commits, hashes de videos y motor, rangos de control, RMS y retardo **lógico**. La tercera salida repite `opposed`, pero declara **inválidos artificialmente** los cuadros 90–119 y envía `targets=[]` con `release_s=0`; no pretende que el video presente una oclusión real. Las salidas no se suben al repositorio.

| Replay | Frecuencia objetivo desde píxeles | RMS lineal PCM | Máximo retardo control→bloque | SHA-256 WAV |
|---|---:|---:|---:|---|
| Aligned | 220,000–220,000 Hz | 0,195188954 | 192 muestras = 4 ms | `4afaad3561b76adf8a4ac25d1d9f1b1d0415606a2d2ec04aacb54e57a2ac3e5d` |
| Opposed | 148,096–291,904 Hz | 0,195188395 | 192 muestras = 4 ms | `1371663c0bc53c1ceea94e5a9692c378c78f513a18efaca586ce4ef485ffa56c` |
| Opposed + invalidez inyectada | 148,096–291,904 Hz fuera del tramo | 0,182561220 | 192 muestras = 4 ms | `e439ce7476ab62859d32b09fdbd392c2670056198a97850659cfb66013ac9c73` |

Cada WAV contiene 384.000 muestras por canal. El control se aplica al **primer bloque de 256 muestras cuyo inicio no antecede su PTS**; el máximo observado fue 192 muestras, menor que el límite configurado de 256 muestras (5,33 ms). Es cuantización del renderer, **no** latencia cámara→oído. Los 240 índices de control aparecen en la traza de voces de cada salida. En el caso inválido, la señal es exactamente cero entre las muestras 144.128 y 191.999, equivalente a 3,002667–4,000000 s; el comienzo se demora al siguiente bloque. Hay señal antes y después. El PCM de `aligned` y `opposed` tiene RMS casi idéntico, pero eso no iguala sonoridad percibida ni garantiza discriminación auditiva.

Se ejecutó el script dos veces con `report.json` **idénticos byte por byte**, `py_compile` y `git diff --check`. El checkout de video era `80a47c1`, el de Weaver `cc5fb57` y el de Shaper `f8bfe07`; código del motor `b8491a46e31134dcf49dde30613006a416023c404498f9641f63972778270889` y entorno `0aa5106f842e3e935ac61f7153536e6bbc938707e3e26b3cf61a42fe2e415214`.

## Frontera de inferencia

Este ensayo ya recorre **píxeles sintéticos + PTS → fase calculada → controles Shaper → WAV y traza**. No usa el tracking de HarMoCAP ni el router live de Weaver, no usa `beacon-spatial`, no mide sincronía física entre cámaras y no contiene una persona. El ejemplo de invalidez verifica la respuesta a una bandera externa construida; queda por demostrar que una oclusión real se detecta y marca correctamente. Tampoco evalúa escucha humana, belleza, eficiencia o estados de conciencia.

Para un video de baile autorizado, el siguiente gate es congelar original, PTS, calidad por señal y mapeo antes de escuchar; comparar controles espaciales, temporales y relacionales sobre **el mismo soporte válido**, y revisar el WAV junto al video con evaluadores independientes. Para Nico, además hay que observar soga y manos por separado, medir error y cobertura, y resolver la procedencia de fase y el reloj. La ruta live HarMoCAP→Weaver→Beacon conserva [una issue propia de tiempo e identidad](https://github.com/AlterMundi/harmonic-weaver/issues/77); este replay offline no la cierra.

Un [factorial posterior en MP4 fabricados](WEAVER_VIDEO_QR_FACTORIAL.md) añade `Q_xy` proyectado y cruza geometría de imagen con fase antes del render Shaper. Sigue siendo un banco sin personas.

Un [replay adicional del mismo MP4 bajo dos transformaciones](WEAVER_VIDEO_PROYECCION_PCM.md) prueba que el renderer offline puede hacer audible el sesgo de un plano oblicuo: la diferencia de control nace antes de Shaper, al calcular fase de imagen cruda o rectificada con un factor sintético conocido.
