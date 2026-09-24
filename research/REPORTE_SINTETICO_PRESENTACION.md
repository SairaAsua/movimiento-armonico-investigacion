# Banco sintético de presentación: cuatro condiciones y audio diagnóstico

**Ejecutado el 24-09-2026.** Código: [`experimento_sintetico_presentacion.py`](experimento_sintetico_presentacion.py). Datos: [`trayectorias.csv`](datos_sinteticos_presentacion/trayectorias.csv), [`resultados.json`](datos_sinteticos_presentacion/resultados.json) y cuatro WAV de ocho segundos. `python experimento_sintetico_presentacion.py` regenera archivos y verifica aserciones. Sólo usa biblioteca estándar de Python.

Se generaron 960 filas: 30 cuadros/s × ocho segundos × cuatro condiciones. Dos planos del recorrido derecho se cruzan con dos emparejamientos de fase de manos. En ambas condiciones de un plano hay ocho vueltas, igual longitud de recorrido, mismos eventos de cierre y misma distribución de rapidez para cada mano. La mano izquierda conserva exactamente su serie temporal. La derecha conserva su distribución de rapidez pero cambia la coincidencia intracíclo con la izquierda. El banco no contiene cuerpo humano ni soga física.

| Plano | Tiempo | Q lateral | Q anterior | Q vertical | R continuo | R por cierres |
|---|---|---:|---:|---:|---:|---:|
| lateral–anterior | alineado | 0,500095 | 0,499905 | 0 | 1,000000 | 1 |
| lateral–anterior | opuesto | 0,500095 | 0,499905 | 0 | 0,077246 | 1 |
| lateral–vertical | alineado | 0,500095 | 0 | 0,499905 | 1,000000 | 1 |
| lateral–vertical | opuesto | 0,500095 | 0 | 0,499905 | 0,077246 | 1 |

El plano cambia `Q` pero no `R`; el emparejamiento cambia `R` pero no `Q`. El cálculo basado sólo en cierres de vuelta no ve el segundo contraste. Esto muestra que las preguntas espaciales y temporales son separables **por construcción** y que el estimador necesita información dentro del ciclo. No demuestra que mayor `R` sea más bello, menos costoso o mejor para Nico; incluso una fase estable antífasa puede ser adecuada para una tarea.

**Control adverso adicional ejecutado:** una diferencia de fase constante de `0` da `R=1`, pero una diferencia constante de `π` también da `R=1`; sólo cambia el ángulo medio. Una distribución uniforme de fases da `R≈0`. Por eso el análisis conservará **concentración y ángulo** junto con la tarea, y nunca traducirá `R=1` directamente como «correcto» o «bello». Los tres valores están en `resultados.json` bajo `negative_controls`.

Los cuatro WAV son una **sonificación diagnóstica generada desde el CSV**: canal izquierdo codifica el plano con un tono fijo y canal derecho modifica su frecuencia según la diferencia instantánea de fase. No usan Harmonic Weaver ni Beacon y no certifican que un video real proporcione esas señales. Sirven para escuchar que un mapeo separado puede conservar dos diferencias conocidas antes de trabajar con un video de baile autorizado. La etapa siguiente debe medir error de cámaras, identidad, oclusión, timestamps y audio realmente aplicado por la ruta HarMoCAP–Weaver–Beacon.

Escucha comparativa: [plano anterior, alineado](datos_sinteticos_presentacion/lateral_anterior__aligned.wav) / [plano anterior, opuesto](datos_sinteticos_presentacion/lateral_anterior__opposed.wav) / [plano vertical, alineado](datos_sinteticos_presentacion/lateral_vertical__aligned.wav) / [plano vertical, opuesto](datos_sinteticos_presentacion/lateral_vertical__opposed.wav). Usar auriculares estéreo y volumen moderado; la diferencia es diagnóstica, no una escala estética.

El manifest `resultados.json` contiene el SHA-256 del CSV, fórmulas, condiciones y límites. No hay etiquetas de belleza, sensualidad, metabolismo o conciencia sintéticas: inventarlas daría una correlación diseñada, no evidencia.
