# Cuándo un cruce de polilínea 2D resiste el error de posición

**Derivación y banco sintético del 3 de octubre de 2026.** El [par de recorridos con igual `Q`](Q_CRUCES_ORDEN.md) distingue secuencia y autocruce, pero un cruce contado en coordenadas estimadas no tiene por sí mismo certeza geométrica. Esta nota trata **aristas rectas de una trayectoria puntual proyectada en 2D**. No identifica la curva de la soga en un instante, su paso delante–detrás, ni el recorrido continuo entre cuadros. La condición siguiente es una fórmula de esta investigación, no de Laban.

## Cota para la orientación de tres puntos

Sea `O(a,b,c)=det(b−a,c−a)` la orientación firmada en una vista 2D. Supongamos que cada posición verdadera `a,b,c` está a distancia euclidiana a lo sumo `ε` de su posición observada `â,b̂,ĉ`, **en el mismo marco y unidad**. Si `u=b̂−â` y `v=ĉ−â`, la perturbación de cada vector tiene norma máxima `2ε`. Por bilinealidad del determinante y `|det(x,y)|≤||x||||y||`, obtenemos la cota conservadora

`|O(a,b,c)−O(â,b̂,ĉ)| ≤ 2ε(||u||+||v||)+4ε² = B(â,b̂,ĉ;ε)`. **(C1)**

Por tanto, el signo de una orientación observada sólo queda **certificado** si `|O(â,b̂,ĉ)|>B`. La igualdad o un margen menor da signo `unknown`. `ε` debe ser una **cota dura simultánea** que incluya el error pertinente de detección, anotación, calibración/proyección y elección temporal de los vértices. Un RMSE, desviación estándar o intervalo del 95 % no ofrece esta garantía determinista.

## Certificado de cruce propio

Dos segmentos no adyacentes `ab` y `cd` tienen un cruce propio de sus **interiores** si `O(a,b,c)` y `O(a,b,d)` tienen signos opuestos, y también `O(c,d,a)` y `O(c,d,b)`. Si los cuatro signos están certificados y cumplen ambas oposiciones, el cruce de esas aristas permanece bajo cualquier perturbación permitida. Si dos signos certificados respecto de una misma arista son iguales, el par **no** puede tener un cruce propio bajo esa perturbación. En los demás casos, el estado es `unknown`; el criterio no decide contactos, colinealidad, segmentos de longitud cero ni superposiciones. Para declarar simple toda una polilínea cerrada hay que certificar ausencia en **cada par** no adyacente, no sólo en uno.

El [script ejecutable](cruce_trayectoria_incertidumbre.py) aplica `ε=0,05` unidades **inventadas** a los dos recorridos anteriores. Certifica que la trayectoria simple no tiene cruces propios entre los pares de aristas `0–2` y `1–3`, y que la cruzada conserva el cruce `0–2` mientras `1–3` permanece sin cruce. En otro caso, el segmento horizontal `(0,0)→(2,0)` y el vertical `(1,−0,01)→(1,0,01)` se cruzan en el dibujo observado. Si ambos extremos del vertical se trasladan `0,02` unidades hacia arriba —compatible con `ε=0,02`—, dejan de cruzarse. El certificado devuelve `unknown` para el dibujo observado con esa cota. Dos ejecuciones produjeron el mismo JSON (SHA-256 `b4f11f34191149c36abfd556d62c41c58135d51d404fe68912a2c0952bd761ea`). Estos valores no son precisión medida de las cámaras de Saira.

## Frontera temporal y uso futuro

El certificado sólo cubre la **polilínea formada al unir muestras observadas**. Dos trayectorias continuas pueden pasar por lugares distintos entre los mismos cuadros; incluso un certificado de polilínea no prueba un evento real ocurrido en la soga. Para investigar rope flow se deberán definir por separado `hand_path_projected_crossing`, `rope_projected_simultaneous_crossing` y, sólo con referencia de profundidad adecuada, `rope_3d_over_under`. La [nota de identificabilidad de soga](SOGA_IDENTIFICABILIDAD.md) explica por qué no son intercambiables.

En el piloto, el error `ε` y la validez de cada vértice deberán estimarse con referencias independientes por vista, velocidad, oclusión y giro. Las ventanas `unknown` entran en el denominador de cobertura, no se interpolan para mejorar la tasa de cruces. Un evento de cruce sólo podría alimentar el contraste HIT o una capa audible de Beacon después de medir su error temporal, falsos positivos/negativos y dependencia del muestreo en datos reservados. El criterio algebraico aquí prueba una **estabilidad condicional**, no que la soga de Nico se cruce ni que ese cruce sea bello, eficiente o perceptible en audio.
