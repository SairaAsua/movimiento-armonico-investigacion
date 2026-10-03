# Continuidad de `Q_live` entre emisiones

**Propuesta y banco sintético, 3 de octubre de 2026.** El [sobre individual](CONTRATO_Q_LIVE_V0.md) ya exige `path_definition`, versión de marco, cobertura, reloj, incertidumbre y `Q=null` al invalidar. Sin embargo, tres registros estructuralmente válidos pueden contener una ventana de `Q` que mezcla dos definiciones de recorrido. El [control ejecutable](q_stream_transition_gate.py) examina **la secuencia** que aspiraría a alimentar una capa sonora. No recibe cámaras, no modifica HarMoCAP/Weaver/Beacon y no aplica OSC ni audio.

## Invariante propuesto

Para cada `(session_id, stream_id, slot_id, signal_name)`, conservar una huella semántica de algoritmo, manifiesto de entrada, calibración, marco corporal, definición de recorrido y segmento, duración de ventana y dominios de reloj. Si cambia un elemento, el primer registro con la huella nueva debe ser `status=invalid`, `invalid_reason=transition`, `Q=null`. Cualquier invalidez produce un **candidato a reset**; el próximo valor sólo puede aceptarse si su ventana comienza en o después de `available_at_us` del reset, en el mismo reloj de sesión. Esta elección conservadora excluye las muestras anteriores a la disponibilidad del reset y exige llenar una ventana nueva. No se atribuye a una regla histórica de Laban ni a un contrato ya implementado en Beacon.

Dentro de esa clave se exigen `source_frame_id` y `source_time_us` crecientes mientras no cambie la huella, `feature_window_end_us` no decreciente y `available_at_us` no decreciente. Cambiar `session_clock_id` dentro de una sesión se rechaza: comparar microsegundos de dos dominios sin mapa validado no tiene sentido. Un cambio de `source_clock_id` o `clock_map_id` necesita transición explícita; el validador no prueba que ese mapeo físico sea correcto. Los cuadros omitidos son posibles, pero un mismo cuadro no debe volver a sonar como nueva observación del mismo slot.

| Secuencia construida | Cada registro pasa el esquema individual | Control de secuencia |
|---|---:|---|
| Valor `co_rotating` → `invalid/transition` con `waist_relative_step_body_axes` → valor tras una ventana nueva | Sí | Acepta candidatos `valor → reset → valor` |
| Cambio de `path_definition` seguido directamente de valor | Sí | Rechaza falta de reset |
| Reset explícito, luego valor cuya ventana comienza **antes** de su disponibilidad | Sí | Rechaza mezcla con pasado |
| ID de cuadro repetido con tiempo posterior | Sí | Rechaza muestra duplicada |
| Cambio de reloj de sesión con microsegundos plausibles | Sí | Rechaza comparación de dominios |

`python3 research/q_stream_transition_gate.py` ejecuta estas secuencias en memoria usando el validador individual existente; dos corridas produjeron JSON idéntico, SHA-256 `4361b097420f6b380799f945c4f5960d52d98ba7c6b682dc4c588529589d5bbe`. El script comprueba que las cuatro secuencias adversas pasan individualmente y que cada una se rechaza **por la razón esperada** sólo al mirarlas en orden. Los microsegundos e IDs son sintéticos. No son una tasa de falla de HarMoCAP ni evidencia de que un adaptador real resetee las bandas.

## Fronteras antes de conectar Beacon

- `value_candidate` significa que la secuencia es coherente con este invariante. Si `uncertainty.status=not_estimated`, como en el fixture, **no** autoriza llamar calibrado al sonido. Si figura `bounded`, la existencia y el dominio físico del perfil de validación siguen requiriendo comprobación fuera de este JSON.
- `reset_candidate` es una obligación para el adaptador, no una confirmación de que el instrumento recibió y aplicó un reset atómico de todas las bandas asociadas a `Q`. El gate real deberá registrar control aplicado y audio, además de demostrar qué sucede con `suppress`, `reset`, latencia y pérdida ([ensayo de transición](BEACON_TRANSICIONES_Y_RESET.md)).
- Si un stream desaparece sin emitir invalidez, este control no puede verlo: se necesita vencimiento por última observación y lease del receptor. Tampoco descubre un cambio de patrón de rope flow si el productor conserva los mismos campos; ese cambio debe provocar `invalid/transition`, y una futura versión de contrato podría identificar el patrón explícitamente.
- La primera emisión de una secuencia parcial puede ser válida sin que el script haya visto el arranque de su ventana. Para un uso científico completo se necesita archivo continuo o evidencia del estado inicial; un consumidor live debe hacer handshake y empezar en estado apagado hasta recibir una ventana nueva validada.

El siguiente paso de ingeniería corresponde a la [issue de contratos/audio](https://github.com/SairaAsua/movimiento-armonico-investigacion/issues/13) y a issues propias de los repositorios que implementen productor, adaptador o instrumento. Esta nota sólo hace revisable la política de continuidad antes de solicitar ese cambio.
