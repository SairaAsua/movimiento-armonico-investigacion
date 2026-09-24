# Cobertura de video y sesgo de selección en rope flow

Decisión metodológica del 23 de septiembre de 2026. No hay tomas de Nico: el riesgo se deduce de la tarea y debe verificarse en el piloto. La geometría Laban que interesa incluye giros, cruces, cambios de plano y trayectorias amplias. Esas mismas acciones podrían tapar muñecas o soga, salir del volumen calibrado o crear ambigüedad entre vistas. Si sólo analizamos los tramos reconstruidos, el conjunto estudiado puede ser distinto del movimiento que queríamos explicar.

## Evidencia y alcance

En el estudio original de [Uhlrich y colaboradores sobre OpenCap](https://pmc.ncbi.nlm.nih.gov/articles/PMC10586693/), la validación se hizo en tareas definidas como caminar, sentarse/levantarse, sentadillas y saltos; el método triangula puntos 2D de varias cámaras y luego usa un modelo temporal para estimar marcadores. Los autores señalan que puntos ocluidos o identificados erróneamente pueden producir trayectorias 3D físicamente irreales y recomiendan que cada segmento sea visible por dos cámaras. Ese resultado **no** cuantifica el fallo en rope flow, no valida HarMoCAP y no autoriza trasladar sus errores medios a la soga o los giros de Nico. Motiva comprobar cobertura por tarea y vista, además de exactitud entre los casos que sí se reconstruyen.

La pérdida no afecta sólo gestos grandes y ocultos. [Koul y Novembre (2025)](https://link.springer.com/article/10.3758/s13428-024-02546-6) encontraron menor correspondencia de rapidez OpenPose–Vicon para movimientos espontáneos de **baja amplitud** en personas sentadas. El estudio no estima el error de nuestro montaje, pero señala otra vía de selección: un segmento pequeño puede conservar una trayectoria aparentemente continua y aun así tener escasa relación con la referencia. Por eso `S=1` debe exigir calidad geométrica suficiente además de detección continua; el informe debe cruzar cobertura y error con amplitud por segmento, incluyendo tanto las manos amplias como la pelvis relativamente quieta.

## Dos preguntas con denominadores diferentes

Sea `S=1` si un bloque cumple la calidad requerida para un descriptor. El promedio de una respuesta `Y` entre bloques válidos estima `E[Y | S=1]`; la pregunta sobre **todos los bloques intentados** apunta a `E[Y]`. Son iguales sólo bajo condiciones que deben justificarse, no por defecto. Aquí `S` podría depender de giro, velocidad, plano, iluminación y experiencia del ejecutante; algunos de esos factores también podrían influir en ratings o autoinforme. Por eso una asociación calculada tras excluir `S=0` puede cambiar de magnitud o signo respecto del repertorio completo. Es una posibilidad de diseño, no un sesgo observado todavía.

La primera pregunta publicable es **instrumental**: de todos los bloques intentados, ¿qué proporción permite estimar cada descriptor con error aceptable? La segunda es **sustantiva**: entre bloques donde ese descriptor es medible, ¿predice la valoración/experiencia? La segunda debe decir explícitamente a qué subconjunto se aplica. Un modelo de belleza no puede recibir una predicción HIT en clips donde la fase no existe o no se midió; tampoco debe tratar esa ausencia como «disonancia».

## Registro mínimo desde la primera captura

1. Crear un ID y una fila para **cada intento** antes de aplicar filtros de calidad. Guardar sesión, patrón, inicio/fin, cámaras previstas, estado de calibración y motivo de aborto o repetición. Los intentos repetidos conservan nuevos IDs y enlace con el original.
2. Separar fallos: archivo ausente, desincronía, fuera de campo, oclusión de mano, oclusión/cruce de soga, ambigüedad de identidad, bajo contraste, marco corporal inválido y fase no aplicable. Un bloque puede ser válido para `reach_proj_norm` e inválido para dirección 3D; `S` es **por descriptor**, no una etiqueta única de clip «bueno».
3. Conservar medidas que pueden leerse incluso cuando falla la reconstrucción: patrón/orden previstos, tiempo, vista con mayor cobertura, giro observable, amplitud aproximada anotable, duración y motivo del fallo. No convertir una anotación gruesa en coordenadas 3D precisas.
4. Definir antes qué tramos de video bruto pueden valorarse visualmente aun si falla la pose. Si el juez puede verlos, incluir una muestra de clips inválidos para geometría en una **descripción separada de cobertura estética**; nunca imputarles descriptores ausentes. Si el propio video es ininterpretable, registrar esa pérdida.
5. Reportar una tabla por tarea, giro/plano, sesión y descriptor: intentos, admisibles para rating, admisibles para 2D, para 3D y para fase; error frente a referencia dentro de cada estrato donde exista. Mostrar tiempos faltantes y fallos consecutivos, no sólo promedio de confianza por cuadro.

## Análisis y decisión de paso

En desarrollo, comparar los bloques `S=1` y `S=0` con las variables observables en ambos: tarea, orden, giro, duración y ratings si el video es juzgable. Si la pérdida aumenta justamente en transiciones o movimientos amplios, optimizar ubicación/iluminación y repetir el **piloto de medición** antes de congelar sesiones confirmatorias. No elegir el montaje por el signo de la correlación estética; la decisión se toma por calidad geométrica y cobertura.

En las sesiones reservadas, publicar la cobertura junto a cada contraste `base → Laban → HIT`. Comparar modelos en **las mismas filas** y mostrar cuántas se perdieron al agregar cada familia de descriptores. Un análisis de casos completos describe sólo su dominio válido. Un modelo de probabilidad de validez o ponderación puede explorarse si hay suficientes datos y causas observadas, pero no recupera por arte de magia geometría nunca medida ni resuelve pérdidas dependientes de una experiencia no observada. Si la validez está demasiado concentrada en patrones fáciles, la conclusión se limita a esos patrones o el estudio se reporta como factibilidad.

Esto conserva la diferencia entre «el modelo reconstruyó una trayectoria plausible» y «observamos suficientemente la trayectoria para contrastar esta afirmación». Un prior temporal puede reparar continuidad visual, pero no convierte una oclusión sin referencia en verdad de movimiento.

Conecta con [piloto de validación](PILOTO_VALIDACION_VIDEO.md), [diccionario de señales](DICCIONARIO_SENALES_V0.md), [estimandos](ESTIMANDOS_Y_CONTRASTES.md) y [selección de clips](EXPERIENCIA_ESTETICA.md).
