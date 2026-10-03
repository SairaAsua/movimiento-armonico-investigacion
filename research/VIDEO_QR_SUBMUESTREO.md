# El mismo video con menos cuadros: estabilidad de Q y fase

**Banco sintético de sensibilidad, 2 de octubre de 2026.** El [script](video_qr_submuestreo.py) relee los cuatro [MP4 del factorial proyectado](WEAVER_VIDEO_QR_FACTORIAL.md) y conserva sólo uno de cada `k` cuadros para `k=1,2,3,5,6,10`, probando **todos los desplazamientos iniciales posibles**. Usa los PTS originales de los cuadros retenidos. No simula exposición, obturador, compresión adicional, ruido ni pérdida de identidad de una cámara física. La pregunta es más estrecha: si la misma señal ideal se observa en una retícula temporal más rala, ¿se conservan `Q_x`, `R` y el avance angular continuo necesario para sonificar fase?

```sh
python research/video_qr_submuestreo.py \
  --input-dir /salida/de/weaver_video_qr_factorial \
  --phase-repo /checkout/de/PR-26 \
  --output-dir /ruta/nueva/para/reporte
```

El programa verifica los hashes de los MP4 contra el reporte original, los decodifica otra vez y entrega un `report.json` local. Se ejecutó dos veces con reportes byte por byte idénticos, `py_compile` y `git diff --check`. `R_wrapped` es el módulo de la media de `exp(iΔφ)` **en los cuadros retenidos**; puede calcularse sin recuperar cuántas vueltas ocurrieron entre dos cuadros. `unwrap valid` aplica la regla declarada de este fixture: ambos marcadores avanzan sin invertir sentido y cada paso observado debe tener incremento angular en `(0,π)`. No es una prueba general de fase para danza real.

| Geometría y relación | 30 fps: `Q_x`, `R` | 10 fps: rango `Q_x`, `R` | 5 fps: rango `Q_x`, `R` | 3 fps: rango `Q_x`, `R`; unwrap válido |
|---|---|---|---|---|
| Eje x / aligned | 0,740; 1,000 | 0,742–0,756; 1,000 | 0,662–0,799; 1,000 | 0,261–0,925; 1,000; **0/10** |
| Eje x / opposed | 0,740; 0,078 | 0,741–0,756; 0,077–0,078 | 0,676–0,793; 0,071–0,082 | 0,254–0,936; 0,016–0,269; **0/10** |
| Eje y / aligned | 0,265; 1,000 | 0,264–0,267; 1,000 | 0,228–0,305; 1,000 | 0,050–0,639; 1,000; **0/10** |
| Eje y / opposed | 0,265; 0,076 | 0,263–0,265; 0,075–0,077 | 0,235–0,300; 0,065–0,085 | 0,048–0,673; 0,016–0,268; **0/10** |

Los rangos representan el mínimo y máximo entre **desplazamientos de inicio**, no intervalos de confianza. A 15 fps y 6 fps todas las variantes también pasaron `unwrap` en este fixture; el reporte conserva sus rangos completos. A 3 fps ninguna de las diez posiciones de muestreo por condición pasó la regla de fase continua, aunque `R_wrapped=1` en las condiciones alineadas. Además, los rangos de `Q_x` de las dos geometrías se superponen. **Un número de concentración estable no certifica que el avance temporal entre cuadros sea identificable.** Un sonificador que necesite fase continua debe marcar esa entrada inválida; no puede usar el `R` modular para inventar vueltas intermedias.

Las elipses tienen una vuelta por segundo y una modulación intracíclo deliberadamente fuerte; por eso estos FPS no son umbrales transferibles a la soga de Nico. El rango de `Q_x` también combina cuerda poligonal más larga entre muestras y diferencias de tramo inicial/final. La decisión sobre cámaras reales exige velocidad aparente, exposición, oclusión, error de posición, PTS efectivo y diferencia mínima de fase/geométrica que se quiera distinguir ([presupuesto temporal](PRESUPUESTO_ERROR_CAMARAS.md), [protocolo de fase](FASE_ROPEFLOW.md)). Esta prueba no añade audio ni cambia el gate humano pendiente: primero hay que validar señales y su soporte, después sonificarlas.
