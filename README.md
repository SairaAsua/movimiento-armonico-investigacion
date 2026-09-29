<p align="center">
  <img src="assets/movimiento-armonico-cover.svg" alt="Una trayectoria corporal se transforma en una onda: espacio, tiempo y sonido" width="100%">
</p>

<h1 align="center">Movimiento armónico</h1>

<p align="center"><strong>Del gesto que vemos al movimiento que podemos medir y escuchar.</strong></p>

<p align="center">Una investigación del equipo de <strong>Harmonic Beacon</strong> sobre danza, rope flow,<br>organización del movimiento y sonificación.</p>

<p align="center">
  <a href="papers/ARTICULO_TEORETICO_METODOLOGICO.md">Leer el artículo</a> ·
  <a href="papers/ARTICULO_TEORETICO_METODOLOGICO.pdf">Descargar el PDF</a> ·
  <a href="docs/DOSSIER_MOVIMIENTO_ARMONICO.pdf">Ver el dossier</a> ·
  <a href="https://github.com/SairaAsua/movimiento-armonico-investigacion/issues/14">Seguir la investigación</a>
</p>

---

### La pregunta

Cuando una persona mueve una soga, baila o encuentra una forma de desplazarse que percibimos como fluida, **¿qué relaciones concretas entre espacio, tiempo y cuerpo podemos observar?** ¿Coinciden con lo que siente quien se mueve, con lo que ve otra persona y con el esfuerzo que exige la tarea?

Queremos estudiar esas relaciones sin dar por sentado que belleza, placer, coordinación y economía fisiológica sean lo mismo. El primer caso previsto es **Nico practicando rope flow**, con figuras comparables y grabaciones autorizadas. Antes de interpretar su movimiento, hay que averiguar qué pueden medir de verdad las cámaras.

| 01 · Describir | 02 · Contrastar | 03 · Escuchar |
|:---|:---|:---|
| Recorridos, planos y direcciones inspirados en **Laban**. | Relaciones de fase y recurrencia propuestas desde **HIT**, junto con experiencia y juicios independientes. | Señales validadas convertidas en sonido mediante **HarMoCAP → Harmonic Weaver → Beacon**. |

<table>
  <tr>
    <td width="50%"><img src="assets/laban-dancers-1914.jpg" alt="Rudolf Laban y su compañía en Ascona, 1914" width="100%"></td>
    <td width="50%"><img src="assets/contemporary-dance-2009.jpg" alt="Intérpretes de danza contemporánea sobre un escenario, 2009" width="100%"></td>
  </tr>
  <tr>
    <td align="center"><em>Historia del estudio espacial del movimiento · 1914</em></td>
    <td align="center"><em>Movimiento escénico contemporáneo · 2009</em></td>
  </tr>
</table>

