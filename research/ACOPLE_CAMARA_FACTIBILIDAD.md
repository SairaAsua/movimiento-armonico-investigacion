# ¿Puede el video recuperar dónde ocurre el acento?

Banco sintético del 24 de septiembre de 2026 para el [descriptor de acople espacio–tiempo](ACOPLE_ESPACIO_TIEMPO.md). Se ejecutó [este script reproducible](acople_camara_sintetico.py) con Python estándar. **Todos los parámetros son inventados**: ninguno describe una Reolink, una «logicam», el Moto G ni el movimiento de Nico.

## Escenario y resultado

Una mano idealizada recorre un círculo **plano proyectado** seis veces en tres segundos (`f=2 Hz`). Dos leyes temporales tienen el mismo recorrido y diferente ubicación del acento. Se simulan 120 tomas de cada ley por condición, con ruido gaussiano independiente por coordenada y cuadro; en el escenario difícil, 10 % de puntos desaparecen independientemente. Otra condición elimina puntos sólo cerca del acento rápido. Se calcula la rapidez por diferencia de puntos adyacentes y la diferencia de rapidez media ponderada por arco entre semiplanos `x≥0` y `x<0`, dividida por radio. No se enlazan cuadros separados por huecos. El frente corporal y la proyección se suponen **perfectamente conocidos**. No hay desenfoque, compresión, error de reloj, oclusión por partes corporales ni reconstrucción 3D.

La diferencia continua teórica entre los dos hemisferios es aproximadamente `±7,086 s⁻¹` a 2 Hz. El valor «ideal por cuadros» varía ligeramente con FPS por la asignación discreta de segmentos a semiplanos. Los resultados de la semilla fija del script son:

| FPS | Radio proyectado | Ruido σ por eje | Pérdida de puntos | Ideal por cuadros A/B | Media estimada A/B | Error absoluto medio vs. ideal | Signo correcto de 240 tomas | Pares conservados |
|---:|---:|---:|---|---:|---:|---:|---:|---:|
| 30 | 50 px | 1 px | 0 % | +7,16 / −6,79 | +7,10 / −6,77 | 0,12 s⁻¹ | 100 % | 100 % |
| 60 | 50 px | 1 px | 0 % | +6,91 / −6,91 | +6,74 / −6,74 | 0,19 s⁻¹ | 100 % | 100 % |
| 120 | 50 px | 1 px | 0 % | +7,13 / −7,13 | +6,56 / −6,57 | 0,57 s⁻¹ | 100 % | 100 % |
| 30 | 15 px | 2 px | 10 % uniforme | +7,16 / −6,79 | +5,73 / −5,75 | 1,45 s⁻¹ | 100 % | ≈81 % |
| 60 | 15 px | 2 px | 10 % uniforme | +6,91 / −6,91 | +4,62 / −4,87 | 2,31 s⁻¹ | 99 % | ≈81 % |
| 120 | 15 px | 2 px | 10 % uniforme | +7,13 / −7,13 | +3,02 / −3,06 | 4,24 s⁻¹ | 85 % | ≈81 % |
| 60 | 50 px | 1 px | 10 % uniforme | +6,91 / −6,91 | +6,74 / −6,77 | 0,26 s⁻¹ | 100 % | ≈81 % |
| 60 | 50 px | 1 px | 40 % **sólo en región rápida**, ≈9 % global | +6,91 / −6,91 | +6,34 / −6,36 | 0,57 s⁻¹ | 100 % | ≈85 % |

**Interpretación acotada:** en esta fórmula con diferencias crudas, más FPS reduce el desplazamiento por cuadro mientras el ruido posicional se mantiene fijo; la longitud de cada segmento se sesga y el contraste se atenúa. La capacidad de clasificar el signo en un ejemplo de efecto deliberadamente grande no certifica precisión del valor ni sensibilidad a diferencias pequeñas reales. Las pérdidas son independientes y por eso aproximadamente `0,9²=0,81` de los pares sobreviven; en rope flow real pueden concentrarse en cruces o tramos rápidos y producir un sesgo **direccional**. A 30 fps hay menos muestras para acentos más breves o ciclos más rápidos; esta simulación no autoriza elegir 30 fps como regla.

**Pérdida informativa:** el último par de filas de 60 fps y 50 px ilustra el riesgo. La regla regional pierde aproximadamente 9 % de puntos en total, **menos** que el 10 % uniforme, y conserva más pares (85 % frente a 81 %); aun así su error medio del contraste aumenta de 0,26 a 0,57 s⁻¹ porque faltan precisamente muestras del acento. La regla es artificial y se conoce por construcción; en video real habría que mapear visibilidad por región, rapidez y cruce, además de informar una tasa global. No se puede reparar ese sesgo interpolando los tramos ausentes como si hubiesen sido observados.

## Decisión para el banco técnico

1. Medir en originales de cada cámara el radio/desplazamiento del gesto **en píxeles**, ruido de una referencia estática y de un objeto móvil de trayectoria conocida, FPS/PTS efectivos, desenfoque y pérdidas **por región del recorrido**. El tamaño aparente de la mano y soga no basta: interesa precisión del punto seguido.
2. Reproducir el mismo análisis de `C` sobre el objeto de referencia a las tasas/formatos realmente disponibles, con y sin filtro fijado. El filtro puede reducir ruido pero cambiar amplitud y desplazar el acento; informar ambos errores y latencia. Una referencia estática sola no valida velocidad.
3. Estimar un error de `C` por patrón, escala en imagen, velocidad y semiplano, y compararlo con la **diferencia mínima de interés** fijada antes de ver juicios o estados subjetivos. Reportar errores de cada media regional, cobertura y fallos de signo; no aprobar el descriptor sólo por signo correcto en este contraejemplo.
4. Si sólo se valida una proyección frontal, nombrar `spatial_speed_contrast_proj` y limitar la inferencia a ese plano. Para frente corporal 3D durante giros se requieren la reconstrucción y el marco validados; no convertir la simulación plana en una garantía de lectura Laban 3D.

Este banco complementa el [presupuesto de muestreo y ruido](PRESUPUESTO_ERROR_CAMARAS.md) y la [bifurcación del piloto](PILOTO_VALIDACION_VIDEO.md). No propone una compra ni una especificación mínima de sensor antes de evaluar el equipo disponible.
