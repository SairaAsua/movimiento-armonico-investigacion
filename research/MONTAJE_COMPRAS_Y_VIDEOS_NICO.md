# Montaje propuesto, compras e inventario inicial de videos de Nico

**Versión de planificación, 24-09-2026.** A pedido de Saira, por ahora se deja definido **cómo sería** el estudio: no se instala HarMoCAP/Beacon, no se convoca a Nico ni se compra equipo desde esta nota. Saira ya cuenta con unas cuatro Reolink, unas cuatro «logicam» y un Moto G; modelos, modos de grabación y archivos originales aún no se identificaron. Los videos existentes se pueden reunir mediante **un catálogo de rutas y procedencia**, sin mover los originales ni llamar dato cinemático a un montaje narrativo.

## La idea en una frase y el orden de ejecución

Observar a Nico hacer figuras habituales de rope flow y preguntar si una descripción reproducible del **recorrido espacial inspirada en Laban** y una descripción **temporal de relaciones entre señales propuesta desde HIT** explican algo de la experiencia informada y de la percepción estética, por encima de patrón, velocidad y cadencia. Primero se valida qué se puede medir; sólo una fase posterior, con instrumento adecuado, pregunta por costo oxidativo o efecto causal del sonido Beacon. El [plan completo](PLAN_INVESTIGACION.md) y la [ficha de congelamiento](FICHA_CONGELAMIENTO_ESTUDIO.md) contienen decisiones y límites.

1. **Reunir material ya existente.** Inventariar videos originales sin editar, fecha aproximada, quién filmó, dispositivo, permiso de uso, duración, cuerpo/soga visibles, sonido, continuidad de vueltas y presencia de cortes. Mantener derivados de revisión separados del archivo original. Los clips existentes pueden elegir figuras habituales y probar visibilidad; sin calibración, reloj o permiso no demuestran 3D ni economía.
2. **Banco sin personas.** Usar una cámara de cada tipo, objeto de tamaño conocido, tablero de calibración y un evento luminoso visible al principio y final. Comparar originales, PTS, blur, cobertura y sincronía. El [banco sintético de fase intracíclo](BANCO_FASE_INTRACICLO_CAMARAS.md) ya prueba la lógica en archivo, no las cámaras físicas.
3. **Diseño con Nico.** Después de permiso y revisión ética aplicable, escoger una o dos figuras que Nico realmente haga; filmar intentos completos desde varias vistas fijas, incluyendo entradas, giros, errores y salidas. Registrar palabras de Nico sobre la experiencia por **bloque** y juicios visuales independientes por **clip**, con sus unidades separadas ([ficha de experiencia](FICHA_EXPERIENCIA_BLOQUE_V0.md)).
4. **Análisis y paper.** Medir error/cobertura de geometría Laban y fases antes de contrastar modelos `base → +Laban → +HIT` sobre los mismos días reservados. Si sólo hay 2D fiable, el artículo informa 2D y sus límites. Metabolismo y Beacon son fases posteriores con sus propios instrumentos y controles.

## Lista de compras por prioridad

No se recomienda comprar otra cámara ni sensores corporales antes de comprobar originales y óptica. Las cantidades siguientes son **para preparar un banco de dos o tres vistas**, no una orden de compra cerrada; revisar primero qué ya existe en casa.

