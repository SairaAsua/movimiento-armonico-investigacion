# Cuándo dos realizaciones cuentan como el mismo motivo espacial

**Decisión de diseño, 03-10-2026.** La [lectura mediada del minueto en *Choreographie*, pp. 54–64](https://github.com/SairaAsua/movimiento-armonico-investigacion/blob/c9f42b7/research/LABAN_MINUETO_BAILE_1926.md) distingue un nombre de paso de sus realizaciones rítmicas, pero también admite cambios de amplitud y ejecución. Por ello «misma figura» según el intérprete o `Q` parecido **no certifican** que la geometría se conserve. Esta nota define un filtro propuesto para contrastes Laban × HIT; no informa pares observados de Nico ni equivalencia validada con cámaras.

## Objeto del contraste

Antes de ver valoraciones o experiencia, elegir una figura de rope flow y definir su inicio, fin, sentido, número de vueltas/cruces, manos activas, apoyo y relación básica de la soga con el cuerpo. Dos intentos pueden pertenecer al mismo **nombre de motivo** y, sin embargo, recorrer curvas distintas. El par de comparación se seleccionaría sólo entre intentos con la misma tarea, marco espacial y repertorio reconocido. La trayectoria de sala, la trayectoria relativa al torso, el movimiento del torso y, si se identifica, la curva de la soga responden preguntas diferentes; declarar por adelantado cuál o cuáles constituyen la geometría primaria.

La comparación retiene el **orden espacial**: no basta una distribución de direcciones ni un `Q` similar. Por ejemplo, un círculo plano y un cuadrado plano, ambos simétricos en sus ejes, pueden dar `Q_x=Q_y=1/2` y `Q_z=0` en una definición ponderada por longitud, aunque sus recorridos sean distintos. Tampoco se considerará equivalente una frase que invierte el sentido, repite un lóbulo o cambia de apoyo sólo porque llega al mismo punto.

## Regla de medición candidata

Para cada trayectoria física preseleccionada `i` —por ejemplo, mano izquierda respecto de un marco corporal validado—, representar la **parte observada y continua** como `r_i(u)`, con `u∈[0,1]` igual a fracción de longitud de arco de esa frase. `u` elimina la ley temporal deliberadamente: duración, pausas, rapidez y fase se guardan en otro canal. La escala corporal `L` se fija desde calibración, no se recalcula por par. El frente, origen, rotación y comienzo de frase se registran con una convención común; no se rota ni deforma cada curva para obtener el mejor parecido después de ver los resultados.

En el soporte espacial validado `U_i`, definir `d̂_i = sup_{u∈U_i} ||r̂_{i,A}(u)−r̂_{i,B}(u)||/L`. Esta distancia **punto a punto por recorrido normalizado**, con correspondencia y sentido fijados, es una propuesta del equipo; no es una fórmula de Laban ni una medida de metabolismo. Exigir cobertura de todo el recorrido primario para afirmar semejanza de la frase entera. En tramos faltantes, conservar sólo un resultado **local al soporte observado** o declarar el par indeterminado. La correspondencia por arco exige que el error de muestreo, reconstrucción y registro de `u` también esté acotado: un error posicional por cuadro no basta para acotar `d̂_i` de la curva continua entre cuadros.

Con una cota validada `e_{i,A}` y `e_{i,B}` para la **curva ya registrada en la misma coordenada `u`**, expresada también en unidades de `L` —incluidos errores de cámara, marco, interpolación y correspondencia—, la desigualdad triangular da `max(0,d̂_i−e_{i,A}−e_{i,B}) ≤ d_i ≤ d̂_i+e_{i,A}+e_{i,B}`. Es una cota condicional, no un intervalo de confianza si `e` es sólo una desviación típica. Para un margen práctico `δ_i>0` congelado antes de abrir sesiones reservadas:

| Estado del par | Regla conservadora para **todas** las trayectorias primarias y la estructura discreta |
|---|---|
| `geometry_comparable` | Mismo motivo, sentido, vueltas/cruces y apoyo según definiciones previas; cobertura completa; cada límite superior `d̂_i+e_{i,A}+e_{i,B}<δ_i`. |
| `geometry_different` | Una estructura discreta predefinida difiere, o alguna cota inferior `d̂_i−e_{i,A}−e_{i,B}>δ_i`. |
| `geometry_indeterminate` | Todo lo demás: cobertura insuficiente, registro ambiguo, error sin cota, margen cruzado, discrepancia de anotadores o figura no comparable. |

El valor de `δ_i` debe reflejar la menor diferencia espacial que importe para la figura y superar la resolución real del instrumento; se decidirá con desarrollo y lectura experta, no por la correlación más favorable con belleza, HIT o costo. Una prueba de diferencia sin significación **no prueba equivalencia**: el principio de fijar márgenes prácticos antes del análisis está desarrollado por [Lakens (2017)](https://doi.org/10.1177/1948550617697177). Nuestra regla de cotas para curvas no es el TOST de ese artículo ni hereda sus garantías estadísticas. Para un análisis poblacional de equivalencia entre condiciones haría falta otro diseño con replicación y dependencia por sesión explícitas.

## Comparación HIT que esta regla permite

Dentro de pares `geometry_comparable`, comparar **perfiles temporales medidos en reloj original**: duración, pausas, cadencia y, sólo donde haya ciclos válidos, relaciones de fase independientes y especificadas antes. No convertir la fracción de arco `u` en un reloj HIT ni elegir retrospectivamente una deformación temporal para maximizar `R`. Si geometría y ritmo varían juntos, informar ambos cambios y estimar el aporte incremental con controles; esos intentos no integran el contraste restringido de geometría comparable. La inclusión del par debe cerrarse antes de mirar el resultado externo para evitar selección circular.

**Límites actuales.** No se han medido `e_i`, `δ_i`, cobertura 3D de soga/manos ni acuerdo entre anotadores en Nico. La regla puede ser demasiado exigente para el montaje disponible; en tal caso se publicará la factibilidad y los pares indeterminados, sin relajar el margen después de ver los juicios. La equivalencia aquí es relativa a trayectorias, tarea y márgenes declarados; no significa «movimiento idéntico», eficiencia igual ni conservación de todas las articulaciones.
