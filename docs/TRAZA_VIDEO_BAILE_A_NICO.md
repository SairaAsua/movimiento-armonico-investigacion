# Traza para escuchar movimiento: video de baile → caso principal → tiempo real

Versión 0.1, 24-09-2026. **Plan futuro**, sin video humano seleccionado ni ruta de audio Beacon ejecutada. Los cuatro WAV del [banco sintético](../research/REPORTE_SINTETICO_PRESENTACION.md) sólo prueban una traducción diagnóstica de curvas conocidas.

| Escalón | Entrada | Salida que hay que conservar | Prueba de paso |
|---|---|---|---|
| A. Curva fabricada | CSV con trayectoria y fase verdaderas por construcción | `Q`, `R`, estados y cuatro WAV | Plano y fase distinguibles; caso opuesto no colapsa a `R=1` por usar sólo cierres. **Hecho en datos sintéticos.** |
| B. Cámara sin persona | Animación de puntos u objeto físico registrado por las cámaras reales | Video original/PTS, calibración, marcas independientes, error | Distinguir ambas relaciones temporales con error/cobertura fijados antes del archivo reservado. Pendiente. |
| C. Video de baile autorizado | Original continuo, permiso/licencia verificable, cuerpo visible | Pose cruda/filtrada, timestamps, segmentos válidos, descriptores proyectados o 3D validados | Anotadores revisan muestra ciega; el análisis declara pérdidas y no rellena oclusiones como observaciones. Pendiente. |
| D. Audio offline del baile | Señales validadas de C y escena/versiones fijas | Control nativo aplicado en Weaver/Beacon y audio grabado | Al permutar sólo plano o fase, cambia sólo la capa correspondiente; medir retardo, reinicio e invalidez. Pendiente. |
| E. Video original del caso principal | Permiso específico y figura habitual | Mismos archivos y métricas más experiencia de la persona participante por bloque | El pipeline conserva cobertura/errores en rope flow, cruces y giros; no extrapolar desde danza genérica. Pendiente. |
| F. Feedback vivo a la persona participante | Cámara sincronizada, derivación causal, instrumento verificado | Audio realmente oído, latencia y condiciones de comparación | Comparar sonido contingente/control/silencio y retención en un estudio aparte. Pendiente. |

**Arquitectura:** video original → marcas temporales y calibración → pose/curva con calidad → descriptores espaciales inspirados en Laban y relaciones HIT → canales versionados con unidad/ventana/edad/estado → Harmonic Weaver (escena declarativa) → controles nativos de Beacon → registro del audio. En paralelo se guarda un **archivo científico** con originales y derivaciones; la transmisión live puede descartar cuadros y no sustituye ese archivo.

Antes de D, el driver HarMoCAP de Weaver debe preservar `captured_frame_id` y `captured_at_us` y evitar que dos bundles del mismo cuadro dupliquen la muestra de una persona. El MVP actual tiene transporte de registro, no salida OSC/audio live verificada. Antes de E, se necesita un video original de rope flow de la persona participante: los episodios editados localizados hasta ahora no contienen su movimiento corporal medible. Antes de F, `Q`/`R` offline no se pueden adelantar al reloj live; la señal causal requiere su propia prueba de latencia y datos faltantes.

**Criterio editorial:** el título de cada demo dirá exactamente qué representa: «sonificación de trayectoria sintética», «sonificación offline de video de baile» o «feedback vivo de Nico». Nunca «sonido de la verdad del cuerpo» ni «frecuencia biológica de 40 Hz» sin una medición que lo sostenga.
