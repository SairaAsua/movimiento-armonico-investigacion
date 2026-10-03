# Qué puede decir `Q` si una parte del recorrido está oculta

**Resultado matemático de diseño; no es una fórmula de Laban ni una medición de Nico.** Pertenece a la [Issue #1](https://github.com/SairaAsua/movimiento-armonico-investigacion/issues/1). El descriptor propuesto por el equipo es `Q_k=L⁻¹∫u_k(s)² ds`, donde `u` es la tangente unitaria y `L` el largo **total** de un recorrido en un marco y unos ejes fijados. Sus tres componentes suman uno en 3D. En 2D se aplica la misma cuenta sólo a los ejes proyectados y se nombra `Q_proj`; no recupera el componente de profundidad.

La motivación histórica es conservar recorrido y secuencia, no atribuirle esta fórmula a Laban: el [mecanoscrito de «Tanzkomposition und Schrifttanz»](LABAN_TANZKOMPOSITION_1928.md) distingue caminos, ritmos y acontecimientos; la [matriz del piloto](LABAN_MATRIZ.md) conserva las limitaciones de pose, marco y oclusión. Aquí resolvemos sólo una pregunta instrumental: ¿cuánto puede cambiar `Q` cuando falta un tramo **no observado**?

## Intervalo de identificación

Sea `L_o>0` el largo de tramos observados válidos, `L_h≥0` el largo real de tramos ocultos, `q^o_k` el `Q` calculado **por arco observado** y `q^h_k` la distribución de tangentes oculta. Con `m=L_h/(L_o+L_h)`, por partición de la integral:

`Q_k=(1−m)q^o_k+m q^h_k`, con `q^h_k≥0` y `Σ_k q^h_k=1`.

Si `m` fuese conocido y no hubiera otra restricción geométrica, cada componente tiene el intervalo conservador `[(1−m)q^o_k, (1−m)q^o_k+m]`. Los extremos de componentes diferentes **no son simultáneos**: el vector completo pertenece al simplex trasladado `(1−m)q^o+m Δ₂`. No reemplazar el hueco por una recta, por velocidad cero ni por una repetición del último valor. Esas opciones eligen una continuación sin evidencia.

Si sólo se conoce una cota `L_h≤H` derivada de un límite continuo de rapidez **justificado físicamente** y de los tiempos de los huecos, `m≤m_max=H/(L_o+H)`. Entonces `Q_k` queda dentro de `[(1−m_max)q^o_k, (1−m_max)q^o_k+m_max]`. Es una envolvente; las posiciones de entrada/salida pueden estrecharla, y un estimador de pose con error agrega incertidumbre **además** de ella. El largo observado no es igual al largo físico si la proyección, el muestreo o el error alteran la curva; antes de aplicar esta cota a Nico habría que acotar esos errores por separado. Una cota sobre rapidez media o un máximo visto en el propio clip no es una cota dura de rapidez durante la oclusión.

Si tampoco existe cota superior defendible de `L_h`, `m` puede acercarse a uno y el intervalo se vuelve `[0,1]` para cada componente: **el `Q` de la vuelta completa no está identificado**. Los PTS sólo fechan el hueco; no limitan su largo sin una premisa de rapidez. La distancia recta entre extremos visibles da una **cota inferior**, pero tampoco una superior. La tasa de cuadros visibles o el porcentaje de tiempo válido no equivale a fracción de arco válida cuando la mano acelera precisamente en lo oculto.

Para declarar que el eje `i` domina al eje `j` bajo la envolvente, basta la condición conservadora `(1−m_max)(q^o_i−q^o_j)>m_max`. Si no se cumple, la dominancia puede cambiar con una continuación admisible; el software debe informar `indeterminado` en vez de elegir el mayor componente observado. Esta condición se aplica por pares y es suficiente, no un clasificador histórico de direcciones labanianas. También depende de que marco y ejes permanezcan definidos a lo largo del hueco.

## Testigo de inversión con el mismo material visible

El [banco mínimo](q_cobertura_arco_sintetico.py) toma un tramo visible que va y vuelve sobre `x`, con largo `L_o=2`, y dos continuaciones ocultas que arrancan y terminan en el mismo punto y duran el mismo intervalo: una va y vuelve por `x` y otra por `y`, cada una con largo `L_h=3`. La cámara vería **exactamente el mismo tramo visible** y los mismos extremos del hueco. El primer recorrido completo da `Q=(1,0,0)`; el segundo, `Q=(0,4;0,6;0)`. El cálculo sólo sobre lo visible daría `q^o=(1,0,0)` en ambos y concluiría erróneamente que domina `x` en el segundo. Las velocidades ocultas son elegibles dentro de una misma cota hipotética `H=3`; no se afirma que esas trayectorias sean rope flow físicamente realizable.

Con `m_max=0,6`, la envolvente por componente es `Q_x∈[0,4;1]`, `Q_y,Q_z∈[0;0,6]`: permite ambas clases dominantes. En otro testigo de largo oculto `1` y observado `3` (`m=0,25`), `q^o=(1,0,0)` garantiza que `x` sigue dominando aunque la continuación sea enteramente vertical. El contraste demuestra la lógica de cobertura, no un umbral universal: el margen necesario depende del `q^o` y de cuánto arco pudo perderse.

## Regla para el ensayo y el sonido

Registrar por **vuelta y región de la tarea** largo observado, duración/posición de cada hueco, error de trayectoria, cota de arco oculto si existe, `q^o`, intervalos de `Q` y estado de dominancia. No promediar sólo vueltas completas si su tasa de oclusión difiere por figura, giro o resultado estético. En una vista 2D, la misma lógica habla de `Q_proj`; el 3D sigue sin observarse. Si la categoría espacial queda indeterminada, la capa de audio que dependa de esa categoría se retira o marca inválida; no debe sonar «disonante» por ausencia de datos. Un `Q` retrospectivo de vuelta completa, aun identificado, no es una señal causal para feedback durante esa vuelta.

Para que esta regla llegue a datos de Nico faltan: originales autorizados, prueba de error/PTS/oclusiones del montaje, una cota física de movimiento durante huecos si se la desea usar y revisión experta de si la categoría realmente corresponde a la pregunta labaniana. El testigo sólo prueba una posibilidad matemática; no valida cámara, soga, estética, HIT ni Beacon.
