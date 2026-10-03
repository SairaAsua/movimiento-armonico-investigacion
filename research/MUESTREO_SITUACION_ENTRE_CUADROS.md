# Una mano puede pasar por el centro entre dos cuadros

La medida `rho_min` de [situación del recorrido](LABAN_SITUACION_RECORRIDO.md) es el mínimo de la **polilínea que une muestras válidas**. No es automáticamente el mínimo del movimiento corporal continuo. La [cota de error posicional](PRESUPUESTO_ERROR_SITUACION.md) anterior comparaba dos polilíneas con **los mismos tiempos y segmentos**; por sí sola no cubre una excursión no muestreada. El [contraejemplo reproducible](situacion_entre_cuadros_sintetico.py) separa esas preguntas sin usar movimiento humano.

Dos gestos matemáticos contienen los mismos cuadros extremos durante `h=1 s`: `q₀=(0,5;0;0)` y `q₁=(0,5;0,1;0)`, con origen `(0;0;0)` y escala `R=1`. En uno, el punto sigue la recta entre ellos; en el otro va primero al origen y después a `q₁`, con rapidez constante `1,009902` unidades/s y llegada al origen en `0,495098 s`. Los **cuadros observados son idénticos**, pero:

| Recorrido ideal | `rho_min` | `V_r` |
|---|---:|---:|
| Cuerda entre los dos cuadros | `0,5` | `0,099020` |
| Excursión oculta por el origen | `0` | `1` |

El reloj y las posiciones de ambos cuadros pueden ser perfectos y seguir sin identificar qué ocurrió entre ellos. Un caso radial con los dos extremos iguales muestra que el error de mínimo puede alcanzar exactamente la cota derivada abajo: la mano parece quedarse a radio `0,5`, pero va al origen y vuelve a rapidez máxima `1` unidad/s.

## Cota condicional para mínimos y máximos

Sea `q(t)` la **posición relativa mano–origen en el marco declarado**, con cota de rapidez en el sentido `‖q(t)−q(s)‖≤v_max|t−s|` para **todos** los instantes entre muestras; esto admite cambios bruscos de dirección sin exigir derivada en la esquina. En un intervalo de duración `h`, su cuerda lineal es `ℓ(t)=(1−u)q(0)+u q(h)`, `u=t/h`. Como `‖q(t)−q(0)‖≤v_max t` y `‖q(t)−q(h)‖≤v_max(h−t)`, por combinación convexa:

```text
‖q(t)−ℓ(t)‖ ≤ 2 v_max h u(1−u) ≤ v_max h/2.
```

Si `h_max` es el **mayor hueco real de PTS** en una frase completa, el mínimo y el máximo radiales continuos difieren de los de la polilínea de muestras verdaderas como máximo `v_max h_max/2`. Si además cada posición relativa medida tiene una cota dura simultánea `δ` en los tiempos muestreados, la distancia entre curva física y polilínea **medida** queda acotada por `E=δ+v_max h_max/2`. Con escala estimada `R̂` y error duro `ε_R<R̂`, el intervalo del [presupuesto de escala](PRESUPUESTO_ERROR_SITUACION.md) se aplica sustituyendo `δ` por `E` para `rho_min/rho_max`. El script comprueba la desigualdad en 500 curvas a trozos aleatorias y en el caso radial que alcanza la cota. Es una **garantía condicional matemática**, no una velocidad máxima de Nico.

Un valor observado de rapidez entre cuadros, `‖q₁−q₀‖/h`, es sólo un **límite inferior** de la máxima rapidez que pudo ocurrir entre ellos. No se debe ponerlo en `v_max`: el ejemplo oculto tiene dos cuadros con desplazamiento pequeño y una excursión veloz. Hacen falta una restricción física justificada de la tarea o una referencia dinámica más rápida, validada para el dominio de giros/transiciones; un percentil de desarrollo no es una cota dura universal. `h_max` proviene de tiempos de captura suficientemente confiables, no sólo de FPS nominal. Si se pierden muestras, falla la identidad o el origen/marco cambia sin control, esta fórmula no repara esos fallos.

## Lo que la cota no salva

Un límite de distancia entre curva y cuerda **no** determina longitud de trayectoria, orden de excursiones ni variación radial total. Las dos curvas anteriores tienen extremos y duración idénticos, pero `V_r=0,099020` y `1`. Por eso la nueva cota puede rescatar una afirmación acotada sobre `rho_min/rho_max` **si** `v_max` existe; no convierte `V_r`, `Q` o la fase HIT entre cuadros en magnitudes continuas certificadas. Esas señales exigen error de muestreo y tarea evaluados por separado frente a referencia.

Para el banco instrumental de Saira, registrar PTS y máximo hueco por frase, velocidad relativa de mano–origen frente a referencia dinámica y cobertura de giros/oclusiones. Probar explícitamente patrones en los que la mano cruza el centro entre cuadros. Si no hay `v_max` defendible, informar `rho_min` **de la polilínea muestreada** con esa etiqueta precisa y no atribuirle el mínimo continuo del gesto. Ningún resultado aquí indica belleza, eficiencia o consonancia.
