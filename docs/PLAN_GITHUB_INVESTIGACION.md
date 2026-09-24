# Plan de trabajo en GitHub Issues

Versión 0.2, 24-09-2026. El [repositorio privado de investigación](https://github.com/SairaAsua/movimiento-armonico-investigacion) ya contiene [el índice general](https://github.com/SairaAsua/movimiento-armonico-investigacion/issues/14) y las 13 issues de las partes indicadas abajo. Este archivo explica su alcance localmente; **el estado y los bloqueos vigentes viven en esas issues**, no aquí. No se publicó información personal ni videos. El repositorio público `Mar-IA-no/HarMoCAP` sólo debe alojar trabajo de ese software, no el protocolo completo ni videos de Nico. Se consultaron sus issues abiertos/cerrados: el único visible era #2 sobre documentación de remotos, sin solapamiento con esta investigación. Harmonic Weaver y Beacon tienen sus propios repositorios/contratos; sus cambios de código tendrán issues y PR propios, enlazados desde el tablero privado.

## Issues abiertas y orden

| Issue | Trabajo | Dueño probable | Depende de | Criterio de aceptación revisable |
|---|---|---|---|---|
| #1 | Cotejar Laban y matriz espacial | investigación | obras + especialista | Fuente, interpretación y fórmula separadas; guía versionada. |
| #2 | Cámaras y sincronía sin personas | captura | modelos + tablero | Originales/PTS, calibración, error y decisión 2D/3D. |
| #3 | Consentimiento, repertorio y originales | investigación privada | Nico + Saira | Una o dos figuras habituales, permiso y archivo privado. |
| #4 | Validar descriptores Laban | investigación + experto | #1–#3 | Error/cobertura y acuerdo independiente. |
| #5 | Validar fase intracíclo | investigación | #2–#3 | Señales independientes, error temporal y controles negativos. |
| #6 | Experiencia y estética | investigación privada | #3 | Autoinforme por bloque, ratings ciegos por clip. |
| #7 | Contraste base → Laban → HIT | investigación | #4–#6 | Mismas filas, reserva por día y análisis congelado. |
| #8 | Costo oxidativo | laboratorio | #3 + VO₂/VCO₂ | Bloques fisiológicos y resultado rotulado correctamente. |
| #9 | Coordinar contrato temporal en Weaver | ingeniería | #2, #5 | Issue propia en repositorio de código, enlazada aquí. |
| #10 | Sonificar video de baile | ingeniería + permisos | #2, #4, #5, #9 | Escena y audio grabados; capas distinguibles. |
| #11 | Video de Nico y feedback vivo | investigación + ingeniería | #3, #6, #10 | Cobertura/latencia y controles de efecto/retención. |
| #12 | Paper 1 de factibilidad | investigación | #1–#5 | Resultados reales, incertidumbre y nulos. |
| #13 | Contrato Beacon y audio extremo a extremo | ingeniería | #9–#10 | Issues/PR de código enlazadas, reset y audio comprobados. |

**Enlaces reales:** [#1 Laban](https://github.com/SairaAsua/movimiento-armonico-investigacion/issues/1), [#2 cámaras](https://github.com/SairaAsua/movimiento-armonico-investigacion/issues/2), [#3 consentimiento/repertorio](https://github.com/SairaAsua/movimiento-armonico-investigacion/issues/3), [#4 descriptores](https://github.com/SairaAsua/movimiento-armonico-investigacion/issues/4), [#5 fase](https://github.com/SairaAsua/movimiento-armonico-investigacion/issues/5), [#6 experiencia](https://github.com/SairaAsua/movimiento-armonico-investigacion/issues/6), [#7 contraste](https://github.com/SairaAsua/movimiento-armonico-investigacion/issues/7), [#8 metabolismo](https://github.com/SairaAsua/movimiento-armonico-investigacion/issues/8), [#9 contrato Weaver](https://github.com/SairaAsua/movimiento-armonico-investigacion/issues/9), [#10 baile a audio](https://github.com/SairaAsua/movimiento-armonico-investigacion/issues/10), [#11 Nico/feedback](https://github.com/SairaAsua/movimiento-armonico-investigacion/issues/11), [#12 paper](https://github.com/SairaAsua/movimiento-armonico-investigacion/issues/12), [#13 contrato Beacon](https://github.com/SairaAsua/movimiento-armonico-investigacion/issues/13).

Cada ticket público de código deberá tener **un solo issue dueño**, alcance concreto, pruebas y PR en rama de función. Los tickets de investigación con consentimientos, rutas privadas o material identificable permanecen en el espacio privado. Una issue pública puede describir sólo interfaz y fixture sintético. No usar este archivo como tracker de estado: GitHub es el estado canónico.

## Primer hito viable sin material humano

#1 (fuentes y guía), #2 en su componente de preparación, #5 con datos sintéticos y #9/#13 en diseño de contratos se pueden avanzar sin grabar a Nico. El [dataset ejecutado](../research/datos_sinteticos_presentacion/resultados.json) es un fixture para #5/#10; no cierra #4, #7 ni #6.
