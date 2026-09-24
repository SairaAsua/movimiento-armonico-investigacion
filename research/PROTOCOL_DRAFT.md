> **Borrador histórico inicial, no operativo.** La primera fase actual está definida en el [protocolo piloto 0.1](PROTOCOLO_PILOTO_V0.md) y en el [plan centrado en Laban](PLAN_INVESTIGACION.md). Las seis sesiones, IMU, EMG y calorimetría sugeridas abajo eran opciones exploratorias tempranas, no requisitos ni decisiones tomadas. No hay protocolo ejecutado.

# Borrador de estudio preliminar: rope flow

23 de septiembre de 2026. Propuesta de diseño, no protocolo ejecutado ni resultado. Participante propuesto: Nico. Fuentes y discusión en los reportes R1–R4 y la bibliografía del archivo. Este documento contiene decisiones sugeridas [P], que deben ajustarse a la práctica real, los instrumentos disponibles y la tolerancia del participante.

## Pregunta y alcance

¿Los patrones de coordinación temporal entre segmentos corporales durante rope flow se asocian con menor costo metabólico para una tarea comparable, mayor valoración estética y mayor experiencia subjetiva de fluidez?

La intención de Saira incluye una hipótesis más amplia: estados vividos como belleza, sensualidad, orgasmo o experiencia mística podrían compartir formas de organización corporal. El primer estudio aborda asociaciones durante rope flow; no pone a prueba por sí solo la equivalencia entre esos estados ni una jerarquía de conciencia.

Separar cuatro ejes permite poner a prueba sus relaciones: organización motriz, economía metabólica, percepción de observadores y experiencia de quien se mueve. Ningún eje funciona como etiqueta automática de los demás.

## Hipótesis contrastables propuestas

1. Dentro de un mismo patrón y rango de cadencia, las relaciones de fase entre segmentos permiten caracterizar diferencias reproducibles entre sesiones.
2. Algunos patrones de coordinación se asocian con menor costo metabólico por ciclo, controlando cadencia, amplitud, duración y tipo de movimiento. Puede haber resultados nulos o una relación no lineal.
3. Belleza, sensualidad y fluidez percibidas tienen asociaciones que deben estimarse por separado con esas variables. No se codifica de antemano “bello = eficiente”.
4. Los reportes de absorción, facilidad y placer de Nico se relacionan con algunas variables, sin asumir que sean intercambiables ni deducibles desde la cara.
5. Una representación relacional inspirada en HIT aporta información predictiva adicional frente a medidas simples de cadencia, amplitud y cantidad de movimiento. Esta sería una prueba más específica de la utilidad del marco.

El resultado negativo también es informativo: si belleza acompaña una mayor amplitud o complejidad, pero no menor costo por tarea comparable, no se sostiene esa parte de la cadena. Si una métrica HIT no mejora al modelo sencillo en sesiones nuevas, no hay ventaja demostrada de ese descriptor en esta tarea.

## Dos tipos de registro complementarios

Registro naturalista: sesiones completas de la práctica habitual, con transiciones y errores incluidos. Sirve para reconocer el repertorio, no para fijar retrospectivamente qué cuenta como éxito.

Registro comparable: un patrón que Nico ya domina, misma soga y rango de movimiento, con bloques repetidos a cadencias cómodas. El orden de las condiciones se contrabalancea. Una condición de atención corporal inspirada en Kaparo puede estudiarse después, con una instrucción definida; no mezclar simultáneamente cambios de atención, música, técnica y equipamiento.

Un punto de partida logístico, sujeto a piloto, sería una sesión de familiarización y seis sesiones de registro, con tres condiciones de cadencia cómoda y dos repeticiones por condición. Esto no es un cálculo de potencia ni garantiza inferencia concluyente. La duración de los bloques metabólicos se decide mediante observación de estabilización y tolerancia, no por la duración deseada del clip. Puede requerir reducir condiciones o distribuirlas en más días.

Mantener un bloque comparable sin Beacon; registrar el sonido ambiente y cualquier metrónomo. El sonido puede modificar la coordinación y debe tratarse como una condición experimental, no como un fondo neutral.

## Instrumentación por pregunta

