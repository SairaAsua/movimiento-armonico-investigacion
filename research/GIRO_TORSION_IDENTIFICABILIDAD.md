# Giro global y torsión local: contraejemplo para rope flow

Banco matemático del 24 de septiembre de 2026. No contiene video humano ni valida categorías Laban. Complementa la [guía de anotación](ANOTACION_LABAN_PILOTO.md) y el [diccionario de señales](DICCIONARIO_SENALES_V0.md) después de leer el método de [Palnick Tsachor y Shafir (2019)](https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2019.00572/full): en sus datos, fusionar rotación espacial y torsión corporal ocultó una distinción potencialmente relevante. Su estudio fue de gestos emocionales breves, no rope flow; aquí sólo aprovechamos el problema de representación.

Sea `R_p(t)` la orientación de pelvis y `R_t(t)` la de tórax en un marco fijo de sala. La orientación del tórax **respecto de la pelvis** es `R_rel(t)=R_p(t)ᵀR_t(t)`. Si una cámara cambia de orientación mediante la misma rotación rígida `G` para ambos, `(G R_p)ᵀ(G R_t)=R_rel`: la torsión relativa no cambia. En cambio, la orientación de pelvis en sala sí depende del marco declarado. Un yaw aislado es sólo una proyección de estas rotaciones; puede ser engañoso con inclinación, cruces o ángulos próximos a una discontinuidad de representación.

El [script reproducible](giro_torsion_sintetico.py) hace girar una mano fija al tórax de 0° a 90° en la sala bajo dos construcciones:

| Construcción | Pelvis | Tórax | Mano en sala | Tórax respecto de pelvis |
|---|---|---|---|---|
| A: giro rígido global | gira `θ` | gira `θ` | `(cos θ, sin θ, 0)` | 0° |
| B: torsión local | fija | gira `θ` | `(cos θ, sin θ, 0)` | `θ` |

La **serie completa de posiciones de mano en sala es idéntica**. Con ella sola —o con un solo punto de soga que siga esa mano— ningún clasificador puede saber cuál construcción ocurrió. La mano respecto de pelvis sí cambia sólo en B. Esto obliga a medir, con error conocido, **al menos dos marcos segmentarios** antes de atribuir el giro a toda la persona o a una articulación axial. Un video 2D puede no resolver esas orientaciones incluso si la mano se sigue perfectamente.

Para el piloto: conservar `R_p`, `R_t`, `R_rel`, la orientación de cámara/sala, visibilidad y error; comparar referencia física de giro global y torsión local por separado. Si no se identifica una de las orientaciones, su contraste queda inválido. Las etiquetas de especialistas sobre giro/torsión pueden servir de referencia observacional en las vistas que reciban, pero acuerdo en una sola vista no prueba exactitud 3D. No convertir una torsión fuerte en «disonancia», ni un giro fluido en «consonancia» sin el resultado externo correspondiente. Beacon sólo podrá usar estos canales después de validar captura, latencia y la interpretación que su audio comunica.
