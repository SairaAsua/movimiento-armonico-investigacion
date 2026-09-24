# Simetrías de Laban: matemática útil y límites de la escala de doce

Nota de investigación, 23-09-2026. Fuente principal leída completa en su [versión HTML: Ashley Walls White, *Group Theory and Modern Dance Composition* (2020)](https://arxiv.org/html/2005.11642v1), [ficha del preprint](https://arxiv.org/abs/2005.11642). White formaliza **su propia interpretación matemática** de figuras y recursos coreográficos asociados a Laban; no es el texto original de *Choreutics*, ni una validación empírica de movimiento, economía o belleza. Su figura 5 presenta una escala primaria de doce direcciones y su figura 6 la rotula como un reloj de doce posiciones. Falta cotejar el orden concreto con *Choreutics* completo y con un especialista antes de usarlo como escala histórica de referencia.

## Transformaciones definibles sin fingir que son fisiología

Con `x=lateral`, `y=anterior`, `z=superior` en un marco corporal derecho, definimos reflejos algebraicos sobre una trayectoria espacial `p(t)`:

| Operación | Coordenadas | Determinante | Qué cambia |
|---|---|---:|---|
| Inversión lateral `I_LR` | `(-x,y,z)` | −1 | Izquierda/derecha |
| Inversión anterior `I_FB` | `(x,-y,z)` | −1 | Delante/detrás |
| Inversión vertical `I_HL` | `(x,y,-z)` | −1 | Alto/bajo |

Cada operación aplicada dos veces devuelve el original; los tres reflejos conmutan y generan ocho transformaciones, el grupo de cambios de signo `(Z₂)^3`. Sobre el conjunto ideal `V(φ)={(0,±1,±φ),(±1,±φ,0),(±φ,0,±1)}` preservan los doce vértices y las treinta aristas de longitud mínima. **Cada reflejo individual invierte orientación espacial** (`det=-1`): no es una rotación propia del cuerpo ni pertenece al grupo de rotaciones del icosaedro. El producto de dos tiene `det=+1` y corresponde aquí a una media vuelta alrededor del eje restante. Esta formulación de coordenadas y su [comprobación sintética](simetrias_laban.py) son nuestras, apoyadas en la idea de inversiones de White, no una fórmula atribuida a Laban.

Para datos, el ensayo correcto de la operación es aplicar el mismo mapa a **trayectorias completas y marco corporal**, conservando orden temporal. Si se transforma sólo una lista de etiquetas y no la trayectoria, se prueba la notación, no la medición. Bajo una isometría ideal se conservan distancias, rapidez escalar y curvatura no firmada; cambian lateralidad y signos de orientación/fase según la definición. Esto da pruebas de coherencia para un algoritmo de Laban. **No** crea una ejecución humana de la variante: la soga, la mano dominante, anatomía y gravedad pueden impedir equivalencia física, especialmente bajo reflejo vertical. Para comparar una variante real, registrar nueva ejecución, tarea y cobertura; no asignarle el costo ni la experiencia de la señal transformada. Un espejo de cámara y una inversión coreográfica también son situaciones distintas: el primero cambia la imagen disponible, no el movimiento realizado ([espejo y fase](ESPEJO_ORIENTACION_FASE.md)).

## Por qué el reloj `Z₁₂` no valida una escala observada

White coloca las doce direcciones de la escala primaria en un reloj `Z₁₂` y relaciona triángulos, cuadrángulos y diámetros con los subgrupos `4Z₁₂`, `3Z₁₂` y `6Z₁₂`. Esto es una manera precisa de **describir un orden ya elegido**. Sin embargo, cualquier lista de doce direcciones distintas puede numerarse 0…11 y, una vez numerada, tendrá esos mismos subgrupos: `4Z₁₂={0,4,8}` contiene tres posiciones de un triángulo aritmético en el reloj, `3Z₁₂={0,3,6,9}` cuatro de un cuadrángulo, y `6Z₁₂={0,6}` dos posiciones diametrales. La existencia de cosets no prueba que la **posición corporal**, la **distancia euclidiana** ni la **adyacencia de aristas** de una ruta real obedezcan a la escala histórica. Tampoco basta encontrar doce visitas a direcciones: importa el orden, los tramos entre ellas y el marco.

### Lectura concreta de las figuras 3–6 del PDF de White

Inspección visual del [PDF original, pp. impresas 8–11](https://arxiv.org/pdf/2005.11642), no sólo del HTML: la figura 3 da la leyenda de símbolos, la 5 los ordena y la 6 asigna índices 0…11. Emparejando esa leyenda con los nombres `v₁…v₁₂` que White enumera en la p. 4, se obtiene **en su convención**, no por lectura directa de Laban:

| Índice del reloj | Vértice de White | Dirección en el marco corporal `x=lateral, y=anterior, z=superior` |
|---:|---:|---|
| 0 | 1 | adelante-arriba `(0,+1,+φ)` |
| 1 | 3 | derecha-arriba `(+φ,0,+1)` |
| 2 | 5 | derecha-adelante `(+1,+φ,0)` |
| 3 | 9 | adelante-abajo `(0,+1,−φ)` |
| 4 | 11 | derecha-abajo `(+φ,0,−1)` |
| 5 | 7 | derecha-atrás `(+1,−φ,0)` |
| 6 | 10 | atrás-abajo `(0,−1,−φ)` |
| 7 | 12 | izquierda-abajo `(−φ,0,−1)` |
| 8 | 8 | izquierda-atrás `(−1,−φ,0)` |
| 9 | 2 | atrás-arriba `(0,−1,+φ)` |
| 10 | 4 | izquierda-arriba `(−φ,0,+1)` |
| 11 | 6 | izquierda-adelante `(−1,+φ,0)` |

El [cálculo reproducible](simetrias_laban.py) comprueba que esta secuencia visita los doce vértices una sola vez, cada paso consecutivo (incluido 11→0) une vértices vecinos a distancia `2`, y cada índice `k+6 mod 12` es el antipodal de `k`. Es, por tanto, un **ciclo hamiltoniano antipodal** del grafo icosaédrico de esta construcción. Pero no es el único: enumerando ciclos con inicio fijo y equiparando ambos sentidos hay **1280 ciclos hamiltonianos**, de los cuales **20 en total, incluida la secuencia de White**, cumplen la misma condición antipodal de medio recorrido. Estos conteos son del grafo ideal, no de Laban ni de Nico. La condición «ciclo de doce aristas + opuestos a seis pasos» restringe una secuencia pero no identifica por sí sola la secuencia concreta de White.

Una segunda comprobación determina las **60 rotaciones propias** del icosaedro por la imagen de una arista orientada. La órbita de la secuencia de White bajo ellas contiene **exactamente los veinte ciclos antipodales**. Por tanto, las otras 19 rutas no son formas geométricas distintas: son **orientaciones rotadas de la misma forma** respecto de los ejes corporales fijados. Si se permite girar la plantilla libremente para cada clip, esas veinte comparaciones colapsan en un mismo modelo y no pueden usarse como controles independientes. La orientación anterior/lateral/superior es parte de la hipótesis, no un parámetro inocuo de ajuste.

El mismo [chequeo sintético](simetrias_laban.py) exhibe una pérdida concreta en el descriptor de planos `Q`: reflejar **lateralmente** la ruta de White cambia su secuencia de vértices en el marco corporal, pero en cada tramo sólo cambia el signo de la componente lateral del desplazamiento. Como `Q` usa cuadrados de componentes, la serie de aportes `Q` es **idéntica tramo por tramo** en ambas rutas, también en cualquier ventana móvil formada con los mismos tramos y tiempos. El promedio de todo el ciclo ideal es `Q=(1/3,1/3,1/3)` para las dos. El banco verifica además que el [mapeo hipotético de tres ganancias Beacon](INTEGRACION_HARMOCAP_BEACON.md) `g_k=0,2+0,4Q_k` produce controles idénticos para los doce tramos, mientras la componente lateral firmada distingue el espejo. Esta igualdad no exige elegir el inicio del ciclo ni borrar el tiempo: muestra que ni siquiera el flujo causal de `Q` permite identificar siempre la orientación/secuencia de White. Una capa sonora que use únicamente `Q` conservará planos de movimiento, pero necesitará otra señal validada, con signo y orden, si su propósito es hacer audible la escala.

`20/1280 = 1/64` es la proporción combinatoria de ciclos hamiltonianos ideales con esa condición bajo una elección **uniforme de ciclos**. No es la probabilidad de observar la secuencia en una persona, ni un valor `p`: las rutas biomecánicamente accesibles, la tarea de soga, la orientación corporal y las reglas de detección de eventos hacen que las secuencias observadas no sean uniformes. Tampoco sería un contraste justo elegir retrospectivamente el mejor de veinte recorridos y compararlo con una sola secuencia rival.

La tabla permite preparar un comparador *White-2020* explícito para una eventual trayectoria 3D de Nico. No autoriza afirmar que una figura ocho de rope flow siga la escala primaria: hay que comprobar si visita regiones identificables con ese orden, cuánto tiempo pasa entre ellas y qué recorrido real une los hitos. Una coincidencia por inversión, cambio de inicio o rotación global puede ser permitida sólo si esa familia de equivalencias se declara **antes** de mirar las sesiones reservadas; cada libertad adicional amplía la línea base del ajuste.

### Contraste posible, condicionado al repertorio real

Sólo si una frase habitual contiene una **serie de episodios direccionales distinguibles de forma independiente de la plantilla**, se puede probar ajuste a la secuencia: primero dos observadores marcan los límites de esos episodios sin ver los doce vértices ni los resultados estéticos; luego se calculan para cada episodio vectores de posición y de desplazamiento **por separado**, con incertidumbre angular y marco corporal validado. La variable Laban que se pretende cotejar (línea de movimiento, posición o ambas como hipótesis distintas) se fija con especialista y fuente histórica antes de abrir sesiones reservadas. No forzar doce eventos por frase ni cortar una improvisación hasta que aparezca el orden deseado.

Para una frase que sí cumpla ese criterio, congelar la orientación de la plantilla en el cuerpo y comparar el **mismo error angular de la secuencia ordenada** para White y sus otras 19 orientaciones rotadas, admitiendo para todas exactamente las mismas libertades justificadas (por ejemplo inicio circular; reversa sólo si el patrón admite ambos sentidos). Este contraste sólo pregunta si la **orientación corporal concreta** que White dibuja se ajusta mejor que otras orientaciones de la misma forma. Reportar su rango, margen e incertidumbre por sesión, además del error de trayectorias continuas sin cuantización. Si la pregunta es por la **forma antipodal sin orientación**, se evalúa la familia completa frente a secuencias no antipodales y descriptores continuos, contando el ajuste de orientación dentro del procedimiento de referencia. Si se exploran los 1280 ciclos, el resultado es una búsqueda más flexible y su línea base cambia. Sin 3D válido o con muchos episodios ambiguos no hay contraste de escala: se informa cobertura, no un puntaje optimista calculado sólo en las frases fáciles. Un buen ajuste fuera de muestra mostraría **especificidad descriptiva para esta tarea**, todavía no intención de Nico, eficiencia energética, experiencia mística ni validación general de Laban.

La unidad matemática para una prueba futura sería una secuencia de direcciones corporales **predefinida por fuente y experto** más el grafo de su sólido correspondiente. Para cada frase observada, registrar: (a) direcciones continuas con incertidumbre; (b) transiciones entre regiones asignadas de modo congelado; (c) cobertura y ambigüedad de asignación; (d) coincidencia de orden y de enlaces geométricos frente a esa escala; y (e) comparación con órdenes alternativos y con descriptores continuos sin sólido ([contraste de redes](REDES_CONTRASTE_GEOMETRICO.md)). Una mera coincidencia de índices modulares, ajustada tras mirar el video, sería circular.

## Uso en la investigación de Nico

1. Incluir reflejos e inversiones en el **banco de coherencia del algoritmo**, no como etiquetas de «consonancia». Verificar que los descriptores de longitud/rapidez sean invariantes y los de lateralidad cambien según contrato. Conservar qué marco y qué señales se transformaron.
2. Si una secuencia de Nico parece semejante a una escala, describir primero la trayectoria y sus errores; sólo después cotejar con la secuencia histórica fijada. Diferenciar figura ocho de soga, posición de muñeca y dirección de desplazamiento.
3. La operación `Z₁₂` de White pertenece a **composición de direcciones**. La φ de los rectángulos del icosaedro pertenece a **geometría de vértices**; la φ de HIT apéndice E pertenece a **consulta de fase**. Ninguna implica a las otras ([cotejo HIT–Laban](PUENTE_LABAN_HIT.md)).

**Limitación de la fuente:** el PDF confirma que en la sección «The Octahedron» White escribe que el estabilizador rotacional de un vértice sólo contiene identidad y una media vuelta. Para un octaedro regular completo, el eje que atraviesa ese vértice y el opuesto admite también giros de 90° y 270°: el estabilizador rotacional tiene **cuatro** elementos. El par que White usa puede ser un subgrupo elegido, pero no el estabilizador completo que nombra. Por esta razón independiente, sus tablas de permutaciones no se adoptan como especificación de software. El artículo es una propuesta matemática, no un estudio de fiabilidad de anotación; falta cotejar la escala en *Choreutics* antes de atribuirle a Laban la secuencia concreta de la tabla.
