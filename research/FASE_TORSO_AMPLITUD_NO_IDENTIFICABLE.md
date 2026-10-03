# La fase de torso puede no ser identificable aunque `R` observado sea 1

Contraejemplo matemático del 3 de octubre de 2026. Complementa el [control de procedencia](FASE_PROCEDENCIA_CIRCULAR.md), el [banco de estimadores de fase](FASE_ESTIMADORES_BANCO.md) y la [cota de cambio neto de torso](https://github.com/SairaAsua/movimiento-armonico-investigacion/blob/7c49764/research/TORSO_CAMBIO_RESOLUBLE.md). No usa video de Nico, errores medidos de cámaras ni una ecuación de Laban o HIT.

## Misma observación, fases verdaderas incompatibles

Supongamos cuatro ciclos de un segundo con una mano de fase de referencia `φ_h(t)=2πt` y una estimación de orientación de torso `ŷ(t)=a sin(2πt)`, con `a>0`. Un ajuste ideal de seno por ciclo a `ŷ` asigna fase `φ̂_t,k=2πt` en los cuatro ciclos. Por tanto la diferencia torso–mano es cero y su concentración circular observada es `R̂₁:₁=1`.

Si el error absoluto de orientación validado fuera sólo `|ŷ(t)−y(t)|≤ε` y `2a≤ε`, son compatibles al menos estas dos historias verdaderas:

| Historia verdadera | Señal de torso `y(t)` | Desfase verdadero por ciclo | Concentración verdadera |
|---|---|---|---|
| A: seno observado | `a sin(2πt)` en los cuatro ciclos | `0,0,0,0` | `R₁:₁=1` |
| B: inversión alternada | `a s_k sin(2πt)`, con `s_k=+1,−1,+1,−1` | `0,π,0,π` | `R₁:₁=0` |

En B, `|ŷ−y|` es cero en los ciclos positivos y como máximo `2a` en los negativos; ambas historias satisfacen la **misma** observación y el mismo presupuesto de error. La señal B es continua en los límites de ciclo porque allí `sin(2πt)=0`; su derivada puede cambiar abruptamente. Es una construcción de identificabilidad, no una ejecución corporal natural ni un modelo de ruido aleatorio. Cambiar los signos de **todos** los ciclos daría además `R=1` con fase media `π` en vez de `0`: incluso cuando la concentración queda igual, el desfase puede ser desconocido.

Con valores **hipotéticos** `a=0,04 rad` (≈2,29°) y `ε=0,10 rad` (≈5,73°), la diferencia máxima de B es `0,08 rad`, menor que `ε`. El [script de biblioteca estándar](fase_torso_amplitud_sintetica.py) verifica las 400 muestras, las fases ideales por ciclo y `R̂=1` frente a `R_B≈0`. Si `ŷ` se normaliza antes de calcular fase, su amplitud pequeña desaparece del resultado: una salida numérica suave no restituye la información perdida.

## Decisión para el contraste Laban–HIT

1. La fase de una variable corporal exige una **oscilación identificable en esa variable**, no sólo pose 3D presente, cambio neto de torso resuelto entre algunos eventos o fase del reloj de soga. La prueba debe informar amplitud/radio de fase, error en esa amplitud, regularidad, fase frente a eventos de referencia, cobertura y estado por ciclo. No fijar `φ_t=0` cuando el torso está quieto o por debajo de resolución: la fase es `undefined` para ese ciclo.
2. Un par torso–mano entra en `Rₚ:q` sólo cuando **ambas** fases se estiman de observaciones segmentarias propias, con error angular de fase aceptable y soporte temporal conjunto. El registro de dependencia incluye el marco corporal: si la fase de mano se obtuvo restando orientación del mismo torso, esa referencia compartida debe figurar como entrada y se compara con el cálculo en sala cuando ambos sean válidos. Esto no vuelve automáticamente tautológico todo contraste en marco corporal, pero cambia la pregunta y puede añadir error correlacionado.
3. Antes de usar el valor para predecir un juicio o sonificarlo, perturbar las series **dentro del error instrumental medido** y repetir extracción de fase y `R` sobre ciclos válidos. Informar si relaciones 0, π o alternancia siguen siendo compatibles. No elegir sólo perturbaciones independientes por cuadro si el error tiene sesgo o correlación temporal. La cota `2a≤ε` es un caso adverso suficiente, no un umbral universal de calidad.
4. Si la fase de torso no se identifica, aún pueden reportarse trayectoria y situación espacial de la mano inspiradas en Laban, cadencia de tarea y fase de una mano/soga que sí pasen sus propios controles. Beacon puede hacer oír esos canales etiquetados; no debe sustituir la fase de torso faltante por «desarmonía» ni denominar una relación inexistente «conexión core–mano».

El `R` calculado aquí es **descriptivo de señales construidas**. No prueba que HIT prediga belleza, economía o conciencia; sólo muestra que un contraste HIT no puede ser evaluado desde una fase cuyo error permite historias incompatibles.
