# Control diagnóstico Laban–HIT frente al contrato de Beacon

Prueba **numérica offline**, 24 de septiembre de 2026, [script](beacon_factorial_controles.py). Usa una [copia fijada](sources/beacon_spatial.contract.de2768c3.json) del [contrato público de `beacon-spatial` en `de2768c3`](https://github.com/AlterMundi/beacon-spatial/blob/de2768c3a4f07cc0d744c89bf6e63b168e5f2b61/beacon_spatial.contract.json), SHA-256 `84383e254cd19f520eb5e19c7d6dedb0af93c95ad8b226aeb4c7694bde936dbb`. No arranca HarMoCAP, Weaver, OSC, SuperCollider ni audio. El contrato admite `/beacon/gain/{N}`, `N=1…13`, ganancia `0…3` y lag declarado de 50 ms. Son **ganancias de filtros**, no frecuencias corporales ([auditoría DSP](BEACON_BANDAS_NO_FRECUENCIAS_CORPORALES.md)).

Se toman los cuatro casos del [control factorial sintético](LABAN_HIT_FACTORIAL.md): `Q` es un descriptor espacial de trayectoria; `R₁:₁` resume fase relativa a lo largo de **ocho segundos completos**. Por construcción ambos son **resultados retrospectivos**; el vector siguiente podría aplicarse en un replay después del bloque, pero **no** era conocido en vivo al inicio. Una versión live necesitaría Q/R causales, ventana, error, disponibilidad y vencimiento propios ([fase causal](FASE_CAUSAL_BEACON.md)).

El mapeo diagnóstico propuesto, arbitrario pero verificable, usa dos componentes independientes de `Q` (la lateral se deduce porque `ΣQ=1`) y un control separado de `R`:

```text
ganancia banda 4 = 0,2 + 0,8 · Q_anterior
ganancia banda 5 = 0,2 + 0,8 · Q_vertical
ganancia banda 6 = 0,2 + 0,8 · R₁:₁
```

| Plano y timing | `/beacon/gain/4` | `/beacon/gain/5` | `/beacon/gain/6` |
|---|---:|---:|---:|
| Lateral–anterior, fase trabada | 0,600 | 0,200 | 1,000 |
| Lateral–anterior, fase modulada | 0,600 | 0,200 | 0,578 |
| Lateral–vertical, fase trabada | 0,200 | 0,600 | 1,000 |
| Lateral–vertical, fase modulada | 0,200 | 0,600 | 0,578 |

El script comprueba el hash del contrato, sus rangos, cuatro vectores distintos y que cambiar sólo el plano afecta sólo bandas 4/5, mientras cambiar sólo la fase afecta sólo banda 6. En el fixture, **Q inválido resetea bandas 4/5**, **R inválido resetea banda 6** y la pérdida común resetea las tres; una capa sólo puede seguir sonando si su propia procedencia y vigencia siguen válidas. El `0` es una instrucción de silencio para el instrumento, **no** «movimiento disonante». La política exacta de reset y el default deben comprobarse en Weaver y en el instrumento ([hallazgo de `suppress`/`reset`](BEACON_TRANSICIONES_Y_RESET.md)).

La salida numérica es inyectiva **sólo para estos cuatro casos**. No prueba que el audio difiera ni que una persona oiga el plano o la fase: bandas 4–6 están centradas en 160, 200 y 240 Hz, su entrada puede no tener energía allí, los filtros se solapan y el lag modifica el resultado. Para cerrar el gate, fijar una entrada acústica con energía conocida, rutear los cuatro vectores por la cadena real, registrar controles **aplicados** y audio grabado, igualar duración/nivel y probar pares adversos a ciegas. Repetir con dato inválido y verificar silencio o default después de la latencia medida. Esta prueba prepara esa comparación sin presentarla como validación de Laban, HIT, belleza o experiencia.
