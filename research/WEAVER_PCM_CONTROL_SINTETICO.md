# Control sintético del audio offline de Weaver/Shaper

**Alcance y fecha:** banco de software del 2 de octubre de 2026, para la [issue de contrato temporal #9](https://github.com/SairaAsua/movimiento-armonico-investigacion/issues/9). No se usaron cámara, video, persona, servicio, dispositivo de audio ni datos de rope flow. La salida es un WAV local producido por el renderer offline de Weaver con el motor de bloques de Shaper; no recorre el OSC de `beacon-spatial`.

Se fijaron [Weaver `cc5fb57`](https://github.com/AlterMundi/harmonic-weaver/tree/cc5fb57df815a2657eb06cbaa94fa8ad64d6ad2f) y [Shaper `f8bfe07`](https://github.com/AlterMundi/harmonic-shaper/tree/f8bfe07017d17da1d71e5370c437dd929d9dc997). El [script reproducible](weaver_pcm_control_sintetico.py) utiliza `PCMWriter` y `AudioEngine.render_block` directamente. Exige NumPy, Pydantic y SoundFile; los checkouts se pasan de modo explícito. Crea cuatro WAV estéreo float, de 4.800 muestras por canal a 48 kHz (0,1 s): silencio, voz de 220 Hz, repetición idéntica y voz de 330 Hz. Entre las dos voces activas sólo varía `frequency_hz`; ganancia, fase, panorama, timbre, master y tiempos se mantienen iguales. El script compara los hashes del WAV y del registro de voces, la ausencia de señal en el control vacío y el pico FFT de cada tono.

```sh
python research/weaver_pcm_control_sintetico.py \
  --weaver-repo /ruta/al/checkout/harmonic-weaver \
  --shaper-repo /ruta/al/checkout/harmonic-shaper \
  --output-dir /ruta/nueva/para/salidas
```

El directorio de salida debe ser nuevo. El script escribe WAV, `voice-frames.jsonl` y `report.json` localmente; esos archivos no se incorporan al repositorio. El reporte congela commits y hashes del código y entorno de síntesis. En la ejecución documentada se usaron Python 3.12, NumPy 2.4.4 y SoundFile 0.14.0; `engine_code_sha256=b8491a46e31134dcf49dde30613006a416023c404498f9641f63972778270889` y `engine_environment_sha256=0aa5106f842e3e935ac61f7153536e6bbc938707e3e26b3cf61a42fe2e415214`.

| Control | Pico FFT | RMS lineal | SHA-256 del WAV |
|---|---:|---:|---|
| Sin voz | — | 0 | `12b407365cdda9ec8fa23477c6849eb9f50bc50a5cef99a270f850f07d56acba` |
| 220 Hz | 220 Hz | 0,191800 | `3b17202dc1f209e1b6957679161d404248fcc88945a49b725cda74bead6ac0cf` |
| 220 Hz repetido | 220 Hz | 0,191800 | `3b17202dc1f209e1b6957679161d404248fcc88945a49b725cda74bead6ac0cf` |
| 330 Hz | 330 Hz | 0,191794 | `052bbaef33c64cced10e80c8baa4b803e268a68f6e91fd8f58f4dac3cbe03ea1` |

La repetición produjo también el mismo hash de `voice-frames.jsonl`; el cambio de frecuencia produjo otro WAV y otro registro. Esto comprueba que **un control de frecuencia explícito llega al PCM y es reproducible en el entorno fijado**. El RMS casi igual entre tonos muestra además que un WAV distinto no implica por sí solo más intensidad ni una cualidad estética. El pico FFT coincide porque el tono se inyectó directamente: no es una frecuencia descubierta en el cuerpo.

## Frontera científica y siguiente prueba

Este control **no** demuestra que una característica de Laban o HIT se pueda inferir de video, que una fase corporal module correctamente el sonido, que una persona perciba la diferencia en contexto ni que una variación acústica mida belleza, eficiencia, placer o conciencia. Tampoco prueba la ruta live de Beacon. Confirma solamente el último tramo de una futura cadena de sonificación offline.

La próxima comparación defendible requiere una señal de movimiento con unidades, reloj, cobertura y estado de validez; un mapeo sonido congelado antes de mirar los juicios; y controles que cambien **sólo geometría**, **sólo ritmo** o **sólo relación entre señales**, conservando el mismo soporte temporal. En particular, una pérdida de muñeca o soga debe generar estado inválido en la entrada y una política sonora declarada, no un cero interpretado como quietud. Luego se pueden guardar WAV y registros junto con el video autorizado y pedir juicios independientes; primero habría que verificar sincronía y error del material físico.
