# Sincronía multivista: de eventos comunes a fase confiable

Nota instrumental del 23-09-2026. Saira informó aproximadamente 4 Reolink, 4 «logicam» y 1 Moto G; [modelos y propiedades temporales siguen pendientes](CAMARAS_PREPARACION.md) y no se anotaron eventos reales. El [paquete de captura](PAQUETE_CAPTURA_NICO_V0.md) exige eventos visibles en cada original para relacionar sus relojes. Esta nota fija el primer ajuste y, sobre todo, **lo que ese ajuste no prueba**.

## Evidencia técnica directa

[Šmíd y Matas (2019), *Rolling Shutter Camera Synchronization with Sub-millisecond Accuracy*](https://cmp.felk.cvut.cz/~matas/papers/smid-2019-rolling_shutter_sync-1902.11084.pdf), usan destellos compartidos, timestamps de cuadros y, para cámaras con obturador rodante, la **fila** donde aparece el borde del destello. Ajustan una transformación con desfase y deriva entre cámaras. En cuatro videos de un partido de hockey, reportaron una desviación temporal de aproximadamente 0,3–0,5 ms para eventos compartidos en ese montaje (abstract y secciones 3–5). **Ese rendimiento no se traslada** a las cámaras ni a las anotaciones manuales de este piloto. Su método subcuadro requiere destello que afecte gran parte de la escena, obturador rodante, borde de fila detectable y modelo del barrido; un clic sobre «el cuadro del flash» no lo implementa.

[OpenCap](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1011462) sincroniza sus videos mediante correlación de velocidades de puntos corporales antes de triangular. Es una opción de ingeniería para sus tareas validadas; durante rope flow una señal periódica puede alinearse con un desplazamiento de **un ciclo completo** y producir un pico plausible. Por eso nuestro banco técnico prefiere eventos comunes no periódicos y revisa la alineación con marcas independientes. La [documentación de ffprobe](https://ffmpeg.org/ffprobe.html) respalda extraer secciones de cuadros y timestamps, pero un PTS es tiempo de presentación del medio; no demuestra por sí mismo el instante físico de exposición.

## Modelo inicial y registro

Elegir una cámara de referencia y marcar **el mismo evento identificado** en cada vista. No emparejar simplemente «flash 1, flash 2» si alguno puede faltar; asignar `event_id` estable y revisar visualmente. Guardar `camera_id`, `event_id`, `pts_s`, cuadro/fila usada, criterio de borde, incertidumbre de marcación y versión de anotación en un CSV **privado**. Al menos tres pares distribuidos en la toma permiten ajustar un modelo y comprobar residuos; más eventos distribuidos permiten detectar mejor discontinuidades.

Para una cámara `c`, el ajuste propuesto es `t_ref = a_c + b_c (t_c − t0_c)`. `a_c` es tiempo de referencia en el origen elegido; `b_c−1` cuantifica deriva relativa por segundo. La transformación vale sólo dentro del intervalo cubierto por eventos y con ajustes de cámara estables. El [script de ajuste](ajustar_relojes.py) lee un CSV reducido a `event_id,camera_id,pts_s`, empareja por ID, exige que los PTS de eventos emparejados **crezcan estrictamente en ambas vistas**, ajusta mínimos cuadrados y reporta residuales de ajuste y de exclusión de un evento a la vez. Un evento invertido o dos eventos con el mismo PTS requieren revisar el original y la anotación; no se «corrigen» invirtiendo un reloj. El script **no** detecta flashes, no usa filas ni incertidumbre de clic, no elimina atípicos y no ofrece precisión subcuadro. Un residual cero con tres clics cuantizados no significa error físico cero.

Ejemplo de entrada sin personas:

```csv
event_id,camera_id,pts_s
e0,referencia,0.400000
e0,lateral,0.000000
e1,referencia,10.402000
e1,lateral,10.000000
e2,referencia,20.404000
e2,lateral,20.000000
```

Uso: `python3 ajustar_relojes.py eventos.csv --reference referencia`. La salida JSON da `origin_pts_s`, `reference_at_origin_s`, `slope_reference_per_camera_second` y `relative_drift_ppm`, además de residuos por evento. La secuencia de tres filas del ejemplo basta sólo para demostrar el formato; se recomienda más cobertura de tiempo y eventos intermedios para el banco real.

## Interpretación de los residuos

- **Residual de ajuste** bajo: eventos compatibles con una línea. No mide error de exposición, error común a todas las cámaras, ni sesgo de anotar siempre el mismo borde equivocado.
- **Residual al retirar un evento** alto: ese evento es difícil de predecir desde los otros; puede ser clic errado, cuadro omitido, PTS irregular o cambio real de reloj. Revisar el original; no borrarlo automáticamente para embellecer el ajuste.
- **Residual que cambia con tiempo:** posible deriva no lineal o salto. Detener inferencia multivista en ese segmento o emplear otro modelo **validado** con más eventos; no extrapolar el ajuste lineal fuera del rango de flashes.
- **Pocos eventos o marca de cuadro solamente:** el límite de cuantización sigue vigente. A 30 fps uniformes, medio cuadro equivale a ~16,7 ms por evento; a 2 ciclos/s implica ~12° de fase **antes** de sumar errores de dos señales y del giro/oclusión. Véase [presupuesto temporal](PRESUPUESTO_ERROR_CAMARAS.md).

La aceptación se decide por la **menor diferencia de fase o posición** que el estudio quiera resolver. Si se pretende contraste de fase p:q, propagar error de ambos relojes/eventos y coeficientes p, q; si se pretende 3D, comprobar además desplazamiento espacial causado por el residual a la velocidad de imagen real. Cuando no se alcanza resolución suficiente, usar sólo análisis por vista o eventos de ciclo gruesos. Ninguna buena sincronía corrige un punto anatómico mal identificado o una soga invisible.

El [ejemplo estéreo con un punto móvil](PRESUPUESTO_ESPACIAL_ESTEREO.md) convierte ese segundo requisito en una comprobación: incluso con píxeles ideales, `10 ms` de desfase pueden producir varios centímetros de profundidad falsa según velocidad y línea base. En el banco físico, evaluar un objeto de trayectoria y dimensiones conocidas en todo el volumen; repetir a velocidades representativas, con eventos de sincronía al principio, medio y final. Medir error 3D y cobertura **por velocidad y región**, no aceptar el par de cámaras sólo porque el ajuste de flashes tenga residuales pequeños. PTS correctos no garantizan el instante de exposición ni corrigen automáticamente rolling shutter.

## Comprobación reproducible del script

Se creó un CSV sintético con cinco eventos donde `t_ref=0,4+1,0002·t_c`. El script recuperó `b=1,0002`, `200 ppm` y residuales numéricamente nulos. Al introducir una discordancia de 20 ms en el evento central, el máximo residual de ajuste fue 16 ms y el máximo al dejar uno fuera fue 20 ms. La revisión 0.2 rechazó además un evento invertido en la cámara y dos eventos con el mismo PTS en la referencia. Estas pruebas verifican álgebra y controles del archivo, **no** precisión temporal de cámaras ni validez de la anotación de destellos.
