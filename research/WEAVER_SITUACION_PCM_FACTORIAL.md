# Situación espacial audible en el PCM offline: banco sintético

**Ensayo de integración retrospectivo, 3 de octubre de 2026.** El [script reproducible](weaver_situacion_pcm_factorial.py) consume los [ocho casos `Q`–situación–`R`](https://github.com/SairaAsua/movimiento-armonico-investigacion/blob/research/path-situation-candidate/research/beacon_situacion_controles.py) de la PR #28 y entrega sus cinco ganancias numéricas a `PCMWriter` de Harmonic Weaver, que renderiza con Harmonic Shaper. **Este WAV no sale de `beacon-spatial`**: las bandas 4–8 de aquel contrato se representan aquí como cinco *voces Shaper* a frecuencias fijas 220, 330, 440, 550 y 660 Hz. El ensayo demuestra un recorrido de controles hasta PCM de un instrumento offline distinto, no la ruta OSC HarMoCAP→Beacon.

```sh
python research/weaver_situacion_pcm_factorial.py \
  --situation-repo /checkout/de/la-PR-28 \
  --weaver-repo /checkout/harmonic-weaver \
  --shaper-repo /checkout/harmonic-shaper \
  --output-dir /ruta/nueva/para/salidas
```

Requiere NumPy, SoundFile y dependencias de Weaver/Shaper. La salida **local nueva** contiene ocho WAV estéreo de 1 s a 48 kHz, trazas `voice-frames.jsonl` y un `report.json` con commits, hashes, ganancias, amplitudes FFT y RMS. No se suben aquí los WAV. Los descriptores se calculan con ocho ciclos completos y luego se fijan desde el comienzo del WAV de replay; no son señales disponibles durante el movimiento. No se usaron video, cámaras, soga, Nico, interfaz de audio, servicio ni OSC.

Para el par de círculos del plano lateral–anterior con fase `locked`, `Q=(0,5;0,5;0)` y `R=1` en ambos. Las primeras tres ganancias Shaper son `0,6 / 0,2 / 1,0` en ambos; las dos de situación cambian como sigue:

| Situación sintética | `rho_min` | `V_r` | Ganancias 550 / 660 Hz | Amplitud FFT 550 / 660 Hz en PCM | RMS |
|---|---:|---:|---:|---:|---:|
| Círculo alrededor del origen | `0,499998` | `0,001571` | `0,466666 / 0,201257` | `0,051809 / 0,022050` | `0,101259` |
| Mismo círculo desplazado | `0,199999` | `0,381974` | `0,333333 / 0,505579` | `0,036751 / 0,056081` | `0,104325` |

Los hashes de WAV son distintos. En los cuatro pares que conservan plano y fase, la diferencia absoluta en los bins de 550 Hz está entre `0,015058` y `0,015153`; en 660 Hz, entre `0,034030` y `0,034183`. Las otras tres voces **no son perfectamente independientes después de la mezcla**: en el par mostrado sus bins cambian `0,000116`, `0,000008` y `0,000208` aunque sus ganancias objetivo sean iguales. La síntesis y normalización del motor pueden producir esa interacción. Un WAV diferente y una diferencia FFT no prueban que una persona identifique la situación espacial: haría falta prueba a ciegas con nivel/sonoridad comparables y pares adversos.

La [propagación de error de la PR #28](https://github.com/SairaAsua/movimiento-armonico-investigacion/blob/research/path-situation-candidate/research/BEACON_SITUACION_INCERTIDUMBRE.md) limita incluso el paso anterior: bajo una cota hipotética de `0,01` unidades, los **controles numéricos** asignados a la voz de 550 Hz permanecen separados, pero la cota peor caso de `V_r` no garantiza separación de los controles de 660 Hz. Ni siquiera la separación garantizada de controles demuestra separación robusta del PCM tras la mezcla. Este render usa los valores nominales del fixture; **no** incorpora error, no valida 3D de una cámara y no corrige la incertidumbre con el sonido.

**Revisiones y verificación:** situación `512f96a`, Weaver `cc5fb57`, Shaper `f8bfe07`; identidad del motor `b8491a46e31134dcf49dde30613006a416023c404498f9641f63972778270889`. Dos ejecuciones completas produjeron el mismo SHA-256 de `report.json`, `23803d50d07243232b868d724646b989c6ced5ee4e3b2054594a5df627f17255`. El código comprueba ocho WAV distintos y que cada par de situación conserve exactamente sus tres primeras ganancias objetivo. El siguiente gate experimental es un video autorizado con reloj y calidad, seguida de prueba perceptiva; para afirmar audio Beacon hacen falta su adaptador OSC y salida aplicada del instrumento real.
