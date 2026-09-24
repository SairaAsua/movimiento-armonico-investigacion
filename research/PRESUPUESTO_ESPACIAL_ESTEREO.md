# Presupuesto espacial de dos cámaras para trayectorias de rope flow

Nota instrumental del 23 de septiembre de 2026. Complementa [la ambigüedad de una vista](IDENTIFICABILIDAD_2D_3D.md) y el [presupuesto temporal](PRESUPUESTO_ERROR_CAMARAS.md). **Son escenarios geométricos sintéticos, no precisión medida de las cámaras de Saira ni de HarMoCAP.** La meta es convertir «tengo cámaras» en requisitos verificables para la geometría de Laban: ¿puede el montaje resolver el cambio de dirección y profundidad del tramo que interesa?

## Relación y supuestos

Para dos cámaras pinhole paralelas y rectificadas, separadas por línea base `B` y con focal `f` en píxeles, la disparidad horizontal `d` de un mismo punto satisface `d=fB/Z`; por tanto `Z=fB/d`. [RealSense expone esta relación de disparidad/profundidad](https://www.realsenseai.com/stereo-depth/the-basics-of-stereo-depth-vision/) y su [herramienta de calidad](https://github.com/realsenseai/librealsense/blob/master/tools/depth-quality/readme.md) distingue exactitud, ruido espacial, cobertura y ruido temporal. La fórmula deriva de la geometría ideal y no requiere esa marca de cámara.

Linealizando para error pequeño de disparidad, `σ_Z≈Z²σ_d/(fB)`. Si ambos puntos de imagen tienen errores horizontales independientes con desviación `σ_px`, entonces `σ_d≈√2 σ_px`. Esta es una **derivación nuestra** bajo independencia. No captura sesgo de calibración, distorsión residual, emparejamiento erróneo, oclusión, desenfoque, latencia, rolling shutter ni movimiento distinto entre cuadros. La identidad corporal y la de la soga pueden perderse al cruzarse; en tal caso la triangulación matemática no rescata la correspondencia equivocada. Tampoco puede inferirse `σ_px` de la resolución nominal de video: hay que medir error real de puntos localizados en el volumen de interés.

Al aumentar `B` mejora la resolución de profundidad ideal, pero puede reducirse la zona visible simultáneamente y crecer la oclusión o dificultad de correspondencia. Un montaje con ópticas convergentes sigue siendo triangulable tras calibración; este cálculo rectificado sirve para ordenar escenarios, no para dictar la ubicación física final.

## El desfase puede crear profundidad falsa aun sin ruido de píxel

Para el mismo modelo ideal, imaginemos un punto a profundidad fija `Z` que avanza paralelo a la línea base a velocidad constante `v`. Si la cámara izquierda lo ve en `t` y la derecha en `t+δt`, pero el algoritmo trata ambas vistas como simultáneas, la disparidad observada pasa a `d=f(B−vδt)/Z`. Su profundidad errónea es `Ẑ=ZB/(B−vδt)` si `vδt<B`; cuando `vδt≥B`, este triangulador incluso rechaza la correspondencia por disparidad nula o negativa. La relación es una **derivación nuestra** y el signo depende de la dirección de movimiento/desfase. No modela aceleración, ópticas convergentes, obturador rodante ni otros errores.

El [banco determinista](estereo_sintetico.py) usa **sólo como ejemplo** `Z=3 m`, `v=2 m/s` y `δt=10 ms`, sin ruido de píxel: el sesgo de profundidad es `26,09 cm` con `B=0,25 m`, `8,22 cm` con `B=0,75 m` y `4,05 cm` con `B=1,50 m`. Un error temporal que parece pequeño frente al ciclo puede superar la diferencia espacial que se pretende asignar a un plano o dirección. No se sabe si Nico, la soga o alguna cámara presentan esos valores; la prueba física debe medir velocidad en imagen, desfase residual y error 3D **juntos** durante un movimiento representativo. Una línea base mayor reduce este sesgo ideal pero no se elige sólo por esta ecuación: cobertura y oclusiones también importan.

## Banco ejecutable

El [simulador estándar de Python](estereo_sintetico.py) genera dos observaciones ruidosas **sin desfase** por punto, reconstruye dos extremos de un tramo y compara dirección 3D. Usa semilla fija, 20.000 repeticiones, `f=1200 px`, `Z=3 m`, error gaussiano independiente de `1 px` por coordenada, y desplazamiento real de `0,15 m`. Son valores ilustrativos, **no las especificaciones del equipo**. La función de desfase anterior es un contraste determinista separado; la tabla siguiente sólo varía error de píxel. Salida verificada:

| Línea base | Disparidad a 3 m | `σ_Z` lineal | `σ_Z` simulada | Error angular p95 de tramo lateral | Error angular p95 de tramo en profundidad |
|---:|---:|---:|---:|---:|---:|
| 0,25 m | 100 px | 4,24 cm | 4,30 cm | 38,5° | 6,8° |
| 0,75 m | 300 px | 1,41 cm | 1,43 cm | 14,9° | 3,2° |
| 1,50 m | 600 px | 0,71 cm | 0,72 cm | 7,6° | 3,0° |

El error angular del tramo **lateral** es especialmente sensible a ruido en profundidad porque el vector verdadero tiene componente de profundidad cero y cualquier diferencia espuria inclina la dirección. En el tramo puramente en profundidad, el error angular puede ser pequeño aunque la **longitud** reconstruida tenga error: por ello esta tabla no es una prueba de que la magnitud del movimiento esté bien medida. El simulador verifica además que, sin ruido, la triangulación recupera exactamente un punto 3D dentro de tolerancia numérica. Simular ruido gaussiano independiente da un piso optimista, no un intervalo de confianza de una cámara real.

## Regla de decisión para el estudio de Laban

1. Inventariar modelo, resolución, lente, tasa real, exposición, obturador y disponibilidad de control manual; medir la zona de solapamiento del volumen donde se mueven manos, tronco y soga. No elegir `f` a partir de la ficha nominal si el video cambia de zoom o recorte.
2. Calibrar intrínsecos/extrínsecos y rectificar; comprobar después con **puntos y longitudes de referencia no usados para calibrar**, distribuidos por centro/bordes, profundidad y alturas. Registrar error de reproyección, error físico 3D, cobertura de correspondencias y diferencias por región; el primero por sí solo no certifica el segundo.
3. Capturar objetos/patrones que reproduzcan velocidad, cruces y oclusiones de rope flow. Estimar la incertidumbre real por punto, tramo y tipo de movimiento; incluir error temporal de [sincronización/exposición](PRESUPUESTO_ERROR_CAMARAS.md). Probar asimismo la estabilidad de ejes corporales durante giros.
4. Para cada descriptor previsto —dirección, situación central/periférica/transversal, plano, proximidad a red, orden de línea— comparar su **separación mínima de interés** con distribución de error, sesgo y cobertura medidos. Si dos direcciones o dos redes rivales quedan dentro de la incertidumbre, informar `indistinguible_con_este_montaje`; no bajar un umbral hasta obtener una preferencia.
5. Si sólo se dispone de una vista válida, o multivista falla en los patrones clave, conservar descriptores `*_proj` y preguntas 2D del [piloto](PROTOCOLO_PILOTO_V0.md). El cálculo estéreo no justifica declarar inválido todo el proyecto; acota qué conclusión espacial puede sostenerse.

La prueba espacial precede al ajuste de redes cuboctaédrica/icosaédrica. Una red con menor error geométrico que otra por pocos grados no es interpretable si el cambio de cámara, error de segmentación o incertidumbre de reconstrucción ya supera esa diferencia. La elección de montaje se cerrará con inventario y banco físico; hoy no hay datos para recomendar comprar un sensor o una separación exacta.