| Prioridad | Cantidad orientativa | Elemento / especificación para pedir | Para qué sirve / cuándo comprar |
|---|---:|---|---|
| Preparar ahora si falta | 1 | **Tablero ChArUco o damero impreso mate**, fijado plano a soporte rígido, con cuadrado medido con regla; tamaño suficiente para verse nítido a la distancia de trabajo | Calibrar lente y relación entre vistas. OpenCV recomienda patrón plano, mate y de tamaño apropiado en píxeles; sus esquinas ChArUco permiten vistas parcialmente ocultas ([patrones](https://docs.opencv.org/5.0/tutorials/calib3d/camera_calibration_pattern/camera_calibration_pattern.html), [calibración ChArUco](https://docs.opencv.org/5.0/tutorials/objdetect/aruco_calibration/aruco_calibration.html)). Para el ejemplo OpenCap se usa damero A4 o mayor con cuadros ≥35 mm, medidos tras imprimir; **ese valor pertenece a su flujo**, no es umbral universal de nuestro montaje ([guía OpenCap](https://www.opencap.ai/best-practices)). |
| Preparar ahora si falta | 2–3 | **Soportes firmes** para las cámaras elegidas: trípodes, abrazaderas o fijaciones equivalentes; un soporte de teléfono para Moto G si participa | Evitar que el encuadre/calibración cambie entre tomas. En captura multivista las cámaras deben quedar fijas después de calibrar ([OpenCap](https://www.opencap.ai/best-practices)). Elegir rosca y alimentación según modelos reales, no comprar nueve soportes por la cantidad de cámaras disponible. |
| Preparar ahora si falta | 1 | **Cinta métrica o regla rígida** y marcas de suelo removibles; fondo mate contrastante si el espacio es visualmente cargado | Medir tablero, distancia y volumen; repetir ubicación de Nico y cámaras. Las marcas no convierten por sí solas el video en 3D. |
| Preparar ahora si falta | 1 | **Luz de sincronía visible** desde todas las vistas, accionable al inicio y al final, con eventos separados y no periódicos | Estimar desfase y deriva. Puede ser una lámpara/LED ya disponible; no comprar un sistema de disparo profesional antes de medir el error requerido. Guardar además PTS originales. |
| Condicional tras ver una muestra | 1–2 | **Luces continuas difusas** con alimentación estable y exposición controlable por la cámara elegida | Sólo si la soga/manos aparecen borrosas u oscuras. Antes de elegir modelo, probar luz existente, velocidad de obturación y si aparece parpadeo/banding. |
| Condicional tras estimar volumen de archivos | 1 | **Disco externo** con espacio suficiente y copia de resguardo independiente | Sólo si el almacenamiento disponible no alcanza para originales, hashes y copias. La capacidad se decide con minutos, bitrate y política de conservación reales; no fijar TB por intuición. |
| Posterior, con hipótesis e instrumental | — | IMU seleccionada, referencia de fuerza, sEMG o **acceso/alquiler de calorimetría indirecta** | No forman parte de la compra inicial. Cada uno responde a una variable distinta ([decisión de sensores](SENSORES_DECISION.md)); un reloj de pulso no reemplaza VO₂/VCO₂ para costo oxidativo. |

**Compatibilidad:** la ruta actual **OpenCap Multi-Camera** pide al menos dos dispositivos iOS; el Moto G informado es Android, así que no debemos comprar materiales suponiendo que entrará sin más en ese flujo ([requisitos oficiales](https://www.opencap.ai/get-started)). OpenCV y el análisis de archivos originales son una ruta de calibración propia que habrá que validar, no una garantía automática de precisión para rope flow.

## Videos existentes localizados y su uso

Se identificaron dos episodios audiovisuales **editados** sobre ideas de Nico, producidos con guion, tarjetas y voces sintéticas. No contienen movimiento corporal continuo de rope flow ni sirven como datos cinemáticos. No se encontraron en el material revisado originales confirmados de Nico haciendo soga. Los nombres, rutas, hashes y accesos a archivos personales quedan en el inventario local, fuera de GitHub.

Cuando Saira y Nico ubiquen originales, completar un catálogo **privado** de procedencia, permiso, duración, continuidad, visibilidad del cuerpo/manos/soga y tiempos por cuadro. No mover los medios crudos a este repositorio.

## Decisión pendiente antes de comprar más

Ver **un archivo original de cada tipo de cámara** y una muestra de los videos previos de Nico que Saira recuerde. Eso decide soportes compatibles, luz, almacenamiento y si conviene un piloto 2D o intentar 3D. Sin esa evidencia, la lista anterior es una preparación reversible y de bajo costo; no hay fundamento para comprar cámaras nuevas, IMU o equipo metabólico.
