# ¿Sobrevive al error la diferencia numérica entre situaciones?

El [mapeo exploratorio a Beacon](BEACON_SITUACION_MAPEO_OFFLINE.md) da ganancias distintas para dos círculos sintéticos de igual `Q` y fase, con diferente situación radial. El [banco ejecutable](beacon_situacion_incertidumbre.py) añade una pregunta anterior a la escucha: **¿siguen separados los controles si la geometría tiene error?** Usa las [cotas matemáticas de situación](PRESUPUESTO_ERROR_SITUACION.md) y el contrato numérico fijado; no estima errores de cámara ni genera audio.

Para una cota dura simultánea `δ` de cada punto **relativo al origen**, con alcance `R=2` conocido exactamente en el fixture, `rho_min` verdadero pertenece a `[(d̂−δ)/R,(d̂+δ)/R]` (truncado en cero). La función `g₇=0,2+0,8ρ/(1+ρ)` es creciente, así que los extremos del intervalo pasan por esa función en el mismo orden. La diferencia nominal de los dos controles es `0,133333`, pero la comparación robusta usa **los intervalos**, no sólo esa resta. Si además el alcance tuviese error, se deben usar los denominadores `R̂±ε_R` del presupuesto espacial; el script admite esa cota aunque el ejemplo fija `ε_R=0`.

Para `V_r`, la cota publicada es `|V̂_r−V_r|≤min(1,6nδ/max(L,L̂))`. Como sólo conocemos `L̂` en una aplicación, sustituir el denominador por `L̂` da una cota más conservadora. Intersectamos `[V̂_r−b,V̂_r+b]` con `[0,1]` y lo transformamos por `g₈=0,2+0,8V_r`. Una ganancia dentro de un intervalo no es una distribución de probabilidad ni una promesa de audibilidad.

| Cota construida `δ` | Banda 7: situaciones distinguibles por intervalos | Banda 8: situaciones distinguibles por intervalos | Lectura |
|---:|:---:|:---:|---|
| `0,01` unidades, `R=2` | Sí | No | El margen de `rho_min` sobrevive a esta cota hipotética; la cota peor caso de `V_r` es `1` para 8000 segmentos. |
| `0,31` unidades, `R=2` | No | No | Incluso el orden de las ganancias de banda 7 deja de estar garantizado por intervalos disjuntos. |

Las curvas recorren ocho ciclos y tienen longitud `50,2654` unidades. Con `n=8000`, la cota de `V_r` ya es trivial para `δ=0,01`: `6nδ/L̂≈9,55>1`. Esto **no demuestra** que el error efectivo de `V_r` sea enorme; demuestra que esta garantía por error independiente en cada vértice no alcanza para sostener la interpretación del control. Una cota informativa requeriría medir estructura temporal del error, validar un estimador filtrado o usar una referencia dinámica, sin ajustar el filtro después de oír el resultado deseado.

Con alcance fijo y los mínimos nominales `0,199999` y `0,499998`, los intervalos de `rho_min` son disjuntos sólo si `2δ/R < 0,499998−0,199999`, es decir `δ < 0,299999` unidades aproximadamente. Esta es una **condición suficiente del fixture**, no una especificación para comprar cámaras: `R`, el marco y el error conjunto deben medirse para el repertorio y la velocidad de interés.

La comparación supone el mismo origen, marco, definición de frase, malla temporal y correspondencia de puntos; `δ` incluye error de punto **y origen**, y no cubre oclusión, identidad errónea, desplazamiento entre cuadros ni error de fase. En el [sobre actual](CONTRATO_SITUACION_V0.md) la incertidumbre figura `not_estimated`, por lo que ningún caso de una persona puede recibir todavía la etiqueta «separación robusta». Incluso con intervalos de control disjuntos, falta registrar el audio real del instrumento y comprobar discriminación de oyentes; filtros solapados y espectro de entrada pueden ocultar la diferencia.

**Decisión:** conservar banda 7/8 como canales exploratorios de replay, pero no presentar ocho vectores diferentes como ocho sonidos distinguibles ni usar banda 8 para decidir «consonancia». El banco técnico futuro debe fijar qué separación espacial importa y medir error suficiente para un intervalo de control informativo antes del ensayo perceptivo.
