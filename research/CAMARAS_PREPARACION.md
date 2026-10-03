# Preparación de cámaras para geometría de Laban

Documento de diseño iniciado el 23 de septiembre y actualizado el 24 de septiembre de 2026. Saira informó **unas cuatro Reolink, unas cuatro cámaras llamadas «logicam» y un Moto G**. Las cantidades son aproximadas y «logicam» se conserva como nombre dado por Saira, sin inferir marca o modelo. No se conocen modelos exactos, resolución, FPS reales, óptica, sincronización ni disponibilidad de archivos originales. Esto especifica qué comprobar para decidir el instrumento; no supone instalación de HarMoCAP ni captura humana.

## Inventario provisional recibido de Saira

| Grupo / IDs de trabajo | Cantidad informada | Uso a comprobar, no asumido | Datos faltantes antes de elegir montaje |
|---|---:|---|---|
| Reolink `R1`–`R4` | ≈4 | Vistas fijas del volumen si permiten exportar video original con tiempos útiles | Modelo de cada una; alimentación/red, óptica, resolución/FPS y compresión efectivos, modo de grabación/exportación y si inserta cuadros o cambia FPS |
| «logicam» `L1`–`L4` | ≈4 | Vistas cercanas de manos, pelvis o soga si el controlador conserva cuadros/tiempos y admite ajustes | Marca/modelo exactos; computador/puerto, formato de captura, FPS real, enfoque/exposición y archivo sin transcodificación posterior |
| Moto G `M1` | 1 | Cámara móvil independiente o referencia visual temporal, según su modo real de video | Modelo/versión, resolución/FPS disponibles, tasa variable, enfoque/exposición, estabilización y acceso al archivo original |

Los IDs son **provisorios**, no números de serie. No se necesita encender las nueve fuentes a la vez. Primero comparar una vista de cada tipo con un patrón y un movimiento de objeto, después escoger el par o conjunto que dé mejor cobertura, tiempo y calibración para la pregunta elegida. Una mezcla de dispositivos puede tener relojes, compresión y obturadores diferentes; la cantidad por sí sola no garantiza 3D ni fase entre cámaras.

**Chequeo local de dispositivos, 24-09-2026, sólo lectura:** este equipo mostró `/dev/video0` y `/dev/video1` con el **mismo identificador físico** de una cámara integrada `Integrated_Webcam_HD` (Microdia en USB). Son dos nodos del mismo dispositivo, no dos vistas independientes. No apareció aquí un dispositivo identificable como Reolink, «logicam» o Moto G; este resultado **no demuestra** que las cámaras de Saira no existan ni que estén disponibles para la prueba en otro equipo o por red. `v4l2-ctl` no está instalado; no se abrieron streams, no se tomó video y no se registran números de serie en esta carpeta. La cámara integrada tampoco valida el montaje previsto. El inventario `R/L/M` continúa pendiente de revisión física y archivos originales cuando se haga el banco técnico.

## Qué se necesita saber de cada cámara

Registrar modelo y lente; resolución y tasa reales, no sólo nominales; posibilidad de fijar enfoque, exposición, balance y velocidad de obturación; si graba timestamps por cuadro o tasa variable; formato de video, compresión, audio y disponibilidad de archivo original; modo de alimentación y duración máxima. Anotar altura, distancia, orientación, campo completo cubierto y si el cuerpo/soga siguen visibles en giros y cruces. El espacio y la iluminación pueden importar más que una resolución nominal alta.

Registrar también si la **vista previa o el archivo exportado están espejados** y si algún preprocesamiento invierte el eje horizontal. El [control de orientación y fase](ESPEJO_ORIENTACION_FASE.md) fija una referencia asimétrica `L/R` y una vuelta de sentido conocido antes de interpretar trayectorias: las distancias pueden ser idénticas bajo espejo mientras el sentido de giro cambia.

Una prueba técnica con objetos y patrón de calibración puede responder muchas preguntas sin captar todavía a un participante. Para comparar cámaras se necesita un evento común registrable, por ejemplo una luz visible en todas las vistas; después se mide desfase y deriva a lo largo del tiempo. Un aplauso captado en audio también puede ayudar, pero su precisión dependerá de los relojes, micrófonos y procesamiento. No asumir que colocar dos videos en el mismo segundo garantiza sincronización cuadro a cuadro.

