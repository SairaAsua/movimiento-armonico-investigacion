# Control nulo circular para las redes espaciales

Nota computacional del 23 de septiembre de 2026. Complementa el [contraste geométrico justo](REDES_CONTRASTE_GEOMETRICO.md) y su [sanity check](redes_sanity.py). La pregunta concreta es si una menor distancia a vértices de un icosaedro o cuboctaedro puede aparecer **sin** que el gesto siga una escala de Laban. Este banco no usa personas, video ni trayectorias de rope flow; tampoco reconstruye una escala histórica.

## Construcción

El [script reproducible](redes_circulos_nulos.py) genera 201 círculos ideales, cada uno con 24 posiciones unitarias en un plano de orientación aleatoria. Son patrones deliberadamente genéricos. Calcula, para cada posición, el ángulo al vértice más próximo de una plantilla de doce vértices normalizados y promedia esos ángulos por círculo. **Sólo puntúa posiciones radiales**: no evalúa orientación de línea, situación del recorrido ni secuencia de aristas. Este límite es parte de la prueba; si el puntaje se publicara como «fidelidad a Laban», ya sería un cambio injustificado de constructo.

Se prueban 72 giros de la plantilla alrededor del eje vertical, separados 5°. Un giro por red se elige usando exclusivamente el primer círculo de **desarrollo**; luego se congela y se puntúan los 200 restantes. Para mostrar el optimismo de ajuste, se compara esa evaluación con permitir que cada círculo de prueba elija su propio giro mínimo. Ambas redes tienen la misma libertad de giro, pero distinta cobertura esférica intrínseca.

## Resultado del banco, semilla 1701

| Red | Giro elegido en desarrollo | Error medio en 200 círculos, orientación fija | Error medio con giro libre por círculo | Reducción mediana por giro libre | Máxima reducción observada |
|---|---:|---:|---:|---:|---:|
| Cuboctaedro | 350° | 22,69° | 19,65° | 1,98° | 11,50° |
| Icosaedro | 5° | 22,18° | 19,57° | 1,82° | 8,77° |

Con la orientación congelada, el icosaedro dio menor error en **116 de los 200 círculos nulos**; no hubo empates. Esa frecuencia no es un resultado sobre movimiento humano ni una prueba estadística de superioridad de red. Sí demuestra que una ventaja icosaédrica puede aparecer en una colección de círculos genéricos sin contenido Laban, como ya sugería la diferencia de cobertura de la esfera en el [sanity check](REDES_CONTRASTE_GEOMETRICO.md). Ajustar el giro directamente sobre el clip evaluado crea un segundo sesgo: por construcción, el error sólo puede disminuir. Aquí esa disminución alcanzó 11,50° en un círculo cuboctaédrico y 8,77° en uno icosaédrico.

El script comprueba que las posiciones generadas tienen norma uno y que el error tras búsqueda libre nunca excede al error con orientación fija. Las cifras son deterministas bajo este código/semilla; no son intervalos para cámaras reales.

## Consecuencia para el piloto de Nico

1. Declarar **qué** se compara: posición radial, dirección de desplazamiento o secuencia de líneas. Si se pretende probar una escala, el puntaje de vértices del banco no alcanza.
2. Justificar la orientación con una fuente coreútica verificada o estimarla **solo** en sesiones de desarrollo. Reservar días completos sin reajustar un giro por clip, mano o figura. Reportar orientación y todos los grados de libertad.
3. Contrastar la red con un modelo de trayectoria continua sin poliedro y con controles que conserven la forma genérica, plano, amplitud y cadencia del patrón. Los círculos isotrópicos aquí sirven para revelar un fallo posible; **no** son el nulo anatómico definitivo de Nico.
4. Para cada patrón real, estimar la distribución nula después de medir sus restricciones biomecánicas y de tarea. Conservar recorridos completos y orden cuando la pregunta sea una escala; permutar solo la propiedad cuya contribución se quiere aislar. Una permutación que rompe la física de la soga no es control válido.
5. Propagar error de cámara y anotación. Si la diferencia entre redes es comparable al error angular del [montaje estéreo](PRESUPUESTO_ESPACIAL_ESTEREO.md), declarar que ese montaje no distingue las redes para ese patrón. El resultado externo —belleza, experiencia o costo— sigue siendo otra pregunta, a medir independientemente.

Este control modifica la regla de interpretación: **un error geométrico pequeño o una victoria entre dos poliedros no es evidencia suficiente de organización coreútica específica**. La referencia deberá incluir geometría propia de la tarea, complejidad comparable y evaluación en sesiones reservadas. No se eligió aquí una red «correcta» para rope flow.
