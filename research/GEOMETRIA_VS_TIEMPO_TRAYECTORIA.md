# La misma línea, otro ritmo: separar geometría de tiempo

Nota matemática del 23 de septiembre de 2026. Ningún dato humano fue usado. Una frase de rope flow tiene al menos dos objetos: **la curva recorrida** y **la ley temporal con que se recorre**. Laban motiva estudiar líneas, planos y secuencias espaciales; HIT propone contrastes temporales propios. Si una medida espacial se calcula como promedio de cuadros, incorpora también el tiempo que Nico permanece en cada zona, y puede confundirse con cadencia o pausa.

## Dos promedios legítimos, preguntas diferentes

Para una curva `x(t)` y un descriptor local `g(x)` —por ejemplo distancia angular a una dirección de referencia—, el promedio por **tiempo** es `G_t = (1/T) ∫₀ᵀ g(x(t)) dt`. Pesa más los lugares donde el ejecutante permanece más tiempo. El promedio por **longitud de recorrido** es `G_s = (1/L) ∫₀ᴸ g(x(s)) ds`, con `L=∫₀ᵀ ||ẋ(t)||dt`; pesa cada tramo según distancia recorrida. Si `x` recorre la misma línea en el mismo sentido, pero con distinta velocidad positiva, `G_s` permanece igual mientras `G_t` puede cambiar. Esta igualdad presupone el **mismo recorrido observado y el mismo marco**, no sólo extremos iguales ni una deformación de la curva por el movimiento real.

Para una secuencia coreútica, el **orden** de tramos también importa: un histograma `G_s` igual no asegura el mismo orden de direcciones. Guardar la serie ordenada y sus transiciones, además de los promedios. Para HIT y experiencia, conservar por separado duración, pausas, aceleración, eventos de ciclo y fases; parametrizar todo por longitud de arco borraría justamente el ritmo que queremos contrastar.

## Contraejemplo exacto sin personas

Sean dos ejecuciones de la misma circunferencia de radio uno, de igual duración `0≤t≤1`:

- `A(t)=(cos(2πt), sin(2πt))`.
- `B(t)=(cos(2πq(t)), sin(2πq(t)))`, `q(t)=t+0,8t(1−t)`.

La derivada `q'(t)=1,8−1,6t` es positiva en todo el intervalo, así que B sigue **el mismo camino, en el mismo sentido y una vuelta completa**. Ambas dedican exactamente la mitad de la **longitud de arco** a la semicircunferencia con parámetro `q≤0,5`. A dedica el 50 % del **tiempo** a ella; B sólo `(1,8−√1,64)/1,6 ≈ 0,3246`, porque la atraviesa más rápido al comienzo. El [script de comprobación](geometria_tiempo_sintetica.py) verifica ambas proporciones con Python estándar. No es una estimación del efecto esperado en Nico.

