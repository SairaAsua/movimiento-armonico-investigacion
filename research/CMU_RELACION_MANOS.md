# Separación 3D entre proxies de muñeca en una toma pública de danza

**Ensayo de factibilidad offline, 03-10-2026.** Se reutiliza **sólo** la toma pública [CMU 05_02](CMU_DANZA_BANCO_REAL.md): 1.123 cuadros de marcadores a 120 Hz, auditados por SHA-256. El [script reproducible](cmu_relacion_manos.py) exige `numpy` y `ezc3d`, lee el C3D desde `research/sources/cmu_mocap/` (ignorado por Git) y no publica marcadores ni imágenes. El [contraejemplo matemático anterior](https://github.com/SairaAsua/movimiento-armonico-investigacion/blob/0d27a64/research/RELACION_ESPACIAL_MIEMBROS.md) mostró que `Q`, rapidez y fase individuales no determinan una relación espacial 3D. Esta toma **no tiene soga, Nico, valoración estética, fase de tarea, fuerza ni referencia anatómica independiente**.

## Punto, marco y denominador

La mano izquierda se representa por la media de `LWRA/LWRB`; la derecha, por `RWRA/RWRB`, **proxies de marcadores** y no centros articulares verificados. Los cuatro marcadores, hombros, cintura y dos etiquetas de control de orientación tienen residual no negativo y coordenadas finitas en los 1.123 cuadros; ello sólo señala disponibilidad según el archivo. La escala fija `L=303,531939 mm` es la mediana del ancho entre marcadores de hombros durante los **primeros 120 cuadros**, calculada antes de resumir el resto. No se optimiza a un resultado estético ni usa la toma completa para calibrar retrospectivamente una señal que se quiera llamar live.

El vector `Δp(t)=p_R(t)−p_L(t)` se expresa en sala y en ejes corporales derivados de hombros/cintura. La norma da la misma distancia en ambos marcos hasta precisión numérica, como debe ocurrir bajo rotación rígida. El **signo de la componente vertical**, en cambio, depende de la convención corporal. La proyección lateral–vertical elimina la componente delante–detrás de ese marco móvil: es una **proyección ortográfica construida**, no un video de una Reolink ni el resultado de un detector 2D.

| Resultado en anchos de hombros `L` | Mínimo | P5 | Mediana | P95 | Máximo |
|---|---:|---:|---:|---:|---:|
| Distancia 3D entre medias de pares de muñeca | 0,596430 | 1,150451 | 2,061350 | 3,731890 | 4,177092 |
| Componente vertical firmada, derecha menos izquierda | −1,346327 | −1,244535 | −0,023209 | 1,498940 | 2,537216 |
| Distancia 3D menos distancia proyectada lateral–vertical | 0,000000 | 0,000104 | 0,008188 | 0,388544 | 0,654193 |
| Diferencia absoluta de distancia al usar `LWR0/RWR0` | 0,000418 | 0,012803 | 0,185295 | 0,411231 | 0,450459 |

La proyección reduce la distancia en más de `0,1 L` en **283/1123 cuadros (25,2 %)**. Esto comprueba que la profundidad de esta toma puede importar para ese descriptor; no estima el error de ninguna cámara propia. `LWR0/RWR0` son **otros puntos del mismo archivo**, posiblemente derivados (sus residuales son exactamente cero en todos los cuadros), no una verdad externa. La discrepancia mediana entre elecciones de proxy, `0,185 L` (~56 mm), demuestra sensibilidad a la definición operacional de «muñeca», **no** error anatómico ni sesgo del primer proxy. Los cuantiles por cuadro son descripciones de una sola toma autocorrelacionada, no intervalos de confianza ni 1.123 personas independientes.

## Misma toma, cuatro vistas ortográficas fijas

La proyección anterior usa ejes que **siguen al cuerpo**, no una cámara quieta. Para acercar el análisis al problema de una toma monocular, fijamos los ejes lateral, vertical y frontal del **primer cuadro** como base de sala y construimos cuatro planos de imagen virtuales separados por giros azimutales de 45°. Para un eje de visión unitario `n`, la identidad geométrica es `D_proj²=D_3D²−(n·Δp)²`; cambiar `n` altera `D_proj` sin cambiar el vector corporal 3D. No se usa pinhole, óptica, detector, oclusión ni las cámaras disponibles: son proyecciones ortográficas del **mismo** archivo de marcadores.

| Azimut virtual fijo | Mediana de `D_proj/L` | Mediana de pérdida `D_3D−D_proj` en `L` | Cuadros con pérdida `>0,1 L` |
|---:|---:|---:|---:|
| 0° | 1,972262 | 0,046318 | 470/1123 |
| 45° | 1,358088 | 0,595251 | 986/1123 |
| 90° | 0,621071 | 1,569135 | 1082/1123 |
| 135° | 1,404485 | 0,452333 | 966/1123 |

Dentro de **cada mismo cuadro**, el rango de las cuatro distancias proyectadas tiene mediana `1,597231 L`, P95 `2,708326 L` y máximo `3,374422 L`; supera el umbral ilustrativo `0,1 L` en **1112/1123 cuadros**. Es un barrido deliberadamente amplio de vistas, no la variación esperable entre las Reolink disponibles. La diferencia `283` frente a `470` cuadros para la primera proyección tampoco mide error: la primera rota con el cuerpo, la segunda permanece fija. Los cuatro ángulos no son cuatro muestras humanas independientes, y las diferencias de sus medianas no sustituyen el contraste cuadro a cuadro.

Para comparar dos frases o estados de Nico a partir de una sola vista, hay que mantener cámara, encuadre y escala, describir orientación del torso respecto de ella y comprobar si esa orientación cambió entre condiciones. Una diferencia de `D_proj` puede surgir de profundidad o giro sin cambio de `D_3D`; tampoco puede corregirse de forma universal con la fórmula anterior si `n·Δp` es desconocido. El piloto deberá contrastar `D_proj` con referencia 3D/dinámica si pretende una relación espacial corporal; si sólo hay 2D, el resultado se mantiene como **descriptor de imagen dependiente de vista**. Para la lectura inspirada en Laban, distancia escalar proyectada tampoco conserva quién pasó delante, arriba o primero.

## Desfase artificial entre señales

El mismo script conserva **intactas** las dos trayectorias 3D y compara `D(t)=||R(t)−L(t)||` con `D_k(t)=||R(t+k/120)−L(t)||` sobre el soporte temporal común. Repite el desplazamiento hacia adelante y hacia atrás; `k` es una perturbación **impuesta**, no un residual medido de cámaras ni una triangulación multivista. En cada pareja se verifica `|D_k−D|≤||R(t+k/120)−R(t)||` por desigualdad triangular.

| Desfase impuesto a derecha | Cuadros comparables | P95 de `|D_k−D|` en `L`, adelante / atrás | Cuadros con error `>0,1 L`, adelante / atrás |
|---:|---:|---:|---:|
| 1 cuadro = 8,33 ms | 1.122 | 0,030930 / 0,031291 | 0 / 0 |
| 2 cuadros = 16,67 ms | 1.121 | 0,062242 / 0,062941 | 12 / 13 |
| 4 cuadros = 33,33 ms | 1.119 | 0,122875 / 0,127590 | 118 / 132 |
| 8 cuadros = 66,67 ms | 1.115 | 0,241249 / 0,256246 | 322 / 389 |

El umbral `0,1 L` es **ilustrativo** y los cuadros vecinos no son réplicas independientes. Para esta toma, un desplazamiento de cuatro cuadros ya cambia la distancia en más de ese umbral en parte del recorrido; no establece que 33 ms sean tolerables o intolerables para Nico. El error de cámaras incluye otros mecanismos: dos vistas desfasadas pueden reconstruir **mal cada punto 3D** antes de emparejar las manos. Este ensayo sólo aísla el error de **emparejar dos trayectorias 3D ya dadas** en tiempos distintos. En el banco propio habrá que medir instantes de exposición/sincronía, error dinámico de reconstrucción y la diferencia mínima que el contraste quiera resolver; la rapidez observada entre cuadros no certifica una cota física de rapidez continua.

## Decisión para el estudio y Beacon

Conservar `Δp` firmado y `D=||Δp||` **por par nombrado**, marco, escala, reloj y estado de calidad. La distancia permite una comprobación de invariancia al marco rígido; su resumen escalar pierde quién pasó arriba, adelante o primero. Si el piloto sólo recupera una proyección, publicar `D_proj` con vista y unidades, sin renombrarlo `D_3d`. Si se quiere medir el orden vertical o contramovimiento histórico, hará falta además profundidad y orientación corporal validadas, tarea definida y acuerdo con especialista Laban.

En el banco técnico propio, una separación dinámica conocida entre dos marcadores/objetos debe servir de **referencia física** a velocidades, giros y oclusiones representativas; después se medirá error y cobertura por par sobre intentos completos. La toma CMU carece de esa referencia y por ello no valida exactitud. Para comparar frases de Nico, el par, el proxy, el marco, la escala y un margen mínimo de diferencia se fijarán en desarrollo antes de sesiones reservadas. `Q`, `R` HIT y la separación son preguntas distintas; ninguna de las tres prueba belleza o eficiencia. Una señal Beacon de separación sólo sería elegible después de verificar disponibilidad causal, latencia, expiración y audibilidad de su mapeo, sin iniciar ahora la cadena live.
