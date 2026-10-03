# Qué identifica una cámara cuando la soga se curva y cruza

Nota matemática de diseño, 23-09-2026. La actividad es **rope flow**, no salto. Esta nota distingue trayectoria del cuerpo, curva de la soga y paso de la soga respecto del cuerpo. El contraejemplo es propio y sintético; no hay grabaciones de Nico.

## Tres objetos observacionales

- **Puntos corporales:** muñecas, manos, torso y apoyos, con su visibilidad, marco y error. La muñeca puede seguir girando aunque la soga cambie de plano, se afloje o se oculte.
- **Curva visible de soga:** centrolinea de la soga en cada imagen, expresada como conjunto de píxeles o como curva 2D con incertidumbre. Si la soga uniforme se cruza o se oculta, el orden de sus tramos y la correspondencia temporal pueden ser ambiguos.
- **Evento de tarea:** un paso con lado, sentido y relación corporal definidos. Exige verificar la soga, no sólo periodicidad de muñecas. Puede ser `no_observable` aunque la mano sea nítida.

Una geometría 3D idealizada de la soga sería `r(s,t)∈R³`, con `s` como distancia material desde un extremo identificado; la cámara observa una proyección `P(r)` y sólo parte de la curva por oclusión. Para un primer piloto, declarar el objeto **efectivamente visible**: `rope_projected_curve`, `hand_trajectory` y `task_event` se guardan en campos distintos. La reconstrucción `rope_3d_curve` necesita calibración, correspondencia entre vistas y un presupuesto de error propio, adicional al de pose corporal.

## La figura no identifica por sí sola el punto material

Aunque se recuperase la **curva 3D completa como conjunto de puntos** `C(t)`, falta demostrar qué punto de `C(t)` es el mismo trozo de soga en otro instante. Contraejemplo matemático propio, deliberadamente más simple que el rope flow: para una cuerda cerrada homogénea y sin marcas, `r_ω(s,t)=(cos(s+ωt),sin(s+ωt),0)`, con `s∈[0,2π)`. Para cualquier `ω`, la figura observada es siempre la misma circunferencia unitaria; un punto material, en cambio, tiene rapidez `|ω|`. Con masa lineal constante `μ`, su energía cinética sería `K=πμω²`. La misma película de la **figura sin marcas** admite así `ω=0` y `ω≠0`: no identifica ni fase material ni energía cinética. No afirmamos que Nico use una cuerda cerrada; el ejemplo aísla la diferencia lógica entre figura y identidad material.

