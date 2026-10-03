# Cuándo un cambio neto de torso supera el error de pose

Regla geométrica de diseño, 3 de octubre de 2026. Se aplica a **dos instantes o eventos previamente definidos**, no a la frase completa ni a una afirmación sobre energía. No se ha medido el error de las cámaras de Saira. Complementa el [contraejemplo de mano y torso](CENTRO_TRAYECTORIA_CONTRAEJEMPLO.md), el [presupuesto angular de direcciones](MARGEN_ANGULAR_INCLINACIONES.md) y el [ensayo de jitter del marco](CMU_UMBRAL_MARCO_VENTANA.md).

## Traslación neta del origen corporal

Sea `ĉ₀,ĉ₁` la posición estimada del **mismo origen anatómico** en un marco de sala fijo y en instantes sincronizados. Supongamos cotas *duras* `||ĉᵢ−cᵢ||≤eᵢ`, obtenidas de validación pertinente para esos instantes. Con `D̂=||ĉ₁−ĉ₀||` y `E=e₀+e₁`, la desigualdad triangular da

`max(0,D̂−E) ≤ ||c₁−c₀|| ≤ D̂+E`. **(T1)**

El límite inferior positivo certifica sólo **desplazamiento neto** bajo esas cotas; un regreso al origen entre cuadros puede tener `D̂≈0`. Si una diferencia mínima de interés `τ_D` se fija *antes* de mirar el resultado, clasificar `cambio_neto_resuelto` cuando `D̂−E>τ_D`, `dentro_del_margen` cuando `D̂+E<τ_D`, e `indeterminado` en el resto. `dentro_del_margen` no afirma inmovilidad continua. Una igualdad con la frontera queda indeterminada.

## Giro neto del marco de torso

Para orientaciones `R₀,R₁∈SO(3)` estimadas en la misma convención anatómica, usar la distancia geodésica `d(A,B)=acos(clamp((tr(AᵀB)−1)/2,−1,1))`, en radianes entre 0 y π. Si la referencia instrumental respalda cotas *duras* `d(R̂ᵢ,Rᵢ)≤aᵢ`, la desigualdad triangular del espacio de rotaciones da, con `Θ̂=d(R̂₀,R̂₁)` y `A=a₀+a₁`,

`max(0,Θ̂−A) ≤ d(R₀,R₁) ≤ min(π,Θ̂+A)`. **(T2)**

Usar una diferencia mínima `τ_Θ` fijada previamente y la misma lógica de tres estados. No restar yaw en grados sin revisar discontinuidades o inclinación: (T2) mide **giro 3D neto** y no dice qué articulación lo causó. Si la pregunta es torsión del tórax respecto de pelvis, estimar además `R_rel=R_pᵀR_t` y su error propio; la [distinción giro/torsión](GIRO_TORSION_IDENTIFICABILIDAD.md) muestra por qué el giro de la mano no lo reemplaza.

**Ejemplo exclusivamente hipotético:** `Θ̂=10°` y `a₀=a₁=3°` dan giro verdadero compatible entre `4°` y `16°`; si `Θ̂=4°`, el intervalo es `[0°,10°]`. Con `D̂=30 mm` y `e₀=e₁=5 mm`, la traslación neta queda entre `20` y `40 mm`. No son tolerancias aceptadas para el montaje, sólo aritmética del presupuesto. Para el par [sintético de mano/torso](CENTRO_TRAYECTORIA_CONTRAEJEMPLO.md), un detector ideal observaría `8,59°` y `0,14986` unidades de origen entre `t=0` y `t=π/4` en la realización B; el resultado operativo depende de cotas reales y de `τ`, no de esos números fabricados.

## Qué debe medirse antes de aplicar la regla

- Las cotas de cada pose deben corresponder a **origen y orientación anatómicos**, tarea, zona del volumen, velocidad, oclusión, algoritmo, filtro y reloj reales. La validación de un objeto rígido estático sólo mide parte de esa cadena; no certifica tórax o pelvis durante rope flow. Dos estimadores sobre el mismo video no son referencia independiente.
- Un error RMS, un percentil 95 % o una desviación estándar **no son cotas duras** y no se insertan en (T1–T2) para decir «certificado». Pueden producir intervalos probabilísticos si se modelan dependencia temporal y cobertura; el informe debe llamarles probabilísticos. Un sesgo compartido entre cuadros puede reducir error de diferencia, mientras jitter anticorrelacionado lo amplifica. Si se valida directamente el **error del cambio entre dos instantes** bajo la misma tarea, usar ese presupuesto pareado en vez de sumar límites marginales como si fueran su precisión real.
- Elegir instantes por eventos de la tarea, no por maximizar después `D̂` o `Θ̂`; registrar desfase de reloj y error de selección temporal. El cambio neto entre dos cuadros no cuantifica ida y vuelta, rapidez, trabajo mecánico ni origen causal. Para un trayecto completo informar la serie y cobertura, no convertir un par válido en garantía para toda la frase.

**Puerta hacia HarMoCAP/Beacon:** transmitir `torso_translation_net` o `torso_rotation_net` sólo con unidad, origen, referencia, par de eventos, reloj, intervalo de incertidumbre, cobertura y estado. `indeterminado` y pose ausente son estados sin valor interpretable; un sintetizador no debe convertirlos en «disonancia» ni en `core_initiated`. Una capa sonora de torso, si se desarrolla, representa un cambio medido y requiere un ensayo perceptivo distinto antes de afirmar que comunica organización corporal.
