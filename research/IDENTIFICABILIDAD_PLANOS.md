# Cuándo una curva 3D define un plano, y cuándo no

Nota matemática original, 23-09-2026. Responde a la [lectura histórica del minueto](LABAN_MINUETO_PLANOS.md): los planos «puerta», «rueda» y «mesa» pueden inspirar una pregunta sobre **orientación de recorridos**, pero el algoritmo siguiente es nuestro. No representa una fórmula recuperada de Laban ni asigna valor estético o fisiológico. Requiere trayectorias 3D y marco corporal con error validado; una vista 2D siempre está en el plano de imagen y **no** prueba que el gesto real sea plano.

## Ajuste geométrico y ambigüedad

Para una ventana de puntos 3D `p₁,…,pₙ`, calcular el centro `μ` y la covarianza `C = (1/n) Σ(pᵢ−μ)(pᵢ−μ)ᵀ`. Sus autovalores ordenados `λ₁ ≥ λ₂ ≥ λ₃ ≥ 0` describen dispersión a lo largo de tres ejes ortogonales. La normal del plano de mínimos cuadrados es el autovector de `λ₃`; `sqrt(λ₃)` es el error perpendicular cuadrático medio **dentro de esa ventana**. El signo de la normal no identifica otro plano: comparar orientaciones con `arccos(|n₁·n₂|)`.

Esta fórmula da el mismo peso a cada **muestra**, no a cada tramo recorrido. Si Nico se detiene o se mueve despacio en una zona, esa zona aporta más cuadros y puede orientar la PCA de una frase no plana aunque el camino espacial sea igual. Para una pregunta geométrica pura, comparar con una curva remuestreada por distancia de arco; para una pregunta de **tiempo vivido en regiones**, conservar ponderación temporal. Esas dos salidas responden preguntas distintas y se nombrarán por separado. La visibilidad desigual de una zona puede sesgar ambas.

La condición `λ₃≈0` **no basta**. Una línea recta tiene `λ₂≈λ₃≈0`: contiene infinitos planos y la normal que devuelve un programa es arbitraria. Para llamar estimable a la orientación se necesita que la segunda extensión `sqrt(λ₂)` exceda claramente el error de posición 3D y que el segundo autovalor se separe del tercero. Si `λ₁≈λ₂≈λ₃`, la curva ocupa volumen y el «mejor plano» tiene mucho residuo; no convertirlo en una etiqueta cardinal. Los márgenes serán específicos del montaje y de la mínima diferencia angular de interés, no un umbral universal heredado de un artículo ajeno.

El [banco reproducible](planos_sinteticos.py) comprueba cuatro casos ideales con Python estándar:

| Curva construida | `λ₁, λ₂, λ₃` | Lección |
|---|---|---|
| Círculo en XY | `0,5; 0,5; 0` | Plano horizontal matemáticamente identificado, normal Z. |
| Círculo en XZ | `0,5; 0,5; 0` | Otro plano identificado; diferencia de normales **90°**. |
| Círculo XY trasladado e inclinado 37° | `0,5; 0,5; 0` | Conserva autovalores bajo movimiento rígido y devuelve **37°** frente al plano inicial; prueba la parte no diagonal del cálculo. |
| Línea exacta en X | `0,33331; 0; 0` | Residuo perpendicular cero pero orientación de plano **indeterminada**. |
| Curva con extensión en XYZ | `0,5; 0,5; 0,08` | El mejor plano tiene dispersión perpendicular `sqrt(0,08)=0,28284`; llamarlo plano requiere una tolerancia que aquí no se ha justificado. |

Dos líneas casi rectas con perturbación senoidal de amplitud `0,01` en Y o en Z producen ambas residuo plano cero y dispersión secundaria de apenas `0,00443`, pero sus normales calculadas difieren **90°**. Es un contraejemplo directo a «si el residuo es bajo, el giro de normal es una transición real». Son curvas fabricadas y unidades abstractas; no estiman el ruido de cámaras de Saira.

## Regla para una serie temporal de rope flow

1. Predefinir segmento (mano, punto de soga identificado o tronco), marco (sala o cuerpo), duración/posición de ventana y política para transiciones entre patrones **durante desarrollo**, antes de ver ratings. Fijar un mínimo de puntos observados y tramos de curva suficientes; no rellenar `held` como datos nuevos. El plano de la **forma de la soga en un instante** y el plano de la **trayectoria de un punto de soga durante una frase** son objetos diferentes.
2. Reportar `λ₁,λ₂,λ₃`, normal axial, `sqrt(λ₃)`, `sqrt(λ₂)`, longitud de trayectoria, cobertura, estado de visibilidad, error posicional y sensibilidad a otra ventana razonable. Una etiqueta cardinal sólo se considera si la orientación supera el error de captura y hay acuerdo con analistas donde corresponda.
3. Si la curva es lineal o su plano es volumétrico/inestable, usar estado científico `invalid` con razón `plane_undefined`. **No** asignar la dirección de la línea al plano: son objetos diferentes ([Longstaff 2001](LABAN_VECTOR_LONGSTAFF_2001.md)). Tampoco llamar «disonancia» a la falta de identificación instrumental.
4. Una transición entre planos requiere dos ventanas **válidas** y un tramo intermedio documentado. Una ventana que cruza dos figuras puede volverse no plana y luego saltar a otra normal; ese salto puede ser frontera de análisis, no cambio súbito del cuerpo. Comparar límites manuales, ventanas superpuestas y segmentación por tarea antes de contarlo.
5. Mantener esta orientación de plano separada de [`plane_alignment_A`](DICCIONARIO_SENALES_V0.md), que mide alineación direccional con planos predefinidos y puede dar valores altos en dos planos para una línea. La primera ajusta un plano a la curva; la segunda usa planos elegidos de antemano. Ninguna por sí sola representa el sentido histórico completo de «puerta/rueda/mesa».

Para validar con cámaras, mover una referencia conocida en XY y XZ en varias zonas del volumen y en velocidades que el montaje soporte; repetir tras desmontar/reinstalar. Medir error angular de la normal, tasa de `plane_undefined` y falsas transiciones inducidas por oclusión/ruido. Después, con sesiones consentidas, verificar los mismos límites por patrón, giro y vista. Si el caso real no supera esos controles, el primer paper conserva trayectorias o planos proyectados con su incertidumbre y excluye la etiqueta 3D del contraste con HIT/Beacon. Véase [piloto de video](PILOTO_VALIDACION_VIDEO.md).
