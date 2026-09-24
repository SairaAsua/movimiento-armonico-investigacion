# Revisión independiente: validación y diseño hacia un paper

2026-09-23. Documento local de planificación; no ejecuta capturas ni intervenciones. [E] evidencia o guía primaria; [T] definición conceptual; [P] propuesta; [L] límite.

## 1. Nombrar correctamente cada estudio

[T] Observar repetidamente a Nico durante su práctica habitual es un estudio observacional intensivo de caso único. Su factibilidad se evalúa mediante señales utilizables, sincronización, tolerancia y cumplimiento, no por significación estadística. Asignar prospectivamente condiciones cambia el diseño: comparar feedback Beacon y control en períodos aleatorizados sería un experimento N-of-1 cruzado.

[E] CENT orienta reportes de N-of-1 prospectivos con múltiples cruces; SCRIBE se desarrolló para diseños experimentales de caso único en intervenciones conductuales. Son guías de reporte, no certificados de validez ni requisitos universales para observar movimiento. TIDieR permite describir una intervención reproducible: materiales, procedimientos, responsable, dosis, modificaciones y cumplimiento. Lectura: resúmenes y registros oficiales/editoriales, no verificación completa de cada checklist. [CENT](https://www.bmj.com/content/350/bmj.h1793), [SCRIBE](https://pubmed.ncbi.nlm.nih.gov/27231387/), [TIDieR](https://www.bmj.com/content/348/bmj.g1687).

[L] Un experimento no deja de ser potencialmente clínico porque incluya una persona sana o carezca de medicamentos. ICMJE considera asignación prospectiva, intervención relacionada con salud y resultado biomédico/sanitario. [P] Clasificar el futuro Beacon según su objetivo y revista antes de captar participantes; aplicar las exigencias pertinentes, sin imponer automáticamente guías clínicas a la observación artística. Lectura: política oficial. [ICMJE](https://www.icmje.org/recommendations/browse/publishing-and-editorial-issues/clinical-trial-registration.html).

## 2. Validación instrumental vinculada a la hipótesis

[P] Definir primero la diferencia que interesa detectar y después la precisión necesaria. Si la hipótesis depende de desfases, validar el reloj común, latencia y deriva además de los ángulos. Para movimiento aproximadamente periódico, un error temporal δt produce error de fase aproximado 360·f·δt grados. El presupuesto de error debe contemplar incertidumbre temporal, reconstrucción espacial, filtrado y definición de ciclo.

[P] Comparar video/IMU contra una referencia adecuada durante rotaciones, cruces de brazos y oclusiones representativas de rope flow. Informar error angular y temporal por segmento, velocidad y patrón; cuantificar pérdidas y sesgo. Definir márgenes aceptables antes de mirar el resultado. No basta el buen desempeño promedio en movimientos sencillos.

[E] Bland y Altman explicaron por qué correlación elevada no demuestra acuerdo entre instrumentos. [P] Usar diferencias, sesgo y límites de acuerdo con intervalos de incertidumbre, adaptados a medidas repetidas y dependencia temporal. Validar también la incertidumbre de la referencia. Para fases circulares, utilizar diferencias circulares: 359° y 1° están próximos. Lectura: resumen del artículo original y copia del autor localizada. [Bland–Altman](https://doi.org/10.1016/S0140-6736(86)90837-8).

## 3. Repetibilidad y resultados principales

[P] Repetir medición dentro de una sesión y entre días, reinstalando sensores y recalibrando cámaras. Separar variación del instrumento, del evaluador y del propio movimiento. Reportar error absoluto, sesgo entre días y estabilidad de la clasificación; una correlación test–retest aislada puede ocultar errores grandes. Con n=1, no estimar fiabilidad poblacional entre personas.

[P] Para factibilidad, elegir como resultado principal la proporción de bloques con todas las señales indispensables utilizables bajo criterios previos. Para asociación, elegir uno: por ejemplo, cambio en potencia metabólica neta por unidad de una métrica cinemática fijada, dentro de patrones comparables. Belleza, sensualidad, placer y absorción serían resultados secundarios separados. Si el objetivo principal fuese estética, declararlo antes y conservar metabolismo como secundario; evitar decidir según qué asociación resulte positiva.

[L] Ninguno de esos resultados representa automáticamente conciencia elevada. Energía metabólica corresponde a bloques compatibles con la dinámica respiratoria; no convertir fotogramas o clips breves en observaciones energéticas independientes.

## 4. Tamaño, confusión y prueba independiente

[P] Dimensionar sesiones y bloques mediante simulaciones basadas en precisión deseada, variabilidad piloto, autocorrelación, tendencia de aprendizaje y datos perdidos. Expresar la precisión en unidades interpretables del resultado principal. Más fotogramas afinan trayectorias, pero no multiplican sujetos ni sesiones independientes. Un piloto pequeño puede revelar inviabilidad; no asegura potencia para contrastar HIT.

[P] Registrar y controlar patrón, cadencia, amplitud, soga, descansos, fatiga, práctica acumulada, música, temperatura, sueño y expectativa. Conservar todas las tomas admisibles, obtener valoraciones ciegas a sensores y evitar seleccionar únicamente clips “bellos”. Predefinir exclusiones y sensibilidad a datos faltantes; los fallos de captura podrían concentrarse justamente en movimientos complejos.

[P] Reservar sesiones completas posteriores como prueba independiente. Congelar extracción, filtros, variables y parámetros con sesiones de desarrollo. Comparar un modelo base —cadencia, amplitud, patrón, suavidad— contra el mismo modelo más una predicción cuantitativa específica de HIT. Evaluar mejora predictiva y calibración en sesiones reservadas, con incertidumbre; igualar oportunidades de ajuste. [L] Si HIT sólo cambia el nombre de una variable convencional, no constituye aporte incremental. Si se reajusta mirando las sesiones reservadas, dejan de ser prueba independiente.

## 5. Beacon: intervención posterior y criterios para avanzar

[P] Sólo después, estudiar feedback contingente frente a control sonoro comparable en volumen, timbre y exposición, con orden aleatorizado. Un control podría reproducir sonido previamente grabado sin contingencia actual; documentar su credibilidad y posibles diferencias motivacionales. No usar disonancia dolorosa, sobresaltos ni indicaciones motoras peligrosas. Un control sonoro puede tener efectos propios; estima la contribución de la contingencia, no una ausencia absoluta de intervención.

[P] Registrar efectos de período y condición anterior. El descanso metabólico no borra aprendizaje: si hay transferencia duradera, el crossover simple no identifica limpiamente efectos reversibles y debe rediseñarse. Describir Beacon mediante TIDieR y usar CENT cuando corresponda al diseño finalmente elegido.

[P] Criterios de avance: instrumento suficientemente preciso para el contraste; repetibilidad aceptable; tarea comparable; protocolo y resultado principal fijados; asociación comprobada en sesiones reservadas; y, para Beacon, contingencia verificable y arrastre manejable. [L] Un resultado nulo o un límite técnico también permite un paper de factibilidad honesto; no prueba ni refuta toda HIT.
