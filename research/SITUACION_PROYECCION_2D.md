# La misma pose 2D puede ocultar dos situaciones 3D

Este [contraejemplo ejecutable](situacion_proyeccion_ambigua.py) particulariza para `rho_min` y `V_r` la [ambigüedad monocular general](IDENTIFICABILIDAD_2D_3D.md). Es **geometría sintética** de la [issue #4](https://github.com/SairaAsua/movimiento-armonico-investigacion/issues/4), no una prueba con HarMoCAP, cámaras o Nico. Su alcance es una secuencia de **coordenadas de pose 2D**: otras pistas de los píxeles podrían ayudar a estimar profundidad, pero también exigirían validación externa.

Usamos una cámara pinhole ideal con proyección normalizada `(u,v)=(X/Z,Y/Z)`. El origen corporal está fijo en `c=(0,0,2)` y tiene la misma imagen `(0,0)` en ambos mundos. La mano aparece en los mismos tres puntos `(u,v)=(-0,5;0),(0;0),(0,5;0)`:

| Mundo | Mano 3D para cada `u` | Recorrido relativo a `c` | `Q` | `rho_min`, con alcance fijo `a=2` | `V_r` |
|---|---|---|---|---:|---:|
| A | `(2u,0,2)` | `(-1,0,0) → (0,0,0) → (1,0,0)` | `(1,0,0)` | `0` | `1` |
| B | `(3u,0,3)` | `(-1,5;0;1) → (0;0;1) → (1,5;0;1)` | `(1,0,0)` | `0,5` | `0,535184` |

Las imágenes de mano y origen, el orden de cuadros y el tiempo pueden ser idénticos. `Q` también es idéntico porque ambas trayectorias relativas son líneas paralelas al eje X. Sin embargo, en A la mano pasa por el centro corporal y en B queda a una unidad de profundidad; `rho_min` y `V_r` difieren. El script calcula esos valores y falla si alguna igualdad construida deja de cumplirse. Los otros puntos del cuerpo pueden mantenerse iguales en ambos mundos: **las coordenadas 2D de la mano y del centro no seleccionan la profundidad de la mano**.

Esto no establece un error de `0,5` para ningún detector. Muestra una **no identificabilidad** incluso con keypoints 2D perfectos y reloj perfecto. Por ello un `rho_min_proj` en píxeles o imagen normalizada puede ser útil para describir lo visible, pero no se convierte por su nombre en el `rho_min` 3D de [situación](LABAN_SITUACION_RECORRIDO.md). Para informar situación 3D hacen falta reconstrucción multivista o una restricción física explícita y error contrastado en el volumen y movimiento de interés. Una red monocular con prior puede producir una estimación 3D; el prior y su error para rope flow deberán declararse y probarse por separado.

Para la futura ruta HarMoCAP–Weaver–Beacon, el [sobre de situación](CONTRATO_SITUACION_V0.md) exige origen, escala, 3D y calidad válidos. Si sólo hay HarMoCAP 2D, la capa espacial podrá usar un descriptor **proyectado y nombrado como tal**, con otro contrato y otro contraste perceptivo, sin adjudicarle la distinción central/periférica 3D. Una diferencia audible entre mundos estimados no resolvería por sí sola la ambigüedad visual: el sonido repetiría el prior o la decisión del mapeo, no una medición independiente.
