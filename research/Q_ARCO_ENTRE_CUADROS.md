# El arco entre cuadros también cambia `Q`

**Resultado matemático del proyecto para la [Issue #1](https://github.com/SairaAsua/movimiento-armonico-investigacion/issues/1).** No es una fórmula de Laban ni un resultado sobre Nico. Completa la [cota de error en posiciones muestreadas](Q_ERROR_POSICIONAL_MUESTREO.md): esa cota compara poligonales cuyos vértices ocurren en los mismos tiempos; aquí se compara el recorrido **continuo** con su poligonal aun si todos los vértices se observan sin error. El [script reproducible](q_arco_entre_cuadros.py) calcula los ejemplos.

## Un alias geométrico con vértices exactos

En un segundo, sea `r(t)=(t, a sin(2πnt))` metros, `0≤t≤1`, `a=0,005 m` y `n=30`. A `t_i=i/30`, todos los puntos registrados son exactamente `(i/30,0)`: la poligonal mide `Q_y=0` y largo `1 m`. La curva real hace una oscilación completa entre cada par de cuadros; su desviación transversal máxima es sólo 5 mm. Una integración numérica de alta resolución de `Q_y=∫u_y² ds/∫ds` da `0,290290` y largo `1,194452 m`. La incertidumbre de **posición en los cuadros es cero**; el error procede sólo del arco no observado. El ejemplo exige una ondulación de 30 Hz y no pretende representar el gesto de Nico; esta frecuencia de movimiento tampoco se relaciona con los centros de filtro de Beacon. Muestra que FPS y exactitud de vértices, por sí solos, no acotan `Q` de la curva continua.

## Una cota condicional por curvatura y longitud recorrida

Si cada tramo de curva entre dos muestras es regular, está parametrizado por longitud de arco `s`, y su tangente unitaria `u(s)` cumple `||du/ds||≤κ_max`, sea `h_i` el **largo de arco verdadero** de ese tramo y `h_max=max_i h_i`. `κ_max` tiene unidad `m⁻¹`; `κ_max h_max` es adimensional. Para `κ_max h_max<2`, la cota siguiente asegura además que ningún cordón tiene longitud cero:

`|Q_k(curva) − Q_k(poligonal exacta)| ≤ min(1, 3 κ_max h_max)`.

Demostración conservadora. En un tramo de longitud `h`, el promedio de tangentes `m=h⁻¹∫u(s)ds` es el vector cordón dividido por `h`. La hipótesis de curvatura implica `||u(s)−m||≤κ_max h/2` y por tanto `1−||m||≤κ_max h/2`. Con dirección del cordón `c=m/||m||`, se sigue `||u(s)−c||≤κ_max h`. Entonces `|u_k(s)²−c_k²|≤2κ_max h`, mientras que la pérdida de largo `h−||cordón||≤κ_max h²/2`. Al comparar los numeradores de `Q` y normalizar por los largos total verdadero y poligonal, las dos contribuciones dan como máximo `3κ_max h_max`. Es una **cota suficiente, generalmente holgada**; un valor ≥1 no informa más que `0≤Q_k≤1`.

Para relacionarla con la cadencia de video se necesita también una cota física de rapidez `v_max` en el mismo marco: si el mayor intervalo entre tiempos efectivos de captura válidos es `Δt_max`, entonces `h_max≤v_max Δt_max` y se puede usar `min(1,3κ_max v_max Δt_max)`. FPS nominal sin PTS reales, una cámara sin calibrar o una estimación de curvatura suavizada del **mismo video** no certifican esos supuestos. Hay que justificarlos con referencia dinámica independiente o tratar el resultado como sensibilidad bajo supuestos explícitos. En 2D la cota describe la **curva proyectada** y no permite inferir `Q` corporal 3D.

Como chequeo aritmético, el script usa un arco circular de `1 m`, radio `10 m` y 30 segmentos: `κ_max=0,1 m⁻¹`, `h_max=1/30 m`, cota `0,01`. Obtiene `Q_x` continuo `0,996673327` y poligonal `0,996674247`, dentro de la cota. Este círculo comprueba la implementación del ejemplo, no la validez de la hipótesis de curvatura para rope flow.

## Decisión para el piloto y Beacon

El error espacial total puede dividirse por desigualdad triangular: **curva continua → poligonal de vértices verdaderos → poligonal observada**. La primera diferencia requiere un supuesto verificable de movimiento entre cuadros; la segunda usa la [cota de error posicional](Q_ERROR_POSICIONAL_MUESTREO.md), con error de marco/correspondencia adicional. No sumar «porcentajes de confianza» ni llamar física a una cota obtenida sólo de un filtro. En desarrollo, comparar cadencias, exposición y una referencia dinámica donde exista; si la cota o la sensibilidad abarcan la distinción entre planos que el estudio quiere hacer, informar `Q` como **indeterminado** para ese subdominio y no emitir un tono de «disonancia» a partir de él.
