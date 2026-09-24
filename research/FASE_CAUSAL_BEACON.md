# Fase de tarea offline y fase que Beacon podría conocer en vivo

Nota metodológica, 23 de septiembre de 2026. La [fase de rope flow](FASE_ROPEFLOW.md) define retrospectivamente `θ(t)=2π(t−tₖ)/(tₖ₊₁−tₖ)` entre dos cruces válidos de la soga. Esa interpolación describe un ciclo **completo**, pero en `t<tₖ₊₁` el evento final aún no ocurrió. Reproducirla como si Beacon la hubiera conocido en ese momento introduce información futura ([predicción HIT sin fugas](HIT_PREDICCION_SIN_FUGAS.md)). La distinción es técnica y empírica: ninguna de las dos fases mide por sí sola belleza, costo metabólico ni un estado de conciencia.

## Estimador causal mínimo para un ensayo de ingeniería

Después de dos eventos de tarea **aceptados** `tₖ₋₁<tₖ`, el último período observado es `T̂ₖ=tₖ−tₖ₋₁`. Mientras no llegue otro evento, una estimación causal simple sería

`θ̂_live(t) = 2π (t−tₖ)/T̂ₖ (mod 2π)`, para `t≥tₖ`.

Requiere dos cruces reales, no dos picos de rapidez. Se marca `warmup` antes de tener un período completo; `estimated` durante una ventana definida; `expired` si pasa demasiado tiempo sin otro cruce, en vez de seguir inventando vueltas. Un umbral ilustrativo de `1,5 × T̂ₖ` está en el [banco sintético](fase_causal_sintetica.py); **no** es un valor aceptado para Nico. Reversa, transición o pérdida de identidad de soga requieren `invalid` por otra regla, incluso si siguen llegando máximos de movimiento. El evento puede detectarse tarde: el sistema debe registrar `event_time_us` (tiempo de captura estimado), `available_at_us` (cuando el detector lo confirmó) y la incertidumbre de ambos. El sonido sólo puede responder desde `available_at_us`.

En la [ruta actual HarMoCAP→Weaver](RUTA_HARMOCAP_WEAVER_BEACON.md), el driver elimina precisamente el ID y tiempo de captura del bundle antes de llamar al motor; éste estampa hora de recepción y puede reemitir un slot anterior al llegar otra persona. No se puede reemplazar `event_time_us` por esa hora ni calcular `T̂ₖ` contando callbacks. La futura extensión debe propagar procedencia por slot/evento y un mapeo explícito entre el reloj monótono de HarMoCAP, los PTS originales y el reloj que registra Beacon. Hasta entonces, el estimador de esta sección es especificación matemática y banco sintético, no una capacidad live demostrada.

Si el siguiente período real vale `Tₖ₊₁`, antes de conocerlo el error sin envolver en un instante `tₖ+τ` es

`Δθ(τ) = 2π τ (1/T̂ₖ − 1/Tₖ₊₁)`.

Esta igualdad es una resta algebraica entre predicción causal y fase retrospectiva del ciclo. No requiere suponer que una señal corporal es un oscilador físico. Muestra que una concentración temporal calculada offline con el evento futuro no puede transportarse intacta al tiempo real. Error de reloj y latencia se suman a esta diferencia; el error total se medirá extremo a extremo en la cadena concreta.

## Banco reproducible

[`fase_causal_sintetica.py`](fase_causal_sintetica.py) usa sólo biblioteca estándar y eventos **inventados**. Su ejecución verificada produjo:

| Caso | Conocimiento live | Fase live | Fase retrospectiva | Consecuencia |
|---|---|---:|---:|---|
| Ciclo constante de 1 s, a 2,5 s | Cruces a 0, 1 y 2 s | 180° | 180° usando el cruce de 3 s | Coinciden sólo bajo la constancia construida. |
| Ciclo siguiente de 0,8 s, a 2,4 s | Cruces a 0, 1 y 2 s; **2,8 s aún desconocido** | 144° | 180° tras observar 2,8 s | Error live de −36° en medio ciclo. La aceleración sesga un sonificado que copie la interpolación offline. |
| Sin nuevo cruce a 3,6 s tras 2 s | Último período = 1 s | `expired`, sin fase | No hay ciclo completo válido | Un valor numérico continuo ocultaría la pérdida de evento. |
| Un solo cruce | Sin período observado | `warmup`, sin fase | No corresponde | No inventar velocidad de referencia. |

