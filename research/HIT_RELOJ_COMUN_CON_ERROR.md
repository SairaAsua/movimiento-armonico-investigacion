# Un reloj de tarea imperfecto puede fabricar asociación residual entre manos

**Contraejemplo algebraico y banco sintético, 3 de octubre de 2026.** Complementa el [control de ritmo común](CONTROLES_RITMO_COMUN.md) y la [auditoría de procedencia de fases](FASE_PROCEDENCIA_CIRCULAR.md). No hay datos de Nico, cámara, fase circular ni prueba de acoplamiento fisiológico. El modelo representa **residuos locales de tiempo** en torno a un ciclo; una estimación angular real necesita tratamiento propio de envoltura y error de eventos.

## Problema de identificación

Sea `U` una variación no observada del pulso de tarea, `A=U+ε_A` y `B=U+ε_B` dos observaciones independientes de manos **condicionadas en `U`**, y `W=U+ν` un reloj de soga/música medido con error. `ε_A`, `ε_B`, `ν` y `U` son independientes en este ejemplo, de media cero, con varianzas `σ_h²`, `σ_h²`, `σ_w²` y `τ²`. **No hay interacción mano→mano.**

Si se resta de cada mano el mismo reloj observado, `A−W=ε_A−ν` y `B−W=ε_B−ν`: la covarianza residual es `σ_w²`, enteramente por el error compartido de referencia. Incluso usando el **coeficiente óptimo poblacional** de regresión lineal `λ=τ²/(τ²+σ_w²)`, los residuos son `r_A=(1−λ)U−λν+ε_A` y `r_B=(1−λ)U−λν+ε_B`. Por tanto

`Cov(r_A,r_B)=τ²σ_w²/(τ²+σ_w²)>0` si el pulso y su error tienen varianza positiva.

Condicionar por el reloj **verdadero** `U` daría `ε_A` y `ε_B`, con covarianza cero. Condicionar por `W` deja incertidumbre sobre `U`; por eso una asociación residual positiva no demuestra organización mano–mano adicional. Tampoco basta reemparejar frases: esa operación separa dos series que compartían tanto el pulso verdadero como **el error del mismo reloj**, de modo que puede reducir la correlación incluso bajo el mundo sin interacción.

## Banco reproducible

El [script](reloj_comun_error_sintetico.py) genera 400 frases de 32 ciclos, con `τ²=1`, `σ_w²=0,25`, `σ_h²=0,09` y semilla `20261003`. Cada frase se reempareja con la siguiente para el control. No se ajustó `λ` con el resultado: se usa su valor poblacional conocido, `0,8`, que favorece al método de ajuste. Los resultados son propiedades de este fixture, no tamaños esperados para rope flow.

| Comparación | Correlación teórica | Correlación simulada |
|---|---:|---:|
| Residuos de ambas manos tras regresión óptima sobre `W` | `0,689655` | `0,691234` |
| Mismos residuos, reemparejando **frases** de una mano | cercana a `0` bajo este generador | `0,003480` |
| Resta directa del mismo `W` en ambas manos | `0,735294` | `0,735955` |
| Resta del pulso verdadero `U` | `0` | `−0,003972` |

Dos ejecuciones entregaron JSON idéntico byte a byte (SHA-256 `530123bee4d487a9102266bf7ef0c70af8e36617701b09a140e7a406260db66a`). Los valores simulados se compararon con la derivación y el caso de reloj perfecto; no hay inferencia estadística sobre personas. Un reemparejamiento que «rompe» la covariación observada puede ser un **falso indicador de coordinación residual** si la referencia compartida era ruidosa.

## Decisión para la prueba HIT

Antes de llamar «ajuste entre segmentos más allá del ritmo común» a una covariación residual, estimar error, retardo y procedencia de los eventos del reloj de tarea mediante referencia independiente en el subdominio estudiado. Si se usan dos anotadores sobre el mismo video, distinguir desacuerdo humano de un sesgo compartido del propio archivo; dos algoritmos que heredan el mismo evento tampoco constituyen referencias independientes. Hacer una sensibilidad de error de reloj: cuánto de la covariación residual podría explicarse por la incertidumbre de `U` dada `W`. Si el intervalo plausible incluye toda la asociación, reportar **no identificable** bajo ese montaje. Un modelo explícito de variable latente o de errores de medición puede ser útil si sus supuestos y referencias son defendibles; no se corrige el problema eligiendo a posteriori el ajuste que deja el residuo deseado.

El contraste principal de predicción incremental `base → +Laban → +HIT` sigue siendo una pregunta distinta: el descriptor relacional puede mejorar un predictor porque resume una señal común que la base midió mal. Eso sería utilidad predictiva de esa representación, **no** prueba de interacción entre manos, menor carga correctiva o una causa corporal. El audio futuro de Beacon debe conservar `signal_source`, anclajes y calidad de reloj por capa; hacer sonar dos residuos correlacionados no valida su interpretación fisiológica.
