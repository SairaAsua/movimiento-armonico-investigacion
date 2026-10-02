# Un mismo recorrido en video, dos leyes temporales

**Banco sintético sin personas ni soga.** [Video A: ritmo uniforme](datos_sinteticos_video_ritmo/circulo_uniforme.mp4) · [video B: ritmo variable](datos_sinteticos_video_ritmo/circulo_reparametrizado.mp4) · [script reproducible](video_curva_ritmo_sintetico.py) · [manifiesto](datos_sinteticos_video_ritmo/manifest.json). Extiende el [contraejemplo matemático](GEOMETRIA_VS_TIEMPO_TRAYECTORIA.md) para la [issue #5](https://github.com/SairaAsua/movimiento-armonico-investigacion/issues/5), sin probar HIT ni el repertorio de Nico.

Un cuadrado blanco de 7×7 píxeles representa **un punto proyectado** que recorre el mismo círculo analítico de radio 95 px, centro `(160,160)`, una vez en tres segundos. En A, la fase de construcción es `u=t`; en B, `u=t+0,8t(1−t)`, con `0≤t≤1`. Como `du/dt=1,8−1,6t>0`, B recorre el mismo círculo en el mismo sentido y sin detenerse, más rápido al principio. Estas ecuaciones son del proyecto, no de Laban. Los dos MP4 tienen 90 cuadros a 30 fps; el último PTS es 2,966667 s y la duración nominal es 3 s.

El análisis **no lee las coordenadas del generador**: decodifica cada MP4, encuentra los 49 píxeles blancos del marcador, calcula su centroide y obtiene los tiempos de `ffprobe`. Con esos puntos estima el ángulo alrededor del centro, lo desenvuelve y mide en los **89 intervalos observados** la fracción de tiempo y la fracción de longitud recorrida en la primera semicircunferencia. No cierra artificialmente el último cuadro con el primero. El centro y radio de la escena son conocidos y forman parte del instrumento de este banco; en un video humano exigirían marco/calibración y referencia propios.

| Medida desde píxeles y PTS | A uniforme | B reparametrizado |
|---|---:|---:|
| Tiempo observado en la primera semicircunferencia | 0,5056 | 0,3258 |
| Longitud observada en esa semicircunferencia | 0,5059 | 0,4969 |
| Largo poligonal de los 89 intervalos | 591,11 px | 597,01 px |
| RMSE radial frente al círculo construido | 0,285 px | 0,249 px |

El resultado reproduce **cualitativamente** el contraste exacto del modelo continuo: la forma subyacente es igual y la ocupación temporal cambia. Los porcentajes medidos no son los valores continuos exactos `0,5` y `≈0,3246`: los cuadros discretos, la cuantización a píxeles y la ausencia del intervalo de cierre introducen error. Incluso el largo poligonal observado difiere unos 5,9 px entre clips; por eso «misma curva» se refiere a la **construcción analítica**, no a igualdad exacta de las dos polilíneas extraídas. El video fue codificado sin pérdida con `libx264rgb`; el RMSE radial refleja principalmente la rasterización del centro, no una evaluación de seguimiento de soga.

La decisión de medición para el piloto queda concreta: distinguir una estadística espacial ponderada por recorrido de otra ponderada por tiempo/PTS; guardar la serie y su orden; informar el error de extracción y la cobertura. Si una asociación con belleza o economía desaparece al controlar la ocupación temporal, no se atribuirá automáticamente a geometría inspirada en Laban. Este banco tiene **una sola señal** y no mide relaciones entre fases independientes, acoplamiento, esfuerzo, costo energético, belleza ni conciencia. Para HIT aún faltan dos señales con procedencia separada, evento de tarea válido y un resultado externo reservado. Para Nico faltan video autorizado, referencia independiente de trayectoria y prueba de cámaras.

Reproducir desde la raíz con FFmpeg/FFprobe: `python research/video_curva_ritmo_sintetico.py`. El script regenera ambos MP4 y el manifiesto, verifica 90 cuadros, PTS crecientes, los 49 píxeles por marcador, ausencia de inversión y los contrastes esperados. No inicia servicios ni usa cámaras.
