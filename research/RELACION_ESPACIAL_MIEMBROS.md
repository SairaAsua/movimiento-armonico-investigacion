# Relación espacial entre miembros: lo que `Q` y la fase no conservan

**Banco matemático, 03-10-2026.** La [lectura de *Choreographie*, pp. 3–12](LABAN_FORMA_CONTRAMOVIMIENTO_1926.md) motiva observar las rutas de elementos corporales **entre sí** y no sólo sus trazas individuales. El [script reproducible](relacion_espacial_miembros_sintetica.py), con Python estándar, formaliza una pérdida de información. Sus curvas y unidades son ideales: no contienen movimiento de Nico, soga, biomecánica, belleza ni una fórmula histórica de Laban.

## Dos construcciones con resúmenes idénticos

Durante una vuelta `0≤t≤1`, con `θ=2πt`, separación basal `d=1` y altura `h=0,5`, definimos:

`L(t)=(cosθ−d/2, sinθ, h sin2θ)`;

`R_par(t)=(cosθ+d/2, sinθ, h sin2θ)`;

`R_opp(t)=(cosθ+d/2, sinθ, −h sin2θ)`.

La mano izquierda es exactamente la misma en ambas condiciones. La derecha recorre una curva reflejada respecto del plano `z=0`: conserva longitud de arco, **serie completa de rapidez**, distribución radial en `z²` y cada componente de `Q` ponderado por arco, porque `Q` eleva al cuadrado las componentes tangentes. Sus proyecciones `x–y` también son idénticas. La fase de cada órbita `x–y` respecto de su **centro conocido** es `θ`; por ello `R₁:₁=1` y el ángulo medio de fase es `0` en ambos casos. En este fixture la fase se conoce por construcción; no se valida un estimador de video.

Sin embargo, la distancia entre manos es `D_par(t)=d`, frente a `D_opp(t)=√(d²+4h² sin²2θ)`. El script verifica `Q=(0,343184; 0,343184; 0,313633)` por mano y condición, y que el rango de distancia cambia de `1,000000–1,000000` a `1,000000–1,414214` en unidades arbitrarias. Una cámara que sólo observa `x–y` no distingue estas construcciones. **Ni siquiera `Q` + `R` + ángulo medio + rapidez individual las distinguen.** Un modelo que conserva posiciones 3D **firmadas** de ambas manos sí puede hacerlo; la pérdida pertenece a esos resúmenes, no a todo análisis cinemático.

## Descriptor candidato, referencia y gate

Para dos puntos corporales **nombrados** `p_i(t),p_j(t)` en el mismo marco y reloj, guardar primero el vector relativo firmado `Δp_ij(t)=p_j(t)−p_i(t)` y su calidad. La distancia `D_ij(t)=||Δp_ij(t)||` es un resumen invariante a traslación y giro rígidos, útil para esta pregunta pero incapaz de decir si una mano pasó arriba o abajo de la otra. Por ello la componente vertical firmada, la relación con el frente corporal y el orden de eventos son resultados separados. Una serie completa puede resumirse por frase con media, rango o duración bajo un umbral **predefinido según la tarea**; no inventar un umbral «armónico» después de ver ratings.

Si la validación entrega cotas euclidianas duras `ε_i,ε_j` en cada punto simultáneo, la desigualdad triangular da `|D̂_ij−D_ij|≤ε_i+ε_j`. Para comparar dos condiciones independientes con las mismas cotas, el error de su diferencia puede llegar a `2(ε_i+ε_j)`, antes de sumar desincronización o errores de reconstrucción que no estén incluidos en esas cotas. Un margen menor no se declara resuelto. Si sólo hay desviaciones estándar, usar propagación/cobertura empírica, no reemplazar esas cotas por un percentil sin decirlo. No se interpolan oclusiones como observaciones; una mano sin identidad fiable invalida el par.

La referencia instrumental mínima es una distancia **conocida y dinámica** entre marcadores/objetos dentro del volumen y la velocidad del gesto, además de acuerdo de anotadores cuando se pregunta por una categoría histórica. Una regla estática sola no verifica error durante cruce o giro. En el repertorio de Nico habrá que escoger si el par pertinente es mano–mano, mano–torso, brazo–pierna u otro tras observar tareas y consultar a especialista Laban; este fixture no demuestra que un patrón real sea «contramovimiento» de Laban. Con soga, `mano–soga` requiere además identidad de tramo y seguimiento independiente.

El [factorial Laban–HIT existente](LABAN_HIT_FACTORIAL.md) cambia relación temporal con marginales individuales igualados. Este banco cubre otra dirección: relación **espacial** distinta aun con igual fase conocida. En el contraste predictivo, `Δp` sería un candidato espacial de `base + Laban inspirado`, mientras fase entra como rasgo temporal separado. Ambos se prueban sobre las mismas unidades y contra un resultado independiente; si una base ya contiene ambas posiciones 3D, añadir su diferencia determinista no agrega información observacional por sí solo. Para Beacon, `D` o `Δp` sólo puede emitirse con las dos fuentes válidas, sincronizadas y con latencia conocida; el color del sonido no probará eficiencia ni estado de conciencia.
