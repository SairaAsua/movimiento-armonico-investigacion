# Un reloj de tarea imperfecto puede fabricar asociación residual entre manos

**Contraejemplo algebraico y banco sintético, 3 de octubre de 2026.** Complementa el [control de ritmo común](CONTROLES_RITMO_COMUN.md) y la [auditoría de procedencia de fases](FASE_PROCEDENCIA_CIRCULAR.md). No hay datos de Nico, cámara, estimación de fase desde video ni prueba de acoplamiento fisiológico. El modelo representa **residuos locales de tiempo** en torno a un ciclo; transformarlos en ángulos para un control algebraico no equivale a extraer fase real, que requiere tratamiento propio de envoltura y error de eventos.

## Problema de identificación

Sea `U` una variación no observada del pulso de tarea, `A=U+ε_A` y `B=U+ε_B` dos observaciones independientes de manos **condicionadas en `U`**, y `W=U+ν` un reloj de soga/música medido con error. `ε_A`, `ε_B`, `ν` y `U` son independientes en este ejemplo, de media cero, con varianzas `σ_h²`, `σ_h²`, `σ_w²` y `τ²`. **No hay interacción mano→mano.**

Si se resta de cada mano el mismo reloj observado, `A−W=ε_A−ν` y `B−W=ε_B−ν`: la covarianza residual es `σ_w²`, enteramente por el error compartido de referencia. Incluso usando el **coeficiente óptimo poblacional** de regresión lineal `λ=τ²/(τ²+σ_w²)`, los residuos son `r_A=(1−λ)U−λν+ε_A` y `r_B=(1−λ)U−λν+ε_B`. Por tanto

`Cov(r_A,r_B)=τ²σ_w²/(τ²+σ_w²)>0` si el pulso y su error tienen varianza positiva.

Condicionar por el reloj **verdadero** `U` daría `ε_A` y `ε_B`, con covarianza cero. Condicionar por `W` deja incertidumbre sobre `U`; por eso una asociación residual positiva no demuestra organización mano–mano adicional. Tampoco basta reemparejar frases: esa operación separa dos series que compartían tanto el pulso verdadero como **el error del mismo reloj**, de modo que puede reducir la correlación incluso bajo el mundo sin interacción.

**Límite de este contraejemplo:** para la diferencia angular directa **1:1** de dos fases medidas independientemente y corregidas con *exactamente el mismo* reloj por muestra, `[(A−W)−(B−W)] mod 2π = (A−B) mod 2π`. El error de `W` se cancela algebraicamente, por lo que no cambia el `R₁:₁` par a par. En el generador, la concentración esperada es `exp(−σ_h²)` bajo errores gaussianos angulares independientes, aunque `A` y `B` sólo compartan `U`: un `R` alto puede describir seguimiento de la tarea sin interacción mano→mano. La cancelación no autoriza inferir causalidad; tampoco se traslada sin más a relojes distintos por señal, tiempos mal alineados ni relaciones `p:q` con `p≠q`, donde queda un término de referencia. El artefacto demostrado aquí corresponde a **covariación de residuos condicionados al reloj imperfecto**, una pregunta distinta de la concentración 1:1 directa.

## Banco reproducible

El [script](reloj_comun_error_sintetico.py) genera 400 frases de 32 ciclos, con `τ²=1`, `σ_w²=0,25`, `σ_h²=0,09` y semilla `20261003`. Cada frase se reempareja con la siguiente para el control. No se ajustó `λ` con el resultado: se usa su valor poblacional conocido, `0,8`, que favorece al método de ajuste. Los resultados son propiedades de este fixture, no tamaños esperados para rope flow.

| Comparación | Correlación teórica | Correlación simulada |
|---|---:|---:|
| Residuos de ambas manos tras regresión óptima sobre `W` | `0,689655` | `0,691234` |
| Mismos residuos, reemparejando **frases** de una mano | cercana a `0` bajo este generador | `0,003480` |
| Resta directa del mismo `W` en ambas manos | `0,735294` | `0,735955` |
| Resta del pulso verdadero `U` | `0` | `−0,003972` |

Como control de alcance, el script aplica también `|mean exp(iδ)|` a las diferencias construidas. La fase relativa 1:1 directa y la obtenida tras restar el mismo `W` dan ambas `R=0,913907` (esperado `0,913931`); sus diferencias muestra a muestra son menores que `2,3×10⁻¹⁶` radianes por redondeo. Ese cálculo no estima fase de una grabación ni valida `R` sobre rope flow.

Dos ejecuciones entregaron JSON idéntico byte a byte (SHA-256 `8151a590839da8d6ae53fd671a35c2a60b985182eb8180998bc9c3f239a9ef44`). Los valores simulados se compararon con la derivación y el caso de reloj perfecto; no hay inferencia estadística sobre personas. Un reemparejamiento que «rompe» la covariación observada puede ser un **falso indicador de coordinación residual** si la referencia compartida era ruidosa.

