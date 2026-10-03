# Longstaff (1996): dos ochos visibles, distintas acciones

Lectura documental del volumen II, apéndice XVI, pp. impresas 159–172, de [*Cognitive Structures of Kinesthetic Space*](https://openaccess.city.ac.uk/id/eprint/11876/2/Cognitive%20Structures%20of%20Kinesthetic%20Space%20-%20vol2.pdf). Este apéndice desarrolla una **taxonomía exploratoria de Longstaff**, informada por coreútica, anatomía y control motor. No es una transcripción de una escala de *Choreographie* o *Choreutics*, ni una teoría comprobada sobre rope flow. Se consultó el PDF completo del volumen II; las páginas indicadas son las impresas en el documento.

## Qué distingue la propuesta

Longstaff parte de trayectorias de un punto de un **miembro corporal** y cruza cuatro atributos: arco fundamental, articulación única o múltiple, acción de una o varias fases, y transición abrupta o gradual entre fases (pp. 159–163, 172). Una *fase de acción* designa allí un tramo de acortamiento de un grupo muscular que produce un trazo espacial (pp. 160–162). No es el ángulo de fase de una oscilación estimado desde video para HIT, ni necesariamente una vuelta de la soga. La taxonomía excluye deliberadamente locomoción del cuerpo completo y acciones excéntricas o estáticas (pp. 159–160). Por tanto no describe sin extensión el sistema cuerpo+soga, ni permite inferir activación muscular a partir de pose.

En su clasificación, un ciclo vuelve a su punto inicial; transiciones solapadas pueden producir una curva redondeada y las discretas, una forma angular (p. 167). El propio autor presenta el esquema como preliminar y pendiente de refinamiento anatómico (p. 172). Una trayectoria y sus causas articulares son observaciones diferentes: Longstaff señala que incluso la circunducción de un hombro puede incluir una rotación menos evidente en la traza distal (p. 168).

## Dos hipótesis de producción para una figura en ocho

| Clase propuesta por Longstaff | Criterio cinestésico/articular en el apéndice | Consecuencia para observar rope flow |
|---|---|---|
| **Ciclo con reversión** (*reversing-cycle figure-8*, pp. 170–171, tablas M–O) | Los dos lóbulos ciclan en sentidos opuestos; puede haber reversión de rotación articular. El apéndice da ejemplos de cadera, combinación hombro–codo–antebrazo y muñeca–antebrazo. | Segmentar los lóbulos y registrar su **sentido firmado** en un plano/marco declarado; comprobar articulaciones en otra capa. No llamar reversión articular a un cambio de sentido aparente en una sola cámara. |
| **Ciclo continuo** (*continual-cycle figure-8*, pp. 171–172, tablas P–Q) | La articulación puede mantener un sentido de ciclo mientras otra acción desplaza el eje o centro; el ejemplo conecta el extremo de una hélice con su inicio. | Una proyección con dos lóbulos puede ocultar un ciclo articular continuo y desplazamiento del centro. Conservar trayectoria 3D, orientación corporal y articulaciones si son identificables; de otro modo la clase queda `undetermined`. |

La diferencia tiene dos niveles que **no se identifican entre sí**: geometría observada de la mano y coordinación que la produjo. La misma silueta proyectada no prueba que Nico haya ejecutado alguno de los mecanismos de las tablas. La soga flexible agrega una tercera trayectoria: mano, curva de soga e identidad de un punto material de la soga tampoco son intercambiables ([límite de identificabilidad](SOGA_IDENTIFICABILIDAD.md)).

## Operacionalización candidata, todavía sin datos de Nico

1. Definir el punto seguido (`hand`, `rope_curve` o `rope_material_point`), marco (`camera`, `body` o `world`), plano de proyección y calidad temporal. Guardar ambas manos por separado.
2. Anotar los dos lóbulos de cada ocho y sus orientaciones firmadas, incluyendo cruces, oclusiones y cambios de plano. Si una proyección 2D no determina el sentido espacial, emitir `undetermined_3d`, no una etiqueta de Longstaff.
3. Para contrastar el **mecanismo**, añadir orientación de hombro, codo, antebrazo y tronco con incertidumbre; comprobar si el sentido articular cambia o continúa. HarMoCAP 2D y los videos no calibrados no bastan para esa inferencia.
4. Mantener tres relojes conceptuales: fases de acción de la taxonomía, lóbulos/ciclos de la figura y fase periódica entre señales independientes para HIT. Un mismo nombre de variable `phase` no debe ocultar estas definiciones.
5. Comparar, cuando existan clips consentidos y evaluación reservada, la fiabilidad entre anotadores y la cobertura de cada clase; conservar `undetermined`. Una etiqueta geométrica estable no prueba fluidez, belleza, economía metabólica, placer ni conciencia.

**Decisión:** usar esta taxonomía como **hipótesis de anotación y contraste** para figuras en ocho, no como verdad de terreno ni “matemática de Laban”. Antes de integrarla al piloto debe revisarse con una persona experta en Laban/rope flow y cotejarse con las obras originales de Laban. Los [tres niveles de segmentación](FRASES_TRANSICIONES_SEGMENTACION.md) permanecen separados: el cambio entre figuras puede ser una transición sin fase HIT aunque incluya una curva reconocible.
