# El ruido de orientación puede fabricar cobertura para `C`

Ensayo del 24 de septiembre de 2026, [script reproducible](cmu_umbral_marco_ventana.py), sobre la misma [toma pública CMU 05_02](CMU_DANZA_BANCO_REAL.md). Es una **simulación de error hipotético** en una persona bailando sin soga, no una estimación del error de las cámaras de Saira ni un resultado de Nico. Se verifica el SHA-256 del archivo antes de calcular. Se usa la escala causal de los primeros 120 cuadros (`303,532 mm`), la mano izquierda, `W=120` tramos a 120 Hz y el gate exploratorio `arco ≥ 0,5 L` y `≥2` tramos **en ambas** regiones.

La primera emisión válida del [replay causal](ACOPLE_CAUSAL_REPLAY.md) ocurre en el cuadro 529: `C=+2,964053 L/s`; el arco delantero es `0,518119 L`, apenas `0,018119 L` sobre el umbral. El cuadro 528 precedente es inválido. Tras construir el vector de muñeca relativo al torso se rota cada cuadro con Rodrigues, simulando error sólo en la **orientación** del marco. Se recalculan regiones, tramos y rapidez; no se alteran los puntos de muñeca/cintura en sala. Las 1.000 réplicas por condición usan semilla `20260924` y error angular vectorial RMS nominal `σ` con componentes `N(0,σ²/3)`. Se comparan errores independientes por cuadro, AR(1) con `ρ=0,95` por cuadro y un sesgo constante por ventana. Los percentiles siguientes son entre perturbaciones de **este caso**, no intervalos poblacionales.

| Estructura | RMS hipotético | Cuadro 528 pasa el gate | Cuadro 529 pasa el gate | `C` 529 p5 / med / p95 **entre válidos**, L/s |
|---|---:|---:|---:|---:|
| Independiente | 0,25° | 0,1 % | 98,2 % | +2,767 / +3,089 / +3,424 |
| Independiente | 0,5° | 10,1 % | 95,8 % | +2,689 / +3,421 / +4,290 |
| Independiente | 1° | 72,3 % | 98,9 % | +2,470 / +4,335 / +6,620 |
| Correlación `ρ=0,95` | 1° | 25,7 % | 91,8 % | +2,566 / +3,095 / +3,708 |
| Sesgo constante | 1° | 26,4 % | 98,4 % | +2,964 / +2,964 / +3,011 |

El hallazgo más incómodo es que **más ruido puede aumentar la cobertura aparente**: con 1° independiente, un cuadro que nominalmente no alcanzaba el recorrido mínimo pasa el gate en 72,3 % de las simulaciones, porque el jitter añade longitud al recorrido. El cuadro 529 sigue siendo mayormente válido, pero la mediana condicional de `C` pasa de `+2,964` a `+4,335 L/s`. Por tanto una tasa alta de «válidos» no acredita exactitud: la cobertura y el sesgo de valor deben evaluarse juntos. Los resultados dependen de este segmento, de la posición respecto del plano delante/detrás y de la estructura temporal del error; no son tolerancias universales para rope flow.

Para el [piloto instrumental](PILOTO_VALIDACION_VIDEO.md), medir en el montaje real jitter cuadro a cuadro, error correlacionado, orientación durante giro, error de punto y relojes con una referencia adecuada. Propagar los errores observados a **ambos** resultados: (a) probabilidad o rango de cruzar el gate y (b) rango de `C` condicionado a pasar. Congelar la regla de calidad en desarrollo antes de valorar estética, HIT o experiencia. Para Beacon, una transición `invalid → estimated_valid` inducida por ruido de orientación no debe disparar una nota que se interprete como mejora del movimiento. La política de sonido/reset sigue pendiente de prueba real ([contrato](CONTRATO_C_LIVE_V0.md), [estados](BEACON_TRANSICIONES_Y_RESET.md)).
