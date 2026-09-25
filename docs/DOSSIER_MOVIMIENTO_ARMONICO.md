# Movimiento armónico, experiencia y sonido
## Investigación del equipo de Harmonic Beacon sobre movimiento y sonido

**Versión de presentación · 24 de septiembre de 2026**
**Estado:** propuesta metodológica y banco sintético reproducible. No hay aún resultados experimentales del caso principal.

### La pregunta

Queremos saber si ciertas maneras de organizar un movimiento de rope flow se relacionan con una experiencia vivida de fluidez o consonancia, con su belleza y sensualidad percibidas, y con menor costo fisiológico para **una tarea comparable**. Una hipótesis del programa plantea que en ciertos momentos puede haber una reorganización corporal y subjetiva extraordinaria. Esta hipótesis orienta preguntas; no se usará como etiqueta anticipada de los videos ni como resultado ya demostrado.

El primer estudio será un caso intensivo de rope flow. El alcance inicial es **otra sesión de la misma persona realizando figuras comparables**, no todas las personas ni todas las danzas. Primero averiguaremos qué se puede observar de verdad con las cámaras disponibles; después probaremos asociaciones en sesiones nuevas; finalmente estudiaremos si escuchar el movimiento mediante Beacon cambia la ejecución o la experiencia.

### Qué tomamos de cada marco

| Referencia | Elemento útil | Traducción al estudio | Límite que cuidaremos |
|---|---|---|---|
| **Rudolf Laban** | Space Harmony/Choreutics: kinesfera, dirección, planos, recorridos, secuencias; Effort como vocabulario cualitativo. | Describir trayectorias de mano/cuerpo, ubicación frente a dirección de movimiento, continuidad y organización espacial. Una persona formada en Laban revisará anotaciones y categorías. | Nuestras ecuaciones de trayectoria son operacionalizaciones actuales, **no ecuaciones históricas de Laban**. Sus libros *Choreographie* y *Choreutics* siguen pendientes de lectura integral. |
| **Harmonic Information Theory (HIT)** | Hipótesis de relaciones simples, fase, recurrencia, estabilidad y procesamiento de patrones. | Predicciones temporales concretas: después de controlar cadencia, rapidez y geometría, ¿una relación entre señales independientes anticipa mejor el siguiente ciclo o una respuesta externa? | Las conjeturas de menor costo y sensibilidad biológica no están validadas en rope flow. Fase estable tampoco significa por sí sola placer o eficiencia. |
| **Risa F. Kaparo** | Atención somática y vocabulario de sensación, respiración y movimiento. | Preguntas neutrales a la persona participante inmediatamente después de cada bloque sobre facilidad, placer, atención, esfuerzo y continuidad vivida. | Es una guía para escuchar la primera persona, no un biomarcador ni evidencia de un estado místico. La obra completa aún no fue cotejada. |
| **Michael Levin** | Organización y control bioeléctrico multiescala en otros sistemas biológicos. | Pregunta futura sobre adaptación y reorganización ante perturbaciones; separar nivel celular, neural y cinemático. | Sus resultados en morfogénesis no prueban bioelectricidad celular específica ni conciencia elevada durante rope flow. ECG/EMG, si se agregan, miden otras señales. |
| **Práctica de rope flow y Harmonic Weaver** | Repertorio corporal real; coautoría de HIT; router de fuentes hacia instrumentos. | Elegir figuras que la persona participante realmente practica, formular predicciones HIT y preparar sonificación trazable de señales validadas. | El software transporta controles; no decide por sí mismo qué es bello, eficiente o consciente. |

### Qué queremos probar, en orden

**1. Identificabilidad instrumental.** ¿Podemos recuperar de videos originales la posición y el recorrido de manos y cuerpo, distinguir plano y giro, contar ciclos y estimar fase dentro del ciclo? Compararemos cada descriptor con marcas independientes, visibilidad, error y cobertura. Si una cámara sólo ofrece 2D confiable, diremos 2D.