**Primer paso ejecutable cuando estén los equipos:** una muestra corta de cada `R/L/M` con objeto medido y luz/evento común al inicio y final, guardando **el archivo directamente generado** por ese equipo y su configuración. El [inspector de video](inspeccionar_video.py) puede leer FPS y tiempos de cuadros de esos archivos; no descubre por sí solo el reloj físico ni demuestra sincronía. Comparar resolución útil de manos/soga, desenfoque en movimiento, cuadros perdidos y deriva antes de decidir si vale la pena la calibración multivista. Registrar los fallos de exportación/transcodificación como fallos del flujo, no descartarlos del inventario.

El [presupuesto de error temporal y desenfoque](PRESUPUESTO_ERROR_CAMARAS.md) distingue FPS real, residual de sincronización y tiempo de exposición. Incluye escenarios calculados sin datos de Nico; las tolerancias se fijarán a partir de la diferencia de fase/recorrido que el estudio necesite distinguir. Su sección sobre **orden de inicios** convierte intervalos de evento en una decisión de identificabilidad y de eventual compra, sin deducirla del FPS nominal.

El [banco sintético de acople espacio–tiempo](ACOPLE_CAMARA_FACTIBILIDAD.md) añade una pregunta para comparar `R/L/M`: ¿se recupera el **lugar del acento de rapidez** con un objeto de referencia, a la escala en píxeles y FPS efectivos del archivo? Más FPS, por sí solo, no responde a esa pregunta.

El [paquete de captura](PAQUETE_CAPTURA_NICO_V0.md) ordena la prueba técnica, el registro por intento y el resguardo de originales. Incluye un [inspector de video](inspeccionar_video.py) para resumir timestamps de archivos con ffprobe; esos tiempos son diagnósticos del medio, no relojes sincronizados de cámaras.

## Decisión por nivel de geometría

| Objetivo | Montaje tentativo | Condición que decide su utilidad |
|---|---|---|
| Describir movimiento en un plano | Una cámara fija con cuerpo y soga visibles | La profundidad proyectada y las oclusiones no afectan la pregunta elegida |
| Contrastar dos proyecciones | Dos o más vistas, cada una con tiempo y calibración propios | La misma fase del movimiento debe poder localizarse en las vistas; sin esto sólo hay comparaciones visuales |
| Recuperar trayectorias 3D | Múltiples vistas con calibración intrínseca/extrínseca, sincronización y puntos comunes | Error 3D medido contra referencias en la región real del movimiento, incluidos cruces y giros |
| Añadir orientación bajo oclusión | Cámaras más IMU seleccionadas | Alineación temporal y calibración IMU comprobadas, sin que el sensor cambie el gesto |

[OpenCap (Uhlrich y colaboradores, 2023)](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1011462) demuestra una ruta validada para reconstrucción 3D con dos o más teléfonos en las tareas de su estudio. No constituye validación de rope flow ni de nuestras métricas coreúticas. Puede servir como referencia metodológica o instrumento alternativo para evaluar, según compatibilidad de las cámaras existentes. HarMoCAP, en el [commit auditado](agent_reports/06_harmocap_auditoria.md), produce coordenadas 2D; disponer de varias cámaras no cambia por sí solo esa salida a 3D.

El [contraejemplo de identificabilidad](IDENTIFICABILIDAD_2D_3D.md) muestra dos recorridos 3D de distinta longitud que generan exactamente la misma curva en una imagen ideal. Por ello una vista sólo sostiene variables proyectadas, salvo que una restricción espacial adicional se compruebe de forma independiente.

## Comprobación antes del protocolo con Nico

1. Definir dos o tres patrones concretos de rope flow y las partes críticas visibles: manos, codos, pelvis, tronco y, si se decide, soga.
2. Fijar la referencia espacial: suelo, vertical, anterior corporal, orientación de cámaras y volumen de trabajo.
3. Medir estabilidad de tiempo, distorsión de lente y error de calibración en todo el volumen, no sólo en el centro de la imagen.
4. Comprobar cuántos cuadros útiles se conservan durante rotaciones y oclusiones; registrar pérdidas y confusiones entre izquierda/derecha.
5. Comparar segmentos de referencia o anotación manual con la salida del sistema elegido. Definir margen de error a partir de la menor diferencia de dirección/fase que el estudio necesita distinguir.
6. Guardar originales, timestamps y configuración. Las salidas suavizadas o renderizadas no reemplazan el material de referencia.

La decisión de adquirir IMU o usar un sistema 3D concreto viene después de esa comprobación. Si la geometría 3D no puede recuperarse con precisión suficiente, el primer paper puede concentrarse en la viabilidad y en descriptores 2D delimitados.
