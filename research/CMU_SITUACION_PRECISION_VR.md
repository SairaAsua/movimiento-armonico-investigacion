# Cuándo la cota de `V_r` informa algo: cálculo sobre CMU 05_02

Este es un **ejercicio de diseño** con la toma externa de danza moderna [CMU 05_02](CMU_DANZA_BANCO_REAL.md), sin soga, Nico, Reolink, «logicam», Moto G ni HarMoCAP. El [script reproducible](cmu_situacion_precision_vr.py) relee el C3D local después de verificar su SHA-256 `04bb9be74cd9183eb9f873b26c6eb4dbbf613747af5d6d0ef41f146b859d51d7` y los marcadores auditados. El archivo fuente **no se publica en este repositorio**. Usa la misma trayectoria de muñeca relativa a cintura en ejes co-rotantes y nueve ventanas de un segundo por lado que el [análisis de marcos](cmu_situacion_marcos.py). La escala para convertir a milímetros es el ancho mediano de hombros del primer segundo, `303,531939 mm`; **no** es alcance anatómico.

Del [presupuesto geométrico](PRESUPUESTO_ERROR_SITUACION.md), si hay `n` segmentos de longitud total observada `L̂` y cada punto relativo tiene error duro simultáneo a lo sumo `δ`, se cumple `|ΔV_r|≤min(1,6nδ/max(L,L̂))`. Como `max(L,L̂)≥L̂`, la condición `δ≤0,1 L̂/(6n)` es **suficiente** para que esa cota no exceda `0,1`. No es necesaria ni estima el error real. Elegimos `0,1` para mostrar la escala del problema, **no** como diferencia mínima relevante de rope flow. También calculamos la cota que resultaría si `δ=1 mm` fuera una hipótesis; no hay evidencia aquí de que una cámara tenga ese error.

| Lado y grilla derivada del C3D | Ventanas×fases | Mediana (mín.–máx.) de `δ` suficiente para cota ≤0,1, mm | Mediana de cota si `δ=1 mm` | Fracción con cota ≤0,1 bajo esa hipótesis |
|---|---:|---:|---:|---:|
| Izquierda, 120 Hz | 9 | `0,118506 (0,015556–0,314359)` | `0,843836` | `0/9` |
| Derecha, 120 Hz | 9 | `0,114387 (0,020080–0,295386)` | `0,874227` | `0/9` |
| Izquierda, 30 Hz | 36 | `0,417315 (0,028047–1,248895)` | `0,239628` | `4/36` |
| Derecha, 30 Hz | 36 | `0,379592 (0,062677–1,169453)` | `0,263441` | `8/36` |
| Izquierda, 24 Hz | 45 | `0,512165 (0,031349–1,561882)` | `0,195249` | `5/45` |
| Derecha, 24 Hz | 45 | `0,473343 (0,078936–1,457150)` | `0,211263` | `10/45` |

Las grillas de 30/24 Hz se obtienen descartando cuadros interiores en **todas** las fases posibles, conservando extremos; pueden contener `30–31` o `24–25` segmentos. Son versiones correlacionadas de las **mismas nueve ventanas**, no nuevos sujetos ni ensayos. No hay antialias, óptica, exposición, compresión, calibración de cámaras ni estimación de pose. La [prueba separada de decimación](cmu_situacion_decimacion.py) ya mostró que cambiar la grilla cambia `V_r` y `Q`; reducir `n` estrecha esta cota conservadora, **pero también cambia la polilínea que se mide**. Por tanto la tabla no recomienda filmar a 24/30 Hz ni comprar un instrumento de precisión submilimétrica: una cota suficiente puede ser mucho más estricta que el error efectivo observado, y la precisión real depende de tarea, filtro, marco, reconstrucción y referencia.

Para el banco de Saira habrá que medir error por punto relativo y por frase completa frente a referencia dinámica, comparar FPS/PTS reales, blur, oclusiones y variación de `V_r` bajo procesamiento fijado en desarrollo. Si la cota dura es trivial, se puede informar **sensibilidad empírica con su dominio y cobertura**, o dejar `V_r` exploratoria; no convertir un percentil de error en garantía universal. `rho_min` tiene un presupuesto distinto, pero exige además el [gate de poses espurias](situacion_calidad_sintetica.py). En todo caso, la prueba de una relación Laban/HIT con Nico necesita días reservados y observadores independientes, no este C3D.

La [comparación de sesgo, deriva y jitter artificiales](CMU_SITUACION_ERROR_TEMPORAL.md) muestra además que el mismo límite de error por punto puede afectar `V_r` de forma muy distinta según la relación temporal entre errores consecutivos. Es evidencia de diseño para medir autocorrelación y no sólo magnitud.
