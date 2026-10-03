# Cuando el error de `Q` se vuelve un control sonoro plausible

**Derivación numérica retrospectiva, 3 de octubre de 2026.** El [banco de recta 3D con ruido](Q_RUIDO_MUESTREO.md) mantiene el movimiento físico idéntico: una recta lateral de largo 1, cuyo descriptor verdadero es `Q=(1,0,0)`. Aquí se aplica sólo la asignación **diagnóstica** propuesta en el [contrato científico HarMoCAP–Beacon](INTEGRACION_HARMOCAP_BEACON.md): las tres componentes `Q` a ganancias de las bandas 4–6 mediante `g_k=0,2+0,4Q_k`. No se inició Beacon, no se enviaron mensajes OSC ni se grabó sonido. Los valores de `Q` usan la **frase completa de un segundo**, así que tampoco son controles disponibles al comienzo de un feedback vivo.

## Propagación exacta del error de descriptor

El control verdadero de esta recta sería `g_true=(0,6;0,2;0,2)`. Bajo errores de posición independientes e isotrópicos por eje, los ejes `y` y `z` son simétricos; por ello `E[Q̂_y]=E[Q̂_z]=(1−E[Q̂_x])/2`. La suma de ganancias permanece siempre en 1, pero esa constancia **no protege** de distribuirlas mal entre bandas. Si `q=E[Q̂_x]`, entonces

`E[ĝ]=(0,2+0,4q; 0,4−0,2q; 0,4−0,2q)`,

`||E[ĝ]−g_true||₁=0,8(1−q)`.

Se aplicó esa identidad a las medias de 400 réplicas del perfil de velocidad uniforme, `σ=0,002` unidades por eje, semilla `20261003`. Las dos últimas columnas iguales son **expectativas por simetría del modelo**, no medias independientes medidas para cada eje en el reporte original.

| Cuadros/s simulados | `E[Q̂_x]` | Ganancia esperada banda 4 | Ganancia esperada bandas 5 y 6, cada una | Distancia L1 al control verdadero |
|---:|---:|---:|---:|---:|
| 30 | 0,985993 | 0,594397 | 0,202801 | 0,011205 |
| 120 | 0,817006 | 0,526802 | 0,236599 | 0,146395 |
| 480 | 0,419446 | 0,367778 | 0,316111 | 0,464443 |
| 1920 | 0,339401 | 0,335760 | 0,332120 | 0,528479 |

En el límite de ruido dominante, `Q̂→(1/3,1/3,1/3)` y los tres controles tienden a `1/3`, aunque el movimiento verdadero siga siendo lateral. La distancia L1 al vector de control correcto tiende a `8/15≈0,533333`. El mapeo conserva rangos del contrato y suma de ganancias, por lo que esas **comprobaciones de sintaxis** no revelan el fallo científico. Un mismo movimiento a distinta tasa de muestreo podría generar distintos controles nominales sin que cambie el cuerpo. Esta es una **posibilidad matemática bajo el modelo**, no una predicción de audibilidad: filtros, audio de entrada y estado del instrumento determinan si una persona oiría algo.

## Gate antes de un experimento Beacon

La cadena tiene que conservar `observed/invalid`, definición del recorrido, tasa/PTS y presupuesto de error junto al vector `Q`. Para cada ventana y subdominio físico, comparar el **intervalo plausible del control** contra la diferencia que se promete hacer audible; si se solapan las alternativas espaciales de interés, la capa se deshabilita o se reporta indeterminada, no se envía el valor nominal como «movimiento equilibrado». El reset de bandas después de `invalid` requiere prueba en el adaptador y registro del control efectivamente aplicado. Una ganancia válida matemáticamente (`0,2…0,6`) no certifica una observación corporal válida. La suma fija tampoco iguala nivel ni sonoridad de la salida.

El banco con [curva y retículas anidadas](Q_RUIDO_MUESTREO.md) muestra además que bajar FPS para reducir pasos de ruido puede perder curvatura o fase; el gate debe escoger procesamiento sobre una referencia física, con dominio de velocidad y orientación declarado. Sólo después se probará la ruta `HarMoCAP → Weaver → beacon-spatial` con entrada sonora fijada y audio registrado. Nada aquí compara belleza, eficiencia, experiencia, HIT ni el movimiento de Nico.
