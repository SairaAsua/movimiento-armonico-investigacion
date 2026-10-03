# Orientación y situación del recorrido: candidato geométrico para rope flow

**Banco de geometría sintética; sin datos de Nico ni validación de categorías Laban.** Trabajo de desarrollo de la [issue #4](https://github.com/SairaAsua/movimiento-armonico-investigacion/issues/4), dependiente del cotejo conceptual de la [#1](https://github.com/SairaAsua/movimiento-armonico-investigacion/issues/1).

## Motivo histórico y frontera de atribución

En [«Tanz und Musik» (1929), p. 134](https://www.dbnl.org/tekst/_int001inte01_01/_int001inte01_01_0176.php), Laban afirma que una misma inclinación espacial puede aparecer central o periféricamente; la [nota de lectura](LABAN_TANZ_UND_MUSIK_1929.md) documenta el pasaje y las limitaciones de la transcripción digital. [Longstaff (2001), pp. 72–75 y 82–83](https://ickl.org/wp-content/uploads/2016/04/Proceedings_2001_TXT.pdf) interpreta orientación de una línea y situación central/periférica/transversal como aspectos diferentes de la lectura coreútica. **Las ecuaciones de abajo son nuestras**, diseñadas para preguntar si una medición conserva esa diferencia. Ni el artículo breve de Laban ni Longstaff publicaron estos tres descriptores o umbrales para rope flow. El facsímil del artículo de 1929 y los libros completos siguen sin cotejarse aquí.

## Tres cantidades continuas, ninguna etiqueta automática

Sea `p₀,…,pₙ` una trayectoria **3D válida** de un punto corporal respecto de un origen `o` declarado, en un marco espacial y una frase definidos de antemano. Sea `R>0` una escala de alcance fijada por tarea y participante **antes** de analizar esa frase, no el máximo de la misma trayectoria. La curva es la polilínea entre muestras; `L=Σ‖pᵢ₊₁−pᵢ‖` debe ser positivo. En el [script reproducible](situacion_recorrido_sintetica.py):

| Candidato | Definición | Qué añade y qué no dice |
|---|---|---|
| `Q` | `Qⱼ=Σ‖Δpᵢ‖(Δpᵢ,ⱼ/‖Δpᵢ‖)²/L`, para los tres ejes | Distribución de **orientaciones de desplazamiento** ponderada por arco. Es ciega a una traslación de todo el recorrido; no indica situación respecto del centro. Cambia si rotamos los ejes elegidos. |
| `rho_min` | `minₛ‖p(s)−o‖/R` sobre los **segmentos finitos** observados | Cercanía mínima de la curva al origen; el mínimo de la recta infinita que contiene un segmento puede ser falso para el trecho realmente recorrido. No basta para clasificar una frase completa. |
| `rho_max` | `maxᵢ‖pᵢ−o‖/R` | Alcance máximo de la polilínea; puede informar cobertura y calibración, pero un solo extremo no describe la situación de toda la frase. |
| `V_r` | `Σ(rᵢ+rᵢ₊₁−2mᵢ)/L`, donde `rᵢ=‖pᵢ−o‖` y `mᵢ` es el radio mínimo **sobre el segmento finito** `i` | Variación total de radio a lo largo de toda la polilínea dividida por su longitud, entre 0 y 1. Distingue idealmente un arco de radio constante de un avance radial; depende del muestreo y del ruido. Usar sólo `Σ|rᵢ₊₁−rᵢ|` perdería la bajada y subida radial dentro de una cuerda. |

Para un segmento de extremos relativos `a,b`, `rho_min` proyecta el origen a `a+t(b−a)` con `t=clip(−a·(b−a)/‖b−a‖²,0,1)`; si el segmento tiene longitud cero, usa `‖a‖`. Esto evita llamar «central» a un trecho que no llega al centro sólo porque su **recta extendida** sí pasaría por él. Si `L=0`, `Q` y `V_r` son inválidos; no se rellenan con cero.

## Contraejemplos ejecutados

`python research/situacion_recorrido_sintetica.py` produce estos valores con origen `(0,0,0)` y `R=1,5` unidades arbitrarias; todos los puntos están dentro de ese radio. Son figuras matemáticas, no posturas observadas:

| Curva ideal | `Q` | `rho_min` | `V_r` | Lectura limitada |
|---|---:|---:|---:|---|
| Recta de `(-1,0,0)` a `(1,0,0)` pasando por el origen | `(1,0,0)` | `0` | `1` | Cruza el centro. |
| Recta paralela de `(-1,0.5,0)` a `(1,0.5,0)` | `(1,0,0)` | `0,333333` | `0,618034` | Misma orientación `Q`, diferente situación. |
| Tramo de `(0.4,0,0)` a `(0.8,0,0)` | `(1,0,0)` | `0,266667` | `1` | Su línea **infinita** pasa por el centro, el trecho observado no. |
| Semicírculo poligonal de radio `1,5` | `(0.5,0.5,0)` | `0,998795` | `0,024549` | Permanece cerca de la frontera. Las cuerdas entran ligeramente y vuelven a salir; al refinar la malla, `rho_min→1` y `V_r→0` para el círculo ideal. |

El banco también comprueba que trasladar **trayectoria y origen juntos** conserva las cuatro cantidades, y que escalar trayectoria y `R` juntos conserva las razones adimensionales y `Q`. Es una prueba de propiedades del cálculo, no de validez de una categoría histórica o corporal. Un mismo valor de `rho_min` puede describir trayectorias muy distintas; ninguna de estas cantidades por sí sola decide central/periférico/transversal.

## Prueba de sensibilidad en movimiento humano externo

El [archivo CMU 05_02 ya auditado](CMU_DANZA_BANCO_REAL.md) contiene danza moderna con marcadores, **sin soga ni referencia anatómica independiente**. El [script de sensibilidad](cmu_situacion_marcos.py) verifica su SHA-256 `04bb9be74cd9183eb9f873b26c6eb4dbbf613747af5d6d0ef41f146b859d51d7`, residual de diez marcadores y marco no degenerado mediante los lectores existentes. La escala es la mediana de separación de hombros durante los primeros 120 cuadros: `303,532 mm`. En esta prueba `R=1` significa **un ancho de hombros**, no alcance disponible; un valor `rho>1` no es un fallo corporal. Se usan nueve ventanas consecutivas de 120 intervalos a 120 Hz (0–9 s), con extremos compartidos y últimos 42 cuadros fuera.

Se compara la muñeca proxy relativa al centro de cintura expresada (a) en ejes que giran con el torso cuadro a cuadro y (b) en los ejes del primer cuadro, congelados durante la toma. **Ambas restan el traslado de cintura**, pero sólo (a) quita el giro global del torso. El cálculo coteja la rama (a) con el replay CMU anterior. Por conservación de norma bajo rotación, el radio en cada cuadro coincide exactamente; `rho_min` de la *polilínea* puede diferir un poco porque interpolar entre dos cuadros en ejes distintos traza cuerdas distintas.

| Proxy | Máxima diferencia `rho_min` (anchos de hombro) | Mediana / máxima `|ΔV_r|` | Máxima distancia L1 entre `Q` |
|---|---:|---:|---:|
| Muñeca izquierda | `0,000000` a seis decimales | `0,046835 / 0,288521` | `0,402935` |
| Muñeca derecha | `0,000232` | `0,020828 / 0,224827` | `0,388269` |

La diferencia máxima de `V_r` ocurre en la ventana 600–720 (5–6 s) para ambas muñecas. Allí la izquierda da `0,418852` con ejes móviles y `0,130331` con ejes fijos; la derecha, `0,391500` y `0,166673`. La longitud de trayectoria izquierda correspondiente es `2,811059` frente a `9,051072` anchos de hombro, y la derecha `3,513261` frente a `8,280996`: **el denominador de `V_r` cambia mucho** cuando la rotación corporal entra o sale del recorrido. No se atribuye esa ventana a una figura particular sin anotación de la tarea. Los números son descripciones de este archivo y de estos dos marcos, no error de pose ni evidencia de que uno sea la lectura Laban correcta.

La consecuencia práctica es separar dos preguntas: cercanía radial de una mano al centro declarado, relativamente estable frente a una rotación de ejes, y fracción de recorrido radial, que depende mucho de qué movimiento se resta al definir la trayectoria. Registrar ambas versiones en desarrollo; fijar una y su incertidumbre antes de reservar sesiones de Nico. Una sola vista 2D de HarMoCAP no hereda la validez 3D de este C3D ni permite inferir la curva de soga.

### Cambiar el origen no es lo mismo que girar los ejes

El [segundo script CMU](cmu_situacion_origen.py) mantiene los **mismos ejes co-rotantes, archivo, nueve ventanas y escala**; cambia sólo el origen: (a) media de dos marcadores de cintura, (b) punto medio entre ese centro y la media de los dos hombros. Los dos son proxies geométricos, **no** centros anatómicos certificados ni el “core” de una teoría fisiológica. El desplazamiento entre orígenes tuvo mediana `0,816388` y máximo `0,846985` anchos de hombro durante la toma.

| Proxy | Mediana / máxima `|Δrho_min|` (anchos de hombro) | Mediana / máxima `|ΔV_r|` |
|---|---:|---:|
| Muñeca izquierda | `0,276239 / 0,623151` | `0,170647 / 0,251502` |
| Muñeca derecha | `0,239906 / 0,346715` | `0,153589 / 0,302719` |

En la ventana izquierda 480–600 (4–5 s), por ejemplo, `rho_min` pasa de `1,428303` con cintura a `0,805152` con origen medio; la diferencia `0,623151` es menor que el desplazamiento máximo de origen en esa ventana (`0,822814`). Para dos orígenes cuyas posiciones difieren como máximo `δ` en cada muestra, con los mismos tiempos, ejes y escala `R`, la diferencia de mínimos de las polilíneas no puede superar `δ/R`: la interpolación lineal de dos desplazamientos acotados también está acotada por `δ`. El script comprueba esa cota en las 18 ventanas proxy×lado y verifica que el cambio de trayectoria equivale al desplazamiento del origen en el marco móvil.

Este contraste **no estima error instrumental**: cambia deliberadamente el objeto matemático. Muestra que declarar “cercanía al centro” sin fijar qué centro se usa puede producir una diferencia del mismo orden que la medida. La futura guía experta debe escoger el origen según la pregunta, no según cuál resultado parezca más armónico; el banco técnico de Nico deberá medir además la incertidumbre del origen elegido.

## Control factorial con `Q` y fase HIT

El [factorial Laban–HIT anterior](LABAN_HIT_FACTORIAL.md) cruzaba plano `Q` y relación temporal `R₁:₁`. El [nuevo banco 2×2×2](laban_hit_situacion_factorial.py) añade **situación radial**: toma la misma curva circular ideal de la segunda mano y la traslada `0,6` unidades a lo largo del eje lateral, conservando exactamente cada desplazamiento y rapidez cuadro a cuadro. Usa origen fijo `(0,0,0)` y normalizador geométrico `R=2`, que **no** representa alcance humano. La primera mano es el reloj matemático de referencia del banco anterior; las fases son conocidas por construcción, no estimadas de sensores independientes.

| Factor cambiado | `Q` | `rho_min` | `R₁:₁` | Lo que comprueba |
|---|---:|---:|---:|---|
| Círculo sin traslado → trasladado, plano lateral–anterior, tiempo `locked` | `(0,5; 0,5; 0)` en ambos | `0,499998 → 0,199999` | `1 → 1` | Situación distinta con orientación, longitud, rapidez y fase iguales. |
| Círculo sin traslado → trasladado, mismo plano, tiempo `drift` | `(0,5; 0,5; 0)` en ambos | `0,499996 → 0,199997` | `0,472001 → 0,472001` | La separación también persiste con fase variable. |
| Plano lateral–anterior → lateral–vertical, mismo traslado y tiempo | `(0,5; 0,5; 0) → (0,5; 0; 0,5)` | Igual hasta `0,001` por muestreo | Igual | El cambio de plano altera `Q`, no exige cambiar situación o fase. |
| Tiempo `locked` → `drift`, mismo plano y traslado | Igual hasta `0,0001` | Igual hasta `0,001` por muestreo | `1 → 0,472001` | El cambio temporal altera `R`, no exige cambiar geometría continua. |

Los ocho casos y las verificaciones numéricas están en el script. `V_r` también separa el círculo sin traslado (`≈0,0016`, residuo de cuerda) del trasladado (`≈0,382`). El largo analítico es idéntico; el largo poligonal cambia unas millonésimas al muestrear distinta velocidad. El banco prueba que un canal de situación **podría aportar información ausente de `Q/R`** en la representación. No prueba independencia estadística de esas variables en cuerpos, ni que una persona pueda trasladar la figura sin cambiar esfuerzo, intención o tarea. En un Beacon futuro, un mapeo que sólo reciba `Q/R` no podrá hacer audibles estos dos círculos como situaciones distintas; agregar un control requiere antes 3D, origen y escala fijados, validez frente a referencia y una prueba perceptiva del audio producido.

## Condición de medición para el piloto

1. Declarar **qué** trayectoria se mide: mano, codo o curva de soga no son intercambiables. Definir origen, ejes, escala `R`, intervalo de frase, vista y si el marco acompaña la pelvis o conserva orientación de sala. Una base que gira puede producir componentes de desplazamiento aunque el punto esté quieto respecto del cuerpo; la [descomposición del marco móvil](MARCO_MOVIL_DESCOMPOSICION_C.md) hace visible ese problema. Probar sensibilidad a marcos alternativos antes de interpretar `Q` o `V_r`.
2. Exigir 3D con referencia/calibración apropiada si se afirma situación 3D. Una trayectoria 2D de HarMoCAP permite sólo `rho_min_proj` respecto de un origen proyectado y una escala proyectada declarados; profundidad oculta puede cambiar la cercanía real. No llenar oclusiones interpolando y llamar al resultado observado. La [identificabilidad 2D/3D](IDENTIFICABILIDAD_2D_3D.md) y el [protocolo piloto](PROTOCOLO_PILOTO_V0.md) fijan ese límite.
3. Reportar incertidumbre antes de umbrales: con la misma correspondencia temporal y errores máximos de posición `ε_p` y del **origen ya elegido** `ε_o`, el error absoluto de la distancia mínima **no normalizada** de dos polilíneas es como máximo `ε_p+ε_o`; para `R` fijado, `|Δrho_min|≤(ε_p+ε_o)/R`. Cambiar de cintura a otro centro es una decisión de definición, no `ε_o`. Si `R`, ejes o identidad tienen incertidumbre, hay que incorporarla por separado. `V_r` usa diferencias y longitud total, por lo que puede reaccionar fuertemente a jitter y frecuencia de muestreo; el banco ideal no fija su precisión humana.
4. Pedir a especialistas una guía de **situación de recorrido completo**, conservar `no_codable` y desacuerdos, y comprobar acuerdo en frases reservadas. Comparar si estas cantidades continuas discriminan sus juicios mejor que `Q` solo, con los mismos clips y sin ajustar umbrales usando esos juicios de evaluación. Si no hay acuerdo o 3D fiable, informar sólo geometría descriptiva y no una clase Laban.

Para HIT, estas señales serían **contexto espacial** cuyo contraste temporal requiere un reloj de ciclo independiente y controles de tarea; para Beacon, serían canales candidatos sólo después de validar cobertura, incertidumbre y percepción del sonido. `rho_min` pequeño no significa mayor consonancia, belleza, eficiencia, salud ni experiencia especial.