El antecedente empírico de [Orlandi, Cross y Orgs (2020)](https://eprints.gla.ac.uk/227924/) manipuló el tiempo de frases de danza con recorridos aproximadamente conservados y encontró diferencias de valoración estética. No demostró que cualquier reparametrización de una curva tenga ese efecto, ni que la curva fuese geométricamente idéntica; sirve para impedir que tratemos geometría y velocidad como sinónimos.

## Misma curva y misma duración tampoco fijan la dinámica

Para una curva regular `r(s)` parametrizada por longitud de arco en un marco **inercial**, recorrida según `s(t)`, la velocidad es `v=ṡ T` y la aceleración es `a=s̈ T+κ(s)ṡ² N`, donde `T` es tangente unitario, `N` normal y `κ` curvatura. Como `T·N=0`, `||a||²=s̈²+κ²ṡ⁴`. Esta identidad cinemática es una derivación del proyecto, **no** una fórmula de Laban ni una medida de esfuerzo, trabajo o metabolismo. Muestra que forma de recorrido y ley temporal interactúan incluso cuando la dirección y el largo del camino son idénticos. Con marco corporal que gira habría que añadir los términos de transporte descritos en el [contraste de marcos](REDES_CONTRASTE_GEOMETRICO.md).

Contraejemplo exacto, sin personas: en la circunferencia unitaria, `r(t)=(cos θ(t), sin θ(t))`, comparar `θ_A(t)=2πt` con `θ_B(t)=2πt+ε sin(2πt)` para `0≤t≤1` y `ε=1/2`. Ambas trazan **la misma vuelta, en el mismo sentido y en 1 segundo**, pues `θ̇_B=2π[1+ε cos(2πt)]>0`. Cualquier descriptor puramente geométrico ponderado por longitud de arco coincide. Sin embargo, la integral de aceleración al cuadrado en B dividida por la de A es `1+(7/2)ε²+(3/8)ε⁴=1,8984375`. Una integración numérica con 200 000 puntos medios confirmó la expresión a precisión de máquina el 24-09-2026. Esta integral tiene unidades dependientes de escala/duración y **no es energía**: aceleración puede ser centrípeta sin trabajo positivo instantáneo, y el cuerpo completo y la soga añaden otros grados de libertad. El ejemplo sólo refuta la inferencia «misma forma espacial ⇒ misma demanda dinámica».

La decisión para el piloto es registrar, además del recorrido por longitud, el **perfil temporal dentro del ciclo**: rapidez por fase de tarea, pausas/inversiones, variación de período y, sólo con referencia dinámica suficiente, aceleración/curvatura con incertidumbre. Al comparar un descriptor Laban con belleza o costo, el modelo base debe distinguir forma de velocidad, y el análisis de HIT debe aportar organización temporal **más allá** de estos controles. Aceleración numérica obtenida al diferenciar pose ruidosa no se llamará demanda física validada.

## Decisión de medición para Nico

1. **Espacio:** para dirección, plano y cercanía a una red, publicar al menos una versión por longitud de trayectoria cuando el recorrido 3D sea válido. Declarar si se ponderan puntos, segmentos o aristas y en qué marco corporal/sala. La versión por tiempo puede ser resultado diferente, con nombre explícito.
2. **Tiempo:** informar velocidad, cadencia, pausas, duración de segmentos y fase en el reloj real. No normalizar cada frase a un ciclo unitario antes de medir las diferencias temporales que interesan a HIT.
3. **Comparación:** si una medida espacial por cuadros predice belleza, verificar si sobrevive al usar `G_s` y al controlar ritmo/duración. Si desaparece, la señal predictiva podría estar en el **tiempo de permanencia**, no en la forma espacial. También puede ocurrir lo contrario: la forma puede aportar aunque el ritmo cambie.
4. **Validez:** `L` se sobreestima con ruido de pose y el vector tangente es inestable cuando el desplazamiento se aproxima al error de cámara. Elegir filtrado, segmentos válidos, tratamiento de pausas y error por tarea durante factibilidad; no densificar artificialmente zonas ocluidas con interpolación y contarlas como recorrido observado.
5. **Transiciones:** curvas abiertas, reversas y cambios de patrón se segmentan con reglas previas. Una reversa puede visitar dos veces la misma línea; una variable de ocupación espacial y una de secuencia/sentido deben conservarlo.

Estas son operacionalizaciones matemáticas nuestras, no fórmulas históricas atribuidas a Laban. Se conectan con [matemática Laban](LABAN_MATEMATICA.md), [contraste de redes](REDES_CONTRASTE_GEOMETRICO.md), [hipótesis de contraste estructurado](CONTRASTE_ESTRUCTURADO.md) y [estimandos](ESTIMANDOS_Y_CONTRASTES.md).

Para seleccionar **pares reales** que intenten aproximar el contraejemplo ideal «misma curva, otro ritmo», usar la [regla prospectiva de comparabilidad geométrica](EQUIVALENCIA_GEOMETRICA_MOTIVO.md): mismo motivo y orden de frase, trayectoria espacial con error acotado, margen práctico fijado antes de resultados externos y estado indeterminado cuando no se pueda demostrar semejanza suficiente. Compartir nombre de figura o `Q` no satisface esa regla.
