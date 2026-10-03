# Escuchar diferencia de fase recuperada de dos puntos en video

**Sólo banco sintético.** [Video `aligned`](datos_sinteticos_video_ritmo/fase_source_aligned.mp4) · [video `opposed`](datos_sinteticos_video_ritmo/fase_source_opposed.mp4) · [audio `aligned`](datos_sinteticos_video_ritmo/fase_aligned_desde_video.wav) · [audio `opposed`](datos_sinteticos_video_ritmo/fase_opposed_desde_video.wav) · [script](video_fase_audio_diagnostico.py) · [manifiesto](datos_sinteticos_video_ritmo/fase_audio_manifest.json). Usa los puntos rojo y azul generados por el [banco de fase intracíclo](BANCO_FASE_INTRACICLO_CAMARAS.md); no graba personas ni cámaras, y no utiliza el motor de audio de Beacon.

La investigación ya tenía un control decisivo: en dos videos de ocho vueltas, el recorrido proyectado y la distribución marginal de rapidez de cada punto son comparables, pero cambia el **emparejamiento temporal** entre ambos. El [generador y analizador original](ejecutar_banco_fase_archivo.py) recupera `R₁:₁=1` en `aligned` y `≈0,0769` en `opposed` desde píxeles decodificados. Si sólo se interpolan los cierres de vuelta, ambos dan `R_eventos=1` y se pierde lo que ocurre **dentro** del ciclo. El script de esta nota **reutiliza esos videos**: localiza por separado los puntos rojo y azul, calcula sus ángulos proyectados con centros de órbita conocidos, desenvuelve cada serie y resta `δ(t)=φ_azul(t)−φ_rojo(t)`. Comprueba que su `R` coincide con el informe original antes de producir audio.

El generador original entrega FFV1/Matroska; sus bytes de contenedor cambiaron entre dos ejecuciones aunque el audio derivado fue idéntico. Este script genera esos MKV **en una carpeta temporal** para no tocar los artefactos históricos versionados, crea copias MP4 **sin pérdida** con `libx264rgb` y comprueba que los píxeles decodificados son idénticos. Vuelve a calcular `Q`, `R`, ángulos y WAV desde los píxeles y PTS de los MP4 publicados. Dos regeneraciones conservaron el SHA-256 de ambos MP4, ambos WAV y el manifiesto. Los hashes del manifiesto corresponden a los videos publicados, no a los MKV intermedios.

El mapeo sonoro de prueba es `f(t)=220+20δ(t)` Hz, con tono mono de amplitud fija. La fase del oscilador de audio se integra sin saltos entre cuadros; no se usa el siguiente cuadro para suavizar la frecuencia. La portadora 220 Hz y el factor 20 Hz/rad son **elecciones de escucha**, no frecuencias corporales ni una escala de consonancia. La serie `δ` proviene del cuadro ya decodificado: su disponibilidad live dependería de captura, procesamiento y latencia medidos. `R`, que resume los ocho segundos, sólo queda disponible **después** del bloque y no controla estos WAV.

| Resultado | `aligned` | `opposed` |
|---|---:|---:|
| `R` de fase continua desde píxeles | 1,0000 | 0,0769 |
| `R` si sólo se usan cierres de vuelta | 1,0000 | 1,0000 |
| Rango de tono audible | 220–220 Hz | 148,1–291,9 Hz |
| RMS del WAV PCM16 | 7065,14 | 7065,10 |
| Duración | 8 s | 8 s |

Así se comprueba un **contraste audible por regla de síntesis** mientras el nivel medio queda prácticamente igual. No demuestra que una persona distinga los audios en una prueba ciega, que `aligned` sea más bello/eficiente ni que HIT prediga un resultado externo. El ángulo del vector medio en `opposed` sale cerca de π, pero con `R≈0,077` su dirección es inestable y no se interpreta como desfase típico. Ambos puntos fueron generados desde un mismo reloj matemático: separar sus colores al medirlos no elimina la causa común ni prueba acoplamiento causal entre segmentos corporales.

La siguiente transferencia al estudio de Nico requiere puntos corporales/soga con **procedencia propia**, identidad tras cruces y oclusiones, marcos y PTS reconciliados, error angular y cobertura por patrón, y episodios reservados. Para Beacon, habrá que probar una estimación causal de fase, su edad y reinicio al faltar soporte, luego registrar controles aplicados y audio real con entrada acústica comparable. Véanse [procedencia y ritmo común](CONTROLES_RITMO_COMUN.md), [fase causal](FASE_CAUSAL_BEACON.md) y [gate de audio](BEACON_FACTORIAL_CONTROLES.md).

Desde la raíz, ejecutar `python research/video_fase_audio_diagnostico.py` con FFmpeg/FFprobe. Regenera los dos videos sintéticos de partida en una carpeta temporal, crea los MP4 revisables, verifica sus descriptores, y guarda los dos WAV y el manifiesto enlazados arriba. No inicia servicios.

Un [banco complementario](FASE_PROYECCION_OBLICUA.md) usa el mismo procedimiento de píxeles→fase→WAV para mostrar que una diferencia sonora puede proceder sólo de mirar una órbita uniforme en un plano oblicuo. Conserva el audio crudo y el rectificado con el factor sintético conocido, antes de trasladar ese problema al protocolo de cámaras.
