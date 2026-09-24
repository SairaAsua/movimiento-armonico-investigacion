# Qué identifica una cámara y qué exige reconstrucción 3D

Nota instrumental del 23 de septiembre de 2026, sin capturas humanas. Acompaña la [preparación de cámaras](CAMARAS_PREPARACION.md) y el [diccionario de señales](DICCIONARIO_SENALES_V0.md). Es un límite geométrico antes de cualquier error de detector: **una proyección 2D no determina por sí sola la profundidad de una trayectoria 3D**.

## Contraejemplo reproducible

En cámara pinhole ideal, un punto `(X,Y,Z)` produce imagen normalizada `(u,v)=(X/Z,Y/Z)`. Para cualquier curva visible `(u(t),v(t))`, cada función de profundidad positiva `Z(t)` genera una curva física `(u(t)Z(t),v(t)Z(t),Z(t))` con la **misma imagen**. La calibración de una sola cámara fija rayos en el espacio; no elige dónde está el punto sobre cada rayo sin información adicional.

El [script de demostración](proyeccion_2d_ambigua.py), sólo con biblioteca estándar, usa una circunferencia de imagen y dos profundidades: `Z_A(t)=2` y `Z_B(t)=2+0,6 sin(2t)`. La diferencia máxima de proyección calculada es `0`; la longitud de recorrido 3D es `2,513266` frente a `5,690778` unidades y la profundidad del segundo caso va de `1,4` a `2,6`. Esos números dependen de esta construcción sintética, no describen a Nico ni cuantifican error de cámaras reales.

Así, una sola vista puede registrar posición y trayectoria **en la imagen**, tiempos de eventos visibles y ratings visuales de ese clip. Sin una restricción 3D validada, no puede decidir si la mano atravesó un plano corporal, qué longitud recorrió en espacio o a qué dirección icosaédrica 3D se acercó. Una red neuronal monocular puede **estimar** profundidad usando un prior aprendido; la estimación debe contrastarse con referencia externa en rope flow y conservar incertidumbre. No se vuelve identificable por cambiarle el nombre al output.

## Decisión por descriptor del primer piloto

| Descriptor | Una vista fija | Dos o más vistas calibradas/sincronizadas |
|---|---|---|
| Eventos de ciclo cuando soga/sentido son visibles | Sí, con acuerdo de anotación y oclusiones informadas | Puede mejorar cobertura; sincronizar eventos comunes |
| Dirección y recorrido de mano | Sólo coordenadas/ángulos **proyectados**, dependientes de vista | 3D candidato con correspondencias anatómicas y error validado |
| Alcance respecto de tronco | Alcance aparente 2D, afectado por perspectiva | Distancia 3D candidata con origen/escala corporal comprobados |
| Planos corporal frontal/sagital/transversal | Sólo si una tarea y plano se restringen físicamente y se verifica esa restricción | Se pueden estimar tras reconstrucción y validación de ejes del tronco |
| Línea y situación central/periférica/transversal | Descripción visual abierta; ninguna etiqueta geométrica 3D automática | Categorías candidatas tras trayectoria completa y acuerdo de especialistas |
| Comparación de icosaedro/cuboctaedro | Sólo como geometría **proyectada de esa cámara**, sin reclamar escala espacial 3D | Contraste 3D posible con orientación, red, orden y error predefinidos |
| Fase relativa | Posible para señales cuyos eventos se ven y se identifican | Mejor cobertura potencial; requiere reloj común y error temporal |

La [documentación oficial de triangulación de OpenCV](https://docs.opencv.org/4.12.0/d9/d0c/group__calib3d.html) describe reconstrucción desde observaciones correspondientes y matrices de proyección de dos cámaras. En nuestro diseño, dos vistas sólo ayudan si comparten tiempo, calibración y **el mismo punto** visible; cruces de manos/soga, desenfoque, baja separación angular, deriva y oclusiones pueden impedirlo. Un error bajo de reproyección en píxeles no basta para afirmar profundidad exacta: hay que comprobar distancias y posiciones conocidas fuera de los puntos usados para ajustar calibración ([piloto](PILOTO_VALIDACION_VIDEO.md)).

El [presupuesto espacial estéreo](PRESUPUESTO_ESPACIAL_ESTEREO.md) cuantifica con un escenario sintético cómo línea base, focal, distancia y error de localización afectan la profundidad y dirección de un tramo; no representa las cámaras reales disponibles.

## Regla concreta para seleccionar el alcance del paper

Primero se inventarían cámaras y se ensaya con objetos en el volumen real. Se mide cobertura y error físico por profundidad, lateralidad y velocidad. Si sólo se dispone de una vista útil, el paper inicial nombra sus variables `*_proj` y evita conclusiones 3D de planos, redes o eficiencia de recorrido. Si el montaje multivista supera los márgenes derivados de la diferencia que se desea estudiar, se habilitan variables 3D **por descriptor y por patrón**, no todo el análisis a la vez. En ambos casos, lo que ve un analista Laban y lo que calcula la geometría siguen siendo niveles distintos ([anotación](ANOTACION_LABAN_PILOTO.md)).

La limitación geométrica no impide estudiar estética percibida desde clips, autoinforme de bloque o ciclo visible. Sólo obliga a formular exactamente **qué** se midió. Ni la proyección ni la reconstrucción estiman directamente gasto metabólico, placer o conciencia.
