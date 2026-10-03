# Par sintético de situación con nivel de escucha igualado

El [factorial Shaper de situación](WEAVER_SITUACION_PCM_FACTORIAL.md) produjo dos WAV para el mismo `Q`, fase, plano, duración y preset, con distinta posición del círculo respecto del origen. Sus RMS originales eran `0,101258592` y `0,104324992`: un oyente podría distinguirlos por nivel, sin reconocer la diferencia espacial codificada. El [preparador reproducible](preparar_par_situacion_pcm.py) atenua sólo el más fuerte hasta el RMS del más débil, sin tocar frecuencia de portadoras, fase, ecualización o duración.

```sh
python research/preparar_par_situacion_pcm.py \
  --input-dir /ruta/local/del/factorial \
  --output-dir /ruta/local/nueva/para/el/par
```

Lee y verifica los hashes WAV del `report.json` del factorial; rechaza formato, dimensiones o samples no finitos inesperados. Emite `A.wav` y `B.wav` estéreo PCM de 24 bits, 48 kHz, 1 s, y `manifest.json` con procedencia, escala aplicada, nivel y hashes. El manifiesto revela que **A es el círculo centrado y B el desplazado**: el coordinador de un futuro test ciego debe ocultarlo a participantes y generar un orden de presentación independiente. No se publica el par como resultado perceptivo humano.

| Estímulo | Factor lineal | RMS final | Amplitud FFT final a 550 Hz | Amplitud FFT final a 660 Hz |
|---|---:|---:|---:|---:|
| A, centrado | `1` | `0,1012585921` | `0,0518086143` | `0,0220501460` |
| B, desplazado | `0,970607229` | `0,1012585915` | `0,0356704891` | `0,0544322245` |

La diferencia residual entre los dos RMS es menor que `10⁻⁹`; las diferencias de amplitud FFT en los bins de situación siguen siendo `0,016138125` y `0,032382078`. Una lectura diagnóstica con `ffmpeg`/`ebur128` dio `−17,6 LUFS` para ambos, **redondeado a 0,1 LUFS en clips de sólo un segundo**. Igualar RMS y coincidir a esa precisión de LUFS reduce un atajo obvio de nivel; no iguala todos los aspectos de sonoridad percibida, timbre, ataque o altavoces. A/B diferentes tampoco demuestra que la diferencia se identifique como «central/periférica».

Además, este par **cambia simultáneamente** las ganancias derivadas de `rho_min` y `V_r`. La [ablación factorial de controles](ABLACION_SITUACION_PCM.md) genera pares separados para saber cuál capa produce cada contraste acústico; sus híbridos no son nuevas observaciones del movimiento.

En el primer intento se escribió WAV float: libsndfile insertó un chunk `PEAK` con timestamp variable, por lo que los archivos tenían samples idénticos pero hashes distintos entre corridas. La exportación final PCM de **24 bits** elimina ese metadato variable; dos corridas sobre los dos renders fuente byte a byte idénticos produjeron WAV y manifiestos idénticos. SHA-256 del manifiesto: `fe6b77558675b1e732573d9ec53f22d1f5ed976528f0fded9334e2ad1f72aea4`. Los WAV permanecen sólo en el archivo local de ensayo; se puede regenerarlos con los commits y controles declarados.

**Para la prueba humana posterior:** presentar A/B/X en orden equilibrado y aleatorio, con X una copia exacta de A o B por ensayo; ocultar etiquetas y resultados; incluir repeticiones idénticas, comprobar audición/equipo y analizar sensibilidad por persona sin tratar ensayos como participantes independientes. Separar dos preguntas: «¿son distintos?» y «¿qué relación del movimiento representa la diferencia?». Mostrar el video sólo en una condición posterior definida de antemano: si se muestra al mismo tiempo, la imagen puede revelar la respuesta. Un resultado sobre este par sintético no valida medición de rope flow ni una categoría de Laban.
