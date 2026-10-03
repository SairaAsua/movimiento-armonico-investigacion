# Una misma línea de mano no identifica la participación del torso

Construcción cinemática sintética, 3 de octubre de 2026. Es un límite de inferencia para el piloto de rope flow: **no** representa un movimiento observado, una categoría Laban validada ni una transferencia de energía. Complementa la [matriz espacial](LABAN_MATRIZ.md), la [descomposición del marco móvil](MARCO_MOVIL_DESCOMPOSICION_C.md) y el [contraejemplo causal](CONTROLES_RITMO_COMUN.md).

## Dos realizaciones con los mismos recorridos

En un plano horizontal y unidades de longitud arbitrarias, sea el recorrido de una mano `w(t)=(cos t, sin t)` y su posición relativa a pelvis/tórax `b(t)=R(t)ᵀ[w(t)−p(t)]`, donde `p` es origen del torso y `R` su orientación. Para `0≤t≤2π`:

| Realización | Origen `p(t)` | Orientación `R(t)` | Mano en sala `w(t)` | Mano en torso `b(t)` |
|---|---|---|---|---|
| A: torso inmóvil | `(0,0)` | Identidad | `(cos t,sin t)` | `(cos t,sin t)` |
| B: torso móvil | `w(t)−R(t)w(t)` | Rotación horizontal de `θ(t)=0,15 sin(2t)` rad | `(cos t,sin t)` | `(cos t,sin t)` |

La igualdad en B es exacta: `Rᵀ[w−(w−Rw)]=w`. En `t=π/4`, `θ=0,15` rad y `||p_B||=2 sin(0,075)≈0,14986` unidades; A mantiene `p=0` y `θ=0`. La dirección, velocidad, figura y tiempo de la **mano** son idénticos en sala y en marco corporal en ambas realizaciones. Una clasificación del recorrido de mano calculada sólo desde cualquiera de esas dos trazas dará lo mismo. Sin embargo, la trayectoria y orientación del torso difieren. El ejemplo usa una compensación construida; no afirma que una persona deba ejecutarla ni que ambos casos cuesten igual.

Más generalmente, para cualesquiera `w(t)` y `b(t)` compatibles, cada orientación elegida `R(t)` admite `p(t)=w(t)−R(t)b(t)`. Por ello, **ni conocer ambas trayectorias de mano determina por sí solo la contribución del torso**. Conservar `p(t)` y `R(t)` medidos rompe esta ambigüedad cinemática; no identifica todavía fuerzas internas, trabajo mecánico ni dirección causal. La pose debe tener visibilidad y precisión suficientes para el tamaño del contraste, especialmente si la diferencia de torso es pequeña.

## Decisión para el estudio

1. Definir por separado la *situación de la línea* respecto de una kinesfera y marco declarados, `path_situation`, y la *participación torso–extremidad*, por ejemplo desplazamiento y giro de torso durante la misma frase. La distinción espacial entre orientación y situación tiene apoyo en el [mecanoscrito «Tanz und Musik»](LABAN_TANZ_UND_MUSIK_MANUSCRITO.md) y en la [lectura de Longstaff](LABAN_VECTOR_LONGSTAFF_2001.md); las dos realizaciones y sus fórmulas son nuestras, no de Laban.
2. Guardar la ruta de mano en sala, la ruta co-rotante, el origen y orientación del torso, los relojes y la incertidumbre de cada uno. No sustituir torso no observado por un valor derivado de la mano, porque la igualdad construida muestra que no hay identificación única.
3. Si sólo son fiables las manos, informar geometría y ritmo de mano con ese alcance; dejar participación del torso y `core_initiated` sin estimar. Si el torso es fiable, puede estudiarse covariación o demora temporal, pero el [contraejemplo de causa común](CONTROLES_RITMO_COMUN.md) sigue impidiendo inferir de ellas transferencia causal de energía.
4. Para Beacon, una capa de trayectoria puede sonar igual en A y B: sólo una señal corporal adicional, cuya calidad se haya verificado, podría distinguirlos. El sonido generado no prueba por sí mismo que uno sea más bello, eficiente o «correcto».

La identidad se puede comprobar sustituyendo las funciones en la definición de `b`; no requiere datos humanos ni elegir un umbral de «armonía». Para aplicar esta decisión al piloto faltan cámaras calibradas, medición de torso y revisión de las categorías espaciales con especialistas.
