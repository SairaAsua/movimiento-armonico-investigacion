# Cuando la visibilidad fabrica asociación espacio–fase

**Banco probabilístico sintético; no representa cámaras ni datos de Nico.** La [definición de `J=I(S;Φ)`](J_ESPACIO_FASE_PONDERACION.md) exige una distribución conjunta sobre tiempo o arco válido. Una selección de cuadros o tramos por visibilidad puede cambiar esa distribución. La cobertura global, e incluso la cobertura igual en cada bin de fase, no demuestra que la tabla de casos observados conserve la relación real.

## Contraejemplo exacto

Tomemos región binaria `S` y fase binaria `Φ` **independientes y equilibradas**: cada una de las cuatro celdas de `P(S,Φ)` vale `0,25`, de modo que `J_real=0`. Supongamos que se observa todo cuando `S=Φ`, pero sólo la mitad de los tramos cuando `S≠Φ`. Esta visibilidad es una regla construida para el banco, no una tasa medida. Las masas **sin renormalizar** quedan:

| | `Φ=0` | `Φ=1` |
|---|---:|---:|
| `S=0`, observado | `0,25` | `0,125` |
| `S=1`, observado | `0,125` | `0,25` |
| `S` desconocida por oclusión | `0,125` | `0,125` |

La cobertura total es `0,75` y también es `0,75` en **cada** bin de fase. Sin embargo, al normalizar sólo los casos observados, la tabla tiene diagonal `1/3` y fuera de diagonal `1/6`; `J_observado=0,056633012` nats. No hubo relación verdadera: el valor positivo lo produjo la selección. El [script exacto](j_cobertura_fase_sintetica.py) reproduce estos números con la función de información mutua del banco anterior.

El mismo archivo observado admite al menos dos tablas completas: si los `0,125` faltantes de cada fase están en las celdas **fuera** de la diagonal, se recupera la independencia `J=0`; si están en las celdas de la diagonal, `J=0,130812036` nats. La asociación de la población no queda identificada sólo por los tramos válidos y los conteos de ausencia por fase. Un control de reloj común tampoco repara automáticamente esta selección.

## Cotas exactas bajo un supuesto explícito

Si la **fase de tarea está identificada independientemente en todos los intervalos intentados**, sólo la región binaria `S` falta y se conoce el peso temporal ausente por cada fase, esas dos completaciones son en realidad los **extremos alcanzables de este ejemplo**, no sólo ilustraciones. Escribamos `p_j=P(Φ=j)>0`, `o_{ij}` para la masa observada de región `i` y fase `j`, y `m_j` para la masa de región desconocida con fase `j`. Entonces `a_j=P(S=0|Φ=j)` sólo puede estar en `[o_{0j}/p_j,(o_{0j}+m_j)/p_j]`. Para dos fases, `J=H(p_0a_0+p_1a_1)−p_0H(a_0)−p_1H(a_1)`, con `H` entropía binaria natural.

El mínimo es **cero** si los dos intervalos de `a_j` se solapan: elegir el mismo valor en ambos completa una tabla independiente. Si no se solapan, el mínimo está en los dos extremos más próximos; al acercar `a_0` y `a_1` baja la divergencia entre sus distribuciones condicionales. El máximo está en una de las cuatro esquinas del rectángulo de valores permitidos: con la marginal de fase fija, la información mutua es convexa en el canal binario `P(S|Φ)`. Esta prueba da cotas **agudas** para las masas exactas y el modelo de ausencia declarado: cada esquina y cada completación usada para el mínimo son tablas posibles. El [script de cotas 2×2](j_cobertura_cotas_2x2.py) calcula las completaciones testigo.

En el primer ejemplo, los intervalos son `a_0∈[0,5;0,75]` y `a_1∈[0,25;0,5]`: se tocan en `0,5`, por lo que `J_completo∈[0;0,130812036]` nats. **El valor visible positivo no permite excluir independencia.** En un segundo banco construido, `o=[[0,4;0,05],[0,05;0,4]]` y `m=[0,05;0,05]` dejan cobertura `0,9` en ambas fases. Los intervalos `a_0∈[0,8;0,9]`, `a_1∈[0,1;0,2]` no se tocan: `J_completo∈[0,192744757;0,368064207]` nats, frente a `J_visible=0,344315085`. Allí la asociación descriptiva **no puede desaparecer sólo por asignar las regiones faltantes** bajo esos supuestos. Tampoco demuestra HIT: progresión común de tarea, artefactos o una tercera señal pueden producirla.

Estas son cotas de **identificación**, no intervalos de confianza. No incluyen error de fase, reloj, clasificación regional, dependencia entre ciclos ni incertidumbre por muestra finita. Si falta la fase misma, no se conoce `m_j`; si se pondera por arco y el recorrido oculto no está medido o acotado, tampoco se conoce el peso ausente. En ambos casos estas cotas 2×2 **no aplican** sin hipótesis adicionales. La regla de región, bins, duración válida y unidades de análisis deben fijarse antes de la evaluación reservada.

## Decisión para el ensayo

Guardar el denominador de **todos los intentos** por frase, ciclo, fase de tarea, vista y condición. Para cada intervalo, conservar `observed`, `held`, `inferred` o `missing`, su causa y duración por reloj; el **arco de un tramo ocluido puede ser desconocido** y no debe rellenarse con una cuerda fingida. `held` no cuenta como una nueva observación de región y `missing` no equivale a región periférica. Informar `J` de casos válidos junto con cobertura por fase y, cuando pueda anotarse la región desde otra vista o referencia independiente, cobertura por **región × fase**. Si la región de un tramo ocluido es desconocida, reportar una sensibilidad que asigne sus pesos temporales de manera explícita a celdas posibles; para `J_s` hará falta además acotar o medir el arco ausente. No afirmar que el caso completo es insesgado sólo porque la cobertura media sea alta.

Si la validez depende de la región verdadera que no se observa, ponderar por probabilidad inversa estimada desde los mismos cuadros válidos no identifica la tabla por sí solo. La ruta primaria sigue siendo mejorar visibilidad/referencia y reservar sesiones completas; un análisis condicionado a subdominios predefinidos debe describir **ese** subdominio, no el repertorio entero. Para contrastar HIT, los modelos base y extendido deben usar las mismas filas, pero además informar qué frases/ciclos quedaron fuera y si su pérdida varía con fase/tarea. Para Beacon, una oclusión retira la señal; no se sonifica como baja consonancia. Nada de este banco demuestra relación estética, fisiológica o causal.
