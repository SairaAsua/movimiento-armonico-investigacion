# Espejo, orientación y fase: un control necesario para rope flow

Nota técnica del 23-09-2026. El [contrato del kit HarMoCAP, commit `bdeebbf5`](https://github.com/Mar-IA-no/HarMoCAP/blob/bdeebbf5bef4f78d1dc6ff43feb8228e994feb49/harmocap-nico-kit/INTERFACE_SPEC.md) especifica coordenadas isotrópicas de imagen (`x_px/alto`, `y_px/alto`), origen arriba a la izquierda, `x` hacia la derecha, `y` hacia abajo y **entrada sin espejo**. Esto es una especificación del emisor auditado, no una prueba de que cualquier teléfono, vista previa, archivo exportado o futuro montaje cumpla esa condición. La [documentación oficial de OpenCV sobre `flip`](https://docs.opencv.org/4.10.0/d2/de8/group__core__array.html) confirma que un volteo horizontal es una operación real de imagen; [notas de geometría computacional de Stanford](https://graphics.stanford.edu/courses/cs268-16-fall/Notes/cmsc754-lects.pdf) describen que una reflexión cambia el signo de la orientación sin cambiar el área absoluta.

## Consecuencia matemática

Para puntos `q_i=(x_i,y_i)` de un ciclo cerrado en **coordenadas de imagen** (y crece hacia abajo), el área firmada de la trayectoria es

`A = 1/2 Σ_i (x_i y_{i+1} − x_{i+1} y_i)`.

Con esta convención, `A>0` indica una vuelta **visualmente horaria en pantalla**; si se convierte a coordenadas físicas con eje vertical hacia arriba, el signo se invierte. Un espejo horizontal del archivo, `x' = W−x` con `W=ancho/alto`, transforma `A' = −A`. Las distancias, longitudes, velocidades escalares y área absoluta permanecen iguales. Por eso un control basado sólo en suavidad, radio o proximidad a un poliedro puede pasar mientras el **sentido del recorrido** queda equivocado.

Si una fase angular proyectada se define como `θ=atan2(y−c_y,x−c_x)` y se refleja tanto punto como centro, entonces `θ' = π−θ` (módulo `2π`). La fase desenrollada invierte la dirección temporal. Para dos señales reflejadas de modo idéntico, la magnitud de sincronía circular 1:1 puede conservarse, pero el **desfase firmado cambia de signo**. Si además se intercambian etiquetas izquierda/derecha, la relación entre fases vuelve a transformarse; no es válido corregir únicamente el signo al final sin auditar etiquetas y anclajes de evento. Una fase no angular basada en eventos tiene otras convenciones: se debe comprobar cada estimador, no aplicar esta identidad mecánicamente a todos.

Para un recorrido realmente 3D, el producto triple `(u×v)·w` cambia de signo bajo una reflexión impropia, pero permanece bajo una rotación física. Un error de *handedness* en calibración puede así conservar longitudes y alterar quiralidad/orden orientado. La plantilla icosaédrica regular es simétrica; una distancia mínima a sus vértices sin orden ni sentido puede no denunciar el error. Esa es otra razón para conservar secuencia y referencias anatómicas observables.

El [script sintético](espejo_orientacion_sintetico.py) prueba las igualdades anteriores para un ciclo sencillo. Su resultado sólo valida estas identidades geométricas, **no** la orientación de una cámara real ni un resultado de Nico.

## Control de captura y análisis

1. En cada fuente guardar original, modelo, configuración de espejo/rotación, dimensión y transformación aplicada por software. Diferenciar la **vista previa** que ve el operador del archivo grabado que procesa el algoritmo.
2. Antes de grabar a Nico, captar una referencia asimétrica claramente rotulada `L/R` y un recorrido físico de sentido conocido visible en todas las vistas. Repetir con el mismo flujo de exportación y preprocesamiento que usaría HarMoCAP; verificar dónde queda `L`, qué mano etiqueta el estimador y qué signo produce `A`.
3. Fijar un marco corporal derecho y una convención explícita: por ejemplo, signos de giro referidos al sujeto y al eje vertical físico, no al espectador. Para cada transformación de cámara registrar matriz y determinante de su parte ortogonal; `det<0` exige reconocer reflexión, no llamarla rotación.
4. En multivista, resolver espejo/rotación antes de triangular y antes de calcular fase. Si una vista no pasa el control, excluirla del descriptor dependiente de sentido o corregir desde el original con transformación trazable. No elegir entre original y espejo según cuál ajusta mejor una escala de Laban.
5. En Beacon, enviar junto al descriptor el marco, convención de signo, versión y estado de validez. Si el sentido no está validado, no emitir una indicación sonora que sugiera giro «correcto»; una salida invariante al espejo podría seguir siendo explorable, pero no sustituye la validación espacial.

Esta comprobación pertenece al banco instrumental previo al estudio humano. Aún faltan inventario de cámaras y grabación técnica real, pero la regla y su prueba sintética pueden fijarse sin intervención de Saira.
