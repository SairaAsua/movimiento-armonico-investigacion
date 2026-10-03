# Una ganancia «HIT» que sólo identifica la cámara

**Banco geométrico sintético de la [Issue #7](https://github.com/SairaAsua/movimiento-armonico-investigacion/issues/7).** [Script ejecutable](hit_proyeccion_q_fase_sintetico.py). No representa una grabación de Nico, un estimador validado de soga ni una prueba de la teoría HIT. Hace concreta una posibilidad señalada por el [modelo algebraico de error compartido](https://github.com/SairaAsua/movimiento-armonico-investigacion/blob/a2e79ae/research/HIT_MEJORA_POR_ERROR_COMPARTIDO.md): una señal temporal del mismo video puede ayudar a **corregir geometría mal observada**, sin aportar organización corporal temporal al resultado.

## Cuatro estados y una proyección compartida

Supongamos dos gestos igualmente frecuentes: la trayectoria espacial verdadera de una mano es `x=cos θ, y=r sin θ`, con semieje `r∈{1,2}`. Independientemente, una cámara ortográfica inclinada comprime la coordenada vertical por `c∈{0,5;1}`: observa `x'=x, y'=cy`. El resultado externo construido `Y` es el `Q_y` **verdadero**, calculado por longitud de arco. El descriptor espacial disponible `X` es `Q_y` de la **curva proyectada**. No se atribuye esta geometría a un signo histórico de Laban; `Q` es nuestra propuesta.

Una segunda señal de referencia ejecuta una vuelta circular uniforme `x_ref=cos θ, y_ref=sin θ`, sincronizada exactamente con un reloj de tarea **independiente de la imagen** en los cuatro estados. La cámara observa `α=atan2(c sin θ,cos θ)`. Calculamos `H=|promedio exp(i[α−θ])|`: concentración de fase **aparente** entre la referencia proyectada y ese reloj. La relación física verdadera es idéntica (`R=1`) en los cuatro estados; sólo cambia la distorsión óptica. Este `H` es un ejemplo de descriptor temporal contaminado, no el futuro estimador mano–soga. Si el reloj también se infiriese del mismo `α`, este contraejemplo particular no funcionaría como está escrito.

| `r` real | `c` cámara | `X=Q_y` proyectado | `H=R` aparente | `Y=Q_y` verdadero |
|---:|---:|---:|---:|---:|
| 1 | 0,5 | 0,260230 | 0,971615 | 0,500000 |
| 1 | 1 | 0,500000 | 1,000000 | 0,500000 |
| 2 | 0,5 | 0,500000 | 0,971615 | 0,739770 |
| 2 | 1 | 0,739770 | 1,000000 | 0,739770 |

Los dos estados centrales generan la **misma circunferencia proyectada** y `X=0,5`, aunque sus recorridos reales y `Y` difieren. `H` revela `c` y resuelve esa ambigüedad sin medir una diferencia de coordinación. El script integra el `Q` continuo y el vector circular en 200.000 puntos por vuelta; no usa ruido, filtros, entrenamiento ni aleatoriedad.

Con cuatro estados equiprobables y el mejor predictor por media condicional (tabla de consulta sin penalización), las pérdidas cuadráticas poblacionales son `MSE(∅)=0,014372404`, `MSE(X)=0,007186202`, `MSE(H)=0,014372404` y `MSE(X,H)=0`. Así `H` **no predice solo** el resultado, pero agregarlo tras `X` mejora la predicción en `0,007186202`. La razón es completamente instrumental: `H` informa cuál proyección produjo `X`. Reservar otro día con las mismas dos posiciones de cámara podría reproducir esa mejora sin validar una hipótesis temporal. En una grabación real, ruido y cambios de tarea alterarían los números; aquí sólo importa la posibilidad lógica.

## Gate para el contraste de Nico

Antes de atribuir una mejora `base+Laban → +HIT` a relaciones corporales, el piloto debe verificar orientación y calibración de cada vista, error de `Q` **y** de fase por condición, más su covariación en los mismos clips. Predefinir un análisis de sensibilidad con `Q` mejor referenciado o con calidad/proyección explícitas, y una comparación de fuentes cuando dos vistas midan el mismo estimando con error propio. La [matriz de fuentes del control algebraico](https://github.com/SairaAsua/movimiento-armonico-investigacion/blob/a2e79ae/research/HIT_MEJORA_POR_ERROR_COMPARTIDO.md#matriz-de-fuentes-para-el-futuro-piloto) define qué significaría ese cruce y sus límites. Las comparaciones deben mantener filas, tarea, resultado externo y días de reserva idénticos, sin seleccionar la vista o la corrección que mejor haga lucir `Δ_H` en los días reservados.

Si no se obtiene referencia dinámica adecuada, el resultado publicable sigue siendo **utilidad predictiva de un pipeline declarado**, no prueba de que la fase sea un mecanismo corporal independiente ni de que belleza, eficiencia o conciencia se deduzcan de `R`.
