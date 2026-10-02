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

## Decisión para el programa

1. Conservar `Q` como resumen de componentes en un marco declarado; no rotularlo «plano», «subespacio», «consonancia» ni «frecuencia corporal». Su sobre científico actual no incluye el tensor completo ([contrato propuesto](CONTRATO_Q_LIVE_V0.md)).
2. Para probar la idea de Nico, generar `M` **offline** sobre el mismo soporte y los mismos tramos válidos que `Q`; registrar marco, ventana, pesos, cobertura y errores. Comparar primero A/B/C y casos degenerados, después clips humanos sólo cuando la reconstrucción 3D y el marco superen referencia independiente.
3. Elegir `k` y un criterio de estabilidad del autoplano en desarrollo, con incertidumbre de los tramos y del marco. Si el salto de autovalores no se distingue del error, reportar **subespacio no identificable**; no usar un autovector arbitrario para sonificar un plano.
4. Separar cuatro preguntas: distribución por ejes (`Q`), covariaciones de direcciones (`M`), orientación de un subespacio estimable (`P`) y secuencia temporal. Comparar su utilidad en las mismas filas con baselines y controles del [plan de estimandos](ESTIMANDOS_Y_CONTRASTES.md); ninguna de las cuatro mide por sí sola experiencia, metabolismo o conciencia.
5. Con video monocular, calcular sólo objetos **proyectados**. Poner `z=0` en la imagen no recupera el rango, el plano ni `Q` corporal 3D ([ambigüedad 2D/3D](IDENTIFICABILIDAD_2D_3D.md)). HarMoCAP/Weaver/Beacon no deberían recibir un nuevo canal 3D por esta prueba sintética; una integración futura requiere contrato, incertidumbre, replay causal y escucha con audio registrado.

**Reproducir:** `python research/q_tensor_subespacios_sintetico.py`. Su salida es un control de definiciones matemáticas, no una observación sobre movimiento humano. Para la colaboración con Weaver, esta nota complementa su [plan de banco independiente](https://github.com/AlterMundi/harmonic-weaver/issues/35), sin copiar código ni ocupar los directorios reservados a Oliva.
