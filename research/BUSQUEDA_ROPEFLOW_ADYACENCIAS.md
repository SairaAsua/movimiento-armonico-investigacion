# Búsqueda reproducible: rope flow y prácticas vecinas

Registro de búsqueda dirigida, 23 de septiembre de 2026. Es una comprobación focalizada de **títulos/resúmenes y fuentes adyacentes**, no una revisión sistemática ni una afirmación de inexistencia de trabajos. Pregunta: ¿hay investigación primaria indexada sobre rope flow como práctica corporal con soga que pueda sustentar directamente geometría, metabolismo, estética o experiencia? La distinción de actividad viene de [la aclaración de Saira](USER_BRIEF.md): no es salto con soga.

## Consultas efectuadas y resultado

Se usaron interfaces públicas sin filtro de año o idioma, con la indexación disponible el 23-09-2026. Los conteos son dinámicos y dependen de cada base. Los enlaces codifican la consulta para repetirla.

| Base/campo | Consulta exacta | Resultado observado | Lectura de los resultados |
|---|---|---|---|
| [PubMed E-utilities](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=%22rope%20flow%22%5BTitle%2FAbstract%5D&retmode=json) | `"rope flow"[Title/Abstract]` | 0 | No hay entrada con esa frase en esos campos de PubMed en la consulta. |
| [PubMed E-utilities](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=ropeflow%5BTitle%2FAbstract%5D&retmode=json) | `ropeflow[Title/Abstract]` | 0 | La grafía junta tampoco recuperó entradas. |
| [PubMed E-utilities](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=%22poi%20spinning%22%5BTitle%2FAbstract%5D&retmode=json) | `"poi spinning"[Title/Abstract]` | 1 | Recuperó el ensayo de Riegle van West et al.; actividad vecina, no la misma tarea. |
| [Europe PMC REST](https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=TITLE%3A%22rope%20flow%22&format=json&pageSize=5) | `TITLE:"rope flow"` | 0 | Cero títulos con esa frase según su índice. |
| [Europe PMC REST](https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=TITLE%3Aropeflow&format=json&pageSize=5) | `TITLE:ropeflow` | 0 | Cero títulos con la grafía junta. |
| [Europe PMC REST](https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=ABSTRACT%3A%22rope%20flow%22&format=json&pageSize=5) | `ABSTRACT:"rope flow"` | 1 | *Jump rope vortex in liquid metal convection*: «rope flow» describe un fluido, no práctica corporal. |
| [OpenAlex Works](https://api.openalex.org/works?filter=title.search%3Arope%20flow&per-page=200) | `filter=title.search:rope flow` | 105 coincidencias de búsqueda; se inspeccionaron los 105 títulos | Sólo 3 contenían la frase contigua «rope flow» y eran de control de producción/fibra de carbono; ninguna correspondía a la actividad física. La búsqueda de OpenAlex es amplia, no un match exacto. |
| [OpenAlex Works](https://api.openalex.org/works?filter=title.search%3Aropeflow&per-page=5) | `filter=title.search:ropeflow` | 0 | No prueba ausencia fuera de OpenAlex. |

Una búsqueda web dirigida por `"rope flow" biomechanics motion capture research`, `"ropeflow" biomechanics study` y `"rope flow" "oxygen consumption" OR "energy expenditure"` produjo clases de falsos positivos: flujo de material, vórtices en turbinas/líquidos, *battle ropes* de entrenamiento y **jump rope**. Materiales de practicantes describen la actividad y vocabulario, pero no miden las cuatro variables del proyecto. Faltan bases específicas de danza/deporte y variantes de nombre como *rope rolling* o programas de marca; el resultado correcto es **no identificado en esta búsqueda**, no «no existe».

**Actualización dirigida, 24-09-2026.** Se repitió una búsqueda web abierta con las consultas exactas `"rope flow" biomechanics motion capture study`, `"ropeflow" movement kinematics metabolic energy` y `"rope flow" Laban movement analysis study`. Entre los resultados inspeccionados aparecieron páginas de formación/comercio sobre la práctica y estudios sobre *rope flow* de fluidos; no se identificó allí un estudio primario instrumentado de rope flow corporal que mida conjuntamente cinemática, economía y experiencia. Esta comprobación no cubre literatura no indexada, bases especializadas ni nombres alternativos de la práctica, y no modifica el resultado limitado de PubMed/Europe PMC/OpenAlex de arriba.

**Ampliación instrumental, 24-09-2026.** Las consultas `"Motion Capture of Character Interactions with a Rope" Porter thesis method motion capture rope BYU`, `human rope swinging motion capture flexible rope study markers biomechanics` y `"Biomechanical Analysis of Cycle-Tempo Effects on Motor Control Among Jump Rope Elites" 6 markers 13 cameras` recuperaron dos antecedentes donde se captura **persona y objeto**: la [tesis de Porter (2012)](https://scholarsarchive.byu.edu/etd/3374/) sobre interacción con cuerda flexible y el [estudio de Zhou y colaboradores (2025)](https://doi.org/10.3390/bioengineering12020162) sobre salto con soga. El primero se examinó sólo a nivel de ficha/resumen; el segundo se leyó inicialmente por resumen y fragmento indexado y luego [a texto completo](SALTO_SOGA_ZHOU_2025_TRANSFERENCIA.md); [alcance de seguimiento flexible](SOGA_VISION_DLO_FUENTES.md). Ninguno resuelve con evidencia directa la medición de rope flow corporal de Nico.

**Ampliación de interacción rítmica, 03-10-2026.** La búsqueda `"Motion Capture of Character Interactions with a Rope" pdf` mostró un [experimento original de Yonekura et al. (2012)](CUERDA_RITMO_MULTIMODAL_YONEKURA_2012.md) con dos personas girando una soga compartida y señales visuales, auditivas y de fuerza. Se leyó el artículo completo. Mide ajuste de frecuencia y respuestas a cambios de pulso, no la fase intracíclo, estética o gasto de rope flow; aporta diseño de entradas y controles multimodales.

## Dos antecedentes vecinos que sí aportan método

**Poi como intervención física.** [Riegle van West, Stinear y Buck (2018)](https://pubmed.ncbi.nlm.nih.gov/29543125/) asignaron aleatoriamente 79 adultos de 60–86 años a poi o tai chi, dos clases semanales durante cuatro semanas, y evaluaron función física/cognitiva en varios momentos. El resumen informa mejoras dentro de ambos grupos en ciertos resultados. Sirve para demostrar que una práctica de objeto giratorio puede definirse como intervención y medirse con resultados funcionales. No informa costo metabólico por ciclo, estética, fase corporal ni estados místicos, y poi usa pesos al extremo de cordones: no es la soga continua de Nico. Texto completo no examinado en esta búsqueda.

**Ampliación posterior:** se obtuvo y leyó el [texto completo](https://anzca.co.nz/wp-content/uploads/2024/05/Effects-of-Poi-on-Physical-and-Cognitive-Function-in-Healthy-Older-Adults-Riegle-van-West-et-al-2019.pdf). Informa ausencia de efecto principal de grupo y limitaciones por falta de grupo inactivo/práctica; por tanto su valor aquí es sobre diseño de intervención, no superioridad de poi. También se examinaron una notación comunitaria de tiempo/dirección y un prototipo audiovisual de poi; [síntesis y límites](POI_ADYACENCIA_Y_TRANSFERENCIA.md).

**Grafo de estados para giro de objetos.** [Varpanen (2014), *Toss and Spin Juggling State Graphs*](https://archive.bridgesmathart.org/2014/bridges2014-301.pdf) construye un grafo de estados de poi y transiciones de manos, incluyendo cruces. Se examinó el artículo completo de ocho páginas. Su modelo **deliberadamente ignora** pesos, cuerpo (salvo línea de hombros) y parte de la dinámica de las cuerdas; por ello es una abstracción combinatoria, no un modelo biomecánico validado ni una receta literal para rope flow. Su aporte transferible es conceptual: representar un patrón por estados, orden de cambios y transiciones admisibles, no sólo por un cuadro o una frecuencia media.

Como antecedente matemático secundario, [Farrington (2015), *Parametric Equations at the Circus*](https://doi.org/10.4169/college.math.j.46.3.173) estudia trayectorias trocoides de ciertos movimientos de poi; se leyó el resumen editorial, no el texto íntegro. Es una posible comparación de curvas geométricas, sin evidencia de que una figura concreta de Nico siga esa curva.

## Consecuencia para el modelo Laban–HIT

El caso Nico puede describirse en **tres niveles que no se sustituyen**:

1. Trayectorias continuas de cuerpo y, si la soga es visible, de la soga: marco corporal, desplazamiento, planos y recorridos desde la [matriz Laban](LABAN_MATRIZ.md).
2. Estados discretos de la tarea: por ejemplo, lado y sentido de paso de la soga, mano que conduce, cruce y transición; vocabulario a definir observando a Nico. La idea de grafo procede por analogía de Varpanen, pero las reglas se construyen para rope flow y se validan con video.
3. Organización temporal dentro de cada estado/transición: eventos, fase y relación p:q de [la especificación](FASE_ROPEFLOW.md), con comparaciones HIT adicionales frente a modelos simples.

El grafo de estados ayuda a comparar **la misma tarea** y a localizar transiciones no periódicas donde una fase continua sería inválida. La forma de la curva, el orden del patrón y su cadencia pueden variar independientemente. Si se ajusta un grafo distinto para cada clip, vuelve a perderse la prueba: definir vocabulario y transiciones durante factibilidad y reservar sesiones para contraste.

## Siguiente ampliación de búsqueda

Para una revisión de alcance publicable, conservar esta búsqueda como piloto, ampliar a bases de danza y ciencias del deporte, probar variantes (*rope rolling*, *rotational movement training*, *poi*, *flow arts*, manipulación de cuerda), usar criterios de inclusión/exclusión antes del cribado y doble revisión humana donde corresponda. La proximidad mecánica debe codificarse: soga continua frente a dos pesos; paso alrededor del cuerpo frente a salto; carga, agarre y número de manos. Ningún antecedente adyacente valida por sí solo la hipótesis de consonancia corporal.
