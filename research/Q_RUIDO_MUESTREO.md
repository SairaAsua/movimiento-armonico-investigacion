# El ruido de posición puede convertir un descriptor espacial por arco en artefacto de muestreo

**Resultado analítico y banco sintético, 3 de octubre de 2026.** La medida `Q` de [nuestra matemática experimental](LABAN_MATEMATICA.md) pondera direcciones por longitud de arco para describir la forma espacial sin contar dos veces una zona atravesada despacio. Esa invariancia es exacta para una curva continua observada sin error y reparametrizada monótonamente. **No es automáticamente una propiedad de `Q` estimado desde cuadros ruidosos.** Ninguna ecuación aquí se atribuye a Laban y no se han probado cámaras ni movimientos de Nico.

## Mecanismo matemático

Para pasos 3D observados `Δy_i`, con longitud `l_i=||Δy_i||`, la componente del eje `x` es

`Q̂_x = [Σ_i (Δy_{i,x})²/l_i] / [Σ_i l_i]`.

Sea `y_i=x_i+ε_i`, con errores de posición independientes por cuadro y eje, isotrópicos `ε_i~N(0,σ²I₃)`. Entonces `Δε_i` tiene desviación estándar `√2σ` por eje. Si la trayectoria física es una recta unitaria sobre `x`, muestreada cada vez más densamente durante un segundo, sus pasos reales son `O(1/n)` y eventualmente quedan por debajo de los pasos de ruido. En el límite de ruido dominante, la simetría de los errores da `Q̂_x→1/3`, aunque el valor verdadero sea **1**. La longitud observada por paso tiende en promedio a `E||Δε||=4σ/√π`; por tanto la longitud poligonal estimada crece aproximadamente como `n·4σ/√π` aunque la recta física siga midiendo 1. Los incrementos de ruido adyacentes comparten un cuadro y no son independientes entre sí, pero la simetría isotrópica y la dependencia local bastan para este límite de promedios. Es una propiedad del **modelo de error propuesto**, no de toda cámara.

La ley temporal sí puede afectar el estimador a tasa finita: a FPS fijo, una zona recorrida despacio tiene pasos verdaderos menores frente al mismo `σ`, así que allí pesa proporcionalmente más el ruido. Dos ejecuciones de **la misma recta y duración**, con `x_A(t)=t` y `x_B(t)=t+0,8t(1−t)`, tienen ambas `Q_x=1` y largo 1 sin error; con ruido pueden arrojar `Q̂` distintos. Esa diferencia sería fuga del ritmo al supuesto descriptor espacial a través del proceso de medición, no una nueva cualidad coreútica.

## Banco reproducible

`python3 research/q_ruido_muestreo.py` usa sólo la biblioteca estándar. Para cada tasa genera 400 pares con **el mismo ruido** aplicado a ambos perfiles, `σ=0,002` unidades por eje, semilla `20261003`; muestra `Q̂_x`, largo y diferencia pareada. FPS significa aquí muestras uniformes de una simulación ideal de 1 s, no rendimiento o tolerancia de las cámaras disponibles.

| Cuadros/s simulados | `Q̂_x` uniforme, media | `Q̂_x` rápido al inicio, media | Largo observado uniforme, media | Largo observado rápido al inicio, media | Diferencia pareada de `Q̂_x`, media |
|---:|---:|---:|---:|---:|---:|
| 30 | 0,9860 | 0,9815 | 1,0073 | 1,0099 | −0,0044 |
| 120 | 0,8170 | 0,8098 | 1,1156 | 1,1456 | −0,0072 |
| 480 | 0,4194 | 0,4328 | 2,3549 | 2,3903 | +0,0134 |
| 1920 | 0,3394 | 0,3406 | 8,7169 | 8,7273 | +0,0012 |

Los valores son medias del fixture, **no** intervalos de confianza para humanos. Los percentiles 5/95 de las 400 réplicas se imprimen en el reporte del script; por ejemplo, para el perfil uniforme a 480 cuadros/s `Q̂_x` cae entre 0,3940 y 0,4429 en esos percentiles. Con `--sigma 0`, los cuatro FPS y ambos perfiles devuelven `Q̂_x=1` y largo 1 a precisión numérica, lo que confirma que la diferencia surge del error construido. Repetir el programa con la misma semilla produce JSON idéntico byte a byte (SHA-256 del reporte: `628875235c48f19af7e9a5476ee9255202a51cdfe9897f497efb5b7e0f032ecf`).

