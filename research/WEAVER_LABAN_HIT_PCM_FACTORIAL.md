# Q espacial × R temporal: replay sintético en Shaper

**Banco de integración offline, 2 de octubre de 2026.** Vinculado a la [issue de investigación #9](https://github.com/SairaAsua/movimiento-armonico-investigacion/issues/9) y al [control PCM básico](WEAVER_PCM_CONTROL_SINTETICO.md). Usa el [factorial matemático existente](LABAN_HIT_FACTORIAL.md), no video, soga, grabaciones humanas ni señales fisiológicas. El [script reproducible](weaver_laban_hit_pcm_factorial.py) calcula `Q` y `R` de las curvas idealizadas y entrega controles a `PCMWriter` de [Weaver `cc5fb57`](https://github.com/AlterMundi/harmonic-weaver/tree/cc5fb57df815a2657eb06cbaa94fa8ad64d6ad2f), que llama `AudioEngine.render_block` de [Shaper `f8bfe07`](https://github.com/AlterMundi/harmonic-shaper/tree/f8bfe07017d17da1d71e5370c437dd929d9dc997). No inicia servicio ni dispositivo de audio y no ejercita `beacon-spatial`.

Los descriptores se calculan con el **bloque completo de ocho segundos** y se representan después en un WAV estático de un segundo por caso. Por tanto es un replay retrospectivo, nunca una medición o respuesta causal durante el movimiento. `Q=(Q_lateral,Q_anterior,Q_vertical)` distribuye el recorrido por eje según una fórmula **del proyecto inspirada en Laban**, no una ecuación histórica. `R` es la longitud media de fase relativa; `R=1` también admitiría una antifase constante, por lo que esta magnitud aislada no mide consonancia ni conserva el ángulo medio.

El mapeo sonoro diagnóstico, fijado antes del render, es:

| Capa | Voz Shaper | Ganancia objetivo |
|---|---:|---|
| Recorrido anterior | 220 Hz | `0,2 + 0,8 Q_anterior` |
| Recorrido vertical | 330 Hz | `0,2 + 0,8 Q_vertical` |
| Concentración de fase | 440 Hz | `0,2 + 0,8 R` |

Las tres voces permanecen activas en las cuatro condiciones; fase inicial, panorama, timbre, master, duración y frecuencias portadoras son iguales. Así se comprueba la traducción de controles sin atribuir una frecuencia física al cuerpo. **Estas voces son un instrumento Shaper, no las bandas 4–6 de `beacon-spatial`** del [otro banco de controles](BEACON_FACTORIAL_CONTROLES.md).

```sh
python research/weaver_laban_hit_pcm_factorial.py \
  --weaver-repo /ruta/al/checkout/harmonic-weaver \
  --shaper-repo /ruta/al/checkout/harmonic-shaper \
  --output-dir /ruta/nueva/para/salidas
```

Requiere NumPy, Pydantic y SoundFile; la salida local nueva contiene cuatro WAV estéreo float de 48.000 cuadros a 48 kHz, trazas `voice-frames.jsonl` y `report.json` con commits y hashes de motor/entorno. Se ejecutó dos veces con reportes byte por byte idénticos, además de `py_compile` y `git diff --check`. En el entorno fijado: `engine_code_sha256=b8491a46e31134dcf49dde30613006a416023c404498f9641f63972778270889`, `engine_environment_sha256=0aa5106f842e3e935ac61f7153536e6bbc938707e3e26b3cf61a42fe2e415214`.

| Plano / tiempo | `Q` | `R` | Ganancias 220 / 330 / 440 | Amplitud FFT de los mismos bins en el PCM final | RMS lineal |
|---|---|---:|---|---|---:|
| Lateral–anterior / locked | 0,5 / 0,5 / 0 | 1,0000 | 0,6 / 0,2 / 1,0 | 0,110165 / 0,036219 / 0,184825 | 0,154007 |
| Lateral–anterior / drift | 0,5 / 0,5 / 0 | 0,4720 | 0,6 / 0,2 / 0,5776 | 0,111608 / 0,036855 / 0,107412 | 0,112375 |
| Lateral–vertical / locked | 0,5 / 0 / 0,5 | 1,0000 | 0,2 / 0,6 / 1,0 | 0,036008 / 0,109820 / 0,184748 | 0,153785 |
| Lateral–vertical / drift | 0,5 / 0 / 0,5 | 0,4720 | 0,2 / 0,6 / 0,5776 | 0,036730 / 0,111403 / 0,107328 | 0,112189 |

La FFT usa la media estéreo de los últimos 0,5 s para evitar el ataque inicial. Los cuatro hashes WAV son distintos. Si se cambia `locked→drift`, las **ganancias objetivo espaciales quedan iguales** y cae la componente de 440 Hz; si se cambia el plano, la ganancia objetivo temporal queda igual y se intercambian las componentes de 220/330 Hz. En la mezcla **no hay independencia perfecta**: con plano fijo, cambiar sólo el objetivo de 440 Hz modificó las amplitudes FFT de 220 y 330 Hz entre 1,3 % y 2,0 %. Con tiempo fijo, cambiar el plano alteró la amplitud de 440 Hz entre 0,04 % y 0,08 %. El motor mezcla, normaliza y limita la señal; una separación en los controles no garantiza separación exacta de las componentes del WAV. El RMS también cambia mucho al cambiar `R`, de modo que una prueba perceptiva posterior tendría que controlar nivel y sonoridad además de timbre.

## Qué permite y qué no permite concluir

El banco verifica que el factorial matemático puede alimentar **el motor offline real de Shaper** mediante Weaver y deja cuantificada una interacción de la síntesis que el mapeo numérico por sí solo no mostraba. No identifica `Q` o `R` desde video, no prueba que Nico pueda ejecutar estas cuatro condiciones, no valida una ruta live HarMoCAP→Weaver→Beacon y no evalúa percepción, belleza, costo energético, placer ni conciencia. Las otras dos [pruebas de video sintético a audio](https://github.com/SairaAsua/movimiento-armonico-investigacion/pull/26) y de [soga 2D a audio](https://github.com/SairaAsua/movimiento-armonico-investigacion/pull/25) usan síntesis propia; no deben confundirse con esta prueba de Shaper.

El [puente siguiente ya usa fase recuperada de video sintético y sus PTS](WEAVER_VIDEO_FASE_PCM.md), incluyendo un reset con invalidez inyectada. Aún falta una serie espacial y temporal de video **humano autorizado** con calidad medida; sólo después, con mediciones confiables, correspondería ensayar el caso de rope flow de Nico.
