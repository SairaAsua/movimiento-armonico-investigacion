# Una línea aparente puede esconder un arco entre cuadros

**Nota matemática del equipo, 03-10-2026; Issue [#4](https://github.com/SairaAsua/movimiento-armonico-investigacion/issues/4).** Aplica al descriptor exploratorio `path_line_residual_h` de un episodio de rope flow. No es una ecuación de Laban ni un resultado medido en Nico. La [lectura mediada de *Choreographie*](https://github.com/SairaAsua/movimiento-armonico-investigacion/blob/7e3bc98/research/LABAN_VOLUTAS_1926.md) motivó conservar el recorrido interior además de la dirección entre extremos; esta nota estudia qué se puede inferir de cuadros discretos.

Sea `p(t)` una trayectoria 3D continua en un **mismo marco** durante `[t₀,t_N]`, con ambos extremos realmente observados. `C` es el segmento que une sus extremos físicos. Definimos `h=max_t dist(p(t),C)`. Los cuadros reconstruidos `p̂_j` definen `Ĉ` y `ĥ=max_j dist(p̂_j,Ĉ)`. Si el error euclidiano de cada punto reconstruido tiene **cota dura** `ε_j`, entonces `e=max_j ε_j+max(ε₀,ε_N)` cubre tanto los puntos como la cuerda: la distancia de Hausdorff entre `C` y `Ĉ` no supera el mayor error de sus extremos. Por tanto `h≥max(0,ĥ−e)`. Esta cota inferior permite detectar un arco visto, pero no afirmar que el resto de la frase fue recto.

## Dos cotas alternativas para el tramo invisible

Si una referencia independiente justifica `||ṗ(t)||≤V` en todos los huecos físicos y `Δ=max_j(t_{j+1}−t_j)`, todo instante está a distancia temporal `≤Δ/2` de un cuadro. La distancia espacial a ese cuadro no supera `VΔ/2`, luego `h≤ĥ+e+VΔ/2`. **La velocidad media entre cuadros no es `V`**: puede ser cero aunque ocurra una excursión y retorno en el hueco.

Hay una segunda opción bajo otro supuesto, a veces más informativo: si `p` es dos veces diferenciable en cada intervalo y una referencia independiente garantiza `||p̈(t)||≤A_j`, la distancia entre `p(t)` y la **interpolación lineal física** de los dos extremos vecinos no excede `A_j(t−t_j)(t_{j+1}−t)/2≤A_jΔ_j²/8`. La distancia a un conjunto convexo, como la cuerda global `C`, no aumenta al interpolar dos puntos más allá del máximo de sus distancias a `C`. En consecuencia:

`max(0,ĥ−e) ≤ h ≤ ĥ+e+max_j(A_jΔ_j²/8)`.

Si ambas cotas dinámicas son defendibles en los mismos intervalos, usar la menor de `VΔ/2` y `max_j(A_jΔ_j²/8)` como término de hueco. Una aceleración estimada por segunda diferencia de **esos mismos cuadros** no certifica `A_j`: puede perder el pico oculto y amplifica el error de posición. Los timestamps deben ser tiempos de exposición física, no FPS nominal ni hora de recepción; error de reloj, reconstrucción multivista y cambio de marco entran en `e` o invalidan el supuesto. Un giro corporal en un marco móvil requiere que la cota de derivadas se establezca **en ese marco**, incluida su rotación. Un golpe, oclusión o cambio de identidad sin cota física deja el intervalo sin límite superior defendible.

## Contraejemplo exacto y decisión

En un único intervalo `0≤t≤Δ`, la curva recta `p₁(t)=(t,0)` y la curva `p₂(t)=(t,(A/2)t(Δ−t))` dan **los mismos dos cuadros extremos**. La segunda tiene `||p̈₂||=A` y se aparta de la cuerda `AΔ²/8` en el centro: la cota de aceleración es alcanzable. Con `A=16` unidades/s² y `Δ=0,5` s, los dos videos de extremos darían `ĥ=0`, pero uno puede tener `h=0,5` unidades. Los valores son inventados y no representan cámaras, manos ni soga reales.

Una tolerancia instrumental `τ` se fija antes de abrir las sesiones reservadas. `ĥ−e>τ` **rechaza** que una sola línea aproxime toda la frase. `ĥ+e+B<τ`, con `B` una de las cotas de hueco válidas, la hace **compatible bajo esos supuestos**. Si los intervalos se superponen con `τ`, falta un extremo, no se validó `e` o no existe `B`, declarar `indeterminate`. Compatibilidad con una línea no identifica una inclinación histórica de Laban, una técnica de soga, belleza ni eficiencia. El resumen final es retrospectivo: su `available_at` ocurre después del último cuadro y de las verificaciones.