Una soga **abierta**, inextensible, con extremo material identificado y **toda** su curva 3D visible podría permitir indexar el material por longitud de arco desde ese extremo; es un supuesto adicional, no una imposibilidad universal de video sin marcas. Elasticidad, deslizamiento en el agarre, falta de un extremo visible, cruces y oclusiones pueden romper esa identificación práctica. Un tracker que reparte nodos uniformemente sobre la curva entrega coordenadas de modelo; para llamarlas trayectorias materiales hay que verificar la correspondencia temporal con una referencia independiente. [Li y colaboradores, DOT](https://fluorescentdot.github.io/) construyeron esa referencia con marcas fluorescentes bajo UV y publicaron correspondencias 2D/3D de objetos deformables, incluida soga; su montaje no valida todavía nuestras cámaras ni la velocidad de rope flow.

## Contraejemplo: misma imagen y mismo largo, diferente profundidad

Con cámara ortográfica ideal `P(x,y,z)=(x,y)`, consideremos dos curvas entre los mismos extremos para `s∈[0,1]`:

`r₊(s)=(s, 0, a sin(2πs))` y `r₋(s)=(s, 0, −a sin(2πs))`, con `a>0`.

Ambas proyectan **exactamente** la recta `(s,0)`; ambas empiezan y terminan a profundidad cero. Sus largos son iguales, porque la rapidez de cada curva es `sqrt(1+(2πa cos(2πs))²)`. Sin embargo, en cada mitad de la cuerda ocupan lados opuestos del plano de imagen. Por tanto, ni imagen monocular perfecta ni conocimiento del largo deciden si un tramo pasa delante o detrás. Una cámara de perspectiva y una soga real requieren un contraejemplo específico para su calibración, pero la proyección 3D→2D mantiene ambigüedades salvo restricciones adicionales verificadas. El [contraejemplo general de pose](IDENTIFICABILIDAD_2D_3D.md) aborda la misma pérdida para puntos corporales.

El ejemplo tampoco dice que la soga de Nico adopte una sinusoide. Sólo prueba que una variable de profundidad **no es consecuencia lógica** de la silueta 2D. En cruces reales se suman oclusión, textura, desenfoque y movimiento rápido; no tratarlos como ruido que un modelo de pose resuelve por decreto.

## Decisión por nivel de captura

| Montaje y evidencia | Variable admisible | Variable que queda pendiente |
|---|---|---|
| Una cámara calibrada en imagen, soga visible | Curva proyectada, ángulo y forma **2D**, tiempo de eventos que se distinguen visualmente | Profundidad, plano 3D, orden frente/detrás no visible, energía mecánica |
| Varias vistas sincronizadas y calibradas, correspondencias y referencias dinámicas comprobadas | Curva y cruces **3D** con cobertura/error por patrón y región | Tramos ocultos a todas las vistas; materialidad de la soga sin marcadores/textura suficiente |
| Muñecas visibles pero soga oculta | Cinemática de manos; posible proxy de cadencia etiquetado como tal | Fase o evento de soga confirmado, tensión y recorrido de soga |

Un color o marcas discretas podrían facilitar correspondencia entre tramos, pero añadir masa, rigidez o fricción cambia la tarea. Antes de adoptarlas, comparar dimensiones, peso y ejecución con y sin marcas y documentar la modificación; no llamar idénticas las condiciones por conveniencia técnica. Si se usa una soga con textura propia visible, intentar primero esa opción sin alterar el implemento. La selección final depende del inventario de cámaras y el consentimiento.

## Efecto sobre Laban, HIT y Beacon

Las direcciones Laban calculadas sobre mano, torso y soga **no son intercambiables**: pueden coincidir en algunas frases y divergir en otras. Registrar el origen de cada vector y conservar las divergencias como dato, sin asignar una única «dirección armónica del cuerpo». Las relaciones de fase HIT pueden comparar mano/soga sólo en ciclos identificables de ambas señales; un proxy de muñeca no verifica fase de soga. Beacon debe recibir un estado explícito de visibilidad/validez, para evitar que una curva inventada durante una oclusión suene como observación. Este es un requisito de diseño futuro, no una capacidad constatada del pipeline actual de HarMoCAP.

Hay además una pérdida **por resumir el recorrido**, incluso si la trayectoria de una muñeca se observase sin error: dos rutas pueden tener [el mismo `Q`, los mismos cuatro desplazamientos y largo, pero diferente autocruce en el tiempo](Q_CRUCES_ORDEN.md). Ese ejemplo es de un punto móvil 2D, no del cruce simultáneo de dos tramos de soga. Refuerza que `Q` no sustituye ni secuencia temporal de líneas ni topología/orden frente–detrás de la soga.

**Prueba de factibilidad pendiente:** registrar con un objeto inerte conocido en el volumen previsto, luego observar el repertorio real de Nico y anotar por patrón qué tramos de soga son visibles en cada vista, dónde se cruzan y si el evento de tarea puede fecharse independientemente de la muñeca. Sin esas pruebas, la variable 3D de la soga queda fuera del análisis confirmatorio.

La [lectura de métodos DLO](SOGA_VISION_DLO_FUENTES.md) especifica cómo medir cobertura, error y recuperación tras oclusión, y por qué una curva imputada por un tracker no se convierte en medición observada. La cifra submilimétrica citada para DLO3DS proviene de **formas sintéticas estáticas** con cámara robótica y parámetros optimizados; no es una tolerancia válida para la soga en movimiento de Nico.
