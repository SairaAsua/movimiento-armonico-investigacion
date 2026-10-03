# `W` en danza externa: cierre y sensibilidad al muestreo

**Banco humano externo de ingeniería, 3 de octubre de 2026.** Apliqué un cálculo diagnóstico al [C3D público CMU 05_02 ya auditado](CMU_DANZA_BANCO_REAL.md), que registra danza moderna con brazos expresivos y una pirueta. **No es rope flow, Nico, una vista de cámara de Saira ni una validación labaniana.** El [script reproducible](cmu_w_cierre_muestreo.py) comprueba el SHA-256 del archivo oficial antes de leerlo; los datos C3D siguen fuera de Git.

## Definición que se ejecutó

Se usó la media de `LWRA/LWRB` o `RWRA/RWRB` como proxy de muñeca, cintura como origen y ejes laterales/anterior estimados **por cuadro** desde hombros y torso. La escala es la mediana del ancho entre marcadores de hombros de toda la toma: análisis retrospectivo, no calibración causal. Se proyectó el recorrido co-rotante en 2D lateral–anterior. El residual del C3D marcó presentes los diez marcadores requeridos en los 1.123 cuadros; eso no certifica precisión anatómica ni ausencia de imputación previa.

Cada mano se dividió en nueve ventanas **fijas, no solapadas** de 1 s: cuadros `0–120`, `120–240`, …, `960–1080`, con ambos extremos incluidos (121 muestras por ventana). No son ciclos detectados de una tarea. Para cada ventana se registró distancia entre extremos, longitud del recorrido muestreado y una poligonal cerrada **por una cuerda recta no observada**. Se calculó su `W` con todos los cuadros a 120 Hz y tras tomar uno de cada cuatro u ocho cuadros, conservando los mismos extremos: grillas de 30 y 15 Hz **sin filtro antialias**. La vista, el marco y la cuerda agregada son parte de la definición; no se evaluó error de posición del C3D.

## Hallazgo descriptivo en esta toma

| Criterio exploratorio | Resultado | Lectura limitada |
|---|---:|---|
| Ventanas de una mano, un segundo | `18` | Nueve por lado; no son vueltas independientes de rope flow |
| Extremos a menos de `0,1` anchos de hombros | `3/18` | Umbral ilustrativo elegido para diagnosticar este banco, no preregistrado ni validado como «cierre» |
| `W` de cuerda recta cambia entre 120/30/15 Hz | `9/18` | Sensibilidad del descriptor **muestreado** al descarte de cuadros; no error frente a `W` físico conocido |
| Cambios de `W` entre las tres ventanas con extremos cercanos | `2/3` | La cercanía por sí sola no estabiliza la cifra bajo este procesamiento |

Las ventanas cercanas exponen los números: izquierda `120–240` tiene brecha `0,0442` anchos de hombros y `W=(2,1,0)` a 120/30/15 Hz; izquierda `240–360` tiene brecha `0,0222` y `W=(0,1,0)`; derecha `0–120` tiene brecha `0,0435` y `W=(0,0,0)`. Sus brechas son respectivamente `9,0 %`, `2,2 %` y `9,4 %` del largo de la polilínea a 120 Hz. Todos esos `W` incluyen el **mismo cierre recto artificial**. La sensibilidad restante puede venir del recorrido fino, del marco estimado o de procesamiento previo del C3D; este ensayo no separa esas fuentes ni identifica un «valor verdadero».

## Decisión para el estudio de Nico

El [contraejemplo ideal de tres cierres](W_CIERRE_APROXIMADO.md) ya demostró no identificación del trayecto físico faltante. La toma CMU añade una constatación práctica: aun fijando una cuerda recta y los extremos de cada ventana, el `W` numérico puede cambiar al espaciar cuadros. Por tanto `path_turning_number_proj` no entra en el conjunto primario de rope flow por entusiasmo ante un valor entero. Primero se necesita (a) definir una **frase/ciclo observado** independientemente de `W`, (b) predefinir vista, punto, marco y política de cierre, (c) medir error dinámico y cobertura de los originales por giro/oclusión, y (d) ensayar sensibilidad a tasa efectiva, fase de grilla y filtros sobre la misma frase. Se informarán también intentos donde `W` sea `unknown`. Si ninguna definición mantiene significado y estabilidad en días reservados, el resultado será de factibilidad negativa para ese descriptor.

Ninguna cifra de esta toma decide si el movimiento fue bello, fácil, eficiente o consonante con HIT. Un `W` estable en una ventana arbitraria tampoco sería una categoría histórica de Laban ni una señal lista para Beacon. Para audio, el [contrato temporal](W_GIRO_TIEMPO_BEACON.md) sigue exigiendo cierre válido y disponibilidad posterior.

**Reproducción:** colocar el [archivo oficial `05_02.c3d`](http://mocap.cs.cmu.edu/subjects/05/05_02.c3d) en `research/sources/cmu_mocap/`, fuera de Git, y ejecutar `uv run --no-project --with ezc3d==1.7.2 --with numpy==2.4.4 python research/cmu_w_cierre_muestreo.py`. Dos ejecuciones locales devolvieron JSON idéntico, SHA-256 `6a22e9b24903e9ab6de3514f79aeb82b4db0d1de35d07c758b7a5107a5290047`; `py_compile`, enlaces locales y `git diff --check` pasaron. La salida contiene sólo descriptores y resumen del archivo público, sin redistribuir posiciones de marcadores.