## El otro extremo: pocos cuadros pierden curvatura

El [segundo banco ejecutable](q_muestreo_compromiso.py) usa una curva sintética no recta `r(t)=(cos 2πt, 0,4 sin 2πt, 0,3t)` durante un segundo. Su referencia numérica densa es `Q=(0,796651; 0,198701; 0,004647)` y largo `4,613361` unidades. Se construye una retícula de 1920 cuadros/s y se retienen subconjuntos **anidados** de 4 a 1920 cuadros/s, usando exactamente el mismo ruido para cada tasa en una réplica. Los 200 errores por eje/cuadro son gaussianos independientes con `σ=0,01` unidades; la semilla es `20261004`. El error espacial es `||Q̂−Q_ref||₁`, no una valoración Laban.

| Cuadros/s simulados | Error `Q` sin ruido | Error `Q` con ruido, media | Error relativo de largo con ruido, media |
|---:|---:|---:|---:|
| 4 | 0,1229 | 0,1228 | 0,0635 |
| 8 | 0,0161 | 0,0174 | 0,0226 |
| 15 | 0,0001 | 0,0096 | 0,0058 |
| 30 | < 0,0001 | 0,0208 | 0,0072 |
| 60 | < 0,0001 | 0,0730 | 0,0362 |
| 120 | < 0,0001 | 0,2438 | 0,1459 |
| 480 | < 0,0001 | 0,8035 | 1,5389 |
| 1920 | < 0,0001 | 0,9166 | 8,4464 |

Al pasar de 4 a 15 cuadros/s, se reduce mucho el error de polilínea; de 15 a 1920, los pasos reales se acortan frente al ruido y el estimador empeora. Este **mínimo cercano a 15** pertenece sólo a esta curva, velocidad, `σ`, duración y métrica de error. Una sensibilidad con `σ=0,0005` (los demás parámetros iguales) trasladó el mínimo observado de `Q` a 30 cuadros/s (`0,000326` frente a `0,000409` a 15); incluso ese cambio de error numérico no es un criterio para cámaras reales. No se recomienda filmar rope flow a 15 ni a 30 FPS a partir de este fixture: una fase intracíclo, una soga rápida o un giro corporal pueden exigir otros intervalos, y el [banco previo de submuestreo de video](VIDEO_QR_SUBMUESTREO.md) mostró que un `R` modular puede aparentar estabilidad cuando el avance angular ya no es recuperable. El segundo reporte fue idéntico byte a byte en dos corridas (SHA-256 `45882a7c2191119b0ea63c33f65536d68e10e531bb0779d9c01c4bad417fd202`); con `--sigma 0`, el error de la salida ruidosa coincide con el error de discretización sin ruido a cada tasa.

## Decisión para el piloto y el contraste Laban–HIT

No se elegirá un FPS «más alto» suponiendo que por sí solo mejora `Q`, ni el mínimo de estos bancos como ajuste para Nico. La caracterización de cámaras sin personas debe medir error de posición **dinámico**, exposición, sincronía, correlación temporal y cobertura por velocidad/volumen; el ruido real probablemente no sea gaussiano ni independiente. Con trayectorias físicas conocidas que incluyan recta, curva, giro y velocidades del dominio previsto, procesar varias tasas efectivas y perfiles temporales de la misma geometría; cuantificar sesgo de largo y `Q`, pérdida de curvatura **y** capacidad de recuperar fase. Fijar filtrado/longitud mínima de paso en desarrollo, evaluarlos sobre recorridos reservados y marcar inválido si el desplazamiento por paso no supera el error relevante. La decisión depende del error conjunto y de la diferencia espacial/temporal que se necesite distinguir, no de un solo número.

Para el contraste incremental `base → +Laban → +HIT`, el supuesto «bloque espacial independiente del ritmo» exige **demostrar estabilidad instrumental** de `Q` bajo leyes temporales comparables y conservar cadencia/perfil de rapidez en la base. Si el descriptor cambia con ritmo sólo por muestreo o filtrado, un incremento predictivo aparente de `+Laban` podría ser información temporal disfrazada. El banco de [submuestreo de video](VIDEO_QR_SUBMUESTREO.md) mostró otro límite, incluso sin ruido: pocos cuadros deforman la polilínea y pueden perder el avance angular entre cuadros. Ambos efectos se evalúan juntos antes de sonificar `Q` o atribuirle una distinción corporal.
