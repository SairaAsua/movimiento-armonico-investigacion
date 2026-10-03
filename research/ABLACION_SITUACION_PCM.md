# Dos capas de situación, ensayadas por separado en audio offline

El [par de escucha anterior](PAR_SITUACION_PCM_NIVEL.md) cambia a la vez `rho_min` y `V_r`; por eso oírlo no indicaría qué capa produjo la diferencia. El [script de ablación](weaver_situacion_ablacion_pcm.py) cruza, como **contrafácticos de controles**, los dos valores de ganancia de cada medida tomados del [factorial sintético original](WEAVER_SITUACION_PCM_FACTORIAL.md). Mantiene las tres ganancias `Q/R` constantes y renderiza cuatro WAV con Weaver `PCMWriter` + Shaper, seguidos de una atenuación PCM24 al mismo RMS global. No ejecuta `beacon-spatial`, video, cámara ni participantes.

```sh
python research/weaver_situacion_ablacion_pcm.py \
  --input-dir /ruta/local/del/factorial \
  --weaver-repo /checkout/harmonic-weaver \
  --shaper-repo /checkout/harmonic-shaper \
  --output-dir /ruta/local/nueva/para/salidas
```

La entrada se verifica por hash y por identidad de código/entorno del motor. `A` es la ganancia del círculo centrado y `B` la del desplazado. **`rhoB_vA` y `rhoA_vB` no representan una curva observada ni necesariamente una combinación geométrica realizable**; sirven para intervenir sólo un control a la vez.

| Estímulo | Ganancia 550 Hz (`rho_min`) | Ganancia 660 Hz (`V_r`) | FFT final 550 Hz | FFT final 660 Hz |
|---|---:|---:|---:|---:|
| `rhoA_vA` | `0,466666` | `0,201257` | `0,050188` | `0,021360` |
| `rhoB_vA` | `0,333333` | `0,201257` | `0,036956` | `0,022140` |
| `rhoA_vB` | `0,466666` | `0,505579` | `0,047151` | `0,051190` |
| `rhoB_vB` | `0,333333` | `0,505579` | `0,034555` | `0,052730` |

La comparación `rhoA_vA → rhoB_vA` cambia **sólo el objetivo de control** de 550 Hz y deja una diferencia FFT de `0,013232` allí, frente a `0,000779` en 660 Hz. La comparación `rhoA_vA → rhoA_vB` cambia **sólo el objetivo** de 660 Hz y deja una diferencia FFT de `0,029830` allí, frente a `0,003037` en 550 Hz. En ambos pares también cambian algo los bins 220/330/440 Hz tras síntesis y normalización RMS; no son canales acústicos matemáticamente ortogonales. Los cuatro RMS finales están entre `0,098091108` y `0,098091112`.

Esto verifica en un instrumento offline que los dos controles **pueden producir contrastes espectrales dominantes distintos** bajo el preset fijado. No prueba que un oyente pueda separarlos ni que el sonido indique de manera inequívoca una situación espacial. Una prueba ciega deberá usar ambos pares aislados y el par doble, equilibrar el orden, registrar equipo/nivel y preguntar por detección antes de pedir atribución espacial. El control cruzado impide atribuir al `rho_min` lo que se oyó por `V_r` en el par original.

**Reproducibilidad:** situación fuente `512f96a`, Weaver `cc5fb57`, Shaper `f8bfe07`; cuatro WAV PCM24 y `manifest.json` fueron idénticos byte a byte en dos ejecuciones independientes. SHA-256 del manifiesto: `e5615994b4b8fb7cbf852d01bc668cd0534645fc7bc6ecd9637c73e23b703d1b`. Los WAV se guardan sólo como artefactos locales. Sus controles derivan de ocho ciclos completos, de modo que son replay retrospectivo, no feedback causal ni medición de Nico. La [incertidumbre espacial previa](https://github.com/SairaAsua/movimiento-armonico-investigacion/blob/research/path-situation-candidate/research/BEACON_SITUACION_INCERTIDUMBRE.md) sigue limitando qué ganancias de una futura medición podrían considerarse separadas antes del audio.
