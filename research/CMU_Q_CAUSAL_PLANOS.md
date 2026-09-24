# `Q_live`: recorrido suficiente y pérdida de planitud local

Replay del 24-09-2026 con el [script reproducible](cmu_q_live_replay.py) y el [C3D público de CMU 05_02 ya auditado](CMU_DANZA_BANCO_REAL.md). Es danza **sin soga**, no Nico ni una sesión de Beacon. Usa dos puntos de muñeca promediados por lado, cintura como origen, ejes corporales estimados por cuadro y escala de hombros fijada en los primeros 120 cuadros. El reloj `cuadro/120 Hz` es **nominal del archivo**, no tiempo óptico físico ni latencia hasta audio.

Por cada tramo de llegada ya recibido se guarda desplazamiento `d` en el marco corporal co-rotante, arco `||d||` y `d dᵀ/||d||`. Para la ventana retrospectiva, `M=Σ(d dᵀ/||d||)/Σ||d||`, `Q=diag(M)` en orden lateral/superior/anterior, con `ΣQ=1`. `M` tiene traza 1 y autovalores no negativos; su autovalor intermedio indica extensión en una segunda dirección, mientras el menor indica movimiento fuera de un plano local. **No** se usa esa observación para bautizar una categoría Laban: un plano requiere error 3D medido, extensión bidireccional suficiente y una normal estable. El gate de `≥0,5` longitudes de hombro y `≥2` tramos es sólo exploratorio.

| Mano | Ventana | Emisiones con arco suficiente / 1003 | Media `Q` lateral/superior/anterior | Mediana λ menor / intermedio |
|---|---:|---:|---:|---:|
| Izquierda | 0,5 s | 737 | 0,347 / 0,252 / 0,402 | 0,028 / 0,242 |
| Izquierda | 1,0 s | 875 | 0,295 / 0,250 / 0,455 | 0,062 / 0,284 |
| Izquierda | 2,0 s | 886 | 0,283 / 0,223 / 0,494 | 0,101 / 0,296 |
| Derecha | 0,5 s | 820 | 0,297 / 0,360 / 0,343 | 0,031 / 0,190 |
| Derecha | 1,0 s | 938 | 0,301 / 0,337 / 0,363 | 0,068 / 0,225 |
| Derecha | 2,0 s | 938 | 0,293 / 0,334 / 0,373 | 0,129 / 0,261 |

Con ventanas más largas se supera el gate de recorrido en más cuadros, pero el menor autovalor mediano también aumenta: la ventana puede mezclar tramos que ya no pertenecen a **un** plano local. Las medias `Q` cambian además con la ventana. No hay una duración que este banco permita elegir para Nico por sí solo. La elección deberá combinar cobertura, error de orientación, duración real de las figuras, estabilidad de la normal y retardo admisible para Beacon; predefinirla en desarrollo, antes de resultados estéticos.

El replay compara cada emisión incremental con un cálculo por lote sobre **los mismos tramos pasados** y comprueba que truncar el archivo futuro no cambia emisiones anteriores. Esto verifica causalidad algorítmica del estimador dado el C3D, no causalidad fisiológica ni disponibilidad real de una pose 3D a ese instante. Una caída de cobertura se trata como `invalid`, nunca como `Q=(0,0,0)` ni como disonancia del cuerpo. Si un futuro canal dice «plano», tendrá que transportar aparte normal, λ, incertidumbre, calidad temporal y estado; `Q` por sí solo expresa distribución de componentes respecto de ejes, no dirección con signo, orden de escala ni fase HIT ([diccionario](DICCIONARIO_SENALES_V0.md), [mapeo de ingeniería](INTEGRACION_HARMOCAP_BEACON.md)).

Ejecutar: `uv run --no-project --with numpy --with ezc3d python docs/beacon-contexto-local/ropeflow-consonancia/cmu_q_live_replay.py`.