**2. Aporte espacial de Laban.** En sesiones reservadas completas, compararemos un modelo base de patrón, cadencia, rapidez y amplitud con el mismo modelo más descriptores espaciales inspirados en Laban. Una mejora fuera de desarrollo apoyaría su utilidad descriptiva o predictiva, sin certificar todavía una teoría estética.

**3. Aporte relacional de HIT.** Sobre las mismas unidades y sin usar información futura, añadiremos desfase, concentración de fase y recurrencia entre señales identificadas por separado. Preguntaremos si aportan algo por encima de la base y de Laban. Un pulso musical común o el mero cierre simultáneo de vueltas son explicaciones alternativas obligatorias.

**4. Experiencia y estética.** La persona participante informará por bloque qué sintió sin escuchar una respuesta sugerida. Evaluadores independientes verán clips completos, elegidos sin seleccionar sólo los más bellos, y puntuarán belleza, sensualidad, fluidez y esfuerzo aparente. La vivencia de la persona participante y el juicio de terceros son dos resultados distintos.

**5. Economía y Beacon.** Sólo con acceso a calorimetría indirecta y bloques fisiológicamente interpretables contrastaremos costo **oxidativo**; video, pulso o el proxy cinemático `kinetic_energy` no lo sustituyen. La intervención Beacon será otro estudio: sonido contingente frente a controles, con audio efectivamente grabado, latencia medida y posible aprendizaje o deterioro evaluados.

La cadena fuerte «consonancia → belleza → sensualidad → menor costo → estado extraordinario» se tratará como un conjunto de relaciones separables. Si alguna falla, el resultado sigue siendo informativo.

### Lo que ya verificamos con datos sintéticos

Generamos **960 filas**, cuatro condiciones de ocho segundos a 30 cuadros/s: dos planos de recorrido de la mano derecha (lateral–anterior y lateral–vertical) cruzados con dos relaciones temporales entre manos (alineada y opuesta). Las condiciones temporales mantienen para cada mano ocho vueltas, duración, recorrido, longitud y distribución de rapidez; cambia el emparejamiento de los avances dentro de cada vuelta.

| Plano | Relación | Q lateral/anterior/vertical | R de fase continua | R sólo con cierres de vuelta |
|---|---|---|---:|---:|
| lateral–anterior | alineada | 0,500 / 0,500 / 0,000 | 1,000 | 1,000 |
| lateral–anterior | opuesta | 0,500 / 0,500 / 0,000 | 0,077 | 1,000 |
| lateral–vertical | alineada | 0,500 / 0,000 / 0,500 | 1,000 | 1,000 |
| lateral–vertical | opuesta | 0,500 / 0,000 / 0,500 | 0,077 | 1,000 |

`Q` es un descriptor **propuesto** de distribución de direcciones del recorrido; `R` es concentración de una relación de fase, no un puntaje de bondad. El control revela un riesgo real de diseño: si sólo marcamos cuándo termina cada vuelta, el algoritmo devuelve `R=1` en ambas condiciones y pierde la diferencia intracíclo. El código, CSV, resultados y cuatro audios de demostración están en `../research/datos_sinteticos_presentacion/`. Los sonidos son una traducción diagnóstica de curvas fabricadas; **no son audio live de Beacon ni prueban belleza, metabolismo o conciencia**.

### De un video de baile al sonido, y después al caso principal

La primera demostración audiovisual usará un video de baile **con licencia/permiso y archivo original** donde se vean claramente cuerpo y ritmo. Conservaremos original, tiempos por cuadro y condiciones de uso. Extraeremos pose y calidad con HarMoCAP u otra herramienta contrastada; corregiremos manualmente una muestra; calcularemos en análisis offline un descriptor espacial y uno temporal que superen el control sintético y el de cámara. Cada señal llevará unidad, ventana, latencia, incertidumbre y estado `observed/held/invalid`.

