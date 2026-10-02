# Referencia 2D para el ensayo público: paquete de desarrollo

**2 de octubre de 2026 · diseño y paquete privado preparados; ninguna anotación humana realizada.** Este trabajo pertenece a la [issue #10](https://github.com/SairaAsua/movimiento-armonico-investigacion/issues/10). Complementa la [guía Laban para rope flow](ANOTACION_LABAN_PILOTO.md) con una tarea anterior y más estrecha: comprobar **posición visible e identidad 2D** frente al detector. No asigna categorías Laban, experiencia ni fase HIT.

## Selección previa a la referencia

El [video de ensayo publicado en Commons](https://commons.wikimedia.org/wiki/File:Persona_dance_rehearsal.webm) tiene hash SHA-256 `573ac41a261d71fc59fbf890d129964061f3c9346bcf6fcf5b4cecb3217e05aa`. El intervalo 152 ≤ PTS < 174 s contiene 550 cuadros del original, con dos estratos por una diferencia visual de superposición: 200 cuadros entre 152–160 s y 350 entre 160–174 s. La [criba técnica](VIDEO_DANZA_PUBLICO_CRIBA.md) documenta licencia, PTS, detector y límites.

El [generador del paquete](preparar_referencia_pose_publica.py) divide **cada estrato en 20 bins de igual número de cuadros** y escoge un cuadro al azar dentro de cada bin con semilla fija `20261002`. El resultado local verificado contiene 40 PNG, un manifiesto con hash de cada PNG y una plantilla de 480 filas: 40 cuadros × 2 personas × 6 puntos (ambos hombros, muñecas y caderas). Los bins tempranos tienen 10 cuadros; los tardíos, 17 o 18. Cada cuadro conserva índice y PTS del original. No se eligieron cuadros por confianza del modelo, calidad estética o resultado HIT. Los originales, PNG, manifiesto del paquete y CSV de trabajo **no se suben al repositorio público**.

Comando para regenerar en un directorio privado **fuera de Git**; el programa rechaza una salida dentro del repositorio y un directorio no vacío:

```bash
python research/preparar_referencia_pose_publica.py VIDEO_ORIGINAL.webm DIRECTORIO_PRIVADO \
  --expected-sha256 573ac41a261d71fc59fbf890d129964061f3c9346bcf6fcf5b4cecb3217e05aa
```

## Guion para dos codificadores independientes

1. Cada codificador recibe su propia copia de `annotation_template.csv`, los 40 cuadros y el original para revisar contexto temporal cuando la identidad sea dudosa. Antes de empezar se acuerda una convención privada A/B basada en atributos visuales constantes, sin nombres. No ve predicciones, confianza, tracks, overlays ni los agregados de HarMoCAP.
2. En cada fila marca `status`: `visible`, `occluded`, `out_of_frame`, `ambiguous_identity` o `unresolvable`. Sólo `visible` admite `x_px`,`y_px` dentro del cuadro original de 852 × 480 píxeles. Anota lado **anatómico**, no izquierda/derecha de pantalla. Puede indicar incertidumbre de localización en píxeles y un comentario breve. Una posición inferida detrás de otra persona no se registra como visible.
3. Si el cuadro aislado no permite seguir A/B, mira un contexto breve del original y registra que lo usó; si tampoco resuelve la identidad, marca `ambiguous_identity`. El contexto ayuda a identificar, pero la coordenada corresponde al cuadro indicado por PTS. Si hay un corte dentro de un intervalo de contexto, no propaga identidad a través de él sin evidencia.
4. Se guardan las dos anotaciones originales antes de cualquier conversación. Las diferencias se revisan después, conservando originales y eventual adjudicación por separado. No se obliga un punto cuando el desacuerdo proviene de oclusión o de un píxel no distinguible.

Una vez cerrados **dos CSV originales independientes**, el [validador de referencia](validar_referencia_pose_publica.py) comprueba el manifiesto y hashes de los PNG privados, todas las 480 claves por observador, estados, coordenadas dentro de 852 × 480 y ausencia de posiciones inventadas en puntos no visibles. Emite por pantalla sólo agregados de acuerdo de estado, distancia entre marcas cuando ambas son visibles y cobertura de torso/muñecas ponderada por los bins de 10/17/18 cuadros:

```bash
python research/validar_referencia_pose_publica.py \
  DIRECTORIO_PRIVADO/manifest.json CODIFICADOR_1.csv CODIFICADOR_2.csv
```

Ejecutarlo localmente, sin redirigir a un archivo público. Los códigos de observador deben ser distintos; el script no puede demostrar que hayan trabajado a ciegas o de forma independiente, ni que una marca visible sea anatómicamente correcta. El acuerdo se informa **antes** de adjudicar desacuerdos. La cobertura ponderada estima la fracción de cuadros fuente donde cada codificador vio los puntos requeridos; no es cobertura validada de HarMoCAP y no lleva un umbral de aceptación automático.

No se pide a estas personas que juzguen belleza, sensualidad, intención, estados internos, eficiencia ni autenticidad de la danza. La licencia publicada para el archivo es CC BY-SA 4.0; eso no transforma a las intérpretes en participantes consentidas de nuestro estudio. El uso de esta referencia queda limitado a desarrollo técnico y a la revisión ética/institucional que corresponda antes de publicar una evaluación de personas.

## Comparación prevista con HarMoCAP

La muestra aleatoria por bins sirve para una descripción de calidad 2D del **mismo video**. Primero informar acuerdo entre codificadores: estado de visibilidad por punto/persona/estrato y distancia entre coordenadas cuando ambas sean visibles. Después, una exportación privada de HarMoCAP sobre los **mismos índices fuente** se empareja con A/B por revisión de identidad; un `track_id` estable no es referencia por sí solo. Reportar omisiones, intercambios y error en píxeles por articulación, separado de la confianza del modelo. Un punto anatómicamente incorrecto con alta confianza cuenta como error.

La [herramienta de diagnóstico](diagnosticar_pose_video_publico.py) puede emitir esa exportación en un directorio **privado y vacío fuera de Git**, mientras procesa los 550 cuadros consecutivos para mantener el estado temporal de ByteTrack. Sólo guarda poses de los 40 índices sorteados, con PTS original, índice fuente, ID efímero y seis coordenadas en píxeles por detección; coteja el SHA-256 del video con el manifiesto. Un `stride` mayor que uno se rechaza para este uso. Requiere el entorno aislado con HarMoCAP, el checkpoint y las dependencias indicadas en la [criba técnica](VIDEO_DANZA_PUBLICO_CRIBA.md):

```bash
python research/diagnosticar_pose_video_publico.py VIDEO_ORIGINAL.webm CHECKPOINT.pt \
  --start-pts 152 --end-pts 174 --stride 1 \
  --private-manifest DIRECTORIO_PRIVADO/manifest.json \
  --private-out-dir OTRA_SALIDA_PRIVADA_VACIA
```

Este archivo derivado contiene posiciones de personas y tampoco se publica. **No** se asigna automáticamente el `track_id` a A/B por proximidad: eso usaría la referencia que se quiere evaluar para elegir la predicción más conveniente. Una revisión de correspondencia de identidad, conservando `unmatched` y cambios de ID, sigue pendiente antes de calcular error anatómico.

**Ejecución técnica del 2 de octubre de 2026:** la exportación privada contiene los 40 `sample_id` esperados; cada índice, PTS y dimensión 852 × 480 coincidió con el manifiesto. El procesamiento continuo cubrió 550/550 cuadros y reprodujo el agregado anterior: 542 con dos detecciones, 8 con una y 3 IDs efímeros. Se verificó el SHA-256 del video y el del archivo derivado privado (`683558d8d667e234e8f305d493b4814847822fe7ddf633ad6bc0cf6038f6f495`). Ninguna posición individual entra a este repositorio. Este resultado certifica **alineación y reproducibilidad técnica**, no precisión de pose ni identidad de intérpretes.

Para un resumen de cobertura de los 550 cuadros, cada cuadro sorteado representa su bin de 10, 17 o 18 cuadros; usar `design_weight_frames` del manifiesto y el denominador completo, no tratar 20/20 por estrato como si los estratos tuvieran igual tamaño. Esta muestra pequeña y temporalmente correlacionada es **piloto descriptivo**: sus 40 cuadros no son 40 personas ni justifican un intervalo de confianza ingenuo por cuadro. El error y la referencia se limitan a 2D proyectado; no validan orientación corporal 3D ni recorrido de soga. Las ocho ocasiones en que el detector produjo sólo una persona merecen una auditoría dirigida adicional, **separada** de esta muestra probabilística.

Si la referencia confirma cobertura suficiente para un descriptor, fijar la regla de validez por señal antes de analizar un conjunto reservado. Si falla una muñeca o identidad, emitir `invalid` para la relación que la requiere; no suavizar una trayectoria a través de la pérdida y llamarla observada. La fase HIT requerirá además evento/ciclo y reloj verificables; el mapeo Weaver/Beacon requerirá controles aplicados y audio registrado. El caso principal de Nico necesitará su propio consentimiento, referencia y validación por día, sin transferir estos porcentajes desde la danza pública.
