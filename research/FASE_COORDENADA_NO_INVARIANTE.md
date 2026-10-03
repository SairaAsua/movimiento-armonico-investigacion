# La concentración de fase depende de la coordenada intracíclo

**Contraejemplo exacto y banco determinista, 3 de octubre de 2026.** Acompaña la [especificación de fase](FASE_ROPEFLOW.md) y el [caso óptico particular](FASE_PROYECCION_OBLICUA.md). Sólo usa ángulos construidos; no hay video, soga, cámaras, Nico, audio ni resultado humano.

## Mismo movimiento cíclico, otro `R`

Dos señales tienen por construcción la **misma fase física** `θ(t)`; ambas cierran sus ciclos en los mismos eventos. El primer analista la expresa como `φ₁=θ`. El segundo usa una coordenada de avance `ψ₁=θ+a sin θ`, con `a=0,9`, mientras deja la otra como `ψ₂=θ`. Como `dψ₁/dθ=1+a cos θ≥0,1`, la transformación es estrictamente creciente: no invierte el gesto, no pierde vueltas y deja fijos sus cierres `0,2π,...`. Sin embargo, deforma cuánto ángulo asigna a cada tramo de la vuelta.

Para muestras uniformes de una vuelta, la relación física 1:1 tiene `R=|⟨exp(i(θ−θ))⟩|=1`. La relación de las dos **coordenadas** pasa a `R=|⟨exp(i a sin θ)⟩|≈0,807524`. Si se aplica la misma transformación a las dos señales, `R` vuelve a `1`. El [script reproducible](fase_coordenada_sintetica.py) calcula los tres casos con 4096 muestras y comprueba monotonicidad y coincidencia de cierres. El valor `0,807524` es propiedad de esta elección artificial, no un efecto estimado de la proyección de Nico ni un umbral HIT.

Esto generaliza el contraejemplo de [círculo oblicuo](FASE_PROYECCION_OBLICUA.md): aun con píxeles perfectos y sin oclusión, `atan2` de dos vistas o variables distintas puede producir una **protophase** dependiente de la observación. [Kralemann y colaboradores (2008), artículo original en *Physical Review E*, resumen editorial consultado](https://doi.org/10.1103/PhysRevE.77.066205), distinguen fases extraídas de observables y fases corregidas para modelos de osciladores; su método y resultados completos no se leyeron aquí. La derivación y el número de este documento son **nuestros**, no un resultado suyo.

## Qué se decide para Laban, HIT y Beacon

Antes de comparar `Rₚ:q` entre patrones, vistas, días o personas hay que declarar **qué es fase**: avance angular de imagen, avance geométrico en un recorrido corporal validado, fase interpolada entre eventos o fase dinámica estimada bajo un modelo de oscilador. No son intercambiables. Registrar señal original, plano/marco, origen de vuelta, sentido, transformación intracíclo, eventos independientes, cobertura, error y disponibilidad temporal; comparar sensibilidad a elecciones de coordenada que el instrumento permita. Para la predicción HIT, fijar la definición durante desarrollo y conservarla en días reservados; un `R` alto obtenido eligiendo después la parametrización favorable no es evidencia adicional.

Una **uniformización** de protophase puede ser apropiada si el objetivo es estudiar un oscilador aproximadamente autónomo bajo supuestos verificados; no debe aplicarse automáticamente al rope flow. El avance rápido/lento dentro de una vuelta puede ser precisamente la información temporal que se desea relacionar con la geometría de Laban o escuchar en Beacon. Si se transforma para hacerlo uniforme, ese contraste cambia de pregunta. Evaluar por separado cierres/eventos, ritmo intracíclo y estabilidad de la relación en cada coordenada justificada; ninguna variante de `R` mide por sí sola belleza, economía o conciencia.
