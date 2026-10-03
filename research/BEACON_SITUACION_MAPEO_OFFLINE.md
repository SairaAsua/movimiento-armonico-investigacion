# Hacer audible una diferencia de situación: control numérico, todavía sin audio

Diseño **exploratorio** de la [issue #4](https://github.com/SairaAsua/movimiento-armonico-investigacion/issues/4), reproducible con `python research/beacon_situacion_controles.py`. Usa los ocho casos del [factorial sintético `Q`–situación–`R`](laban_hit_situacion_factorial.py) y la [copia fijada](sources/beacon_spatial.contract.de2768c3.json) del [contrato público de `beacon-spatial` en `de2768c3`](https://github.com/AlterMundi/beacon-spatial/blob/de2768c3a4f07cc0d744c89bf6e63b168e5f2b61/beacon_spatial.contract.json), SHA-256 `84383e254cd19f520eb5e19c7d6dedb0af93c95ad8b226aeb4c7694bde936dbb`. **No arrancó Weaver, OSC, SuperCollider, cámara ni audio.** El contrato fija `/beacon/gain/{N}` para `N=1…13`, ganancia `0…3`; esos números controlan filtros de un instrumento, no frecuencias corporales.

El [mapeo previo de `Q/R`](BEACON_FACTORIAL_CONTROLES.md) conserva bandas 4, 5 y 6. Esta prueba añade **dos controles de otra capa** sin cambiar los anteriores:

```text
/beacon/gain/7 = 0,2 + 0,8 · rho_min/(1+rho_min)
/beacon/gain/8 = 0,2 + 0,8 · V_r
```

`rho_min≥0` y `0≤V_r≤1` producen controles dentro de `0,2…1,0`, incluso si el radio normalizado supera 1. La función de `rho_min` es compresiva y arbitraria: que una trayectoria más periférica eleve la ganancia de una banda **no** significa que sea mejor, más bella o más eficiente. `V_r` podría omitirse del ensayo humano si su error no pasa el [gate de precisión](PRESUPUESTO_ERROR_SITUACION.md). Ninguna de las dos medidas es una etiqueta automática central/periférica de Laban.

| Curva sintética, mismo plano y fase | `Q` | `R₁:₁` | `rho_min` | `V_r` | Ganancia banda 7 | Ganancia banda 8 |
|---|---|---:|---:|---:|---:|---:|
| Círculo alrededor del origen | `(0,5;0,5;0)` | `1` | `0,499998` | `0,001571` | `0,466666` | `0,201257` |
| Mismo círculo trasladado lateralmente | `(0,5;0,5;0)` | `1` | `0,199999` | `0,381974` | `0,333333` | `0,505579` |

Ambas curvas conservan desplazamientos, rapidez y `Q/R` por construcción; el script comprueba que las bandas 4–6 son idénticas y sólo cambian 7–8. Los ocho casos del factorial generan ocho vectores de cinco ganancias distintos **numéricamente**. Eso demuestra capacidad representacional de este mapeo en esos casos, no audibilidad, fidelidad espacial ni validez de una categoría Laban. Las medidas son de la **frase terminada** y la fase `R` del ejemplo también usa el bloque completo: el vector sólo está disponible para un replay posterior, nunca desde el inicio del gesto. Un instrumento vivo necesitaría estimadores causales nuevos y otra prueba.

Si la situación pasa de válida a `invalid`, las bandas **7 y 8** reciben una orden explícita `0`; si sólo falla Q o R, sus bandas respectivas 4–5 o 6 se resetean sin fingir que la otra capa falló. El cero es una **instrucción de silencio del control**, no una distancia radial ni «disonancia corporal». La prueba numérica confirma esos vectores, pero [Weaver con `invalid:suppress` no enviaría el reset](BEACON_TRANSICIONES_Y_RESET.md): un adaptador futuro debe configurar `reset`, verificar el default de seguridad, reservar propiedad exclusiva de bandas 7/8 y comprobar la escritura **aplicada**. Si dejan de llegar frases, también necesita temporizador de vencimiento propio; la presencia de otras señales no vuelve vigente la última situación.

Para que la **escucha retrospectiva de un video de baile** tenga valor de ingeniería, primero se obtienen video original, reloj, identidad, 3D y calidad válidos; se exporta el [sobre científico de situación](CONTRATO_SITUACION_V0.md) con `not_estimated` o incertidumbre defendible, y se alinean por `phrase_id` los controles con Q/R **sólo cuando comparten definición temporal**. Después se fija una entrada acústica con energía en las bandas, se registra escena/versiones, se envían controles por Weaver y se captura la salida del instrumento. Comparar a ciegas audio A/B de las dos curvas con misma entrada, duración y nivel; pedir primero si se oye una diferencia y, en otra tarea, qué relación representa. Repetir un caso `valid→invalid` y verificar en el audio la retirada de la capa dentro de una latencia medida. Un cambio de controles no garantiza cambio audible, porque filtros, espectro de entrada, solapamiento y oído importan. La [ruta auditada HarMoCAP→Weaver→Beacon](RUTA_HARMOCAP_WEAVER_BEACON.md) aún no conserva toda la procedencia temporal ni demuestra este audio.

No usar el contrato OSC 1.4 de HarMoCAP como si ya contuviera `rho_min` o `V_r`: su pose 2D tampoco valida situación 3D. El [README actual de Nico para Weaver](https://github.com/nicoechaniz/harmonic-weaver) sigue describiendo un router de manifiestos con transporte de registro como MVP; esta prueba se limita al contrato fijado del instrumento y a números calculados. Una implementación requerirá issue/PR propios en los repositorios de producto y verificación extremo a extremo.
