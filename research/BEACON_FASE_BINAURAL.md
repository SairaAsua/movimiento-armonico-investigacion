# Fase del movimiento y fase binaural: frontera para Beacon

**Lectura documental, 03-10-2026.** Issue dueña: [#13, contrato y prueba de audio Beacon](https://github.com/SairaAsua/movimiento-armonico-investigacion/issues/13). No se reprodujo el motor, no se grabó su salida y no se hizo un ensayo de escucha. La lectura de código se refiere a [`beacon.scd` en `de2768c3`](https://github.com/AlterMundi/beacon-spatial/blob/de2768c3a4f07cc0d744c89bf6e63b168e5f2b61/beacon.scd); verificar de nuevo si cambia el commit.

## Tres magnitudes llamadas «fase»

| Magnitud | Definición y unidad | Procedencia necesaria |
|---|---|---|
| Fase de la tarea | Posición dentro de un ciclo de soga, por ejemplo `θ_rope(t)` en radianes, derivada de eventos visibles con reloj y sentido. | Video/observación, ciclo identificable, incertidumbre y cobertura. No existe una fase única durante toda transición no periódica. |
| Fase entre señales de movimiento | `wrap(θ_hand(t) − θ_rope(t))`, si ambas se midieron independientemente y comparten tiempo. | Identidad de cada señal y control de circularidad; véase [procedencia de fases](FASE_PROCEDENCIA_CIRCULAR.md). |
| Fase interaural acústica (IPD) | Diferencia de fase de una **componente de audio a una frecuencia definida** entre canales izquierdo y derecho, en radianes. Para un tono y un retardo puro `Δt`, `Δφ(f) = 2πfΔt` módulo `2π`; no es una propiedad escalar única de un audio arbitrario. | PCM estéreo aplicado, banda/frecuencia, configuración del render y método de estimación. Registrar además diferencia interaural de tiempo (ITD) y de nivel (ILD). |

La igualdad numérica entre `θ_rope` y una IPD, si alguien la programara, sería una **regla de sonificación elegida**, no la medición de una frecuencia o fase corporal en el oído. Rotar el cuerpo tampoco fija por sí mismo la IPD: hace falta definir qué orientación corporal controla qué azimut sonoro, con qué marco de referencia, retardo y política cuando el seguimiento es inválido. La explicación matemática y experimental de fase de soga está en [fase de rope flow](FASE_ROPEFLOW.md).

## Qué hace el motor auditado

Las frecuencias 40/80/120 Hz son [centros de filtros sobre audio entrante](BEACON_BANDAS_NO_FRECUENCIAS_CORPORALES.md), no componentes fisiológicas. El trayecto *wet* pasa cada banda por `FoaPanB` con azimut en radianes y escala `1/dist`, suma B-format y decodifica con `FoaDecode`/kernels Listen a estéreo. El trayecto *dry* suma las bandas filtradas y se mezcla según `mix`. La implementación expone azimut por banda; **no** expone una orden nativa de IPD, ITD o fase izquierda–derecha. El resultado binaural puede contener diferencias interaurales dependientes de frecuencia, entrada, HRTF, azimut y mezcla; su valor no se deduce de la etiqueta 40 Hz ni de un ángulo corporal. El código indica auriculares para la experiencia binaural, pero su salida real y su percepción no están verificadas aquí.

En un estudio experimental de tonos de **250–750 Hz**, Hartmann, Rakerd, Crawford y Zhang encontraron que ITD e ILD interactúan en la localización y que el ángulo aparente se relacionaba más directamente con ITD que con IPD. Es evidencia de que una IPD aislada no basta para predecir la experiencia espacial; **no** demuestra localización, placer ni una relación especial de las bandas de 40/80/120 Hz de Beacon. Fuente primaria: [Hartmann et al., *JASA* 139, 968–985 (2016), DOI 10.1121/1.4941915](https://doi.org/10.1121/1.4941915), [texto y resumen en PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC4769260/).

## Prueba pendiente: del control a lo que se oye

1. **Congelar el instrumento:** commit, audio de entrada con hash, frecuencia de muestreo, HRTF/decoder, auriculares o ruta de reproducción, `mix`, `master`, ganancias, `q`, azimuts y distancias. Conservar los controles *solicitados* y los *aplicados* con sus tiempos. Ningún archivo humano necesita estar en GitHub.
2. **Aislar el efecto:** con una sola banda audible y `mix=1`, renderizar entrada conocida, azimuts simétricos y centro, más condición seca `mix=0`; repetir con una banda alta y con entrada de espectro ancho. Controlar nivel global y evitar atribuir a fase lo que sea diferencia de nivel. Esto verifica la implementación acústica, no la percepción.
3. **Medir el PCM estéreo:** nivel y espectro por canal; ITD o retardo efectivo por correlación en ventanas/bandas donde sea identificable; ILD e IPD por frecuencia con coherencia/energía suficientes. Documentar ambigüedad de fase módulo `2π`, solapamiento de bandas, transitorios, latencia y ausencia de estimación si la banda carece de señal. Comparar el cambio de azimut **aplicado** con estas salidas, no con controles meramente enviados.
4. **Separar percepción de acústica:** si el objetivo es afirmar que se escucha el giro o la organización del gesto, preparar una prueba posterior y ciega de discriminación/atribución, con niveles equilibrados y clips de movimiento cuyo mapeo se haya fijado antes de ver respuestas. La prueba de PCM sola no establece que una persona identifique la rotación ni que la juzgue bella o armónica.

**Regla de paso para HarMoCAP → Weaver → Beacon:** publicar por separado `(a)` error/cobertura de la variable corporal en su propio reloj, `(b)` traza del mapeo a azimut/ganancia y estado inválido, `(c)` controles recibidos/aplicados y `(d)` PCM de salida con métricas acústicas. Solo después se estudia la respuesta humana. El banco sintético o una coincidencia de proporciones no sustituye ninguna de esas cuatro observaciones.
