# Mismo `Q`, mismos tramos, distinto cruce del recorrido

**Contraejemplo matemático del 3 de octubre de 2026.** El descriptor `Q` propuesto en [nuestra matemática espacial](LABAN_MATEMATICA.md) resume componentes direccionales ponderadas por largo. Este [banco ejecutable](q_cruces_orden_sintetico.py) muestra que conservar incluso el **multiconjunto completo de desplazamientos** no recupera el orden de la trayectoria. No representa la soga de Nico, una escala histórica de Laban ni una afirmación sobre belleza o eficiencia.

## Construcción

Ambos recorridos planos parten de `(0,0)`, vuelven allí y usan exactamente una vez los desplazamientos `(-2,0)`, `(-2,-1)`, `(2,-1)` y `(2,2)`. Sólo cambia la secuencia:

![Dos recorridos sintéticos con igual Q y distinto cruce](../assets/q-cruces-orden-sintetico.svg)

| Trayectoria | Vértices en orden | Cruces propios de aristas no adyacentes |
|---|---|---:|
| Simple | `(0,0)→(-2,0)→(-4,-1)→(-2,-2)→(0,0)` | `0` |
| Cruzada | `(0,0)→(2,2)→(0,2)→(2,1)→(0,0)` | `1`, entre aristas 0 y 2 |

La igualdad del multiconjunto implica igualdad exacta de longitud, suma de direcciones con signo, histograma de direcciones sin orden y de todo descriptor que sume una función de cada tramo sin atender a su posición temporal. Para el `Q` de la ecuación experimental, con ejes `x,y,z` y pesos `||d_i||/L`, ambos dan `L=9,30056307974577` y `Q=(0,7517740879151031;0,24822591208489683;0)`. Un detector geométrico de intersección propia sí los separa: en el segundo caso, las aristas primera y tercera se cruzan en sus interiores. Dos ejecuciones del script produjeron JSON idéntico (SHA-256 `35dcc91e98ee801dca400c3ab8933d863f5f95432dd997f481c88033bdfabdbd`).

Este **cruce de una trayectoria puntual dibujada a lo largo del tiempo** no es un autocruce de la curva completa de una soga en un instante ni dice qué tramo de soga pasa por encima en 3D. El script cuenta sólo intersecciones propias de interiores de aristas no adyacentes, no contactos o superposiciones. Los cruces de soga exigen línea central, identidad de segmentos, profundidad y visibilidad propias; la [nota de identificabilidad de soga](SOGA_IDENTIFICABILIDAD.md) y la [auditoría DLO](SOGA_VISION_DLO_FUENTES.md) delimitan esa prueba. Tampoco se deduce una topología física de rope flow desde un trazo 2D de muñeca.

## Consecuencia para el estudio y la escucha

La inferencia espacial inspirada en Laban debe conservar **secuencia de líneas, puntos de cruce y ventana**, además de `Q`, cuando la pregunta sea cómo se organiza un recorrido. Antes de interpretar un cruce desde video, registrar si se trata de autocruce de trayectoria en tiempos distintos, cruce de soga proyectado simultáneo o paso delante/detrás confirmado en 3D. En el piloto, una categoría de cruce sólo será válida en tramos con identidad y error evaluados; de otro modo `unknown`, sin completar con la figura que se esperaba ver.

La [cota de incertidumbre del cruce](CRUCE_TRAYECTORIA_INCERTIDUMBRE.md) formaliza esa última exigencia para **segmentos de una polilínea puntual 2D**: signos de orientación con margen mayor que un error acotado certifican cruces o ausencias; cerca de un contacto, un cambio de posición permitido puede invertir el resultado.

Si ambos recorridos se ejecutaran con una vuelta de igual duración, una fase interpolada **sólo entre cierres de ciclo** daría el mismo reloj a los dos. Un mapeo determinista que reciba únicamente ese reloj y `Q` tampoco podría hacer audible la diferencia de orden/cruce. La [especificación de fase](FASE_ROPEFLOW.md) ya exige microtiempo independiente cuando importa la organización intracíclo; la [ruta futura hacia Beacon](INTEGRACION_HARMOCAP_BEACON.md) necesitaría una señal validada de secuencia o cruce si pretende comunicar esa propiedad. `Q` permanece útil para la distribución de desplazamientos que sí mide; este ejemplo fija su frontera informativa.

## Giro firmado: una propiedad de orden que `Q` no conserva

Para una polilínea plana cerrada con desplazamientos no nulos `d₀,…,dₙ₋₁` y sin pares consecutivos exactamente antiparalelos, definimos el giro local `αᵢ=atan2(det(dᵢ,dᵢ₊₁),dᵢ·dᵢ₊₁)`, con índices cíclicos, y `W=Σαᵢ/(2π)`. La suma sigue la **secuencia dirigida** de tramos; es una versión poligonal explícita del número de rotación de la tangente, presentado para curvas suaves regulares por [Geiges (2008)](https://arxiv.org/abs/0801.0046). Esta definición computacional no aparece como ecuación de Laban y no supone que un giro sea bello o eficiente.

El [banco de giro firmado](q_giro_orden_sintetico.py) calcula `W=1` para la ruta simple de esta nota y `W=0` para la cruzada, pese al mismo `Q` y a los mismos cuatro desplazamientos. Invertir el sentido temporal o reflejar lateralmente la ruta simple deja `Q` igual y cambia `W` a `−1`. Pero `W` **no cuenta cruces**: otra poligonal sintética tiene `W=1` como la simple y dos intersecciones propias entre aristas no adyacentes. El total de giros absolutos también se informa por separado; ninguno de estos números sustituye la secuencia íntegra ni una anotación de soga. Dos ejecuciones del banco produjeron JSON idéntico (SHA-256 `32c0656c90be717f2c97d3aeb2cfffc5185b527899fe28c05e73f391f5e370a2`).

Para rope flow, `W` sería como máximo un **descriptor exploratorio de trayectoria puntual proyectada 2D** en ciclos efectivamente cerrados, con plano/vista, sentido, punto corporal, marco, tiempo de cierre y error declarados. No se extrapola a una curva abierta, a 3D ni a la topología simultánea de la soga. Casi pausas, tramos más cortos que su incertidumbre, proyección oblicua y huecos de muestreo pueden cambiar los giros estimados. El valor de ciclo completo existe **después** del cierre: no debe asignarse a cuadros anteriores como si fuese una señal causal para Beacon. En la comparación Laban–HIT se probaría, si expertos lo consideran pertinente, como rasgo **espacial de orden** junto a `Q` y frente a una base de geometría continua; `R` de fase conserva otra pregunta temporal. Ambas capas requieren resultados externos independientes y sesiones reservadas antes de hablar de «armonía».
