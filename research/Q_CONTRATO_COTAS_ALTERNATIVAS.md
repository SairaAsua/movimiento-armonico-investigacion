# Una cota posicional que el sobre `Q_live` v0 no expresa bien

Nota de diseño para la [Issue #9](https://github.com/SairaAsua/movimiento-armonico-investigacion/issues/9). La [cota determinista por error de posición](https://github.com/SairaAsua/movimiento-armonico-investigacion/blob/72cbad9/research/Q_ERROR_POSICIONAL_MUESTREO.md) y el [presupuesto angular existente](PRESUPUESTO_ERROR_Q.md) protegen la misma magnitud `Q`, pero condicionan en evidencias distintas. Aquí se comprueba su relación con el [sobre científico propuesto](CONTRATO_Q_LIVE_V0.md). No se han medido cámaras, Nico, OSC aplicado ni audio.

Para posiciones muestreadas con error máximo `σ_i`, cada error de tramo es como máximo `ε_i=σ_i+σ_{i+1}`. Con `E=Σε_i`, longitud poligonal observada `L̂` y componente observado `Q̂_k`, si `L̂>E`, la cota **directa** para ese mismo conjunto de tiempos es

`B_pos,k=min{1,[(2/√3)+Q̂_k] E/(L̂−E)}`.

Es conservadora aunque un tramo individual sea demasiado corto para tener una dirección angular identificable. En cambio, el campo `max_angle_error_deg` del sobre v0 toma el **peor ángulo entre tramos**; su validador exige `q_component_abs_bound≥min(1,sin α+TV+m)`. Esto también es seguro, pero puede perder información.

## Testigo aritmético

Considerar dos segmentos observados de `1 m` y `0,001 m`, con tres puntos cuyas cotas posicionales son `0,0005 m`. Entonces `ε_1=ε_2=0,001 m`, `E=0,002 m`, `L̂=1,001 m`. Incluso tomando `Q̂_k=1`, la cota directa por posición es `B_pos,k≤0,004314` (aprox.). En el segmento de 1 mm la cota de desplazamiento iguala su largo: su dirección puede variar arbitrariamente y **no** tiene un ángulo máximo menor que 90° garantizado. El canal angular v0 produce `sin α=1`, por lo que requiere `q_component_abs_bound=1`, aun si `TV=m=0`. Así descarta la distinción espacial de la ventana completa que la cota directa todavía restringe.

El ejemplo es una comparación de **métodos de cota**, no una trayectoria física de Nico ni una validación de `0,5 mm` de error. El número directo tampoco cubre error de marco, identidad, 3D, segmentos ocultos ni curva entre cuadros. Si esas fuentes existen, se acotan aparte; no se suma `B_pos` a `sin α+TV` cuando ambos representan el **mismo** error posicional. Una suma así contaría dos veces la incertidumbre. Una alternativa conservadora para una ventana real sería `min(1, B_pos,k + B_frame,k + m)` sólo después de justificar por separado cada componente, mismo marco/soporte y la fracción de **arco verdadero** perdido.

## Decisión de interfaz

Mantener v0 tal como está para los fixtures y el replay actuales: todos tienen incertidumbre `not_estimated`, y no hay perfil físico que autorice `bounded`. No escribir `B_pos` como `q_component_abs_bound` en v0 cuando quede por debajo del mínimo que exige su validador. Un sobre futuro **versionado** podría declarar `bound_method` y componentes con procedencia: `angular_weight`, `direct_position` u otro método revisado. El consumidor compararía la cota final por componente con la separación espacial que promete hacer audible; `bounded` no implicaría por sí solo que esa separación se resolvió. Cuando un método da sólo el límite trivial, la capa espacial calibrada se retira o se declara indeterminada, nunca se interpreta como disonancia corporal.

Antes de elegir el método para video real hará falta validar cotas de posición **dinámicas** en el volumen, ventanas y figuras de uso, el error de marco y el tratamiento del arco oculto. El código de ejemplo `q_cotas_contrato_sintetico.py` verifica únicamente la aritmética del testigo.
