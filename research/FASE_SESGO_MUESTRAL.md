# Tamaño muestral, dependencia y concentración de fase

Lectura y derivación metodológica, 24-09-2026. Fuente primaria: [Vinck, van Wingerden, Womelsdorf, Fries y Pennartz (2010), *NeuroImage*, doi:10.1016/j.neuroimage.2010.01.073](https://www.psychologie.hhu.de/fileadmin/redaktion/Fakultaeten/Mathematisch-Naturwissenschaftliche_Fakultaet/Psychologie/CompPsy/Papers/vinck2010_wingerden.pdf), PDF original completo de 11 páginas consultado. Su experimento es **neuroeléctrico en ratas**, no rope flow: el aporte transferible aquí es la estadística circular y la condición explícita de independencia de observaciones. El artículo toma las fases como ya estimadas; no valida nuestros detectores de fase, ni una relación armónica corporal, ni una economía energética.

## Identidad finita que importa para HIT

Sea `θ_j` un desfase válido por observación y `R=|Σ_j exp(iθ_j)|/N`. Para `N≥2`, la consistencia por pares de Vinck et al. es `PPC=2Σ_{j<k}cos(θ_j−θ_k)/[N(N−1)]`. Al expandir el módulo cuadrado de la suma compleja se obtiene exactamente

`PPC = (N·R²−1)/(N−1)`.

Si las `θ_j` son muestras **independientes e idénticamente distribuidas** de una distribución circular cuyo vector medio tiene módulo `ρ`, entonces `E[R²]=ρ²+(1−ρ²)/N` y `E[PPC]=ρ²`. En particular, con fases uniformes independientes (`ρ=0`), `E[R²]=1/N`: `R` tiende a parecer mayor con pocas observaciones aunque no haya dirección media poblacional. `PPC` corrige ese sesgo **para `ρ²`, no para `ρ`**. Una estimación `PPC<0` es posible y no debe truncarse a cero ni convertirse por raíz cuadrada en una supuesta `R` corregida. Vinck et al. hacen explícita la independencia usada en la demostración; que los pares compartan observaciones afecta la varianza, no esa esperanza bajo el modelo.

## Por qué los cuadros de una frase rompen la corrección

Un contraejemplo exacto de diseño: tomar `K=3` fases uniformes independientes y repetir cada una `m=4` veces como si fueran `N=12` cuadros nuevos. El vector medio y `R` son los de **tres** fases, no doce. Su esperanza bajo el nulo es `E[R²]=1/3`, mientras aplicar la fórmula de doce observaciones da `E[PPC]=(12/3−1)/11=3/11≈0,2727`, aunque la consistencia poblacional entre fases independientes sea cero. La corrección de Vinck et al. **no elimina dependencia temporal**; aumentar FPS o copiar cuadros no crea ciclos nuevos. El [banco reproducible](fase_sesgo_muestral_sintetico.py) verifica la identidad y la simulación de este ejemplo.

## Regla para el protocolo de Nico

Conservar `R_t` ponderado por tiempo para describir qué fase ocupó los instantes **válidos**, y `R_c` para describir consistencia entre ciclos, como distingue [la especificación de fase](FASE_ROPEFLOW.md). No presentar `N_cuadros` como tamaño muestral independiente ni usar `PPC` sobre todos esos cuadros para «corregir» un efecto HIT. Una comparación adicional podría calcular `PPC` sobre **un ángulo por ciclo**, definido de antemano a partir del vector complejo del ciclo, y reportar también su concentración interna `|z_k|`. Aun entonces, ciclos vecinos de una misma frase pueden depender entre sí y compartir soga, música, fatiga y consigna; examinar esa dependencia en desarrollo y usar sesiones/días para la incertidumbre inferencial. Si no hay suficientes ciclos o sesiones, reportar descripción y precisión limitada, sin inferencia de población.

La fase de cada ciclo debe provenir de señales realmente observadas y comparables; [procedencia circular](FASE_PROCEDENCIA_CIRCULAR.md) y [control de ritmo común](CONTROLES_RITMO_COMUN.md) siguen siendo gates separados. Un `PPC` positivo puede representar fase estable respecto de una tarea o entrada común y no prueba acoplamiento directo, belleza, menor VO₂ ni la conjetura H4 de HIT. Para Beacon en vivo, estas estadísticas de bloque cerrado tampoco son disponibilidad instantánea: cualquier señal causal requiere ventana retrospectiva, cobertura, latencia y vencimiento propios.
