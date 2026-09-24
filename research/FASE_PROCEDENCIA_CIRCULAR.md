# Evitar fase relacional fabricada por un mismo reloj de tarea

Nota matemática de diseño, 23-09-2026. Complementa [fase de rope flow](FASE_ROPEFLOW.md) y [controles de ritmo común](CONTROLES_RITMO_COMUN.md). Es una comprobación lógica del procesamiento, no un hallazgo humano ni una ecuación autoral de HIT.

## El caso tautológico

Sean `t_k` y `t_{k+1}` dos eventos de soga que delimitan el ciclo `k`. La fase retrospectiva de tarea es `θ_k(t)=2π(t−t_k)/(t_{k+1}−t_k)`. Si una «fase de mano izquierda» y una «fase de mano derecha» se construyen ambas copiando esa `θ_k`, entonces `φ_L(t)=φ_R(t)=θ_k(t)`. La diferencia relativa `φ_L−φ_R` es exactamente cero en todos los cuadros y `R₁:₁=|mean(exp(i(φ_L−φ_R)))|=1`, **aunque no se haya medido la mano**.

Agregar a cada copia un desplazamiento fijo `α_L`, `α_R` tampoco aporta prueba: la diferencia será siempre `α_L−α_R`, con `R=1`. Si una función fuerza por construcción el comienzo y final de **ambas** fases a los mismos eventos de soga, el interior puede variar, pero el estadístico queda parcialmente condicionado a coincidencias impuestas. Un `R` alto en ese caso no es observación independiente de coordinación mano–mano. Esta circularidad es distinta de una **entrada común real**: dos señales de mano medidas independientemente pueden responder al mismo pulso de soga o música sin que el algoritmo haya copiado su fase. La segunda situación exige el control condicional ya descrito; la primera exige corregir el pipeline.

## Proveniencia mínima de cada fase

Para cada serie de fase, conservar un registro de dependencia:

| Campo | Ejemplo y motivo |
|---|---|
| `signal_source` | soga visible, muñeca izquierda 3D, muñeca derecha 3D, ángulo de tronco, pulso musical; no llamar «mano» a un reloj de soga. |
| `raw_observation_ids` | Frames, cámara/vista y puntos o eventos de los que salió la señal; permite ver si dos supuestas medidas son copias. |
| `event_anchor_ids` | Eventos que fijaron fase cero y período; declarar si son compartidos con la otra fase. |
| `estimator_version` y `filter_window` | Hilbert, plano posición–velocidad, interpolación por eventos, filtro causal/centrado; define disponibilidad y posibles dependencias de futuro. |
| `available_at` y `validity_state` | Momento en que el valor podía conocerse y causa de invalidez; la fase de tarea offline no se presenta como señal en vivo. |

La prueba HIT que pretenda **coordinación entre segmentos** requiere que cada fase segmentaria derive de observaciones del segmento respectivo y que las dependencias compartidas estén declaradas. Compartir timestamps de cámara o una referencia espacial calibrada es esperable; compartir la propia serie de eventos que define ambas fases cambia la pregunta. Se puede comparar cada mano con la fase de soga como **alineación con la tarea**, pero no presentar dos copias de `task_phase` como acoplamiento mano–mano.

## Regla de inclusión y controles

1. Antes de calcular `R`, revisar el grafo de dependencia de las dos fases. Si ambas son transformaciones deterministas del mismo `task_phase` sin observación segmentaria propia, asignar `relation_state=tautological_shared_source` y excluir el índice de la prueba de HIT.
2. Si las fases de manos se estiman de señales propias pero se *anclan* a eventos de soga, reportar que `R` está condicionado por ese anclaje. Comparar con una estimación de eventos/ángulos de manos independiente donde la visibilidad lo permita y probar sensibilidad a quitar muestras cercanas a los anclajes.
3. Para una relación mano–soga genuinamente observada, exigir soga y mano visibles en el intervalo; si la soga está oculta y se imputa desde muñeca, la relación mano–soga se vuelve circular o dependiente del mismo proxy y se marca inválida para ese contraste.
4. En sesiones reservadas, ejecutar un control negativo de procesamiento: alimentar al cálculo dos copias del reloj de tarea y comprobar que el sistema **rechaza** la relación como tautológica en lugar de celebrar `R=1`. El resultado de rechazo valida el guardarraíl del software, no una teoría del movimiento.

La misma regla aplica a Beacon: una capa sonora puede hacer audible el pulso de tarea y otra la fase de mano, siempre con fuente y latencia visibles en el registro de ingeniería. Que las dos capas suenen consonantes cuando proceden del mismo reloj es comportamiento del diseño sonoro; no observación fisiológica.
