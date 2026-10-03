# Ficha de factibilidad: experiencia informada por bloque

**Borrador v0 · 24-09-2026.** No es una escala validada, un formulario administrado ni un protocolo congelado. Se probará su comprensión con Nico sólo después de acordar participación, tratamiento de video y revisión ética pertinente. Conserva separadas la experiencia habitual del bloque, un posible episodio destacado y cualquier relato extraordinario espontáneo. La unidad de comparación inicial es el **bloque**, no el cuadro.

## Secuencia antes de mostrar imágenes o resultados

Registrar primero `session_id`, `block_id`, fin del bloque según reloj de sesión, hora de inicio y fin de respuestas, versión de la ficha, entrevistador, condición sonora que escuchó Nico durante la ejecución y si ya había visto video, oído sonificación o conocido una puntuación de este mismo bloque. No convertir una respuesta tomada después de una devolución de Beacon en una respuesta ciega.

1. Preguntar: **«Contame qué pasó para vos durante este bloque.»** Registrar la respuesta literal, silencios relevantes y si dijo «no sé» o prefirió no responder. No ofrecer ejemplos como armonía, orgasmo o mística.
2. Preguntar por separado y siempre con la misma ventana: **«Pensando en la mayor parte del bloque…»** facilidad de movimiento, disfrute, atención/absorción, sensación de conexión entre partes del cuerpo y esfuerzo sentido. En el piloto de comprensión, probar para cada ítem una escala provisional `0–4`, donde `0 = nada`, `1 = poco`, `2 = algo`, `3 = bastante`, `4 = muchísimo`; ofrecer además `no sé`, `no aplica` y `prefiero no responder` como estados **no numéricos**. No sumar los cinco ítems. Preguntar si «conexión» y «absorción» significan algo comprensible para Nico, y conservar su explicación: si una palabra no funciona, revisarla antes de la fase reservada, no reinterpretarla después de ver asociaciones.
3. Preguntar: **«¿Hubo algún momento que para vos se distinguió del resto? ¿En qué sentido?»** Admitir `ninguno`, `todo el bloque`, `no localizable`, `no sé` y `prefiero no responder`. Guardar las palabras de Nico y la dimensión a la que se refiere, si la nombró; no suponer que el momento de mayor disfrute fue el de menor esfuerzo o el más bello.
4. Cerrar sin solicitar que Nico adivine la geometría, el gasto energético o cómo lo vería un espectador. Registrar duración y cualquier comentario sobre fatiga de responder o cambio de atención por el cuestionario.

La escala `0–4` sólo sirve para comprobar comprensión y carga en la fase de desarrollo. **No se puede tratar como instrumento validado ni comparar días con versiones de ítems diferentes sin marcar la versión.** Si la prueba revela ambigüedad, revisar anclajes y orden antes de congelar; archivar ambas versiones y las razones del cambio.

**Posible extensión vestibular, aún no parte del guion v0:** si la práctica real incluye giros de cabeza/cuerpo identificables, probar durante desarrollo una pregunta separada sobre mareo o desorientación, **después** de la narración libre y sin insinuar trance o éxtasis. Registrar si se preguntó, a qué bloque se refirió, respuesta literal/estado `no sé/no aplica`, versión y giros corporales observados por separado de vueltas de la soga. No usar esta respuesta como diagnóstico ni sumarla a disfrute o absorción. La [lectura de un estudio de simios que giran el cuerpo con cuerda](GIRO_CUERPO_ESTADO_VESTIBULAR_2023.md) explica por qué las dos rotaciones y la experiencia no son intercambiables; su cifra de velocidad no fija una condición para Nico. La decisión de añadir el ítem al protocolo comparativo se tomaría antes de sesiones reservadas y tras comprobar comprensión/carga.

## Registro mínimo de cada bloque

| Campo | Regla de registro |
|---|---|
| `session_id`, `block_id`, `task_id`, `form_version` | IDs seudónimos que permitan enlazar con el manifiesto de captura sin poner nombre en la tabla analítica. |
| `block_end_session_us`, `response_start_session_us`, `response_end_session_us` | Tiempo de sesión y latencia de respuesta; guardar `clock_mapping_id` si el dispositivo usa otro reloj. |
| `audio_during_block`, `feedback_during_block`, `prior_result_exposure` | Condiciones de escucha y exposición previa, con `unknown` si no se sabe. |
| `free_report_verbatim`, `free_report_status` | Texto literal en archivo privado separado; nunca inferir un `0` del silencio o de un campo vacío. |
| `ease`, `enjoyment`, `absorption`, `body_connection`, `felt_effort` | Cada respuesta y su estado (`answered`, `unknown`, `not_applicable`, `declined`, `missing`). El valor numérico sólo existe para `answered`. |
| `salient_event_status`, `salient_event_verbatim`, `salient_dimension` | Momento destacado opcional; conservar `none`, `whole_block`, `unlocalizable`, `uncertain`, `declined` como posibilidades distintas. |
| `prompt_deviation`, `questionnaire_reactivity`, `notes` | Cambio de guion, ayuda del entrevistador, interrupción o efecto declarado sobre la ejecución posterior. |

Una mención espontánea a «orgasmo», «trance», «unidad» o «mística» permanece **texto literal sensible** con su contexto y significado declarado, no se convierte en diagnóstico ni en una categoría positiva automática. No solicitar detalle sexual en esta ficha. Si se quiere estudiar una de esas vivencias explícitamente, preparar otro consentimiento, definición de caso, instrumento/entrevista y análisis antes de recolectar ese resultado.

## Revisión opcional del video

Sólo después del registro anterior, y en una submuestra seleccionada por regla ajena a puntuaciones Laban/HIT y a clips favoritos, se puede mostrar el video original. Crear un **registro nuevo** `review_id` enlazado al `block_id`: demora desde la acción, clip mostrado, vista, audio, velocidad, pausas, selección del clip, narración posterior literal y límites aproximados que Nico marque para cada dimensión. Guardar incertidumbre de inicio/fin y las opciones `none`, `whole_block`, `unlocalizable`, `unknown`. No sobrescribir el primer relato. Si la incertidumbre de recuerdo y sincronización excede el ciclo, analizar al nivel de episodio o bloque.

## Comprobación antes de usarla en un contraste

En la prueba de comprensión, preguntar a Nico qué entendió por «mayor parte», «conexión» y «absorción», cuánto tardó y si responder cambió su forma de moverse en el siguiente bloque. Si los ítems son claros y tolerables, fijar redacción/orden/escala y una dimensión principal **antes** de abrir días reservados; de lo contrario, informar la limitación o rediseñar. Codificadores de relatos y analistas de video permanecen ciegos a los resultados del otro lado hasta cerrar sus registros. La concordancia futura sólo autorizaría afirmar asociación dentro de Nico entre un descriptor válido y su **experiencia informada**, nunca leer directamente un estado de conciencia desde la cámara o el pulso.

Fundamento y límites: [experiencia de primera persona](EXPERIENCIA_PRIMERA_PERSONA.md), [experiencia y estética](EXPERIENCIA_ESTETICA.md), [sensores](SENSORES_DECISION.md) y [ficha de congelamiento](FICHA_CONGELAMIENTO_ESTUDIO.md).
