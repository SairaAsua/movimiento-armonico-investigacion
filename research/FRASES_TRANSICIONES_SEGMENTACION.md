# Ciclos, transiciones y frases: tres cortes diferentes del rope flow

Nota de diseño del 23 de septiembre de 2026. No hay video de Nico ni segmentación ejecutada. El problema es que una **transición** entre figuras puede ser el momento de mayor interés espacial, estético o vivido, pero la fase p:q presupone señales cíclicas definidas. Excluirla de un cálculo periódico es correcto; excluirla del estudio de la frase completa destruiría parte de la hipótesis.

## Antecedentes empíricos y alcance

En una [prueba de segmentación de una frase de danza](https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2014.01500/full), Bläsing (2015) encontró menos límites marcados por bailarines que por observadores sin formación específica; la música modificó el número de límites en direcciones distintas según grupo. La repetición y aprender la frase también afectaron el grano de segmentación. Es una tarea de observación de danza, **no** una regla universal para Nico ni evidencia de que más o menos cortes sean mejores.

En otro [experimento de agrupación perceptual de movimientos simples](https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2019.01364/full), Charnavel (2019) propuso y probó cambios de parte activa, orientación, apoyo/nivel, dirección, rapidez y cualidad como pistas de límite. El análisis final incluyó 30 observadores no profesionales y 15 estímulos de brazo controlados. Su orden de fuerza perceptual es específico a esa tarea; no se importará como una jerarquía fija de rope flow. Ambos estudios justifican **medir el acuerdo y conservar los desacuerdos** sobre límites, además de registrar experiencia del observador y condición sonora.

## Tres capas de anotación con distinta pregunta

| Capa | Qué marca | Referencia y estado | Uso permitido |
|---|---|---|---|
| Ciclo de tarea | Regreso a configuración y sentido de soga predefinidos dentro de un patrón | Evento visible con tiempo e incertidumbre; inválido ante oclusión/reversa/pausa | Cadencia, periodo y fase sólo entre eventos comparables |
| Patrón y transición | Tramo que Nico reconoce como una figura, cambio entre figuras, improvisación, pausa o reversa | Video completo, nombre local y criterio observable; inicio/fin pueden ser intervalo incierto | Duración, orden, camino espacial y recuperación; no imponer fase única al cambio |
| Frase percibida | Dónde un observador siente comienzo, cierre o nuevo grupo | Anotadores independientes, rol/experiencia, con o sin audio según protocolo; distribución de marcas | Comparar segmentaciones y juicios estéticos sin declarar una frontera perceptual universal |

Una frase puede contener varios ciclos de A, una transición y ciclos de B. Los límites percibidos pueden caer dentro de un patrón repetido o después de él. Ninguna capa debe sobrescribir las otras. Los autoinformes de Nico sobre un **bloque** se mantienen en esa escala: la segmentación posterior de video no fecha con precisión su experiencia interna. Si él identifica espontáneamente un momento, se registra como recuerdo situado, distinto de una marca fisiológica continua.

## Estado de análisis y reglas de frontera propuestas

Para cada intervalo guardar `state ∈ {stable_pattern, transition, pause, reversal, improvisation, unknown}` y la razón observacional. `unknown` significa insuficiencia de evidencia; no «movimiento caótico». `stable_pattern` requiere evento de ciclo aplicable, aunque algún evento individual pueda estar oculto. Una transición comienza cuando deja de cumplirse la configuración/sentido de la figura anterior y termina cuando se establece la siguiente; si eso ocurre gradualmente, guardar un **intervalo de incertidumbre** en vez de inventar un fotograma exacto. La descripción de Nico y la guía de dos anotadores se fijarán tras ver repertorio, antes de ratings confirmatorios.

El cálculo p:q se restringe a tramos donde **ambas** señales y sus ciclos son identificables. En `transition`, `pause`, `reversal` o `unknown`, el campo de fase queda `not_applicable` o `invalid` con causa, no `R=0`. Las transiciones conservan medidas no periódicas: orden de direcciones/planos, giro, duración, distancia/curvatura con error, entrada/salida respecto del patrón y valoración del clip que las incluye. Estas variables no se suman en una nota de «armonía» por conveniencia.

En desarrollo puede probarse un detector de cambio con pistas separadas —parte activa, dirección, plano, rapidez y pausa—, comparándolo con anotaciones de video sin mirar belleza. Su puntaje será de **detección de límites** con tolerancia temporal y cobertura, no de eficiencia ni de consonancia. El entrenamiento y la elección de tolerancia quedan fuera de los días reservados. Reportar desacuerdo entre expertos y legos, y si el audio altera sus límites; una fusión por voto mayoritario no borra las marcas originales.

## Por qué contar estados no basta: control sintético

Las secuencias `ABCABC` y `ABCBAC` contienen exactamente dos apariciones de cada estado `A`, `B`, `C`, y ninguna repetición inmediata. Sin embargo, al comparar el estado de un tramo con el de tres tramos después, la primera tiene `3/3` coincidencias y la segunda `1/3`. Lo comprueba el [script mínimo](frases_orden_sintetico.py). Un histograma de ocupación y el recuento de cambios adyacentes no recuperan la **organización de la frase**. Este ejemplo no dice que recurrencia a distancia tres sea bella, eficiente o una escala de Laban; sólo impone conservar el orden y probar el descriptor contra una respuesta externa.

En el estudio de Nico, la transición no será declarada disonante por estar fuera de una fase estable. Una predicción posible —a elegir sólo si el repertorio la hace contrastable— es que ciertas frases con salida y retorno espacial se juzguen distintas de frases con ocupación semejante pero otro orden, controlando patrón, duración, ritmo y complejidad. Una hipótesis rival sostiene que regularidad continua predice mejor. Ambas pueden fallar. Véanse [contraste estructurado](CONTRASTE_ESTRUCTURADO.md), [fase](FASE_ROPEFLOW.md), [experiencia/estética](EXPERIENCIA_ESTETICA.md) y [estimandos](ESTIMANDOS_Y_CONTRASTES.md).
