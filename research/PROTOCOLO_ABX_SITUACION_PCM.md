# Preparación de una prueba ABX de situación espacial en audio sintético

**Estado:** paquete técnico reproducible; no se ha convocado a oyentes, recogido respuestas ni ensayado Beacon live. Este protocolo pertenece al banco offline de [ablación Shaper](ABLACION_SITUACION_PCM.md), no al piloto instrumental de rope flow con Nico.

## Pregunta y alcance

La primera pregunta es estrecha: **¿puede una persona distinguir, sin video ni etiquetas de origen, estos WAV sintéticos bajo una presentación controlada?** Aun una respuesta afirmativa sólo valdría para estos estímulos, este preset y este equipo de escucha. No diría que el oyente reconoce «centro/periferia», que el movimiento tiene una cualidad labaniana determinada, ni que Beacon transmite el gesto de Nico.

Se preparan tres contrastes de un mismo plano y fase: `rho_only` cambia únicamente la ganancia objetivo derivada de `rho_min`; `v_only` cambia la de `V_r`; `both` cambia ambas. Los híbridos son intervenciones en **controles sonoros**, no nuevas curvas. Todos los WAV ya fueron igualados en RMS global por el banco anterior. Esa igualdad no garantiza igual sonoridad percibida; por eso la prueba debe documentar auriculares/altavoces y nivel, y no interpretar la discriminación como lectura exclusiva de un armónico.

## Preparación local sin participantes

```sh
python3 research/preparar_abx_situacion.py \
  --input-dir /ruta/local/de/la/ablacion \
  --output-dir /ruta/local/nueva/abx \
  --seed SEMILLA_PRIVADA \
  --repetitions 8
```

El programa exige el `manifest.json` y los cuatro PCM24 originales, comprueba SHA-256, formato de 48 kHz/estéreo/1 s, alcance del fixture e igualdad RMS declarada. Crea `para_oyente/ensayos.csv`, copias de audio con nombres opacos y `LEER.txt`; `solo_coordinacion/clave.json` contiene la respuesta, contraste y semilla. **No distribuir la clave, el manifiesto original ni la carpeta fuente al oyente.** Las copias A/B/X de una misma fuente tienen contenido y hash idénticos por diseño: el cegamiento supone que el oyente usa la interfaz de reproducción, no que inspecciona bytes o código. Se debe preparar una carpeta de distribución separada que contenga sólo `para_oyente/`.

La plantilla por defecto produce **24 ensayos**: ocho por contraste, con A/B intercambiados cuatro veces y X asignada cuatro veces a cada respuesta. El orden se mezcla con una semilla guardada sólo en la clave. Son repeticiones de las **mismas cuatro muestras acústicas**; no equivalen a 24 gestos ni a 24 personas. El número es una preparación técnica, no un cálculo de potencia para un estudio humano. Antes de recoger respuestas habrá que decidir tamaño muestral, pausas, máximo de repeticiones, criterio de audición, volumen cómodo, aleatorización por persona y revisión ética aplicable. La tarea ABX pregunta «¿X coincide con A o con B?»; se registra la respuesta sin revelar el contraste. Evitar feedback de acierto durante la sesión.

Para el análisis eventual, informar aciertos e incertidumbre **por contraste y por oyente**, además de sesgo hacia A/B y omisiones. Un agregado de ensayos no debe tratarse como número de personas independientes. Conviene reservar participantes y nuevos pares acústicos para una evaluación confirmatoria si el piloto indica señal; ajustar el preset usando sus respuestas y volver a probarlo sobre los mismos WAV crearía una validación circular. Un resultado nulo puede significar mapeo no discriminable, presentación inadecuada o potencia insuficiente; no refuta la distinción geométrica anterior al sonido.

## Una segunda pregunta que ABX no contesta

**Atribución espacial** requiere otro diseño. Primero se fijaría qué alternativa espacial muestra un video autorizado y qué descriptor válido la distingue. Después se compararían etiquetas o emparejamientos sonido–video con distractores que compartan plano, fase, duración y nivel, sin que la imagen de entrenamiento revele las respuestas del test. Se mediría reconocimiento de esa relación, no sólo preferencia sonora. Un oyente puede superar ABX escuchando 550/660 Hz y seguir sin inferir el recorrido; también puede aprender una convención arbitraria sin que sea una propiedad biológica. Antes de llegar a Nico se necesitan procedencia de video, 3D y error válidos, y luego la salida efectivamente aplicada del instrumento Beacon si se hace una afirmación sobre Beacon.

## Comprobación técnica de este preparador

Con el banco fuente de la PR #22 y semilla **sólo de auditoría** `20261003`, dos ejecuciones independientes produjeron `ensayos.csv` y `clave.json` idénticos byte a byte. SHA-256: lista pública `75131e3000a04655dc91001fcc2274ae7131580fa094b3f15729b67c868f1c50`; clave local `6e9cbfe80786f13af47e053ca82790aa671142e1c5da9ac6ae5c12addb3a0940`. Se verificaron 24 filas, balance por condición/respuesta/orden A–B, ausencia de nombres de origen en la lista pública, hashes de las 72 copias WAV y rechazo de un archivo fuente alterado **antes** de crear salida. Estos son controles de preparación informática, no datos perceptivos.
