# Nico: diseño de caso intensivo y guías de reporte

Nota metodológica del 23 de septiembre de 2026. Es una decisión para redactar protocolos; no hay grabaciones ni ensayo humano. Distinguir **una persona** de un **ensayo N-of-1** evita que muchas ventanas de video aparenten replicación entre participantes.

## Qué diseño tenemos en cada etapa

| Etapa | Asignación de condiciones | Unidad que sostiene la inferencia | Denominación y reporte |
|---|---|---|---|
| Banco de cámara y piloto Laban | Ninguna intervención asignada; se repiten tomas para estimar error y cobertura | Montaje, sesión y tipo de movimiento; ventanas anidadas | Estudio instrumental de caso intensivo. Describir referencia, acuerdo, pérdidas y condiciones de medición. No denominarlo ensayo N-of-1 ni declarar cumplimiento de CENT/SCRIBE. |
| Asociación Laban/HIT–belleza/experiencia | Observación prospectiva de tareas y sesiones reservadas, sin asignación causal de audio | Sesión o bloque según resultado; clips y jueces son niveles anidados | Estudio observacional de caso intensivo. Registrar muestreo, controles, dependencia temporal y límites de generalización. CENT/SCRIBE no son la lista formal correspondiente. |
| Efecto inmediato de Beacon | Condiciones de audio asignadas prospectivamente en bloques comparables, si la prueba técnica lo permite | Bloque asignado; ciclos son medidas repetidas | Posible experimento de caso único. Elegir secuencia, aleatorización y reporte después de comprobar arrastre y estabilidad. SCRIBE puede corresponder si se adopta un diseño experimental de caso único. |
| Aprendizaje/retención con Beacon | Exposición al feedback y pruebas posteriores **sin audio** | Día/sesión y ocasión de retención | Pregunta distinta del efecto inmediato. No tratar las pruebas posteriores como un regreso a la línea de base por simple silencio. |

La [declaración CENT 2015](https://www.bmj.com/content/350/bmj.h1738) reserva su extensión CONSORT a ensayos prospectivos con múltiples cruces de intervención en **la misma persona**, habitualmente ABAB; excluye expresamente otros diseños de caso único. La [declaración SCRIBE 2016](https://pmc.ncbi.nlm.nih.gov/articles/PMC5214372/) cubre la familia de diseños experimentales de caso único en ciencias conductuales; pide identificar estructura, secuencia y reglas de cambio de fase, aleatorización cuando existe, definiciones de medidas y datos brutos. Una guía de **reporte** no convierte por sí sola el diseño en causalmente válido.

## Por qué un ABAB puede fallar aquí

Si escuchar Beacon enseña una forma de coordinar el rope flow, la habilidad puede persistir al retirar el sonido. El segundo A de ABAB ya no representa el estado previo a B. Un descanso que elimina fatiga no elimina necesariamente aprendizaje. La relación medida podría depender de práctica, día, expectativa o secuencia. Esta es una **inferencia de diseño**, no un resultado sobre Nico.

Para el **efecto inmediato**, considerar bloques de audio contingente, audio reproducido y silencio con orden asignado y restricciones predefinidas, después de familiarización. Fijar la misma tarea y registrar periodo, bloque previo y medida de arrastre. Aleatorizar el orden no vuelve independientes los bloques ni hace ciego al ejecutante; el análisis debe conservar la secuencia real. El audio reproducido puede marcar ritmo y por eso es un comparador activo.

Para **aprendizaje**, diseñar una prueba separada sin audio inmediata y otra posterior, con una referencia previa a la exposición y tareas de transferencia definidas. Una sola serie de Nico puede describir cambio temporal, pero la atribución causal de retención necesita controles de práctica/orden y replicación apropiada. Si se propone línea de base múltiple entre patrones, comprobar que aprender uno no entrena los otros; en rope flow esa independencia no se puede asumir. No llamar «washout» al silencio sin evidencia de reversión.

## Qué fijar antes de una sesión confirmatoria

1. **Pregunta y estimando:** efecto asistido mientras suena, adquisición al final de práctica, retención sin audio o asociación observacional; cada uno exige un contraste distinto.
2. **Tarea y unidad:** frase concreta de rope flow, duración, criterio de inicio/cierre, bloque asignable y día. Cuadros y ciclos aportan precisión descriptiva, no nuevos participantes.
3. **Asignación y secuencia:** método reproducible, restricciones por fatiga/familiarización, periodos comparables, regla de interrupción y orden de las pruebas sin audio.
4. **Resultado independiente del sintetizador:** error de tarea o descriptor geométrico válido, con límites de medición. Guardar también jerk, cadencia, fallos, percepción y estado de audio.
5. **Análisis:** tendencia temporal, dependencia dentro de bloque/día, arrastre y datos faltantes. Mostrar trazas por sesión y estimaciones con incertidumbre; cualquier contraste aleatorizado debe respetar el esquema real de asignación.
6. **Reporte:** usar SCRIBE sólo si el diseño final es experimental de caso único; usar CENT sólo si realmente hay múltiples cruces prospectivos con un efecto plausiblemente reversible. Describir intervención con TIDieR si se ejecuta Beacon. Para la fase instrumental, documentar acuerdo y reproducibilidad con la guía pertinente sin forzar etiquetas de ensayo.

Las cantidades de sesiones, bloques, clips y jueces se dimensionarán tras ver repertorio, equipo, error y variación entre días. No hay tamaño de muestra aprobado. El primer paper puede reportar únicamente viabilidad y validez de medición; un ensayo Beacon requerirá protocolo y paper propios.

## Fuentes originales consultadas

- Vohra y cols. [CENT 2015, declaración](https://www.bmj.com/content/350/bmj.h1738) y Shamseer y cols. [explicación y elaboración](https://www.bmj.com/content/350/bmj.h1793). Consulta del 23-09-2026 a través del texto indexado y resumen PubMed; el sitio BMJ devolvió 403 al abrirlo directamente en esta sesión. Alcance y definición corroborados en [PubMed](https://pubmed.ncbi.nlm.nih.gov/26272791/).
- Tate y cols. [SCRIBE 2016, declaración completa](https://pmc.ncbi.nlm.nih.gov/articles/PMC5214372/). Texto consultado; la lista incluye 26 ítems y enumera diseños de reversión, línea de base múltiple y tratamientos alternados.

Relación interna: [plan general](PLAN_INVESTIGACION.md), [estimandos](ESTIMANDOS_Y_CONTRASTES.md), [paper inicial](ESQUELETO_PAIPER.md) y [ensayo Beacon](ENSAYO_BEACON_CONTINGENCIA.md).