Estas fotografías dan contexto histórico y artístico. **No muestran a Nico ni son datos de la investigación.** [Procedencia y licencias](#fotografías-y-créditos).

### El mapa de la investigación

```mermaid
flowchart LR
    A[Video original<br/>y relojes] --> B[Trayectorias<br/>y calidad]
    B --> C[Espacio<br/>Laban]
    B --> D[Tiempo<br/>HIT]
    C --> E[Experiencia,<br/>estética y controles]
    D --> E
    C --> F[Harmonic Weaver]
    D --> F
    F --> G[Beacon:<br/>sonido]
    G --> H[Estudio posterior<br/>de feedback]
```

**Laban** aporta el vocabulario de kinesfera, direcciones, planos, recorridos y cualidades del movimiento. Las fórmulas de este proyecto son traducciones contemporáneas *inspiradas* en ese marco: no se presentan como ecuaciones históricas de Laban. **Harmonic Information Theory (HIT)** inspira predicciones refutables sobre fase y organización temporal; [aquí se documenta la obra y su autoría](research/sources/HIT_extractos.md). **Risa F. Kaparo** ayuda a formular preguntas sobre la experiencia somática. **Michael Levin** abre preguntas sobre organización y adaptación biológica a otra escala, sin que sus experimentos prueben esta hipótesis corporal.

El sonido es un **instrumento de exploración**: una capa audible puede revelar una relación o facilitar el aprendizaje, pero no certifica por sí sola belleza, eficiencia, placer ni un estado de conciencia.

### Qué existe hoy

| Ya se puede leer y reproducir | Todavía requiere observación humana |
|:---|:---|
| [Artículo teórico-metodológico](papers/ARTICULO_TEORETICO_METODOLOGICO.md), [protocolo piloto](research/PROTOCOLO_PILOTO_V0.md), [matriz espacial](research/LABAN_MATRIZ.md) y [diccionario de señales](research/DICCIONARIO_SENALES_V0.md). | Cotejo completo de las obras de Laban y revisión de categorías con especialistas. |
| [Banco sintético reproducible](research/REPORTE_SINTETICO_PRESENTACION.md): 960 filas, cuatro condiciones y cuatro audios. Permite detectar fallos de una medida de fase, no probar una hipótesis sobre personas. | Calibración de cámaras, video original autorizado de rope flow, anotaciones y valoraciones independientes. |
| [Ruta técnica documentada](research/RUTA_HARMOCAP_WEAVER_BEACON.md) y [plan de video a audio](docs/TRAZA_VIDEO_BAILE_A_NICO.md). | Audio producido y registrado de extremo a extremo; después, un ensayo separado de feedback vivo. |

**Estado de la evidencia:** aún no hay mediciones del caso principal ni una cadena de video a audio Beacon validada. Una simulación comprueba propiedades del método, no demuestra que un movimiento sea más bello, consuma menos energía o produzca un estado de conciencia. Para estudiar costo metabólico harán falta instrumentos fisiológicos adecuados; el video por sí solo no mide calorías ni consumo de oxígeno.

### Biblioteca y próximos pasos

- **Lectura principal:** [artículo teórico-metodológico](papers/ARTICULO_TEORETICO_METODOLOGICO.md) · [PDF](papers/ARTICULO_TEORETICO_METODOLOGICO.pdf) · [índice de manuscritos](papers/README.md).
- **Diseño de investigación:** [plan centrado en Laban](research/PLAN_INVESTIGACION.md) · [protocolo piloto](research/PROTOCOLO_PILOTO_V0.md) · [contrastes y estimandos](research/ESTIMANDOS_Y_CONTRASTES.md) · [bibliografía comentada](research/BIBLIOGRAPHY.md).
- **Primer paper empírico:** [Introducción y Métodos en desarrollo](research/BORRADOR_INTRO_METODOS_PAIPER.md) · [esqueleto de factibilidad](research/ESQUELETO_PAIPER.md). Requiere datos reales antes de informar resultados.
- **Trabajo abierto:** [programa e issues](https://github.com/SairaAsua/movimiento-armonico-investigacion/issues/14) · [equipo humano y compras mínimas](docs/EQUIPO_HUMANO_Y_COMPRAS.md) · [traza de un video de baile hacia el caso principal](docs/TRAZA_VIDEO_BAILE_A_NICO.md).

Si colaborás como **persona**, empezá por el artículo y elegí una tarea del programa. Los videos originales y consentimientos se coordinan fuera de GitHub. Si colaborás como **IA**, leé [AGENTS.md](AGENTS.md), el [índice de investigación](research/README.md), el protocolo y la issue dueña antes de editar; conservá siempre la procedencia de las señales y la distinción entre datos sintéticos y humanos.

La investigación se presenta como trabajo del **equipo de Harmonic Beacon**. La autoría académica de futuros artículos se acordará según contribuciones efectivas y revisión del manuscrito. Las personas referentes aportan marcos teóricos; no se las presenta como integrantes del equipo.

### Fotografías y créditos

- **Laban y compañía, Ascona (1914):** autor desconocido; [archivo en Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Rudolf_Laban_and_dancers,_1914.jpg), marcado allí como dominio público.
- **“Bend and Snap”, danza contemporánea (2009):** [Nazareth College](https://commons.wikimedia.org/wiki/File:Bend_and_Snap,_contemporary_dance_performance_at_Nazareth_College_Arts_Center,_Rochester,_New_York_-_20090925.jpg), licencia [CC BY 2.0](https://creativecommons.org/licenses/by/2.0/). Imagen conservada sin modificar.

No se publican videos identificables, consentimientos, datos personales ni registros crudos de participantes en este repositorio.