| Pregunta | Registro propuesto | Qué permite y qué no |
|---|---|---|
| Cómo se mueve | Dos cámaras sincronizadas, calibradas, cuerpo y soga completos | Estimar trayectorias y ángulos; validar frente a observación y sensores. Una pose 2D no mide por sí sola dinámica 3D |
| Cómo gira y se coordina | IMU en pelvis, tronco y muñecas, con sincronización común | Orientación/velocidad angular; revisar deriva, colocación y desalineación |
| Qué músculos participan | sEMG en pares seleccionados con personal competente | Activación eléctrica superficial relativa y coactivación; no fuerza muscular ni gasto total directamente |
| Cuánto cuesta sostener la tarea | Calorimetría indirecta con VO2/VCO2 y línea basal pertinente | Estimación metabólica en bloques compatibles con sus supuestos; no energía instantánea de un gesto |
| Qué pasa con respiración y pulso | Banda respiratoria y ECG o intervalos RR de calidad verificada | Frecuencias y dinámica cardiorrespiratoria; no medidor universal de conciencia |
| Cómo se vive | Reporte breve después del bloque y entrevista al terminar | Experiencia en primera persona, con incertidumbre de memoria temporal |
| Cómo se percibe | Clips con condiciones visuales equivalentes, orden aleatorio y varios evaluadores | Juicios de belleza, sensualidad y fluidez; no diagnóstico fisiológico |

Si no hay calorimetría, la entrega se limita a cinemática y experiencia. Las calorías de un reloj, el pulso o el video no sustituyen una medición validada del costo metabólico. También se debe observar si la máscara y los sensores modifican la práctica que se quiere estudiar.

Frecuencia de imagen propuesta para probar: 60 fps, con exposición que evite desenfoque y registro de timestamps reales. No se declara suficiente hasta comprobar los giros rápidos y la visibilidad de la soga. Para IMU se puede explorar 100–200 Hz, verificando sincronización y señal útil; son valores de partida de ingeniería, no umbrales científicos universales. Frecuencias de sEMG se seleccionan con el equipo y su protocolo específico, no reutilizando las de IMU.

## Matemática mínima para relaciones de fase

Para un segmento con ciclos identificables, estimar una fase phi_i(t) que crece 2π por ciclo y frecuencia f_i(t) = (1/2π) dphi_i/dt. Definir primero qué evento marca el ciclo y en qué sistema de referencia se mide. Un giro completo de soga puede contener más de un pico por articulación; confundir picos con ciclos genera falsos armónicos.

Para frecuencias con relación candidata f_i/f_j = p/q:

`delta_pq(t) = q * phi_i(t) - p * phi_j(t)`

`PLV_pq = abs(mean(exp(i * delta_pq(t))))`

PLV resume estabilidad de la relación de fase dentro de una ventana; no mide por sí misma eficiencia ni conciencia. Informar también la fase media y la distribución. Una antífase estable puede ser organización funcional. Un promedio global de sincronía puede ocultarla.

Las relaciones p/q, pares de segmentos, ventanas y filtros deben fijarse antes de evaluar las sesiones de confirmación. La fase requiere señal oscilatoria válida: no calcularla en segmentos inmóviles, con poca amplitud, ocluidos o durante transiciones no periódicas y luego interpretar el resultado como estado corporal. Comparar la extracción por eventos con otra técnica cuando sea apropiado y revisar sensibilidad al filtrado.

Los armónicos de Fourier dentro de una señal describen también su forma de onda. Su presencia no demuestra acoplamiento entre dos segmentos. Asimismo, la covariación puede provenir de la soga compartida, la cadencia o el metrónomo; no identifica por sí sola una conexión causal.

Como extensiones exploratorias: recurrencia, variabilidad entre ciclos, suavidad normalizada y complejidad temporal. No acumularlas en un “índice de consonancia” con pesos elegidos para favorecer los clips preferidos. Compararlas primero por separado.

## Economía y eficiencia

Para una tarea reproducible, una medida candidata es:

`costo_neto_por_ciclo = (potencia_metabólica_tarea - potencia_basal_pertinente) / ciclos_por_segundo`

Si la potencia está en J/s, el resultado es J/ciclo. La tarea, amplitud y objetivo deben ser comparables; un ciclo diminuto no demuestra mejor economía del mismo gesto. La selección de basal —por ejemplo, postura de pie— necesita quedar explícita.

Hablar de eficiencia mecánica requiere además definir y estimar trabajo mecánico útil. En un movimiento cíclico, el trabajo neto puede acercarse a cero aun con actividad muscular y gasto metabólico significativos. En este primer diseño conviene hablar de economía metabólica de la tarea, no de “perfección energética”. Tampoco convertir entropía informacional a calorías mediante una equivalencia no demostrada.

