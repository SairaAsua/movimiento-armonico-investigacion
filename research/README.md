# Rope flow, consonancia y experiencia corporal

Archivo local de investigación preliminar, iniciado el 23 de septiembre y actualizado el 24 de septiembre de 2026. Responde a la propuesta de Saira de estudiar a Nico haciendo rope flow y relacionar movimiento, economía, belleza, sensualidad y conciencia con HIT. No constituye un paper de resultados ni un protocolo ya ejecutado.

**Estado operativo:** Saira informó aproximadamente 4 Reolink, 4 «logicam» y 1 Moto G; faltan modelos, archivos originales y pruebas de tiempo/calibración. El [primer banco sin persona](PAQUETE_CAPTURA_NICO_V0.md) puede comparar una unidad de cada tipo antes de elegir montaje. El [estudio con Nico](PROTOCOLO_PILOTO_V0.md) todavía requiere repertorio real, consentimiento y determinación ética; metabolismo exige instrumentación propia. No hay captura, instalación live ni audio Beacon validados. La lectura integral de *Choreographie*/*Choreutics* continúa pendiente ([estado de fuentes](LABAN_ACCESO_OBRAS.md)).

**Preparación práctica sin captura nueva:** [montaje, lista de compras e inventario inicial de videos de Nico](MONTAJE_COMPRAS_Y_VIDEOS_NICO.md). Se identificaron episodios editados de contexto, pero todavía ningún original confirmado de Nico haciendo rope flow.

**Nueva fuente autoral mediada:** se leyó una traducción web de [ocho notas de Laban sobre ritmo](LABAN_NOTAS_RITMO.md). Permite fundamentar que su marco relaciona espacio, tiempo y fuerza; no proporciona una ecuación de eficiencia corporal ni reemplaza los libros pendientes.

**Fuente autoral impresa:** se leyó en alemán, mediante transcripción diplomática, [«Tanz und Musik» (1929)](LABAN_TANZ_UND_MUSIK_1929.md). Distingue frecuencia tonal y ángulo espacial, orientación central/periférica y desaconseja un mapeo pitch↔altura corporal; el facsímil no se cotejó y los libros completos siguen pendientes.

[Reseña de Brandt (1927)](LABAN_RESEÑA_BRANDT_1927.md): recepción muy cercana a *Choreographie* que relaciona icosaedro, espacio, tiempo, fuerza y escritura del recorrido; leída por OCR, no sustituye el libro de Laban.

[Auditoría de acuerdo LMA en datos públicos](LABAN_OSF_ACUERDO_REANALISIS.md): reanálisis descriptivo de respuestas originales de analistas certificados; límites de transferencia a rope flow.

[Economía en *Effort* (1947)](LABAN_EFFORT_ECONOMIA_1947.md): cotejo bibliográfico e histórico de Laban/Lawrence y Franco para no confundir eficiencia de tarea, facilidad vivida y gasto metabólico.

[Lectura de Quirarte Rojas (UNAM, 2017)](LABAN_QUIRARTE_UNAM_2017.md): tesis mexicana que cita la traducción de *Coreografía* y reúne láminas de geometría; guía el cotejo pendiente del libro sin reemplazarlo.

[Pérdida de información pitch–espacio](PITCH_ESPACIO_PERDIDA.md): [cálculo de grafo reproducible](pitch_espacio_grafo.py) que muestra qué relaciones no puede comunicar una nota cromática por vértice o un pitch dependiente sólo de altura en nuestra plantilla ideal; define una prueba perceptiva futura para Beacon.

[Situación del recorrido frente a orientación](LABAN_SITUACION_RECORRIDO.md): [banco sintético 3D](situacion_recorrido_sintetica.py) donde trayectorias con el mismo `Q` pasan por regiones distintas respecto del centro, más una [sensibilidad de marcos en CMU](cmu_situacion_marcos.py). Define medidas continuas candidatas y su límite de error, sin adjudicar etiquetas Laban ni resultados sobre Nico.

[Sobre científico sintético de `plane_normal_Q_live`](CONTRATO_Q_LIVE_V0.md): schema, fixture y validador que conservan definición de recorrido, cobertura, reloj, vencimiento e incertidumbre para una futura rama 3D de Beacon; la incertidumbre de CMU sigue `not_estimated`.

[Contrato científico sintético de `spacetime_c_live`](CONTRATO_C_LIVE_V0.md): schema, fixture y validador local para una salida causal con cobertura, relojes, procedencia y estado inválido; aún no es una extensión de HarMoCAP ni una prueba de audio.

[Descomposición del marco móvil](MARCO_MOVIL_DESCOMPOSICION_C.md): identidad exacta y banco CMU para cuantificar cuánto del recorrido co-rotante proviene del cambio de ejes; fija una comprobación necesaria antes de sonificar `C`.

[Sensibilidad del umbral de `C` al marco](CMU_UMBRAL_MARCO_VENTANA.md): Monte Carlo local que muestra que jitter angular hipotético puede aumentar la cobertura aparente y sesgar el valor aun cuando el gate pasa; delimita qué error debe medirse con las cámaras reales.

[Control factorial Laban–HIT](LABAN_HIT_FACTORIAL.md): trayectorias sintéticas separan plano, marginales de velocidad y relación de fase antes de una predicción o sonificación. [Banco de fase intracíclo para cámaras](BANCO_FASE_INTRACICLO_CAMARAS.md): prueba sin personas para ver si los archivos reales conservan la diferencia que una fase calculada sólo entre cierres de vuelta pierde.

[Sensibilidad de `Q_live` al marco corporal](CMU_Q_MARCOS_LIVE.md): misma toma y ventana con recorrido co-rotante o desplazamiento relativo sin giro de ejes; cuantifica la diferencia antes de sonificar.

[Replay causal de `Q_live` en CMU](CMU_Q_CAUSAL_PLANOS.md): cobertura de ventanas y diagnóstico de planitud local; muestra que alargar la ventana gana recorrido pero puede mezclar planos.

[Mapeo diagnóstico al contrato Beacon](BEACON_FACTORIAL_CONTROLES.md): cuatro pares `Q/R` generan vectores de ganancias distintos dentro de rangos reales de `beacon-spatial`; es prueba offline numérica, todavía sin ruta aplicada ni audio.

## Plan de punta a punta

[Sesgo de concentración de fase](FASE_SESGO_MUESTRAL.md): lectura primaria de Vinck et al. (2010), identidad de `PPC` y [contraejemplo ejecutable](fase_sesgo_muestral_sintetico.py) que muestra por qué copiar cuadros o subir FPS no agrega ciclos independientes.

[Plan metodológico centrado en Laban](PLAN_INVESTIGACION.md): lectura, geometría, sensores, validación, estudio, HarMoCAP, Beacon y paper. [Primera matriz Laban → mediciones](LABAN_MATRIZ.md): fuente, observación, descriptor propuesto y prueba de validez. [Matemática experimental](LABAN_MATEMATICA.md): coordenadas, recorridos, planos, poliedros, fases y validación. [Lectura crítica de Longstaff](LABAN_LECTURA_LONGSTAFF.md): secciones pertinentes del volumen I, experimentos y resultado nulo relevante. [Dirección y redes en Laban](LABAN_RED_Y_VECTOR.md): movimiento frente a ubicación y cuboctaedro frente a icosaedro. [Puente Laban–HIT](PUENTE_LABAN_HIT.md): hipótesis, frecuencias, fases y contrastes. [Fase de rope flow](FASE_ROPEFLOW.md): eventos de ciclo, métodos de fase, relaciones p:q y sus límites. [Búsqueda rope flow y vecinos](BUSQUEDA_ROPEFLOW_ADYACENCIAS.md): consultas reproducibles, falsos positivos y transferencia limitada desde poi. [Preparación de cámaras](CAMARAS_PREPARACION.md): inventario y criterios para decidir 2D/3D. [Decisión de sensores](SENSORES_DECISION.md): qué se puede afirmar con cámaras y qué exige IMU, calorimetría u otros instrumentos. [Piloto de validación de video](PILOTO_VALIDACION_VIDEO.md): errores, sincronización, oclusiones y decisiones por descriptor. [Tareas de rope flow](ROPEFLOW_TAREAS.md): vocabulario, frases y ciclos candidatos, pendientes de observar en Nico. [Experiencia y estética](EXPERIENCIA_ESTETICA.md): autoinformes de Nico, valoraciones visuales y contraste con cinemática/metabolismo sin fusionar constructos. [Integración HarMoCAP–Beacon](INTEGRACION_HARMOCAP_BEACON.md): archivo científico, contrato 1.4, extensión futura y pruebas hasta el audio. Incorpora cámaras disponibles, ausencia de instalación y especialistas aún por incorporar.

[Esqueleto del primer paper](ESQUELETO_PAIPER.md): alcance publicable, preguntas por unidad de análisis, secciones redactables, figuras/tablas sin resultados ficticios y guías de reporte pertinentes.

[Ficha de congelamiento del primer estudio](FICHA_CONGELAMIENTO_ESTUDIO.md): decisiones y evidencia que se fijarán tras el piloto, antes de abrir días reservados; todavía es plantilla, no prerregistro.

[Borrador de Introducción y Métodos](BORRADOR_INTRO_METODOS_PAIPER.md): prosa inicial del artículo metodológico con citas trazables, definiciones nuevas separadas de Laban y campos que sólo se completarán al validar las cámaras y observar el repertorio de Nico.

[Cobertura y selección del video](COBERTURA_SELECCION_VIDEO.md): registro de todos los intentos, validez por descriptor y análisis del sesgo posible cuando giros y cruces quedan fuera de los clips reconstruibles.

[Misma trayectoria, distinto ritmo](GEOMETRIA_VS_TIEMPO_TRAYECTORIA.md): diferencia entre ponderar por cuadros y por longitud de recorrido, con [contraejemplo sintético ejecutable](geometria_tiempo_sintetica.py) para separar geometría Laban y tiempo HIT.

[Acople espacio–tiempo](ACOPLE_ESPACIO_TIEMPO.md): misma curva y mismos marginales de rapidez/aceleración, pero acento en regiones corporales opuestas; incluye [control sintético](espacio_tiempo_acople_sintetico.py) y un descriptor condicional a validar antes del piloto.

[Factibilidad del acople con cámaras](ACOPLE_CAMARA_FACTIBILIDAD.md): simulación proyectada con FPS, tamaño de gesto, ruido y pérdida de cuadros hipotéticos; incluye [script reproducible](acople_camara_sintetico.py) y criterios para el banco técnico real.

[AIST++ como banco externo](AIST_BENCHMARK_ALCANCE.md): fuente primaria y estudio de clasificación de géneros; precisa qué puede probar con articulaciones 3D, por qué sus 60 fps no certifican fase física y qué condiciones de acceso faltan antes de usar datos.

[CMU danza moderna, banco humano externo](CMU_DANZA_BANCO_REAL.md): una toma C3D oficial de 1.123 cuadros a 120 Hz procesada con [script auditable](cmu_danza_05_02_audit.py); prueba marco corporal, recorrido de marcadores y sensibilidad del contraste a la definición de «muñeca», sin extrapolar a Nico.

[Replay causal del acople en CMU](ACOPLE_CAUSAL_REPLAY.md): [script reproducible](cmu_causal_c_replay.py) con escala fijada al primer segundo, ventanas retrospectivas y estados sin valor cuando falta una región; cuantifica cobertura y verifica que truncar el futuro no cambia el pasado, sin reclamar audio live.

[Contraste `C` según el marco de movimiento](CMU_MARCOS_C_CONTRASTE.md): con las mismas regiones delante/detrás, la toma CMU invierte el signo izquierdo si se compara recorrido co-rotante con recorrido centrado en cintura; obliga a predefinir marco y a medir error de orientación.

[Ruido temporal del marco corporal](CMU_ORIENTACION_RUIDO.md): [Monte Carlo reproducible](cmu_orientacion_sensibilidad.py) sobre CMU con errores angulares hipotéticos independientes, correlacionados o constantes; muestra por qué el banco de cámaras debe medir jitter y retardo, no sólo error angular medio.

[Filtrado causal del marco](CMU_FILTRO_MARCO_CAUSAL.md): [replay reproducible](cmu_filtro_marco_causal.py) de una media retrospectiva de orientaciones con ruido hipotético; separa reducción de jitter, cambio de `C` y atraso durante giros antes de diseñar la señal Beacon.

[Simetrías y escala de doce en White (2020)](LABAN_SIMETRIAS_Y_ESCALAS.md): lectura visual de las figuras del preprint, secuencia explícita de direcciones y prueba de que las veinte rutas antipodales son rotaciones de una sola forma. Incluye [chequeo sintético](simetrias_laban.py); la atribución histórica a Laban y la aplicabilidad a rope flow siguen pendientes.

[Ciclos, transiciones y frases](FRASES_TRANSICIONES_SEGMENTACION.md): tres capas de segmentación con fuentes experimentales; preserva el orden espacial de transiciones sin asignar fase periódica donde no corresponde. Incluye [control sintético de orden](frases_orden_sintetico.py).

[Experiencia en primera persona](EXPERIENCIA_PRIMERA_PERSONA.md): autoinforme inmediato por bloque y posible entrevista de episodios singulares, con límites de memoria, sugestión y alineación temporal. [Ficha de experiencia por bloque](FICHA_EXPERIENCIA_BLOQUE_V0.md): guion neutral provisional y campos de factibilidad para probar comprensión sin confundir vivencia, video y fisiología.

[Cadena de consonancia, belleza y economía](CADENA_CONSONANCIA_BELLEZA_ECONOMIA.md): regla de comparación conjunta por bloques realmente comparables, pares concordantes/discordantes e inferencias observacionales frente a causales.

[Transiciones y reset en Beacon](BEACON_TRANSICIONES_Y_RESET.md): reproducción aislada de que `suppress` deja el último control enviado mientras `reset` emite el default; define el gate para que la fase no siga sonando como válida durante cambios de figura.

[Ensayo de contingencia Beacon](ENSAYO_BEACON_CONTINGENCIA.md): diseño posterior de efecto inmediato, aprendizaje y retención sin sonido, apoyado en tres experimentos originales de sonificación con resultados favorables y nulos.

[Diseño de caso único y guías de reporte](CASO_UNICO_DISENO_REPORTE.md): separa la observación intensiva de Nico de un ensayo N-of-1 y decide cuándo SCRIBE o CENT podrían corresponder; advierte sobre el arrastre de aprendizaje en Beacon.

[Prueba aislada del kit HarMoCAP](HARMOCAP_KIT_PRUEBA_AISLADA.md): replay/codec/handshake/UDP sintético verificados sobre el commit auditado; delimita qué sigue sin probar en Beacon, cámaras y geometría.

[Gating del receptor de referencia](HARMOCAP_GATING_CONTRATO.md): [regresión reproducible](probar_gating_harmocap.py) que detectó aceptación de frames con generación o contrato no coincidentes pese al handshake previo; criterio pendiente para el receptor Beacon real.

[Protocolo piloto 0.1](PROTOCOLO_PILOTO_V0.md): primer estudio instrumental centrado en Laban, etapas sin datos humanos/observación/evaluación reservada, referencias por descriptor y reglas de paso. Es un borrador para revisión, aún no preregistrado.

[Paquete de captura para Nico](PAQUETE_CAPTURA_NICO_V0.md): secuencia de banco técnico, consentimiento, sesiones e intentos completos con relojes por cámara y archivo privado. Incluye [inspector de video](inspeccionar_video.py) probado con clip sintético y PTS ausente; calcula intervalos sólo entre cuadros contiguos fechados y no se aplicó a cámaras o videos humanos.

[Sincronía multivista](SINCRONIA_MULTICAMARA.md): lectura de un método primario con destellos y obturador rodante, ajuste limitado de desfase/deriva y criterios para no llamar fase confiable a videos mal alineados. Incluye [ajustador de eventos](ajustar_relojes.py) probado con datos sintéticos, sin cámaras reales.

[Estimandos y contrastes por fase](ESTIMANDOS_Y_CONTRASTES.md): qué compara cada unidad, secuencia predictiva base → Laban → HIT, prueba metabólica condicionada y resultados que no apoyarían la hipótesis.

[Effort, estabilidad y economía](EFFORT_ECONOMIA_CONTRASTES.md): distingue cualidad de movimiento en Laban, esfuerzo percibido y costo metabólico; tres experimentos de coordinación muestran por qué no se pueden equiparar.

[Auditoría de Chang 2026](CHANG_2026_AUDITORIA.md): alcance del resumen sobre belleza, coordinación y «economía» en danza latina, con método pendiente de lectura por restricción de acceso al PDF.

[Orden de componentes en las inclinaciones de Laban](LABAN_ORDEN_COMPONENTES.md): verifica qué información contienen los 24 nombres históricos y por qué nuestro descriptor de 24 clases no los reproduce.

[Identificabilidad de la soga](SOGA_IDENTIFICABILIDAD.md): contraejemplo geométrico y decisión sobre mano, curva de soga y evento de tarea con una o varias cámaras.

[Seguimiento de soga flexible, fuentes DLO y DOT](SOGA_VISION_DLO_FUENTES.md): separa reconstrucción de figura, topología e identidad de puntos materiales; examina la estructura documentada del dataset DOT y propone un benchmark externo de dos/cuatro vistas, seguido del banco técnico propio antes de incorporar `rope_3d_curve` o `rope_material_track`.

[Procedencia de fases y circularidad](FASE_PROCEDENCIA_CIRCULAR.md): evita que dos copias del reloj de soga produzcan una falsa relación HIT perfecta.

[Balance energético de la soga](ENERGIA_SOGA_BALANCE.md): distingue energía de la curva, trabajo de los agarres y metabolismo; decide cuándo haría falta fuerza instrumentada.

[Dominio de validez de calorimetría](CALORIMETRIA_DOMINIO_VALIDEZ.md): separa costo oxidativo por bloque de gasto metabólico total en frases intensas/intermitentes y condiciona la incorporación de sensores al patrón real.

[Moore y la armonía como analogía](MOORE_ARMONIA_ANALOGICA.md): delimita lo que una investigadora de manuscritos de Laban afirma en la presentación de su libro y evita equiparar literalmente coreútica, frecuencia corporal y HIT.

[Ruta HarMoCAP → Weaver → beacon-spatial](RUTA_HARMOCAP_WEAVER_BEACON.md): contratos y código público actual, límite del MVP sin audio live y alias `kinetic_energy` que no representa energía física.

[Prueba aislada del driver Weaver](WEAVER_DRIVER_PRUEBA_AISLADA.md): 12 pruebas del enlace con fixtures y control adverso de generación/contrato; sólo llega al transporte de registro, no al audio.

[Contrato real de Beacon en Weaver, offline](WEAVER_BEACON_CONTRATO_OFFLINE.md): escena sintética HarMoCAP→`/beacon/gain/4` compilada con manifiesto auténtico, aún sin OSC/audio.

[Bandas de Beacon y frecuencias corporales](BEACON_BANDAS_NO_FRECUENCIAS_CORPORALES.md): verifica que 40/80/120 Hz son centros de filtros de un audio de entrada, no tonos ni vibraciones corporales garantizadas.

[Guía piloto de anotación Laban](ANOTACION_LABAN_PILOTO.md): capas de observación y lectura experta para rope flow, reglas de codificación, cegamiento, acuerdo entre especialistas y límites de las cámaras. Es diseño pendiente de revisión humana, no una validación realizada.

[Validador de linaje](validar_linaje.py) y [manifiesto sintético](manifiesto_ejemplo_sintetico.json): comprueban la unión estructural anotación→clip→bundle→vistas originales y rango de reloj. El ejemplo no contiene medios reales; pasar el validador no prueba la integridad física de un video ni validez de su geometría.

[Antecedentes de automatización Laban](AUTOMATIZACION_LABAN_ANTECEDENTES.md): comparación de tres estudios originales según repertorio, sensores, referencia y partición de prueba; delimita qué rasgos se pueden probar y por qué sus modelos no validan la coreútica de rope flow.

[Poi, notación y feedback](POI_ADYACENCIA_Y_TRANSFERENCIA.md): lectura completa de un ensayo poi y un prototipo audiovisual, más vocabulario comunitario de tiempo/dirección; precisa cómo usarlos sin confundir poi con la soga continua de Nico.

[Diccionario provisional de señales](DICCIONARIO_SENALES_V0.md): definiciones, unidades, marcos, estados inválidos, propagación de error y prueba necesaria para pasar de video a descriptores Laban/HIT. No modifica el contrato OSC de HarMoCAP.

[Controles de ritmo común](CONTROLES_RITMO_COMUN.md): cuándo una fase estable puede deberse al ciclo compartido, qué comparaciones responden a HIT y por qué desplazar una señal periódica no es un nulo suficiente. Incluye dos casos nuevos en el banco sintético.

[Predicciones HIT escalonadas](HIT_PREDICCIONES_ESCALONADAS.md): distingue organización temporal, recurrencia informativa, robustez ante cambios, carga correctiva y experiencia; especifica qué prueba cada fase y qué no puede concluirse del primer piloto.

[Predicción HIT sin fugas](HIT_PREDICCION_SIN_FUGAS.md): fija corte temporal y sesiones reservadas, distingue ganancia de representación de información sensorial nueva e incluye un [banco sintético](prediccion_relacional_sintetica.py).

[Identificabilidad de 2D/3D](IDENTIFICABILIDAD_2D_3D.md): dos recorridos 3D diferentes con la misma imagen, reglas para llamar proyectada a una variable y requisitos de multivista. Incluye un [contraejemplo ejecutable](proyeccion_2d_ambigua.py) sin datos humanos.

[Presupuesto de error de cámaras](PRESUPUESTO_ERROR_CAMARAS.md): cuantización de evento por cuadro, desfase de reloj y barrido por exposición como errores distintos; incluye una [calculadora de escenarios](presupuesto_camara.py).

[Presupuesto espacial estéreo](PRESUPUESTO_ESPACIAL_ESTEREO.md): relación entre línea base, focal, distancia y error de profundidad/dirección, con [simulación reproducible](estereo_sintetico.py) y reglas para ensayar el montaje físico.

[Presupuesto de error de `Q`](PRESUPUESTO_ERROR_Q.md): cotas separadas para ángulo del recorrido/marco, pesos por longitud y recorrido oculto; decide cuándo una diferencia entre bloques queda determinada sin convertir `Q` en escala de consonancia.

[Contraste geométrico de redes](REDES_CONTRASTE_GEOMETRICO.md): marcos espaciales, sesgos basales de cuboctaedro/icosaedro y reglas de comparación; incluye un [script reproducible de comprobación](redes_sanity.py) sin datos humanos.

[Control nulo circular](REDES_NULO_CIRCULAR.md): círculos sintéticos muestran que cercanía a vértices y ventaja de una red pueden aparecer sin una escala coreútica, y cuantifican el optimismo de girar plantillas por clip; incluye [script](redes_circulos_nulos.py).

[Banco de trayectorias sintéticas](TRAYECTORIAS_SINTETICAS.md): casos de posición frente a dirección, marcos corporal/sala, recorrido completo e invalidez por error; incluye [script ejecutable](trayectoria_sintetica.py), sin datos humanos.

[Giro global y torsión local](GIRO_TORSION_IDENTIFICABILIDAD.md): contraejemplo reproducible en que la mano recorre exactamente la misma curva en sala aunque el cuerpo gire entero o sólo el tórax sobre la pelvis; delimita las señales 3D requeridas y cuándo declarar el descriptor inválido.

[Banco sintético de fase](FASE_BANCO_SINTETICO.md): doble conteo de rapidez, transiciones sin fase, relaciones 2:1 y 1:1, y sesgo por retardo; incluye [script ejecutable](fase_sintetica.py), sin datos humanos.

[Estimadores de fase con perturbaciones](FASE_ESTIMADORES_BANCO.md): [comparación ejecutable](fase_estimadores_sinteticos.py) entre Hilbert offline y posición–velocidad causal con cambio de cadencia, forma asimétrica, ruido, amplitud baja, hueco y un control explícito de fuga futura.

[Longstaff 2001, texto completo](LABAN_VECTOR_LONGSTAFF_2001.md): figuras de símbolos de vector, contraste línea/posición, situación central/periférica/transversal e implicaciones operacionales. [Acceso a las obras originales](LABAN_ACCESO_OBRAS.md): ediciones y páginas de Laban aún por cotejar.

[*The Laban Sourcebook*, vista previa](LABAN_SOURCEBOOK_VISTA_PREVIA.md): introducción y figuras de 1926 reproducidas por McCaw, con distinción entre palabra autoral mediada e interpretación editorial; los capítulos de *Choreography*, *Choreutics* y *The Harmony of Movement* no están en la muestra.

[Tres planos y proporción del icosaedro](PLANOS_RECTANGULOS_ICOSAEDRO.md): deriva la condición áurea que distingue un icosaedro regular de otros doce puntos distribuidos en tres planos ortogonales, con [chequeo sintético](rectangulos_icosaedro.py). Esta condición matemática es nuestra, no una ecuación atribuida a Laban.

[Espejo, orientación y fase](ESPEJO_ORIENTACION_FASE.md): control instrumental del convenio de coordenadas sin espejo de HarMoCAP; muestra por qué el reflejo invierte giro y desfase firmado sin alterar distancias, con [prueba sintética](espejo_orientacion_sintetico.py).

[24 inclinaciones y 26 direcciones](LABAN_24_INCLINACIONES.md): contraste de Longstaff 2018, la retícula de 45° explícita en el manual de Fügedi 2016 y el icosaedro; distingue fuente histórica, convención angular y clasificador propio. Incluye [sensibilidad sintética de 26 direcciones](direcciones_26_sintetico.py).

[Margen angular de clasificación](MARGEN_ANGULAR_INCLINACIONES.md): derivación y [banco sintético](margen_orientacion.py) para saber cuándo una etiqueta exploratoria de orientación resiste el error 3D y cuándo debe quedar incierta.

[Fase causal para Beacon](FASE_CAUSAL_BEACON.md): separa interpolación retrospectiva de predicción en vivo y contiene un [banco sintético](fase_causal_sintetica.py) con aceleración, cruce ausente y protección contra datos futuros.

[Armonía histórica en Laban](LABAN_ARMONIA_HISTORICA.md): lectura completa de Franco 2020, identificación del libro de Moore y corrección clave: contraste/disonancia forman parte de su reconstrucción de armonía; el banco de doce vértices no reconstruye las 26 direcciones descritas allí.

[El minueto y los tres planos](LABAN_MINUETO_PLANOS.md): lectura completa de Longstaff, Treu y Royston 2007; separa el capítulo de 1926 de la reconstrucción por entrevistas y partituras, y motiva describir transiciones de plano en frases de rope flow.

[Identificabilidad de planos](IDENTIFICABILIDAD_PLANOS.md): PCA 3D propuesta para curvas, con condiciones de orientación estable y contraejemplo de línea casi recta que aparenta transición de 90°; incluye [banco sintético ejecutable](planos_sinteticos.py) sin datos humanos.

[Contraste estructurado frente a consonancia constante](CONTRASTE_ESTRUCTURADO.md): lectura completa del experimento de Orlandi 2020 y propuesta de descriptores rivales de estabilidad, contraste y salida–retorno, con controles de velocidad, duración y tarea.

[Matriz de atribución de Laban](COTEJO_AFIRMACIONES_LABAN.md): evidencia autoral disponible, lectura de Longstaff, fórmulas nuevas del proyecto y reglas de cita para el primer paper.

[Archivo de Leipzig](LABAN_ARCHIVO_LEIPZIG.md): manifiestos IIIF, dos manuscritos catalogados con autoría de Laban, dibujos icosaédricos conservados en su fondo y límites de atribución. [Lectura del manuscrito sobre movimiento humano](LABAN_MANUSCRITO_DIRECCIONES.md): combinaciones direccionales, dibujo geométrico, palabras inseguras y consecuencias para nuestros descriptores.

[Lectura de 70 lienzos icosaédricos](LABAN_ICO_ARCHIVO_70.md): mapa visual del conjunto completo en miniatura, 18 lienzos ampliados, fórmula visible de conteo de aristas y límites de transcripción/autoría.

[Cribado de «Alles ist Bewegung»](LABAN_ALLES_IST_BEWEGUNG.md): catorce lienzos de notas catalogadas con Laban como autor, mezcla de temas y decisión de no usarlas como ecuación de consonancia.

Ampliación metodológica: [revisión](agent_reports/05_metodologia_revision.md), [auditoría directa HarMoCAP](agent_reports/06_harmocap_auditoria.md) y [validación/diseño](agent_reports/07_validacion_diseno.md).

## Cómo leer

- [Planteo original y aclaración del usuario](USER_BRIEF.md): intención de la investigación preservada.

- [Informe narrado](NARRATED_REPORT.md): explicación del argumento y sus límites.
- [Síntesis](SYNTHESIS.md): hallazgos principales.
- [Borrador histórico de protocolo](PROTOCOL_DRAFT.md): formulación inicial amplia, sustituida para la primera fase por el protocolo piloto 0.1.
- [Informe cruzado](CROSS_REPORT.md): mapa trazable para recuperar contexto.
- [Bibliografía](BIBLIOGRAPHY.md): referencias y nivel de lectura.
- [Manifiesto de revisión](agent_reports/MANIFEST.md): alcance, procedencia y leyenda.

## Revisiones independientes

1. [Movimiento, Laban, fase y estética](agent_reports/01_movimiento.md).
2. [Fisiología e instrumentación](agent_reports/02_medicion.md).
3. [Conciencia, Kaparo y Michael Levin](agent_reports/03_conciencia.md).
4. [HIT y memoria de HarMoCAP](agent_reports/04_hit.md).

Se realizaron cuatro revisiones mediante agentes colaboradores; hasta tres corrieron simultáneamente y la cuarta después. El agente coordinador integró fuentes, aclaraciones del usuario y propuestas. Reportes originales preservados; no son cuatro experimentos independientes ni validación por consenso.

## Fuentes internas

[Extractos HIT](sources/HIT_extractos.md) con atribución CC BY 4.0 y [snapshot HarMoCAP](sources/HarMoCAP_snapshot.md). Se consultó también documentación de memoria colectiva mediante Drive; no se accedió a su índice vivo. No atribuir a este entorno el funcionamiento descrito en otra instalación.

Skill aplicada: [multi-agent-research](https://drive.google.com/file/d/1wcgaN_YCk3hqqtmlvyg3T5IIAGhXdwUK/view). Ruta local de archivo ya autorizada. Se conserva el formato documental sin trackers locales. Se entregan Markdown; no se generó PDF, pues no se encontró toolchain LaTeX/Pandoc y el usuario no pidió ese formato.

## Lectura central

La hipótesis es investigable si sus dimensiones se miden por separado. La conexión con HIT más concreta es preguntar si las relaciones aportan capacidad explicativa adicional. La equivalencia entre armonía, belleza, economía y estados de conciencia permanece abierta.

No hubo captura humana, entrenamiento de modelos, publicación externa ni ejecución de servicios. El directorio está excluido de Git, dentro del archivo local previamente acordado.
