# Rope flow: repertorio candidato y definición de tareas

Mapa preliminar, 23 de septiembre de 2026. La práctica de interés es rope flow, con la soga moviéndose alrededor del cuerpo y sin exigir saltos. Esta nota prepara el vocabulario para registrar a Nico; **no afirma** que domine o use los patrones listados. Su repertorio real deberá observarse y describirse antes de fijar tareas del protocolo.

## Procedencia del vocabulario

Materiales de practicantes enseñan patrones llamados *underhand figure 8*, *overhand figure 8* y *dragon roll*: [curso de Gregorio Ceccoli](https://gregorioceccoli.com/course/ropeflow-free-online-course/), [guía de Winding Ropes](https://www.windingropes.com/en-ca/pages/start-your-rope-flow-journey) y [programa de Stronger Flow](https://www.strongerflow.com/rope-flow-essentials-program). Son fuentes de práctica y nomenclatura, no estudios de gasto energético, belleza ni estados de conciencia. La terminología varía entre escuelas. Una búsqueda dirigida por `"rope flow"`, `"ropeflow"` combinados con biomecánica, calorimetría y captura no identificó en esta fase un artículo primario que mida simultáneamente estas preguntas. La búsqueda no fue sistemática y la ausencia de hallazgo no demuestra ausencia de literatura.

La [notación comunitaria de flow arts](POI_ADYACENCIA_Y_TRANSFERENCIA.md) separa tiempo relativo y dirección de los implementos en poi. Puede inspirar preguntas para describir el patrón, pero sus seis modos no se imponen a una soga continua; se registrarán primero los nombres y diferencias que Nico usa.

Trabajos científicos sobre salto con soga describen otra tarea. Por ejemplo, un [estudio de salto con soga y cadencia](https://pmc.ncbi.nlm.nih.gov/articles/PMC11851774/) usó marcadores corporales y en la soga; su estrategia instrumental puede inspirar la captura de la soga, pero sus resultados biomecánicos no deben tratarse como resultados de rope flow.

## Ficha mínima por patrón observado

Para cada secuencia que Nico realice, registrar:

- Nombre usado por Nico y variante local; video de referencia con inicio, recorrido y fin.
- Si la soga pasa por delante/detrás, arriba/abajo, a cada lado; dirección de giro y mano que lidera, sin imponer etiquetas comerciales.
- Posición y desplazamiento corporal, giro axial y cambios de apoyo; relaciones con música o metrónomo.
- Evento visible que marca un ciclo completo. Si hay dos vueltas o dos picos por ciclo, especificar qué se cuenta.
- Duración estable, transiciones, pausas y errores; partes de cuerpo/soga ocultas por vista.
- Soga concreta: largo, masa y distribución aproximada, agarre. Cambiarla puede cambiar dinámica y costo.
- Variaciones permitidas para mantener “la misma tarea”: rango de cadencia, amplitud y paso corporal. Una variante artística libre puede requerir otra categoría.

La unidad primaria de observación puede ser la **frase completa** de movimiento; los ciclos son unidades internas dependientes. Cortar sólo los mejores segundos destruye la información de entrada, transición y recuperación que interesa a la coreútica. Si no se identifica ciclo estable, registrar la frase como movimiento no periódico en lugar de forzar una fase numérica.

## Candidatos para el piloto, sujetos a repertorio real

| Tipo | Motivo para observarlo | Pregunta geométrica |
|---|---|---|
| Patrón repetitivo de una dirección, por ejemplo una figura ocho que Nico use | Facilita probar eventos de ciclo y repetibilidad | Forma de recorrido de manos y soga, planos y cambios de dirección |
| El mismo patrón con giro corporal o cambio de frente | Somete a prueba marcos corporal/cámara y oclusiones | Qué se conserva al rotar el cuerpo y qué cambia en el espacio |
| Transición entre dos patrones habituales | Expone organización y recuperación sin asumir periodicidad continua | Orden de formas, dirección y tiempo de transición |
| Improvisación completa habitual | Conserva la práctica artística y la experiencia vivida | Frases, variación, retorno y episodios no clasificables |

No elegir patrones “armónicos” por apariencia antes de recopilar material comparativo. Primero describir el repertorio y la calidad de medición; después reservar sesiones completas para contrastes. La selección definitiva dependerá del movimiento real de Nico, de las cámaras y del resultado principal elegido.

## Subestudio candidato: orden de liderazgo entre manos

La lectura parcial de [series, forma inicial y apoyo en *Choreographie*](LABAN_SERIES_NOTACION_1926.md) plantea una pregunta medible: ¿dos frases con recorridos y ritmos globales parecidos difieren en **qué mano inicia cada episodio y en qué orden se suceden esos episodios**? Los [controles sintéticos](canon_fase_continua_sintetico.py) muestran que `Q`, concentración de fase `R` y ángulo medio iguales pueden ocultar ese orden. Sólo comprueban una insuficiencia matemática de esos resúmenes: no garantizan que las frases sean ejecutables, equivalentes o fisiológicamente distintas con una soga continua. Esta sección prepara una tarea posible para el [Issue #3](https://github.com/SairaAsua/movimiento-armonico-investigacion/issues/3), sin declararla seleccionada.

**Puerta de repertorio y factibilidad.** Con videos originales autorizados, describir primero una figura que Nico ya haga cómodamente, usando su nombre y una frase completa de inicio a fin. Anotar forma inicial, agarres, soga usada, recorrido de la soga, mano derecha/izquierda, frente corporal, apoyos, transición y forma final. Buscar dos variantes **naturales** que alternen el orden de liderazgo sin cambiar la tarea fundamental. Una conversación con Nico puede aclarar si él reconoce esa distinción y si ambas variantes son cómodas. Si no existen o la transición deja de ser la misma figura, el resultado es «contraste no factible en este repertorio»; conservar las frases observadas como descripción y no fabricar una versión `++--`/`+-+-` para confirmar la simulación.

**Definición provisional antes de medir.** El evento de liderazgo será el comienzo observable de una acción direccional de una mano en relación con un punto de referencia de la **soga**, definido para la figura concreta; ni un máximo aislado de muñeca ni una fase calculada de la misma pista duplicada lo sustituyen. Fijar en desarrollo el evento de cierre de ciclo y el criterio de «mismo episodio»; dos anotadores marcarán por separado mano, soga, apoyo y un intervalo temporal de incertidumbre. Sólo afirmar «A precede a B» si sus intervalos de tiempo en un reloj común son disjuntos; si se solapan, tocan, falta soga visible o se pierde identidad de mano, marcar `orden_indeterminado` con causa. La [regla de intervalos](https://github.com/SairaAsua/movimiento-armonico-investigacion/blob/a3241c6/research/ORDEN_EVENTOS_INTERVALOS.md) es un gate lógico, no una calibración ya hecha de estas cámaras. Un frame que trae dos muñecas no resuelve por sí solo el orden dentro del frame.

**Comparación mínima condicionada a esa puerta.** La unidad es el intento/frase, con episodios dependientes dentro de ella. Registrar todos los intentos, incluso arranques, errores y recuperaciones. Para cada variante, documentar cadencia, duración, amplitud/recorrido de soga, rango de desplazamiento corporal, giro, apoyos, visibilidad y cambios de tempo o música; mantener soga, agarre y montaje estables cuando sea posible y cuantificar diferencias residuales. No emparejar a posteriori sólo las frases que se ven bellas o «consonantes». Si Nico acepta una consigna de alternar dos variantes familiares, repartirlas en bloques y contrabalancear el orden entre bloques/días, dejando descansos y práctica registrados; si no, limitarse a un contraste observacional. Fijar la regla de segmentación y elegibilidad durante desarrollo y reservar días enteros para comprobarla, siguiendo el [protocolo piloto](PROTOCOLO_PILOTO_V0.md).

**Lecturas que pueden separarse.** Primero preguntar si dos anotadores y la captura recuperan el mismo orden y cuándo deben abstenerse; informar cobertura y desacuerdo por variante. Después comparar la serie ordenada de eventos y transiciones frente a `Q`, `R`, ángulo de fase y controles de cadencia/ritmo común calculados sólo donde sean identificables. Un hallazgo útil sería que las variantes difieran en orden aun cuando sus resúmenes globales sean próximos; si orden, recorrido de soga o tarea no se pueden distinguir, el contraste falla con esa instrumentación. Cualquier asociación posterior con belleza percibida, experiencia de Nico o costo oxidativo requiere las medidas y unidades independientes de [estimandos y contrastes](ESTIMANDOS_Y_CONTRASTES.md). La dificultad de una transición o el sonido de Beacon no son medidas de gasto energético ni de estado de conciencia.
