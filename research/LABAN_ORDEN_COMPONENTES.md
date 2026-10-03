# Orden de componentes: una comprobación de los 24 nombres de inclinación

Lectura dirigida del [artículo original de Longstaff (2018), tabla 2 y explicación en p. impresa 8](https://janeway.uncpress.org/jmal/article/944/galley/1569/download/), realizada el 23-09-2026. El artículo reproduce y reorganiza la lista que atribuye a *Choreographie* (1926, p. 13); **al iniciar esta nota no se había cotejado el libro directamente**. Longstaff dice expresamente que los tres términos de cada nombre indican componente principal, secundaria y terciaria. Las fórmulas y la decisión de codificación de abajo son nuestras.

**Actualización de fuente, 03-10-2026:** se inspeccionaron imágenes de la traducción inglesa de [p. 13, lista de 24 nombres](http://www.laban-analyses.org/jeffrey/2011-Rudolf-Laban-1926-Choreographie/chapter-04/04-02.jpg) y [p. 15, abreviaturas tripartitas](http://www.laban-analyses.org/jeffrey/2011-Rudolf-Laban-1926-Choreographie/chapter-04/04-06.jpg). La primera lista tres familias (steep/suspended/flat); la segunda confirma que cambiar el orden de letras cambia el nombre. Esto coteja **tablas traducidas**, no la grafía y notación del alemán impreso; la traducción se declara borrador y puede contener errores ([estado y límites](LABAN_CHOREOGRAPHIE_TRADUCCION_2011.md)). La restricción de no presentar nuestra partición de 48 celdas como una norma histórica permanece.

El cotejo adicional del [capítulo 8, pp. 24–26 en esa traducción](http://www.laban-analyses.org/jeffrey/2011-Rudolf-Laban-1926-Choreographie/chapter-08/Swing-Scales-pg24.htm) confirma que el orden de los tres componentes tiene significado cualitativo de predominio. Sin embargo, la tabla de seis deflexiones defensivas de p. 26 **repite literalmente `fore-side-high`** para dos movimientos. Su nota editorial 9 cita una versión de Maletic con `forward-side-low` para el último. Sin el alemán original no se resuelve si es errata del libro, transcripción o traducción; la lista de p. 26 no se usará como generador automático de doce direcciones. Esto no invalida por sí solo la lista distinta de 24 nombres de p. 13.

## Qué orden codifican los nombres

Tomemos `L=|u_lateral|`, `V=|u_vertical|` y `S=|u_sagital|` para una dirección unitaria de un tramo. En cada uno de los ocho octantes, la tabla 2 contiene estas tres órdenes estrictas:

| Familia y ejemplo en octante derecha/arriba/adelante | Orden de magnitud que su nombre sugiere |
|---|---|
| Plana: `right-high-fore` | `L > V > S` |
| Empinada: `high-fore-right` | `V > S > L` |
| Suspendida: `fore-right-high` | `S > L > V` |

La tabla **no enumera** en ese octante las tres permutaciones opuestas: `L > S > V`, `V > L > S` y `S > V > L`. Por aritmética, los signos de componentes más un orden completo tienen `8 × 3! = 48` celdas estrictas; los 24 nombres citados corresponden a una de las dos orientaciones cíclicas del orden en cada octante. Esta es una propiedad de la **lista de nombres**, no demostración de que Laban prohibiera movimientos en los otros sectores ni de que sus signos fueran una partición exhaustiva de todas las pendientes posibles. Longstaff afirma que los signos representan infinitas inclinaciones paralelas y no fija en esa tabla tres valores angulares exactos por nombre.

Por eso `octante × eje dominante` también produce 24 etiquetas, pero cada una funde dos órdenes distintos de secundaria y terciaria. Por ejemplo, `L > V > S` y `L > S > V` reciben la misma etiqueta gruesa «lateral dominante», aunque sólo el primero coincide con la secuencia nominal `right-high-fore` de la tabla para ese octante. **Igualdad de cardinalidad no es equivalencia semántica.**

## Regla computacional propuesta, con abstención

Guardar siempre `(u_lateral,u_vertical,u_sagital)`, su marco, la ventana temporal y la incertidumbre angular. Reportar por separado:

1. `clase_24_gruesa`: octante y eje mayor, sólo si los signos y la dominancia resisten el error medido.
2. `orden_48`: octante y permutación completa de magnitudes, sólo si las tres separaciones resisten el error; usar el [margen angular](MARGEN_ANGULAR_INCLINACIONES.md) ya derivado.
3. `nombre_tabla_2`: candidato textual **sólo** cuando `orden_48` coincide con una de las 24 órdenes listadas por Longstaff. Para la otra mitad, escribir `sin_correspondencia_en_tabla_2`; para empates, bajo desplazamiento o error que cruza una frontera, `indeterminado`. No proyectar a la dirección histórica «más cercana» sin una métrica y una regla de tolerancia predefinidas.

El carácter de un gesto y su armonía coreútica no se derivan de estar dentro de una de esas 24 órdenes. La lista histórica debe validarse mediante lectura de Laban y anotación experta antes de transformarla en variable principal de rope flow. En el primer paper, el vector continuo y el orden de componentes permiten un análisis reproducible aun si no se consigue esa validación. Ninguna clase justifica por sí sola un tono consonante en Beacon.

## Verificación interna y pregunta abierta

El [banco sintético ejecutable](orden_componentes_sintetico.py) enumera los seis órdenes posibles en los ocho octantes: 48 celdas, 24 con una secuencia nominal de la tabla y 24 sin ella. Prueba también que una cota angular dura puede permitir la clase gruesa y exigir abstención en el orden completo, y que un tramo no identificable no recibe clase aunque su vector aparente tenga margen. La función devuelve `orden_nominal_candidato` y no un signo histórico. Esto verifica la aritmética y la lógica de abstención de la propuesta, **no** la historia, la exactitud de cámara ni la percepción humana. Hay que resolver con una fuente autoral y especialistas si el orden nominal expresa regiones abiertas de pendientes, familias alrededor de prototipos o una convención de notación más flexible. Hasta entonces no convertir `nombre_tabla_2` en verdad de referencia para entrenar HarMoCAP.
