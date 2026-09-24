# Banco sintético de ciclo y fase antes de medir rope flow

Comprobación matemática del 23 de septiembre de 2026. El [script Python](fase_sintetica.py) emplea sólo la biblioteca estándar; sus señales son construidas, **no** registros de Nico. Ejecutar `python fase_sintetica.py`. Los ejemplos sirven para probar la coherencia de definiciones y hallar fallos previsibles del análisis, no para verificar HIT o una hipótesis fisiológica.

| Caso | Salida verificada | Consecuencia metodológica |
|---|---|---|
| Posición `sin(2πft)` durante cinco vueltas, rapidez `|cos(2πft)|` | Diez picos de rapidez frente a cinco ciclos anotados | `tempo_bpm` o un detector de intensidad puede marcar doble frecuencia. El ciclo de **tarea** requiere evento con configuración y sentido, y comprobación visual de soga/cuerpo. |
| Eventos en 0, 1, 2, 4, 5 s; intervalo 2–4 s declarado transición | Fase a 1,5 s = π; a 3 s = indefinida | Una ausencia de evento no justifica inventar una vuelta lenta de dos segundos. Pausas, inversos y cambios de patrón necesitan estado explícito. |
| Dos fases con relación 2:1 y cadencia que aumenta gradualmente | Concentración circular `R₂:₁=1`, desfase medio 0,3 rad | El contraste `qφᵢ−pφⱼ` puede seguir una relación aun si la cadencia no es constante, siempre que las fases propias sean identificables. |
| Desajuste adicional de 0,125 Hz mantenido ocho segundos | `R₂:₁≈0` al cubrir una vuelta completa de diferencia | La ventana temporal elegida cambia el resultado; no extraer un único índice de «armonía» de cualquier duración. |
| Dos fases 1:1 alternadas media vuelta | `R₁:₁=1` y desfase medio π | Máxima concentración no implica simultaneidad ni que ángulo cero sea deseable; el desfase esperado depende de la tarea. |
| Una señal de 2 Hz retrasada 20 ms respecto de otra | `R₁:₁=1`, pero sesgo medio de fase de **14,4°** | Un retardo fijo puede dejar intacta la concentración y alterar la interpretación del ángulo; cámaras, OSC y audio requieren sincronía y latencia medidas. |
| Dos eventos por ciclo siguen un reloj común, pero sus variaciones ciclo a ciclo son ortogonales | `R₁:₁=0,984292`, correlación entre residuos `0` | Concentración alta no demuestra covariación adicional entre segmentos una vez considerado el ciclo compartido. |
| Desplazamiento circular de una señal periódica pura | `R₁:₁=1` tras el desplazamiento | Ese desplazamiento no proporciona un nulo válido de sincronía para una señal exactamente periódica. |
| Dos ciclos de 1 s y 3 s, cada uno con fase interna estable pero desfases `0` y `π` | `R_t=0,5`; `R_c≈0`; promedio de `R` dentro de cada ciclo `=1` | El tiempo válido, los ciclos y la estabilidad interna responden preguntas distintas. Promediar módulos de ciclo esconde la inversión de fase. |

El caso 2:1 usa fases matemáticas conocidas; no ensaya Hilbert, fase de posición–velocidad, detección de la soga ni error de cámara. Las muestras de un mismo ciclo no son observaciones humanas independientes; se promedian sólo para ilustrar `R`. En un estudio real se informarán intervalos válidos, ciclos y bloques, incertidumbre de fase y dependencia entre muestras. Una señal común como música o soga puede producir sincronía entre dos segmentos sin que uno cause al otro. El [protocolo de fase](FASE_ROPEFLOW.md) mantiene esa distinción.

Esta comprobación **cambia una decisión para Beacon**: la concentración `R` y el ángulo medio necesitan canales separados, con origen de reloj, estimador y estado de calidad; un `R` alto con 20 ms de error no autoriza una sonificación que pretenda reflejar el desfase real. El campo `beat_phase` de HarMoCAP no se reinterpretará como fase articular. Antes de un mapeo sonoro científico habrá que medir latencia de captura a audio en el montaje concreto ([contrato de integración](INTEGRACION_HARMOCAP_BEACON.md)).

Los dos ejemplos nuevos motivan el [plan de controles del ritmo común](CONTROLES_RITMO_COMUN.md): separar descripción de coordinación, predicción HIT sobre un resultado externo y covariación residual tras considerar soga/música. Ninguno de los ejemplos identifica acoplamiento causal.
