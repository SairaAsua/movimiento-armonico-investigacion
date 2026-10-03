# `Q`, tensor de direcciones y subespacios: tres objetos distintos

Nota matemática y banco sintético del 2 de octubre de 2026. Responde a la pregunta de integración abierta en [Weaver #35](https://github.com/AlterMundi/harmonic-weaver/issues/35): comparar `Q`, el tensor direccional completo y subespacios **sin declararlos equivalentes**. No se usó video de Nico, no se validó ninguna cámara y no se infiere belleza, economía, HIT ni un plano de Laban.

## Qué resume cada objeto

Para tramos 3D válidos `dᵢ` en un **marco y una ventana fijados**, con `ℓᵢ=‖dᵢ‖>0`, `uᵢ=dᵢ/ℓᵢ` y `L=Σℓᵢ`, definir el segundo momento direccional `M=Σ(ℓᵢ/L)uᵢuᵢᵀ`. Es simétrico, semidefinido positivo y tiene traza uno. Nuestra señal `Q=diag(M)` en ejes lateral/superior/anterior registra la fracción del recorrido atribuible al cuadrado de cada componente ([definición usada en replay CMU](CMU_Q_CAUSAL_PLANOS.md)). `Q` descarta las tres covariaciones fuera de la diagonal. `M` retiene esas covariaciones, pero **ambos** descartan el signo de cada `uᵢ`, el orden de tramos, las pausas y la rapidez temporal.

Un punto de la variedad grassmanniana `Gr(k,3)` es un **subespacio lineal de dimensión k**; puede representarse por su proyector ortogonal `P=UUᵀ` con `UᵀU=Iₖ`, distinto del momento `M` general ([Edelman, Arias y Smith, 1998, artículo original](https://math.mit.edu/~edelman/publications/geometry_of_algorithms.pdf)). Se puede *derivar* un candidato de subespacio principal de `M` eligiendo `k` autovectores, pero `k` y el salto `λₖ−λₖ₊₁` necesitan justificación y error medido. Un `M` con autovalores empatados no determina de forma única el subespacio principal de esa dimensión. Tampoco equivale automáticamente al plano de mejor ajuste de **posiciones**, que parte de otra matriz y requiere extensión bidireccional y residual validado ([planos](IDENTIFICABILIDAD_PLANOS.md)).

## Contraejemplo exacto

Sea `eL=(1,0,0)` y `eU=(0,1,0)`. Tres recorridos sintéticos de igual arco total usan: A, sólo dirección `(eL+eU)/√2`; B, mitad de arco en `eL` y mitad en `eU`; C, sólo dirección `(eL−eU)/√2`. En los tres casos **`Q=(1/2,1/2,0)`**. Sin embargo:

| Recorrido | `M` en el bloque lateral/superior | Rango / geometría de direcciones |
|---|---|---|
| A | `[[1/2, 1/2], [1/2, 1/2]]` | Rango 1: línea diagonal positiva. |
| B | `[[1/2, 0], [0, 1/2]]` | Rango 2: direcciones que abarcan el plano lateral-superior; el subespacio principal de dimensión 1 es ambiguo. |
| C | `[[1/2, −1/2], [−1/2, 1/2]]` | Rango 1: línea diagonal negativa, ortogonal a la de A. |

El determinante de ese bloque es `0` para A/C y `1/4` para B. A y C tienen la **misma `Q` y subespacios de dimensión 1 distintos**; A y B tienen la misma `Q` y **dimensión de extensión distinta**. Por tanto ninguna función de `Q` sola puede recuperar el tensor, el subespacio principal o su dimensión en general. Además, permutar los tramos `L,L,U,U` a `L,U,L,U`, o invertir el sentido de cada paso, deja `M` igual: para orden, retorno y fase HIT hace falta conservar la serie temporal. El [script reproducible](q_tensor_subespacios_sintetico.py) comprueba estas igualdades con Python estándar.

Bajo una **rotación fija** de los ejes `R`, `M` se transforma como `RᵀMR`: sus autovalores se conservan, pero `diag(M)` generalmente cambia. En A, al rotar los ejes 45° hasta alinear el primero con la diagonal, `Q` pasa de `(1/2,1/2,0)` a `(1,0,0)`. Si el marco corporal **varía por cuadro**, no se trata simplemente de conjugar un único `M`: cambia cada `dᵢ` y puede cambiar el recorrido observado ([comparación de marcos CMU](CMU_Q_MARCOS_LIVE.md)).

## Qué error permitiría hablar de un subespacio

La [cota ya derivada para cada componente de `Q`](PRESUPUESTO_ERROR_Q.md) también admite una versión para el tensor completo, **si** los tramos visibles verdaderos y estimados pueden emparejarse con la misma identidad y definición de recorrido. Sean `α` una cota del error angular combinado de dirección y marco, `TV=½Σ|wᵢ−ŵᵢ|` la distancia entre pesos de longitud normalizados **sobre los tramos visibles emparejados**, y `m` una cota de la fracción de arco verdadero oculto. Entonces una cota conservadora de norma espectral es

`‖M_completo − M_estimado‖₂ ≤ ε_M = min(1, sin(min(α,90°)) + TV + m)`.

La derivación separa tres cambios. Para dos direcciones unitarias, la norma de la diferencia entre sus proyectores `uuᵀ` y `vvᵀ` es `sin(arccos|u·v|)`. Al promediar con pesos positivos, el error angular no supera el máximo `sin α`. Reponderar proyectores de rango uno cuesta a lo sumo `TV`: para cualquier vector unitario `z`, cada valor `(z·uᵢ)²` está entre cero y uno. El tensor completo es mezcla del visible y el oculto con pesos `1−m` y `m`; dos matrices semidefinidas positivas de traza uno distan como máximo uno en norma espectral. Sumar las tres cotas sobreestima posibles interacciones. **No** cubre error de correspondencia, cambio de articulación, desincronía o un marco cuyo error no esté acotado; esos casos son inválidos, no tensores con `ε_M` pequeño. Un porcentaje de cuadros perdidos tampoco da `m` sin una cota independiente del arco oculto.

De `‖ΔM‖₂≤ε_M` y el principio de mínimo–máximo se sigue que cada autovalor ordenado puede cambiar a lo sumo `ε_M`. Si el salto observado `gₖ=λₖ(M_estimado)−λₖ₊₁(M_estimado)` no excede `2ε_M`, **no se puede certificar** que el subespacio principal de dimensión `k` permanezca separado en el recorrido completo. Si `gₖ>2ε_M`, la separación espectral sí sobrevive a estos errores, pero todavía hay que informar incertidumbre angular del propio subespacio, estabilidad ante ventanas/marcos y pertinencia para la tarea. En el caso B del banco, `g₁=0`: ningún umbral positivo rescata una línea principal única; `g₂=1/2` sólo permite estudiar un plano de **direcciones** si la cota física es suficientemente menor que `1/4`. Eso no convierte el plano en una categoría histórica de Laban ni valida una salida 3D desde una cámara monocular. El script comprueba que cada uno de los tres términos de la cota puede alcanzarse por separado en un caso 2D exacto (5° de error angular, `TV=0,1` y `m=0,1`); no prueba que sus máximos ocurran juntos en un montaje real.

## Decisión para el programa

1. Conservar `Q` como resumen de componentes en un marco declarado; no rotularlo «plano», «subespacio», «consonancia» ni «frecuencia corporal». Su sobre científico actual no incluye el tensor completo ([contrato propuesto](CONTRATO_Q_LIVE_V0.md)).
2. Para probar la idea de Nico, generar `M` **offline** sobre el mismo soporte y los mismos tramos válidos que `Q`; registrar marco, ventana, pesos, cobertura y errores. Comparar primero A/B/C y casos degenerados, después clips humanos sólo cuando la reconstrucción 3D y el marco superen referencia independiente.
3. Elegir `k` y un criterio de estabilidad del autoplano en desarrollo, con incertidumbre de los tramos y del marco. Si el salto de autovalores no se distingue del error, reportar **subespacio no identificable**; no usar un autovector arbitrario para sonificar un plano.
4. Separar cuatro preguntas: distribución por ejes (`Q`), covariaciones de direcciones (`M`), orientación de un subespacio estimable (`P`) y secuencia temporal. Comparar su utilidad en las mismas filas con baselines y controles del [plan de estimandos](ESTIMANDOS_Y_CONTRASTES.md); ninguna de las cuatro mide por sí sola experiencia, metabolismo o conciencia.
5. Con video monocular, calcular sólo objetos **proyectados**. Poner `z=0` en la imagen no recupera el rango, el plano ni `Q` corporal 3D ([ambigüedad 2D/3D](IDENTIFICABILIDAD_2D_3D.md)). HarMoCAP/Weaver/Beacon no deberían recibir un nuevo canal 3D por esta prueba sintética; una integración futura requiere contrato, incertidumbre, replay causal y escucha con audio registrado.

**Reproducir:** `python research/q_tensor_subespacios_sintetico.py`. Su salida es un control de definiciones matemáticas, no una observación sobre movimiento humano. Para la colaboración con Weaver, esta nota complementa su [plan de banco independiente](https://github.com/AlterMundi/harmonic-weaver/issues/35), sin copiar código ni ocupar los directorios reservados a Oliva.

Un [antecedente de golf con Laban e inercia de un implemento](GOLF_LABAN_INERCIA_2024.md) usa otro tensor: el momento de inercia **de masa** del palo, con unidades masa×longitud². Su semejanza algebraica con nuestro `M` adimensional no permite llamar «inercia corporal» a `Q` ni deducir fuerzas de la trayectoria de una soga flexible.
