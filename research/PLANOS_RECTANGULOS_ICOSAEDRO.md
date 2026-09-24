# Tres planos no determinan un icosaedro regular

Nota matemática del 23-09-2026. La [introducción de McCaw a *The Laban Sourcebook* (2011, pp. 11–12)](https://api.pageplace.de/preview/DT0400.9781136979484_A24268502/preview-9781136979484_A24268502.pdf) muestra tres planos de movimiento y los relaciona con un icosaedro, reproduciendo dos figuras de *Choreographie* (1926). Esta lectura es **de McCaw**; no disponemos del capítulo original completo. Para nuestro algoritmo hace falta especificar una condición geométrica que la frase «unir las esquinas de tres planos» deja implícita: esos planos deben contener **rectángulos con una proporción concreta**, además de orientación y centro definidos. La [construcción de referencia de MathWorld](https://mathworld.wolfram.com/RegularIcosahedron.html) da las doce coordenadas de un icosaedro regular con razón áurea.

La inspección directa de las dos páginas de la vista previa precisa el alcance: la figura 0.1 reproduce un octaedro en torno al cuerpo; la figura 0.2, con el rótulo alemán `Dimensionalflächen`, representa tres superficies corporales. **No dibuja doce vértices ni acota rectángulos áureos**. La construcción de abajo formaliza por separado lo que exige un icosaedro regular; no pretende transcribir una operación visible en esa figura. [Registro de la inspección](LABAN_SOURCEBOOK_VISTA_PREVIA.md).

Definamos una familia de doce puntos, construida por nosotros, con `r>0`:

`V(r) = {(0,±1,±r), (±1,±r,0), (±r,0,±1)}`,

con los signos independientes. Cada cuarteto yace en uno de tres planos ortogonales y forma un rectángulo. Para `r≥1`, el lado menor del rectángulo tiene longitud 2. La distancia entre `A=(0,1,r)` y `B=(1,r,0)` es `sqrt(2r²−2r+2)`. Para que sea igual al lado menor, `2r²−2r+2=4`, o `r²−r−1=0`; la solución positiva es `φ=(1+sqrt(5))/2`. En `r=φ`, las aristas elegidas por distancia mínima forman 30 aristas iguales y 20 caras triangulares equiláteras: un icosaedro regular. La deducción de la proporción es geometría euclidiana, **no una fórmula atribuida a Laban**.

En `r=1`, los mismos tres planos y doce puntos producen el conjunto de vértices de un **cuboctaedro** (con arista mínima `sqrt(2)`); en un `r` intermedio, los bordes no son todos equivalentes. El [chequeo reproducible](rectangulos_icosaedro.py) informa distancias y grados de vecindad para `r=1`, `1.4` y `φ`, sin video ni datos humanos. El hecho de que los planos sean frontal, sagital y horizontal tampoco revela cuál de las doce direcciones usa Nico ni en qué orden; esas son preguntas distintas sobre una trayectoria 3D en un marco corporal declarado.

Esta φ es una **condición euclidiana de regularidad del sólido**. HIT §10.2 y apéndice E emplean φ en otro papel matemático: desplazamiento no conmensurable para consultar patrones almacenados en un toro de fases; su lema de activación es conjetural. No se deduce de la igualdad numérica que la plantilla icosaédrica active información, mejore el gesto o minimice energía. El [cotejo HIT–Laban](PUENTE_LABAN_HIT.md) mantiene separadas ambas predicciones.

## Regla para el estudio de rope flow

1. Medir por separado orientación y persistencia de los **planos empíricos** de mano/soga. El [criterio de identificabilidad](IDENTIFICABILIDAD_PLANOS.md) rechaza normales arbitrarias cuando la curva es casi recta o los datos 3D no son confiables.
2. Si se contrasta una **plantilla de icosaedro**, usar `φ` y una orientación congelada antes de evaluar sesiones reservadas. La plantilla expresa una predicción adicional de proporción y orden; no sale de observar tres planos cualesquiera.
3. Comparar contra plantilla cuboctaédrica y descriptor continuo sin sólido, con controles de cobertura basal ya descritos en [contraste de redes](REDES_CONTRASTE_GEOMETRICO.md). Informar cuándo la incertidumbre de cámaras impide distinguirlas.
4. No interpretar `φ`, un ajuste de plano o proximidad a aristas como belleza, ahorro energético, estado místico ni respaldo de HIT. Esas relaciones exigen variables independientes y la [cadena de contrastes](CADENA_CONSONANCIA_BELLEZA_ECONOMIA.md).

Falta cotejar las figuras y texto completos de *Choreographie* y *Choreutics* para decir qué construcción exacta enseñó Laban y qué modificaciones introdujo la tradición. El cálculo anterior puede sostenerse por sí mismo como referencia computacional, aunque la correspondencia histórica permanezca abierta.
