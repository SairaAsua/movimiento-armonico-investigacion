# Brecha reproducida entre el contrato OSC y el receptor de referencia

Registro de auditoría instrumental, 23 de septiembre de 2026. Fuente congelada: [`Mar-IA-no/HarMoCAP` en `bdeebbf5bef4f78d1dc6ff43feb8228e994feb49`](https://github.com/Mar-IA-no/HarMoCAP/tree/bdeebbf5bef4f78d1dc6ff43feb8228e994feb49), verificado como `main` ese día. **No es una prueba del receptor Beacon real**, que no está instalado aquí. Sólo se ejecutaron el codec, replay y [receptor de referencia](https://github.com/Mar-IA-no/HarMoCAP/blob/bdeebbf5bef4f78d1dc6ff43feb8228e994feb49/harmocap-nico-kit/osc_receiver_example.py) con [fixtures sintéticos públicos](https://github.com/Mar-IA-no/HarMoCAP/tree/bdeebbf5bef4f78d1dc6ff43feb8228e994feb49/harmocap-nico-kit/examples/fixtures), dentro del proceso Python, sin cámara, socket, servicio ni audio.

## Regla escrita y dato que realmente viaja

La [especificación de interfaz, sección «Reglas que tu receptor DEBE implementar»](https://github.com/Mar-IA-no/HarMoCAP/blob/bdeebbf5bef4f78d1dc6ff43feb8228e994feb49/docs/INTERFACE_SPEC.md) exige no consumir cuadros hasta que `/hello` y `/calibration` coincidan con la identidad de contrato/calibración del cuadro. El [`/meta` codificado por `build_person_bundle`](https://github.com/Mar-IA-no/HarMoCAP/blob/bdeebbf5bef4f78d1dc6ff43feb8228e994feb49/src/harmocap/interface/osc_codec.py) sí lleva `contract_id` y `calibration_generation` junto a `stream_id`, `captured_frame_id` y `bundle_seq`; **no lleva `calibration_hash`**. Por tanto, la comprobación implementable es: contrato local conocido = contrato del `/hello` = contrato del `/meta`; generación del `/meta` = generación de `/hello` y `/calibration`; hash de `/hello` = hash comprobado de `/calibration`. La frase «hash coincide con el frame» en la especificación no puede verificarse literalmente con el wire 1.4 y debería precisarse al implementar un receptor.

## Reproducción mínima

El [script de regresión](probar_gating_harmocap.py) toma la fixture `calibration.jsonl`: envía handshake de generación 1, cuadro 1 válido, cuadro 92 de generación 2 **sin nuevo handshake**, cuadro 93 con `contract_id=000…` y, finalmente, handshake de generación 2 más cuadro 94 válido. Ejecutado así:

```text
python probar_gating_harmocap.py /tmp/harmocap-replay-audit/harmocap-nico-kit
expected_applied_frame_ids [1, 94]
observed_applied_frame_ids [1, 92, 93, 94]
reference_receiver_stats {'bundles': 8, 'dropped_old': 0, 'gated': 0, 'stream_resets': 1, 'lost': 0}
FAIL: el receptor aplicó frames sin handshake del frame coincidente
```

El proceso salió con código **1**, intencionalmente: la regresión exige el comportamiento de la especificación y el receptor actual no lo cumple. [`ContractReceiver._gated()`](https://github.com/Mar-IA-no/HarMoCAP/blob/bdeebbf5bef4f78d1dc6ff43feb8228e994feb49/harmocap-nico-kit/osc_receiver_example.py) sólo compara la generación y el hash que llegaron en `/hello` y `/calibration`; [`_on_frame()`](https://github.com/Mar-IA-no/HarMoCAP/blob/bdeebbf5bef4f78d1dc6ff43feb8228e994feb49/harmocap-nico-kit/osc_receiver_example.py) no compara `meta[5]`/`meta[6]` con ese estado antes de llamar a `on_movement()`. La prueba anterior pasó el self-test oficial del kit porque éste comprueba codec/UDP básico y no ese cambio adverso de identidad de cuadro. No se afirma que el productor normal emita `contract_id` falso; el riesgo también existe con cuadros atrasados o reordenados durante cambio de calibración.

## Implicación y criterio para Beacon

Una sonificación que aplique un cuadro bajo calibración obsoleta puede convertir un cambio de escala o de contrato en un cambio audible atribuido erróneamente al cuerpo. Para el futuro receptor Beacon, **cada bundle de persona** debe quedar bloqueado si su contrato o generación no corresponden al handshake aceptado, además de las reglas de secuencia y stream. Si el `contract_id` de `/hello` tampoco corresponde al manifiesto local aceptado, no aceptar el stream aunque `/hello` y `/calibration` sean internamente coherentes. El paquete `/crowd` no lleva `contract_id` propio, así que su gating depende del estado de handshake y de stream; no hay una comprobación por cuadro equivalente para crowd en 1.4.

Un parche reviewable en HarMoCAP debería añadir las comparaciones de `/meta`, especificar el rol del hash en el wire y ampliar las pruebas con transición de generación, contrato ajeno, paquete viejo, cambio de stream y entrega posterior al handshake correcto. El [script rojo](probar_gating_harmocap.py) puede servir como aceptación; su prueba verde requeriría ejecutar el receptor modificado. **No se modificó ni publicó el repositorio HarMoCAP**: el trabajo de este programa es documentar la integración futura, y el repositorio externo exige plan y aprobación del usuario antes de cambios significativos. El hallazgo no valida ni invalida las variables Laban/HIT; limita la fidelidad del transporte que debería llevarlas.
