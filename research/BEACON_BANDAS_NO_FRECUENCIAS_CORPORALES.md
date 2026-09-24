# Qué significa 40/80/120 Hz en el motor `beacon-spatial`

Lectura de [SuperCollider `beacon.scd`, commit `de2768c3`](https://github.com/AlterMundi/beacon-spatial/blob/de2768c3a4f07cc0d744c89bf6e63b168e5f2b61/beacon.scd) y del [contrato del instrumento](https://github.com/AlterMundi/beacon-spatial/blob/de2768c3a4f07cc0d744c89bf6e63b168e5f2b61/beacon_spatial.contract.json), 23-09-2026. Es una lectura de código, **no una medición de audio** ni de Nico. El motor auditado puede cambiar; toda prueba futura debe fijar commit/configuración y capturar la salida real.

## Topología que implementa el código

`beacon.scd` toma una **señal de audio de entrada** —archivo en bucle o entrada en vivo según configuración— y la divide en doce filtros pasabanda (`BPF`) más un filtro pasaaltos (`HPF`). Las bandas 1–6 tienen centros `[40,80,120,160,200,240] Hz` y anchos nominales de 40 Hz. Las bandas 7–12 tienen centros `[480,720,960,1200,1440,1680] Hz` y anchos nominales de 240 Hz. La banda 13 es `HPF` con corte de 1800 Hz. Cada banda tiene ganancia; las bandas pasabanda además exponen `rq` (ancho/centro, aunque la dirección OSC se llama `/beacon/q/N`). Azimut, distancia, mezcla wet/dry y master son controles distintos. La rama wet espacializa con `FoaPanB` y decodifica binauralmente; la rama dry suma bandas filtradas. El código aplica `lag(0.05)` a ganancia de banda y azimut.

Por tanto, 40/80/120 Hz son **frecuencias centrales de filtros** en este motor, no oscilaciones medidas de pelvis/pecho/hombros ni necesariamente componentes presentes como tonos puros. Si la entrada carece de energía en una banda, elevar su ganancia no crea automáticamente un armónico sinusoidal de esa frecuencia. El resultado acústico depende de la entrada, del ancho/rq, ganancias, solo, espacialización, mezcla y master. Las bandas pueden solaparse espectralmente; no se debe leer cada una como un canal fisiológico independiente por el mero número armónico.

La [prueba offline de Weaver](WEAVER_BEACON_CONTRATO_OFFLINE.md) registró `/beacon/gain/4 = 0,488...`. En este motor, esa dirección controla la **ganancia de la banda centrada en 160 Hz**; no «pone el movimiento a 160 Hz» ni cambia la frecuencia central. Tampoco verificó un cambio audible, pues sólo registró una intención de control. Para afirmar qué oyó alguien, se necesita el audio de entrada y salida junto al log de controles realmente aplicados y un análisis acústico de la grabación.

## Traducción para el experimento

| Magnitud | Unidad/fuente | Afirmación permitida |
|---|---|---|
| Ciclo de rope flow | Hz o ciclos/min, evento visible y tiempo | Cadencia de tarea; usualmente muy inferior a los centros audibles. |
| Relación de fase mano–soga | radianes/ciclos válidos | Organización temporal de señales medidas, con error y procedencia. |
| Centro de filtro de Beacon | Hz, configuración de `beacon.scd` | Propiedad del sintetizador/filtrado, elegida por diseño. |
| Ganancia `/beacon/gain/N` | factor adimensional, control OSC | Cuánto pesa una banda filtrada en el motor; no energía corporal. |
| Frecuencias de salida | Espectro de audio **grabado**, condicionado por entrada y controles | Resultado acústico medido, que no prueba por sí solo una variable fisiológica. |

Para un primer ensayo de sonificación se puede escoger una ruta de un descriptor cinemático validado a ganancia/azimut con reglas de calidad; describirla como **traducción auditiva**. Si la hipótesis exige que proporciones HIT 1:2:3 produzcan una consonancia audible específica, habrá que declarar una regla generativa o de filtrado, el audio de entrada, la respuesta real del motor y un contraste acústico/perceptual. El hecho de que tres centros de filtro estén en proporción 1:2:3 no demuestra que el gesto corporal lo esté ni que la salida resultante sea percibida como consonante.