El script rechaza explícitamente pasar un evento futuro al estimador live. Estos números prueban coherencia de la fórmula, **no** precisión con cámaras ni éxito de un detector de rope flow. En señales reales, el criterio de expiración debe derivarse de variación normal de cadencia, tasa de falsos cruces y latencia observada. Es posible que un modelo de predicción más elaborado mejore el error, pero se compararía en sesiones reservadas con un baseline causal y sin recibir el evento futuro por filtrado o interpolación.

El mismo script incluye ahora un par de vueltas circulares sintéticas con idénticos hitos. A `t=2,25 s`, ambas reciben `fase_tarea_live=90°`, pero sus ángulos cinemáticos ideales son `90°` y `118,65°`; coinciden de nuevo al completar la vuelta. Es el control de **información representada** para una eventual capa sonora de microtiempo, no un ensayo con cámaras o audio.

## Contrato para archivo y Beacon

Guardar dos productos diferenciados: `task_phase_offline` con intervalo `(tₖ,tₖ₊₁)`, método y disponibilidad **después** de `tₖ₊₁`; y `task_phase_live_estimate` con período pasado, instante de cálculo, vencimiento, error esperado validado y estado. Un algoritmo de relación `p:q` live debe construirse con fases live de **ambas** señales; si una expira, no emitir `R` como si describiera sincronía actual. `beat_phase` de HarMoCAP es otra señal agregada de pulso y no reemplaza ninguna de éstas.

Si Beacon pretendiera expresar la **velocidad o coordinación dentro de cada vuelta**, hace falta un tercer producto diferente: una fase cinemática causal derivada de posiciones actuales de un segmento en un patrón que admita ángulo continuo, con error de posición, radio mínimo, marco, filtrado y latencia verificados. Dos recorridos circulares con los mismos eventos en 0 y 1 s reciben la misma `task_phase_live_estimate` cuando comparten historial, aunque uno tenga `θ=2πt` y otro `θ=2πt+0,5 sin(2πt)`; la [derivación](GEOMETRIA_VS_TIEMPO_TRAYECTORIA.md) demuestra que sus posiciones y aceleraciones intermedias difieren. Un detector de figura ocho no hereda automáticamente este ángulo: puede invertir sentido o pasar cerca del origen. El [diccionario](DICCIONARIO_SENALES_V0.md) reserva `kinematic_phase_live_estimate` sólo donde la geometría y el muestreo superen el gate propio. Si no lo superan, la capa live puede comunicar ritmo de **eventos**, pero no anunciar que escuchamos la organización interna del gesto.

La arquitectura audible —centro de banda filtrada en el [`beacon-spatial` actual](BEACON_BANDAS_NO_FRECUENCIAS_CORPORALES.md), u otra síntesis futura— sigue siendo una decisión de diseño. El retardo desde observación a audio altera el ángulo escuchado: a 2 Hz, 20 ms equivalen a 14,4° de fase, como muestra el [banco previo](FASE_BANCO_SINTETICO.md). Medir por separado error de predicción del siguiente cruce, retardo del detector/OSC/audio y calidad de evento. Si el error temporal acumulado supera la diferencia de fase que el diseño pretende hacer audible, Beacon puede seguir siendo una obra sonora, pero no presentará esa capa como feedback fiel de la fase corporal actual.

Antes de probarlo con Nico faltan definición y anotación de eventos por patrón, cámaras/soga visibles, validación de reloj y detector causal. El [contrato de investigación](INTEGRACION_HARMOCAP_BEACON.md) deberá versionar esta distinción cuando se implemente una extensión; OSC 1.4 no contiene estos campos.