Una escena versionada en Harmonic Weaver enviará esos dos canales a controles separados del instrumento Beacon; registraremos señal, transformación, control aplicado y audio grabado. Compararemos el audio con controles donde se permuta el plano o la fase sin cambiar las otras entradas. Si las dos condiciones no se distinguen en la salida, el mapeo perdió información y debe corregirse. La demo de baile prueba la **cadena técnica**, no la hipótesis del estudio. Sólo después se usará un video original consentido de rope flow y, más adelante, feedback en vivo durante el movimiento.

### Qué necesitamos

**Ya disponible:** aproximadamente cuatro Reolink, cuatro cámaras «logicam» y un Moto G; repositorios HarMoCAP, Harmonic Weaver y Beacon; protocolo y bancos sintéticos. **Para el banco físico:** comprobar modelos/archivos originales; tablero ChArUco o damero mate rígido, dos o tres soportes, cinta/marcas, luz visible de sincronía; iluminación y disco sólo si la prueba lo exige. No comprar IMU, ECG, EMG ni equipo metabólico antes de decidir qué variable falta.

**Equipo humano:** la coordinación define alcance, permisos y criterio de uso de imagen; la persona participante elige figuras habituales y decide si participa y cómo se usan sus videos; una persona con formación en Laban revisa la traducción de categorías; dos o más anotadores independientes ayudan a evaluar acuerdo; alguien de biomecánica/captura y, para costo oxidativo, fisiología del ejercicio o laboratorio con calorimetría. La lista con entregables concretos está en `EQUIPO_HUMANO_Y_COMPRAS.md`.

### Entregables y decisiones

1. **Banco técnico sin personas:** confirmar FPS/PTS, calibración, sincronía, blur, cobertura y error físico; decidir 2D/3D por descriptor.
2. **Desarrollo con videos consentidos:** inventariar originales, escoger una o dos figuras habituales y congelar guía de anotación y análisis.
3. **Sesiones reservadas:** estimar error, acuerdo y predicción base → Laban → HIT sin reajustar con esas sesiones.
4. **Paper 1:** método y factibilidad; posteriores artículos sólo si hay datos para asociaciones, metabolismo o efecto de Beacon.
5. **Demo de sonificación:** primero archivo sintético y video de baile autorizado, después video del caso principal, finalmente intervención live con protocolo independiente.

El [tablero privado de investigación](https://github.com/SairaAsua/movimiento-armonico-investigacion/issues/14) ya contiene trece issues para estas fases; su índice local está en `PLAN_GITHUB_INVESTIGACION.md`. Mantendremos datos personales, consentimientos y videos crudos fuera de GitHub; las futuras issues públicas de código contendrán sólo tareas técnicas y criterios de aceptación.

### Fuentes y documentación base

- [Laban/Bartenieff and Somatic Studies International: Space Harmony](https://labaninternational.org/space/) y el [cotejo histórico local](../research/LABAN_ACCESO_OBRAS.md).
- Fernández Méndez y Echániz, *Harmonic Information Theory: Foundations* (primera edición digital, 2026); [predicciones escalonadas](../research/HIT_PREDICCIONES_ESCALONADAS.md).
- [Kaparo, Somatic Learning](https://www.somaticlearning.com/) y [Levin, 2023, *Animal Cognition*](https://link.springer.com/article/10.1007/s10071-023-01780-3).
- [HarMoCAP](https://github.com/Mar-IA-no/HarMoCAP), [Harmonic Weaver](https://github.com/nicoechaniz/harmonic-weaver) y [auditoría de la ruta](../research/RUTA_HARMOCAP_WEAVER_BEACON.md).
- [Protocolo piloto](../research/PROTOCOLO_PILOTO_V0.md), [estimandos y contrastes](../research/ESTIMANDOS_Y_CONTRASTES.md), [montaje y compras](../research/MONTAJE_COMPRAS_Y_VIDEOS_NICO.md).

**Advertencia metodológica central:** un dato sintético demuestra que una implementación distingue construcciones conocidas; no confirma que la naturaleza, una persona participante o una audiencia produzcan las relaciones hipotetizadas.
