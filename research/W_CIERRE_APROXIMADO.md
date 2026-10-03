# Cierre aproximado de una vuelta: qué `W` puede significar

**Control de identificabilidad espacial, 3 de octubre de 2026.** El [giro firmado `W`](Q_CRUCES_ORDEN.md) sólo está definido para una curva o poligonal puntual 2D cerrada, con vista y sentido fijados. En rope flow, un detector de **ciclo de tarea** puede marcar una vuelta aunque la mano proyectada termine cerca, pero no exactamente en, su posición inicial. Un umbral de distancia entre extremos no crea por sí solo la trayectoria faltante. Esta nota y su [banco ejecutable](w_cierre_aproximado_sintetico.py) separan esas decisiones.

## Mismo prefijo abierto, tres cierres

El banco observa exactamente el mismo prefijo `(0,0)→(1,0)→(1,1)→(0,1)→(0;0,05)`. El último punto dista `0,05` del inicio, dentro de una tolerancia **inventada** de `0,1`. Hay tres terminaciones no observadas que permanecen por completo dentro del disco de esa tolerancia:

| Terminación hipotética | Qué añade | `W` de la poligonal completa |
|---|---|---:|
| Cuerda recta al origen | Segmento de longitud `0,05` | `1` |
| Pequeño lazo a un lado y luego al origen | Giro adicional positivo | `2` |
| Lazo reflejado al otro lado y luego al origen | Giro adicional negativo | `0` |

El prefijo y la distancia entre extremos son idénticos. El lazo de lado `a` añade sólo `4a` de longitud a la cuerda recta y conserva esa diferencia de `W` para cualquier `a>0` de la construcción que quepa en el disco. Así, **cualquier margen positivo** de recorrido permitido por una cota de rapidez sobre el mínimo recto deja espacio matemático para un lazo suficientemente pequeño. Cuando `a` cae por debajo del error de posición o de la resolución temporal, la distinción tampoco puede certificarse con esos datos. El fixture incluye un lazo con lado `0,00005`: el largo adicional es `0,0002` en unidades artificiales y sigue dando `W=2`.

Esto no dice que Nico haga lazos invisibles. Demuestra que ni «los extremos casi coinciden» ni una cota de rapidez con holgura identifican el **giro del trayecto continuo** sin una premisa adicional sobre escala, curvatura, velocidad angular o una referencia de mayor resolución. La [prueba de lazo oculto entre cuadros](CRUCE_TRAYECTORIA_INCERTIDUMBRE.md) presenta la misma frontera para autocruces. La cota de error de `W` en [polígonos ya cerrados](Q_CRUCES_ORDEN.md) certifica otra cosa: estabilidad bajo perturbaciones de **vértices observados** de una poligonal cuyo cierre ya se fijó. No certifica el segmento artificial ni la trayectoria intermedia.

## Decisión de medición para el piloto

Registrar **por separado** el evento de ciclo de tarea, la distancia de los extremos proyectados, su error, el intervalo temporal sin observación y la política de cierre. Hay tres productos posibles y no se renombran entre sí:

1. `W_observed_closed_polygon`: únicamente cuando los puntos muestreados forman un cierre observado conforme a una regla congelada, con error/identidad/cobertura y vista. Sigue siendo `W` de la **poligonal muestreada**, no del movimiento continuo.
2. `W_straight_closure_convention`: si se agrega una cuerda sintética entre extremos observados de una vuelta de tarea, conservar longitud de esa cuerda y la marca `closure_edge_unobserved=true`. Es una propiedad de **esa convención algorítmica**, no un cierre observado.
3. `unknown_continuous_W`: cuando la pregunta sea el giro del recorrido físico completo y no pueda excluirse un tramo faltante que cambie `W`, no sustituirlo por uno de los valores anteriores. Reportar cobertura sobre **todos** los ciclos intentados, incluso los no cerrables.

El nombre `W_observed_closed_polygon` no exige que una mano humana vuelva a la misma coordenada real: señala que el cierre **del objeto discreto declarado** proviene de muestras y de una regla reproducible. En datos ruidosos, decidir si dos extremos estiman la misma posición física exige su propio margen de error y un evento de tarea independiente; no basta redondearlos hasta igualarlos. Si se prefiere cerrar siempre por cuerda recta, publicar análisis de sensibilidad al umbral y al intervalo del cierre y evitar cualquier afirmación topológica sobre la soga 3D. Para la [comparación Laban–HIT](VALIDACION_SITUACION_LABAN_HIT.md), sólo un descriptor con significado y cobertura medidos entra en sesiones reservadas; el cierre no se elige por el valor de `W` ni por la valoración estética.

**Implicación para Beacon:** un `W` de ciclo artificialmente cerrado sería retrospectivo y llevaría `closure_policy`, `view_id`, `feature_window_end_us`, `available_at_us`, incertidumbre y estado. No se sonifica como señal de giro físico en tiempo real; el [giro local causal](W_GIRO_TIEMPO_BEACON.md) tiene otra definición y otros gates. La implementación de audio sigue pendiente bajo la [issue #13](https://github.com/SairaAsua/movimiento-armonico-investigacion/issues/13).

**Reproducción:** `python research/w_cierre_aproximado_sintetico.py`. Dos ejecuciones dieron JSON idéntico, SHA-256 `324ae4b719286c33ef473b35fb40f2d6cc26ff8aa6787616b3836da6c262e423`. Son puntos y tolerancias inventados, sin videos ni cámaras.
