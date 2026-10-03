# Una mejora HIT aparente puede corregir error espacial compartido

**Control algebraico y [script exacto](hit_error_compartido_sintetico.py), 3 de octubre de 2026.** Acompaña el [contraste incremental](ESTIMANDOS_Y_CONTRASTES.md) y la [ablación factorial](factorial_sin_interaccion_sintetico.py). Es un modelo artificial de medición, no una simulación de rope flow, `Q`, fase, belleza ni una ejecución de Nico.

## Testigo con ocho estados equiprobables

Sean `L`, `E` y `N` variables independientes que valen `−1` o `+1` con igual probabilidad. La propiedad externa a predecir depende **sólo** de la geometría verdadera: `Y=L`. El descriptor espacial observado mezcla geometría y error: `A=L+E`. Un segundo descriptor, etiquetado aquí `H` para representar un candidato temporal derivado de la misma adquisición, tiene únicamente información del artefacto: `H=E+N`. No hay relación temporal verdadera en la ecuación de `Y`; además `Cov(Y,H)=0`. El caso es deliberadamente favorable para detectar el problema, no una afirmación de que la fase real de Nico sea ruido.

Con pérdida cuadrática y predictores lineales óptimos para esta distribución, `E[Y|A]=A/2`. Al añadir `H`, la predicción lineal pasa a `Ŷ=(2A−H)/3`. Las pérdidas poblacionales exactas son:

| Entradas disponibles | Predictor | Error cuadrático medio |
|---|---|---:|
| Ninguna (`E₀₀`) | `0` | `1` |
| Espacio observado `A` (`E₁₀`) | `A/2` | `1/2` |
| Candidato `H` (`E₀₁`) | `0` | `1` |
| `A` y `H` (`E₁₁`) | `(2A−H)/3` | `1/3` |

La mejora incremental al añadir `H` después de `A` es `1/2−1/3=1/6`, aunque `H` solo no predice nada de `Y`. También `S=E₁₀+E₀₁−E₀₀−E₁₁=1/6>0`. El mecanismo exacto es que `H` informa sobre `E`, el error que contamina `A`; el modelo conjunto corrige parcialmente `A`. En el límite ideal `H=E`, la predicción `Y=A−H` sería perfecta sin haber descubierto una relación corporal temporal. Reescalar `H` a `[0,1]` no cambia el argumento para modelos con intercepto, pero **no convierte** esta variable en un `R` físico. La identidad, las ecuaciones normales y todas las pérdidas se verifican sobre los ocho estados con fracciones racionales, sin ajuste ni aleatoriedad.

## Qué cambia en el estudio

Una mejora de `base+Laban → +HIT` sobre días reservados puede ser **utilidad predictiva real para ese pipeline** y aun así deberse a corrección de artefactos estables entre días. Separar días evita fuga de entrenamiento, pero no identifica por sí solo el mecanismo de la mejora. Tampoco un `S>0` prueba sinergia corporal: el [otro control exacto](factorial_sin_interaccion_sintetico.py) muestra signos variables de `S` aun con un resultado aditivo verdadero.

Para el piloto, guardar la procedencia de puntos, cámaras, filtros, marcos y relojes de cada `Q` y fase. Medir error y cobertura **por descriptor** con referencias de geometría y eventos suficientemente independientes; examinar si ambos errores covarían con oclusión, orientación y velocidad. En desarrollo, repetir el contraste con un descriptor espacial de referencia mejor validado o con calidad/error explícitos, y con un control temporal que preserve la calidad óptica pero rompa la relación de fase pertinente. Congelar esas comparaciones antes de los días reservados. Un control nulo debe verificarse en la señal para no romper también la tarea o el resultado; ninguna de estas comprobaciones sola elimina todo sesgo.

Si la mejora temporal persiste, el resultado reportable sigue siendo **incremental para las señales, modelos, referencia y días ensayados**. Atribuirla a coordinación HIT requiere descartar explicaciones de calidad instrumental, cadencia, tarea y resultado compartido; atribuir belleza, economía o conciencia requiere resultados externos específicos. Un banco sintético no resuelve esas atribuciones.
