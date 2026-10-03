# Un mínimo radial depende también de cuánto dura la frase

`rho_min` y `rho_max` de [situación del recorrido](LABAN_SITUACION_RECORRIDO.md) son **extremos sobre una ventana**. Su valor cambia al extender la ventana, aun si no cambia la regla que genera los movimientos. Esta nota metodológica de la [issue #4](https://github.com/SairaAsua/movimiento-armonico-investigacion/issues/4) fija el comparador antes de usar clips de Nico; no contiene datos humanos ni una corrección estadística ya calibrada.

Para una misma curva observada que sólo se prolonga con segmentos válidos, el conjunto recorrido anterior está incluido en el nuevo: el mínimo radial de la polilínea no puede aumentar y el máximo no puede disminuir. Una diferencia entre frases de longitud desigual puede reflejar **más oportunidades de alcanzar un extremo**, en vez de una organización espacial distinta. Cambiar además el muestreo, el origen o el marco es otro problema: la [prueba de decimación CMU](LABAN_SITUACION_RECORRIDO.md) muestra que una cuerda nueva incluso puede bajar el mínimo al descartar cuadros.

Un nulo matemático ayuda a ver la magnitud posible, **sin modelar rope flow**. Si `n` radios independientes tienen la misma distribución acumulada `F(r)`, entonces:

```text
P(min(r₁,…,rₙ) ≤ a) = 1 − [1 − F(a)]ⁿ.
```

Si además cada radio es uniforme entre 0 y 1, `E[min]=1/(n+1)`: con 5 observaciones es `0,1667` y con 20 es `0,0476`; para `a=0,1`, la probabilidad de ver al menos un radio ≤ `0,1` pasa de `0,4095` a `0,8784`. La independencia y la distribución uniforme son **sólo un ejemplo**. Cuadros contiguos y ciclos del mismo cuerpo están correlacionados; `n` de cuadros no se debe insertar en esta fórmula como si fueran réplicas independientes. `rho_min` real es el mínimo de **segmentos finitos**, no sólo de radios muestreados, pero conserva la dependencia de la ventana.

## Regla para desarrollo y evaluación

1. Definir comienzo y fin de la frase por eventos de tarea observables, no por el tramo que parece más bello o central. Registrar número de ciclos completos, duración real, PTS, huecos, cobertura, patrón y motivo de cada corte.
2. Para el contraste principal de situación, usar ventanas comparables del **mismo patrón y número predefinido de ciclos** cuando el repertorio lo permita. Comparar `M₀/M₁a/M₁b` en exactamente las mismas frases. Duración, rapidez, cantidad de ciclos y calidad son controles explícitos, no sustitutos de ventanas equivalentes.
3. Como sensibilidad, informar `rho_min` y `rho_max` **por ciclo válido** y su distribución dentro de la frase, además del extremo de frase completa. Los ciclos de una frase y un día siguen siendo dependientes; resumir y reservar por día. Si una condición sólo tiene frases largas y otra cortas, la diferencia de extremos de frase no identifica situación sin supuestos adicionales.
4. Elegir regla de segmentación, mínimo de ciclos, manejo de transiciones e invalidez en desarrollo. En evaluación reservada no recortar hasta encontrar un extremo favorable. Informar todos los intentos y la tasa de ventanas codificables según [cobertura](COBERTURA_SELECCION_VIDEO.md).

Este control no normaliza automáticamente `V_r`: es una razón de variación radial a longitud y puede cambiar si se añade un tipo de ciclo distinto o una transición. Tampoco resuelve profundidad 3D, error posicional o excursiones [entre cuadros](MUESTREO_SITUACION_ENTRE_CUADROS.md). El objetivo es que una eventual diferencia entre condiciones tenga una **unidad temporal y geométrica comparable** antes de conectarla con HIT o hacerla audible.