Los bloques de VO2 no asignan automáticamente un gasto a cada segundo del video: hay cinética fisiológica y retardo instrumental. Un instante que parezca especialmente armónico puede estudiarse cinemáticamente, pero no etiquetarse con el consumo de oxígeno de ese mismo segundo sin un modelo validado.

## Anotación de experiencia y estética

Después de cada bloque, Nico puede puntuar de 0 a 10 facilidad, esfuerzo percibido, absorción, placer, conexión corporal y sensualidad vivida, cada una por separado, con anclajes escritos. Son ítems exploratorios propios; no llamarlos escala validada de flow. Para una medida establecida, seleccionar una escala de estado apropiada y verificar versión española, condiciones de uso y adecuación a bloques cortos.

Registrar además, con preguntas abiertas, cambios en percepción del tiempo, límites corporales o relación con el entorno. No sugerir que debería haber orgasmo o una experiencia mística; recogerlos si aparecen espontáneamente. La ausencia también importa.

Evaluadores externos ven clips de duración y encuadre equivalentes, a velocidad real, sin música añadida, sin conocer sensores, condiciones ni elecciones de Saira. Un pequeño panel inicial de 3–5 personas sirve para explorar desacuerdo, no para establecer belleza universal. Separar belleza, sensualidad, fluidez y esfuerzo aparente. La selección de Saira puede conservarse como anotación de una evaluadora identificada, no como etiqueta fisiológica verdadera.

Usar una muestra sistemática de todos los bloques, incluyendo fragmentos ordinarios. Se pueden añadir los momentos destacados por Saira o Nico como una capa exploratoria. No elegir todo el conjunto de análisis a partir del resultado que se desea explicar.

## Análisis e interpretación

Separar sesiones de exploración y de confirmación; no repartir cuadros contiguos entre entrenamiento y evaluación. La unidad de evidencia sigue siendo una persona con bloques agrupados por sesión. Miles de frames no equivalen a miles de participantes.

Analizar asociaciones dentro de un patrón comparable, considerando cadencia, amplitud, fatiga, orden, práctica, música y calidad de señal. Describir magnitudes, incertidumbre y resultados por sesión; modelar dependencia temporal o remuestrear por bloques/sesiones cuando el tamaño lo permita. No prometer significación con el número de sesiones sugerido.

Para evaluar una representación HIT, contrastar un modelo simple con el mismo modelo más los descriptores relacionales, evaluando en días no usados para ajustar parámetros. Incluir controles de señales que conserven propiedades individuales pero rompan la relación temporal pertinente. Una simple traslación temporal no destruye necesariamente el bloqueo de fase de dos oscilaciones estacionarias; comprobar que cada control rompe lo que pretende romper.

## Relación futura con Beacon y con otras personas

Primero evaluar las asociaciones sin feedback. Después comparar, con orden contrabalanceado, silencio, sonificación contingente y reproducción no contingente de sonido comparable. Así se distingue la contribución de oír sonido de la contribución del vínculo en tiempo real. Conservar los datos originales: una sonificación placentera no valida la fisiología que representa.

La extensión a pareja requiere registrar cada cuerpo y sus experiencias, además de separar coordinación interpersonal de la sincronización común con música o consigna. Ese contraste no está resuelto por estudiar una sola persona.

Antes de registrar a Nico, acordar participación, uso de video e imágenes, posibilidad de detenerse y destino de los datos; evaluar con el equipo de investigación los requisitos éticos de la institución y de la publicación elegida. Esta propuesta documental no declara que esos pasos ya ocurrieron.

## Forma del primer paper

Título provisional: “Coordinación temporal, economía metabólica y experiencia de fluidez durante rope flow: diseño de un estudio exploratorio de caso único”.

Antes de datos: artículo conceptual y protocolo, con hipótesis, fuentes, medidas y análisis previsto. Después de datos: estudio de factibilidad/caso único, con calidad de captura, asociaciones y límites; resultados redactados a partir de mediciones reales. No presentar un espacio de resultados vacío como si fuera un descubrimiento ya obtenido.

El puente más defendible hacia HIT es comprobar si las relaciones aportan capacidad explicativa adicional. La convergencia entre energía, belleza y experiencia sería un hallazgo a establecer, no una condición para admitir los datos.
