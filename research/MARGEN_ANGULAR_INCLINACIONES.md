# Cuándo una etiqueta direccional resiste el error de cámara

Nota matemática y banco sintético, 23 de septiembre de 2026. Aplica a nuestro **descriptor exploratorio** `octante × eje dominante` de 24 clases, descrito en [24 inclinaciones y 26 direcciones](LABAN_24_INCLINACIONES.md). No prueba que esas clases sean los 24 signos vectoriales históricos ni que tengan valor estético. La motivación histórica de separar orientación de posición procede de la [lectura dirigida de Longstaff (2018)](https://janeway.uncpress.org/jmal/article/944/galley/1569/download/); las fórmulas y el criterio siguientes son del proyecto.

## Definición y frontera

Sea `u=(u₁,u₂,u₃)` una dirección 3D unitaria de **un tramo previamente definido**, en un marco corporal o de sala especificado. Para etiquetar un octante, los tres signos deben ser distintos de cero; para etiquetar el eje dominante, una magnitud `|uₖ|` debe exceder estrictamente a las otras dos. Las fronteras de clasificación son planos que pasan por el origen: `uᵢ=0` para un cambio de octante y `|uᵢ|=|uⱼ|` para un empate entre ejes. **No** son umbrales de belleza ni planos de Laban; son discontinuidades de esta codificación digital.

En la esfera unitaria, la distancia angular hasta una frontera `uᵢ=0` es `asin(|uᵢ|)`. Para un par de componentes dentro de un octante, la distancia angular hasta `|uᵢ|=|uⱼ|` es `asin((||uᵢ|−|uⱼ||)/√2)`. Ambas fórmulas se obtienen como distancia de un punto unitario a un plano por el origen: `asin(|n·u|)` para normal unitaria `n`. El mínimo de las tres primeras distancias y de las dos fronteras entre el eje mayor y los otros es la **distancia a cambiar una clase de 24**. Si se conserva además el orden de las tres magnitudes, se agrega la frontera entre segunda y tercera (las 48 celdas estrictas de magnitud/signo). Igualdad exacta produce margen cero.

Si una validación instrumental entrega una **cota dura** de error angular `ε` para ese tramo y marco, entonces una clase está garantizada invariable sólo si `ε` es **menor** que su distancia angular a toda frontera pertinente. Si en cambio el montaje produce un cono de error del 95 %, la conclusión es probabilística bajo ese método de estimación; no escribir «garantizada». Un error de ejes corporales, reloj, oclusión o correspondencia errónea puede dominar el error 3D puntual y debe incluirse. El margen de clasificación se calcula **después** de demostrar que `u` es identificable: un desplazamiento casi nulo carece de dirección física estable aunque su vector normalizado dé un margen grande.

## De error de posición a error de dirección

Para una **dirección de desplazamiento** entre dos instantes, sea `d̂=p̂₁−p̂₀` el vector observado y supongamos, sólo como modelo geométrico, cotas euclidianas duras `||p̂₀−p₀||≤ε₀` y `||p̂₁−p₁||≤ε₁` en el **mismo marco**. Por desigualdad triangular, el vector real `d=p₁−p₀` está a distancia como máximo `δ=ε₀+ε₁` de `d̂`, incluso si los errores de ambos instantes están correlacionados. Si `L=||d̂||>δ`, el ángulo entre `d̂` y cualquier `d` compatible no supera `asin(δ/L)`; es la tangente desde el origen a la bola de error centrada en `d̂`. Si `L≤δ`, la bola toca o contiene el origen: no se certifica una dirección y se marca `undefined`, aunque un detector entregue un vector normalizado. Para un eje hombro→mano vale la misma geometría con errores de **dos puntos simultáneos**, pero no debe confundirse ese eje con desplazamiento temporal de la mano.

Ejemplo **hipotético**, sin datos de las cámaras: si cada extremo tiene cota de 5 mm, `δ=10 mm`; para `L=100 mm` la cota angular es 5,74°, para `L=20 mm` es 30°, y para `L=10 mm` la dirección queda indefinida. Una clase cuyo margen a la frontera sea 8° podría resistir el primer caso, pero no el segundo. Son cotas adversariales conservadoras: una distribución empírica de error, un intervalo del 95 % o la desviación estándar no pueden insertarse como `ε` dura ni prometer garantía. Errores de calibración, frente corporal, transformación co-rotante y sincronía requieren presupuestos propios; sumar sólo error de puntos sería insuficiente para certificar la clase final.

Si se fija de antemano una resolución angular objetivo `α` entre 0° y 90°, la condición suficiente de este modelo es `L > δ/sin(α)`. Con los mismos 10 mm hipotéticos y un objetivo de 8°, el desplazamiento observado tendría que superar 71,85 mm **en el intervalo elegido**; ampliar arbitrariamente el intervalo para conseguirlo puede atravesar otra acción, una pausa o un cambio de dirección, y altera la pregunta temporal. Por eso se congelan conjuntamente la duración/definición del tramo y la precisión requerida. Para certificar una clase, `α` se sustituye por su **margen observado a la frontera**, que cambia de tramo a tramo; no existe un único umbral de distancia universal.

Para posiciones 3D **ya validadas en sus instantes físicos**, si los extremos del tramo se asignan a tiempos con errores acotados `|Δt₀|,|Δt₁|` y sus velocidades están acotadas por `v₀,v₁`, se pueden añadir conservadoramente `v₀|Δt₀|+v₁|Δt₁|` a `δ`. Ésta es una cota de **selección temporal de extremos**, no una reparación de triangulación multivista asíncrona. Mezclar rayos de distintos instantes puede amplificar el error de profundidad según la línea base incluso con píxeles perfectos; el [contraejemplo estéreo](PRESUPUESTO_ESPACIAL_ESTEREO.md) exige medir el error 3D resultante y usarlo como parte del presupuesto de posición. No contar dos veces el mismo desfase si ese error 3D medido ya lo incluye.

## Banco ilustrativo

El [script autónomo](margen_orientacion.py) calcula estos márgenes para tres vectores **inventados**, con un cono hipotético de 3° que no representa las cámaras de Saira:

| Vector no normalizado | Frontera de octante | Frontera de eje dominante | Frontera de orden completo | ¿Clase de 24 estable si el error máximo fuera 3°? |
|---|---:|---:|---:|---|
| `(0,8; 0,5; 0,3)` | 17,64° | 12,37° | 8,21° | Sí |
| `(0,71; 0,69; 0,14)` | 8,05° | 0,81° | 0,81° | No: el eje mayor puede invertirse |
| `(0,99; 0,1; 0,01)` | 0,58° | 39,23° | 3,67° | No: el signo del eje casi nulo puede invertirse |

El tercer caso muestra por qué un eje dominante «muy claro» no basta si el octante es incierto. El primer caso pasa el ejemplo de 3°, pero eso no lo convierte en una inclinación históricamente identificada: sólo confirma estabilidad de **nuestra etiqueta** bajo un error supuesto.

## Uso en Nico y Beacon

1. Con objetos de referencia y pruebas de movimientos rápidos, estimar error angular **por segmento, región y giro** en 3D; incluir cómo se eligieron los extremos del tramo, la sincronización y el marco corporal. No usar la tasa de cuadros nominal como error angular.
2. Para cada tramo, guardar `u`, las tres componentes firmadas, el margen menor pertinente, `ε` o distribución estimada, calidad y causa de invalidez. Si el error alcanza la frontera, conservar la dirección continua con su incertidumbre; no forzar una de 24 etiquetas.
3. Comparar con anotación experta sólo entre tramos que son geométricamente observables y registrar también los excluidos. Un buen acuerdo entre algoritmo y experto para clips fáciles no valida casos ambiguos o de soga oculta.
4. Para sonificación, evitar saltos bruscos de tono debidos a una frontera artificial cuando la dirección estimada oscila por ruido. Una capa continua o un estado de incertidumbre audible son decisiones de diseño posteriores; no son resultados científicos sobre consonancia.

El banco sirve para ensayar el criterio antes de conocer las cámaras. El umbral empírico, la ventana temporal y el repertorio de Nico quedan pendientes de una captura consentida y de la prueba instrumental descrita en [presupuesto estéreo](PRESUPUESTO_ESPACIAL_ESTEREO.md).
