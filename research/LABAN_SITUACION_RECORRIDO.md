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

## Condición de medición para el piloto

1. Declarar **qué** trayectoria se mide: mano, codo o curva de soga no son intercambiables. Definir origen, ejes, escala `R`, intervalo de frase, vista y si el marco acompaña la pelvis o conserva orientación de sala. Una base que gira puede producir componentes de desplazamiento aunque el punto esté quieto respecto del cuerpo; la [descomposición del marco móvil](MARCO_MOVIL_DESCOMPOSICION_C.md) hace visible ese problema. Probar sensibilidad a marcos alternativos antes de interpretar `Q` o `V_r`.
2. Exigir 3D con referencia/calibración apropiada si se afirma situación 3D. Una trayectoria 2D de HarMoCAP permite sólo `rho_min_proj` respecto de un origen proyectado y una escala proyectada declarados; profundidad oculta puede cambiar la cercanía real. No llenar oclusiones interpolando y llamar al resultado observado. La [identificabilidad 2D/3D](IDENTIFICABILIDAD_2D_3D.md) y el [protocolo piloto](PROTOCOLO_PILOTO_V0.md) fijan ese límite.
3. Reportar incertidumbre antes de umbrales: con la misma correspondencia temporal y errores máximos de posición `ε_p` y origen `ε_o`, el error absoluto de la distancia mínima **no normalizada** de dos polilíneas es como máximo `ε_p+ε_o`; para `R` fijado, `|Δrho_min|≤(ε_p+ε_o)/R`. Si `R`, ejes o identidad tienen incertidumbre, hay que incorporarla por separado. `V_r` usa diferencias y longitud total, por lo que puede reaccionar fuertemente a jitter y frecuencia de muestreo; el banco ideal no fija su precisión humana.
4. Pedir a especialistas una guía de **situación de recorrido completo**, conservar `no_codable` y desacuerdos, y comprobar acuerdo en frases reservadas. Comparar si estas cantidades continuas discriminan sus juicios mejor que `Q` solo, con los mismos clips y sin ajustar umbrales usando esos juicios de evaluación. Si no hay acuerdo o 3D fiable, informar sólo geometría descriptiva y no una clase Laban.

Para HIT, estas señales serían **contexto espacial** cuyo contraste temporal requiere un reloj de ciclo independiente y controles de tarea; para Beacon, serían canales candidatos sólo después de validar cobertura, incertidumbre y percepción del sonido. `rho_min` pequeño no significa mayor consonancia, belleza, eficiencia, salud ni experiencia especial.
