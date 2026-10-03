# Una relación angular p:q cambia al girar el marco corporal

**Derivación y banco sintético, 3 de octubre de 2026 · issue [#5](https://github.com/SairaAsua/movimiento-armonico-investigacion/issues/5).** [Cálculo ejecutable](fase_marco_rotante_sintetica.py). Complementa la [especificación de fase](FASE_ROPEFLOW.md) y el [sesgo por proyección oblicua](FASE_PROYECCION_OBLICUA.md). Es una propiedad de **fases angulares planas construidas**; no se atribuye a Laban ni prueba HIT en personas.

## Transformación exacta bajo un giro común

Supongamos dos vectores cíclicos en el **mismo plano**, con ángulos desenvueltos `φᵢ^W(t)` y `φⱼ^W(t)` respecto de ejes fijos de sala. Si el marco corporal gira en ese plano un ángulo conocido `θ(t)` y **ambos** vectores se expresan respecto de esos mismos ejes corporales, `φᵢ^B=φᵢ^W−θ` y `φⱼ^B=φⱼ^W−θ`. Para la relación predefinida `Δₚ:q=qφᵢ−pφⱼ` se sigue:

`Δₚ:q^B(t)=Δₚ:q^W(t)+(p−q)θ(t)`.

Para `p=q`, el término común se cancela algebraicamente. Para `p≠q`, un giro variable puede reducir **o aumentar** `Rₚ:q=|⟨exp(iΔₚ:q)⟩|` sin que haya cambiado el par de trayectorias físicas. Una orientación corporal constante sólo rota el ángulo medio `μ` en `(p−q)θ`, sin alterar `R`; una orientación que varía dentro de la ventana puede cambiar ambos. Este resultado presupone un giro planar compartido, mismo instante y signo, origen consistente y fase angular de posición. **No** se traslada automáticamente a fase por eventos, Hilbert, ángulos de articulación, soga con otro origen o proyecciones 2D oblicuas.

## Dos construcciones 2:1 y control 1:1

El script promedia 20.000 muestras uniformes en diez ciclos con `ω=2π` rad/s y `θ(t)=0,8 sin(ωt)` rad. Las fases usadas permanecen cíclicas y monótonas en ambos marcos; la derivada mínima de la señal lenta en cuerpo es `0,2ω` y la de la rápida en el segundo caso es `0,4ω`. Para `p:q=2:1`, `Δ=φᵢ−2φⱼ`:

| Construcción de fases de sala | `R₂:₁` en sala | `R₂:₁` en cuerpo | Lectura limitada |
|---|---:|---:|---|
| `φᵢ^W=2ωt`, `φⱼ^W=ωt` | 1,000000 | 0,846287 | Relación exacta en sala aparece menos concentrada en cuerpo. |
| `φᵢ^W=2ωt−θ(t)`, `φⱼ^W=ωt` | 0,846287 | 1,000000 | Relación exacta en cuerpo aparece menos concentrada en sala. |

En un control 1:1 con `φᵢ^W=ωt+0,35 sin(ωt)` y `φⱼ^W=ωt`, ambos marcos dan `R₁:₁=0,969609` y el mismo `μ` numérico. Las cifras son propiedades de este caso construido y del promedio elegido, no umbrales transferibles al rope flow. Un `R` alto en cuerpo no es “falso” si la pregunta científica es coordinación **relativa al cuerpo**; sería un error describirlo como relación en sala sin transformar y comprobar el marco.

## Consecuencia para Laban, HIT y Beacon

La geometría inspirada en Laban ya distingue recorrido en sala, centrado en cintura y co-rotante ([contraste de `Q`](CMU_Q_MARCOS_LIVE.md)). La fase HIT debe tener la misma disciplina: guardar `phase_definition`, plano, origen, signo, `coordinate_frame_id`, fuente de `θ`, reloj y error de orientación **por señal**. Si se quiere comparar fase de mano en cuerpo con fase de soga en sala, transformarlas a una referencia común respaldada o definir expresamente una relación mixta; no restar los números como si compartieran ejes. Para angular `p:q`, comparar sala y cuerpo como **análisis de sensibilidad predefinido** y propagar el error temporal y angular de `θ`. Una cota de orientación `E_θ` aporta hasta `|p−q|E_θ` de incertidumbre a `Δ` bajo la transformación común; otras fuentes de error se agregan según su dependencia, sin llamarlas independientes por defecto.

El audio de Beacon puede expresar cualquiera de las relaciones si se nombra cuál y se verifica su disponibilidad causal. Una sonificación de `R₂:₁` corporal no demuestra que dos segmentos mantengan esa relación en sala, que la soga esté coordinada o que el movimiento sea bello/eficiente. Antes de usar un patrón de Nico harán falta marcos y eventos observables, referencia de orientación durante giros, cobertura y comparación por tarea en sesiones reservadas. El control matemático no suple esas mediciones.
