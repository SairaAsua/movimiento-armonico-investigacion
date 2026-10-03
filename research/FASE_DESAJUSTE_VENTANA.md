# Dos ritmos próximos pueden parecer acoplados en una ventana corta

**Derivación y control sintético, sin video ni personas.** Pertenece a la [Issue #7](https://github.com/SairaAsua/movimiento-armonico-investigacion/issues/7) y complementa la [selección de razones](FASE_BUSQUEDA_RAZONES.md). La pregunta aquí es distinta: incluso con `p:q` **prefijado**, ¿cuándo una concentración `R` alta se debe solamente a observar durante poco tiempo?

Para dos fases ideales de tasa constante `φ_A(t)=2πf_A t+α` y `φ_B(t)=2πf_B t+β`, sin mecanismo de acoplamiento, la diferencia generalizada es `δₚ:q(t)=2π(q f_A−p f_B)t+(qα−pβ)`. Sea `Δf=q f_A−p f_B` en Hz. Con tiempo uniformemente ponderado en una ventana continua de duración `T`, la integral se resuelve exactamente:

`Rₚ:q(T)=|(1/T)∫₀ᵀ exp(iδₚ:q(t))dt|=|sin(πΔf T)/(πΔf T)|`,

con límite `R=1` para `Δf=0`. El desfase inicial sólo rota el vector complejo; no cambia su módulo. En la primera lóbulo, dos frecuencias muy cercanas producen `R` próximo a 1 si `|Δf|T` es pequeño. Esto **no demuestra acoplamiento**, recurrencia informativa ni consonancia estética. Tampoco un valor bajo a `T` largo refuta que haya episodios breves de coordinación: responde a otra escala temporal.

El [banco ejecutable](fase_detuning_ventana_sintetica.py) compara la fórmula con integración numérica de punto medio, 100 000 muestras **de cuadratura**, no ciclos independientes. Resultados redondeados:

| Desajuste generalizado `|Δf|` | Ventana `T` | `Rₚ:q` ideal |
|---:|---:|---:|
| 0,02 Hz | 1 s | 0,999342 |
| 0,02 Hz | 5 s | 0,983632 |
| 0,02 Hz | 10 s | 0,935489 |
| 0,02 Hz | 50 s | 0 |
| 0,10 Hz | 1 s | 0,983632 |
| 0,10 Hz | 5 s | 0,636620 |
| 0,10 Hz | 10 s | 0 |

Por ejemplo, dos señales que marcan **1,00 y 1,02 vueltas/s** conservan `R₁:₁≈0,935` durante diez segundos en este modelo, aunque su desfase se deslice continuamente y complete una vuelta en 50 s. Las cifras no son predicciones del repertorio de Nico, de sus cámaras ni de la dinámica de una soga; son una propiedad de la ventana elegida bajo tasas constantes.

## Consecuencia para medición y contraste

Además de `R` y su ángulo medio, archivar duración efectiva según PTS, ciclos completos por señal, perfil de diferencia **desenvuelta** cuando las fases sean identificables, pendiente `Δf` con incertidumbre, cobertura y cambios de tarea. Fijar la ventana principal en desarrollo según la escala de la predicción y el mínimo de datos válidos; mostrar sensibilidad a ventanas más largas **predefinidas**, sin elegir el máximo `R` entre duraciones. No inventar un «mínimo universal» de ciclos: depende del desajuste que se quiera distinguir, error de fase, pausas, oclusión y estabilidad de la tarea. Un intervalo no cíclico queda `not_applicable`.

En el estudio, el nulo relevante debe preservar cadencia y tarea comunes ([controles](CONTROLES_RITMO_COMUN.md)); una línea de fase a tasas constantes es sólo un adversario matemático. Una relación predefinida que parezca fuerte en una ventana breve y se deslice sistemáticamente al observar más ciclos se informará como **coincidencia transitoria o tasas próximas**, no como organización persistente HIT. Para Beacon live, la ventana corta permite respuesta temprana pero no certifica estabilidad: el control debe conservar estado `warmup/estimated/expired`, edad y disponibilidad causal ([diseño](FASE_CAUSAL_BEACON.md)). El sonido agradable de esa ventana tampoco valida el gesto.
