# Los extremos y la variación radial no describen toda la situación

El [banco sintético ejecutable](situacion_ocupacion_arco_sintetica.py) exhibe dos trayectorias 3D con los **mismos** `Q`, `rho_min`, `rho_max`, `V_r`, longitud total, extremos inicial/final y número de puntos, pero con distinta proporción de recorrido cerca del centro. Es un límite de la representación candidata de [situación](LABAN_SITUACION_RECORRIDO.md), no una validación de la coreútica ni una observación de Nico.

Ambas trayectorias avanzan y retroceden sobre el eje positivo X, empiezan a radio `0,2`, terminan a radio `1`, tienen largo total `1,6` y pueden ejecutarse a la misma rapidez constante durante el mismo tiempo. La trayectoria A repite cuatro excursiones entre `0,2` y `0,3` antes de salir a `1`; la B sale a `1` y repite cuatro excursiones entre `0,9` y `1`. En ambas, con origen cero y escala `R=1`, `Q=(1,0,0)`, `rho_min=0,2`, `rho_max=1` y `V_r=1`. Un control Beacon alimentado **sólo** por esos números daría la misma salida bajo el mismo estado e instrumento.

Para preguntar **qué parte del trayecto** ocurre a un radio dado, definimos un candidato de ocupación por longitud de arco:

```text
F_arc(a) = (1/L) ∫_trayectoria 1{||p(s)-o||/R ≤ a} ds.
```

El script calcula exactamente la fracción de cada **segmento finito** dentro de una esfera de radio `aR`, resolviendo sus intersecciones. Para `a=0,4` en este ejemplo, `F_arc=0,625` en A y `0,125` en B. El umbral `0,4` es una elección ilustrativa, **no** un corte Laban ni un valor para Nico. Conservar la curva `F_arc(a)` o cuantiles radiales predefinidos evita elegir un umbral después de escuchar el sonido o ver valoraciones; aun así faltan error, cobertura y pertinencia experta.

`F_arc` pondera por **distancia recorrida**, no por tiempo. Si interesa cuánto tiempo pasa la mano cerca del centro, se necesita otra distribución temporal, con duraciones y pausas observadas; las dos contestan preguntas distintas. `F_arc` también pierde orden: podría igualarse al permutar tramos. Las conclusiones del [control de duración](SITUACION_VENTANA_EXTREMOS.md) siguen vigentes, y el error de pose, origen, marco, profundidad, muestreo y oclusión puede mover los cruces de umbral. No transportar `F_arc` a HarMoCAP/Beacon como señal validada ni sumar otra banda por este ejemplo.

Para la lectura con especialistas, esta familia es una **alternativa de desarrollo** si el juicio sobre la situación de la frase completa no queda explicado por extremos y `V_r`. Elegir antes de los días reservados si se probará alguna estadística de ocupación, cuántos grados de libertad se permiten y contra qué referencia se evaluará. Una mejora elegida retrospectivamente entre muchos umbrales no sería prueba del aporte de una geometría labaniana.
