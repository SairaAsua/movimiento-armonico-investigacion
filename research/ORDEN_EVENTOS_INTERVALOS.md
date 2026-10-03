# Cuándo puede afirmarse qué evento ocurrió primero

**Contrato matemático de investigación, 03-10-2026.** La [lectura de Laban sobre sucesión y simultaneidad](https://github.com/SairaAsua/movimiento-armonico-investigacion/blob/de0908f/research/LABAN_CORRELACIONES_1926.md) motiva preguntar por orden entre miembros; el [contraejemplo](https://github.com/SairaAsua/movimiento-armonico-investigacion/blob/de0908f/research/canon_fase_orden_sintetico.py) muestra que `Q`, `R` global y ángulo medio pueden perderlo. Aquí fijamos una **regla nuestra** para afirmar orden temporal desde observaciones. El [script pequeño](orden_eventos_intervalos_sintetico.py) comprueba la aritmética con tiempos inventados. No estima precisión de cámara, no ejecuta HarMoCAP/Weaver/Beacon y no clasifica un movimiento real.

## Evento como intervalo, no como un cuadro puntual

Para cada evento `e` conservar un intervalo de soporte **cerrado** `I_e=[a_e,b_e]` en un reloj común, su disponibilidad `v_e`, definición de evento, persona/miembro, IDs de los cuadros que lo acotan, estado y procedencia de la cota. `a_e,b_e` deben cubrir el **instante físico del evento** bajo los supuestos declarados, no sólo el timestamp de recepción del primer cuadro que lo muestra. Una detección por cruce de umbral entre el último cuadro anterior y el primero posterior suele dejar el evento entre ambos; esa interpretación requiere además identidad correcta, criterio estable y ausencia de una excursión no observada. Si falta un lado por oclusión, no se reemplaza con un cuadro `held`: el intervalo se amplía justificadamente o el evento queda sin soporte.

Para dos eventos A y B, todos los retardos `t_B−t_A` compatibles con sus intervalos quedan dentro de **`[a_B−b_A, b_B−a_A]`**. Sólo se afirma `A antes que B` si `b_A<a_B`; sólo `B antes que A` si `b_B<a_A`. Si se tocan o solapan, el orden estricto es **indeterminado con este instrumento**, incluso si los timestamps centrales parecen ordenados. La decisión causal no está disponible antes de `max(v_A,v_B)`; una sonificación que se active ahí anuncia una relación **retrospectiva**. Si sólo se conoce una distribución o percentil de error, la regla de intervalos no es una garantía dura; habrá que declarar nivel de cobertura conjunta y probabilidad de orden.

Un mapa de reloj afín `t_c=o+r t_s`, `r>0`, con cota simultánea de error `ε` transforma un intervalo fuente `[a,b]` en un intervalo común conservador `[o+ra−ε, o+rb+ε]` (redondeo externo si se almacenan microsegundos enteros). `available_at` también debe estar expresado explícitamente en el reloj común. Si no hay mapa validado, no se comparan eventos de relojes distintos. El [contrato actual de frontera](PAR_ESPACIAL_FRONTERA_CONTRATOS.md) encontró que HarMoCAP usa reloj monotónico para `captured_at_us` y Weaver reloj de pared por defecto; un mismo nombre de campo no elimina esa diferencia. Tampoco sabemos todavía cuánto separa la marca de software de la exposición óptica real en las cámaras disponibles: esa incertidumbre pertenece a la cota del evento.

## Seis casos construidos

| Caso, microsegundos arbitrarios | Soporte A | Soporte B | Retardo posible B−A | Decisión |
|---|---:|---:|---:|---|
| Clara separación | `[10,20]` | `[31,40]` | `[11,30]` | A antes que B |
| Orden inverso | `[31,40]` | `[10,20]` | `[−30,−11]` | B antes que A |
| Intervalos solapados | `[10,25]` | `[20,35]` | `[−5,25]` | Indeterminado |
| Extremos que se tocan | `[10,20]` | `[20,30]` | `[0,20]` | Indeterminado para orden estricto |
| Mismo cuadro y misma ventana | `[10,20]` | `[10,20]` | `[−10,10]` | Indeterminado |
| Centros `100` y `112`, error duro `±8` por fuente | `[92,108]` | `[104,120]` | `[−4,28]` | Indeterminado |

Los números ilustran **la lógica**, no una tolerancia usable para Nico. Dos muñecas observadas en el mismo bundle HarMoCAP comparten `captured_frame_id`: eso permite una relación espacial **del cuadro** si ambas son válidas, pero no revela cuál inició primero dentro de su exposición/intervalo. `bundle_seq` cuenta emisiones y tampoco es orden de gestos. En cuadros diferentes de una misma cámara, el orden de **cuadros** puede conocerse mientras el orden de dos inicios entre cuadros aún se solapa. En multivista, antes de comparar se añaden sincronización y error de reconstrucción/evento.

## Contrato de investigación hacia Weaver y Beacon

Una señal de orden necesita sus **dos soportes** y tres estados de salida: `A_before_B`, `B_before_A` e `unresolved`/`invalid`, además del intervalo de retardo, disponibilidad, vigencia y causa. `unresolved` no equivale a «simultáneos» ni a disonancia. Al vencer un evento, cambiar persona/calibración/reloj o aparecer una corrección `held/invalid`, se retira cualquier control previo y se propone reset; no se deja sonar una decisión antigua como actual. [Weaver #77](https://github.com/AlterMundi/harmonic-weaver/issues/77) posee la extensión versionada de procedencia temporal; el [replay de reset aislado](PAR_ESPACIAL_LIVE_CONTRATO.md) prueba sólo el comportamiento del motor con controles sintéticos, no este nuevo contrato.

Antes de usar el orden en el estudio de Nico, el equipo humano deberá escoger **qué evento corporal o de soga** corresponde a la tarea, comprobar concordancia entre anotadores, error temporal y cobertura en giros/cruces, y fijar el margen mínimo de retardo que importa para la hipótesis. El análisis reservado informará eventos válidos, indeterminados y faltantes por condición. `R` HIT se calculará sobre señales cíclicas independientes cuando la fase sea identificable; un evento de orden no lo reemplaza. Si algún día se sonifica, se probará primero control aplicado y audio grabado con pares adversos; que el sonido cambie no valida una relación labaniana ni experiencia subjetiva.