## Presupuesto de error para diseñar el contraste

En el mismo modelo poblacional, la covarianza espuria máxima que puede explicar un límite superior `S` de varianza del reloj es `c_max=τ²S/(τ²+S)`; con varianza propia de error de cada mano `σ_h²`, la correlación fabricada sería `ρ_artefacto=c_max/(c_max+σ_h²)`. Para exigir que esa correlación no supere un umbral **elegido para el diseño** `r`, se necesita `c_max≤c_r=σ_h²r/(1−r)`. Si `c_r<τ²`, la condición equivale a `S≤τ²c_r/(τ²−c_r)`; si no, el modelo ya queda bajo `r` incluso con reloj arbitrariamente malo. Se compararía una cota **con incertidumbre** del reloj con esta condición, no un valor puntual elegido para que pase.

El [calculador reproducible](reloj_comun_sensibilidad.py) aplica esas identidades a los parámetros construidos del banco (`τ²=1`, `σ_h²=0,09`). No hay unidades de segundos ni especificación de cámaras aquí:

| Varianza hipotética del reloj `σ_w²` | Covarianza residual atribuible al reloj | Correlación residual atribuible al reloj |
|---:|---:|---:|
| `0` | `0` | `0` |
| `0,01` | `0,009901` | `0,099108` |
| `0,05` | `0,047619` | `0,346021` |
| `0,25` | `0,2` | `0,689655` |
| `1` | `0,5` | `0,847458` |

Para que el artefacto sea menor o igual que `0,1` **en este fixture**, el límite de varianza del reloj sería `0,010101` y el de desviación estándar `0,100504` en unidades de offset construido. Dos ejecuciones del calculador dieron el mismo JSON (SHA-256 `438eb0e13c5386903412745fa69f320db21ed65b0a22387d2a4e186b22e8e778`). Es un ejemplo de dimensionamiento, **no** un umbral de FPS, milisegundos o aceptación para Nico. Si se observan varianzas residuales `V_A,V_B` distintas, un límite `c_max` se traduce en correlación espuria máxima `min(1,c_max/√(V_A V_B))` bajo los supuestos declarados; conviene contrastar primero covarianza en unidades temporales.

Para estimar `S` harán falta referencias del **mismo evento de tarea** con errores caracterizados por vías de adquisición suficientemente independientes. Dos anotadores del mismo cuadro sólo miden parte del desacuerdo de anotación: comparten exposición, cuantización temporal y posibles cuadros perdidos. Si existieran dos relojes `W₁=U+ν₁`, `W₂=U+ν₂` con errores realmente independientes entre sí y de `U`, `Cov(W₁,W₂)=τ²` y `Var(ν_i)=Var(W_i)−Cov(W₁,W₂)`; ésa es una posibilidad de identificación **condicional a esos supuestos**, no una garantía del montaje. Aplicar el presupuesto al contraste de manos exige además que los errores de reloj sean independientes de los errores manuales bajo el nulo. Un pulso de música y un cruce de soga no son réplicas del mismo evento sin una relación física demostrada. Los destellos para sincronizar cámaras fijan correspondencia entre relojes de grabación, pero no validan por sí solos la marca de la vuelta de soga. Si no se puede acotar `S` con evidencia adecuada, la covariación residual no identifica interacción adicional.

## Decisión para la prueba HIT

Antes de llamar «ajuste entre segmentos más allá del ritmo común» a una covariación residual, estimar error, retardo y procedencia de los eventos del reloj de tarea mediante referencia independiente en el subdominio estudiado. Si se usan dos anotadores sobre el mismo video, distinguir desacuerdo humano de un sesgo compartido del propio archivo; dos algoritmos que heredan el mismo evento tampoco constituyen referencias independientes. Hacer una sensibilidad de error de reloj: cuánto de la covariación residual podría explicarse por la incertidumbre de `U` dada `W`. Si el intervalo plausible incluye toda la asociación, reportar **no identificable** bajo ese montaje. Un modelo explícito de variable latente o de errores de medición puede ser útil si sus supuestos y referencias son defendibles; no se corrige el problema eligiendo a posteriori el ajuste que deja el residuo deseado.

El contraste principal de predicción incremental `base → +Laban → +HIT` sigue siendo una pregunta distinta: el descriptor relacional puede mejorar un predictor porque resume una señal común que la base midió mal. Eso sería utilidad predictiva de esa representación, **no** prueba de interacción entre manos, menor carga correctiva o una causa corporal. El audio futuro de Beacon debe conservar `signal_source`, anclajes y calidad de reloj por capa; hacer sonar dos residuos correlacionados no valida su interpretación fisiológica.
