# Del minueto a los planos: una reconstrucción histórica con alcance delimitado

Lectura completa del 23-09-2026: [Longstaff, Treu y Royston (2007), *Rudolf Laban’s Minuet in Choreographie (1926)*](https://historicaldance.org.uk/wp-content/uploads/conferences/OnCommonGround6-Longstaff-etal.pdf), 7 páginas del encuentro *On Common Ground 6*. Es investigación de los autores basada en el capítulo «Minuet» de *Choreographie*, cuatro partituras de notación del minueto e **entrevistas**. No se obtuvo el libro de 1926 ni se reprodujo físicamente su reconstrucción para este proyecto.

## Hallazgo y procedencia de cada afirmación

El artículo indica que *Choreographie* dedica un capítulo al minueto con pasos, motivos musicales, notación Feuillet y una secuencia de 144 compases, pero que el propio capítulo **no explica** su relación con las demás categorías teóricas del libro (p. impresa 52). Los autores compararon esa descripción con un manual anterior de Bernhard Klemm: encuentran coincidencias y algunas alteraciones, como sustituir papeles de «señor/señora» por «persona A/B». **No** es prueba directa de que Laban declarara el minueto origen de todos sus planos.

La conexión entre pasos y planos proviene en gran medida de una **entrevista a Valerie Preston-Dunlop** citada por los autores (pp. 52–53): según su recuerdo, Laban enseñaba el minueto entre danzas históricas y veía en él ejemplos de tres planos cardinales. El artículo analiza luego partituras de diferentes siglos; por la cercanía textual de Laban a Klemm, selecciona una notación del minueto de Klemm realizada por Bartenieff, Jooss, Knust y Reber como la más pertinente a su reconstrucción (pp. 54–55). Esa elección es un argumento histórico de los autores, no una observación instrumental de Laban con cámaras.

| Nombre práctico en el artículo | Orientación descrita | Ejemplo que los autores vinculan al minueto | Límite para Nico |
|---|---|---|---|
| **Door / puerta** | Frontal, vertical | Pasos laterales con ascenso/descenso | La soga o mano puede atravesar ese plano sin que toda la frase sea «de puerta». |
| **Wheel / rueda** | Sagital, vertical | Paso adelante con ascenso/descenso | El eje sagital corporal cambia durante un giro; no confundirlo con la profundidad de la cámara. |
| **Table / mesa** | Horizontal | Balance, barrido lateral de pierna y apertura de brazos, con menor excursión vertical | Un aro de soga horizontal no prueba por sí solo la organización del cuerpo ni una categoría Laban válida. |

Las descripciones de función expresiva o social de cada plano en pp. 53–54 son interpretación pedagógica de este artículo. No derivan matemáticamente de la orientación. Los autores subrayan además **interacciones entre planos** y concluyen que una frase puede pasar por varias organizaciones (pp. 54, 57). Esta lectura converge con [Franco](LABAN_ARMONIA_HISTORICA.md) en no reducir armonía a permanecer en una región fija; no establece que el contraste de planos sea bello, sensual, económico o consciente.

## Traducción operacional propuesta para rope flow

1. **Objeto y marco.** Para cada frase, describir por separado mano izquierda, mano derecha, soga, tronco y pasos; usar plano corporal y plano de sala con ejes documentados. Una proyección de cámara se llama `*_proj`. Si Nico rota, una trayectoria puede conservarse respecto del cuerpo y cambiar en la sala.
2. **Episodio, no pose aislada.** En una ventana que cubra un tramo suficiente de la curva, estimar orientación de un plano ajustado y su residuo/no planaridad. Si una figura ocho necesita dos planos o atraviesa el volumen, no forzar una sola etiqueta. Guardar longitud, duración, cobertura y error de puntos.
3. **Transición observable.** Registrar cuándo una frase pasa entre orientaciones, junto con sentido, velocidad y continuidad. Un ángulo entre normales de planos sólo mide un cambio geométrico; una lectura de frase coreútica requiere secuencia, situación espacial y analistas competentes ([guía](ANOTACION_LABAN_PILOTO.md)).
4. **Comparación externa.** Después de validar cámaras y acuerdo de anotación, preguntar si el orden de planos o su interacción aporta predicción sobre un resultado elegido por encima de patrón, cadencia, amplitud, velocidad y duración. No etiquetar «más armónico» al clip que visita los tres planos con más frecuencia; ese número podría reflejar improvisación, giro o error de captura.

La matemática del ajuste de planos será **nuestra**, no la de Laban: partir de trayectorias 3D validables y una ventana fijada en desarrollo; informar normal, dispersión perpendicular y estabilidad ante cambio de ventana. El [contraejemplo de plano no identificable](IDENTIFICABILIDAD_PLANOS.md) muestra por qué una línea casi recta no autoriza interpretar la orientación que devuelve el software. El primer paper puede defender la utilidad o el fracaso de esa operación en rope flow. No puede afirmar fidelidad histórica plena a *Choreographie* mientras falte cotejo de la edición de 1926.
