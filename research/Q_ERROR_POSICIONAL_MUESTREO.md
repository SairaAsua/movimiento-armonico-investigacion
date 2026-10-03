# Error de posición, muestreo y `Q`

**Resultado matemático de diseño de la [Issue #1](https://github.com/SairaAsua/movimiento-armonico-investigacion/issues/1), no fórmula de Laban ni medición de Nico.** Complementa la [cota de arco oculto](Q_COBERTURA_ARCO.md): allí un tramo falta; aquí todos los cuadros existen, pero sus posiciones tienen error. El descriptor `Q` es la distribución por longitud de componentes direccionales de una poligonal 3D, `Q_k=N_k/L`, con `N_k=Σ_i d_{ik}²/||d_i||` y `L=Σ_i||d_i||`. Los segmentos de longitud cero aportan cero a `N_k` y `L`. La posición, marco corporal y unidad deben estar fijados antes de aplicar la cuenta.

## Cota determinista

Sea `x_i` la posición real de cada punto de la **poligonal a los tiempos muestreados**, `x̂_i` su estimación, y `||x̂_i−x_i||≤σ_i` una cota física verificada. Para el segmento `d_i=x_{i+1}−x_i`, su error de desplazamiento satisface `||d̂_i−d_i||≤ε_i=σ_i+σ_{i+1}`. Definir `E=Σε_i`; es conservador porque comparte errores entre segmentos vecinos.

La función `f_k(d)=d_k²/||d||`, con `f_k(0)=0`, es globalmente Lipschitz con constante `2/√3`: para `u=d/||d||`, `||∇f_k||²=4u_k²−3u_k⁴≤4/3`. La desigualdad también cruza el origen por continuidad. Por tanto `|N̂_k−N_k|≤(2/√3)E` y `|L̂−L|≤E`. Si `L̂>E`,

`|Q_k−Q̂_k| ≤ min{1, [(2/√3)+Q̂_k] E/(L̂−E)}`.

La cota compara **dos poligonales con los mismos tiempos**; no limita el arco continuo entre cuadros. Un [contraejemplo y una cota separada por curvatura](Q_ARCO_ENTRE_CUADROS.md) cuantifican esa segunda diferencia bajo supuestos explícitos. Tampoco cubre error de orientación/escala del marco, identidad de mano equivocada, oclusión, proyección 2D, ni incertidumbre estadística: se necesitan presupuestos separados. Una desviación estándar de pose no es automáticamente una cota máxima `σ_i`. Si `L̂≤E`, esta prueba no certifica nada más estrecho que `Q_k∈[0,1]`. Para clasificar eje dominante, exigir que el límite inferior de un componente supere los superiores de los otros; si no, informar `indeterminado`. Los intervalos por componente son conservadores y sus extremos no ocurren necesariamente a la vez.

## Más cuadros pueden empeorar una trayectoria sin filtrar

El [contraejemplo ejecutable](q_error_posicional_muestreo.py) usa una mano real que recorre un metro recto sobre `x` durante un segundo. En `n+1` muestras, cada punto interior observado se desplaza alternativamente `+5` o `−5 mm` sobre `y`; los extremos observados coinciden con los verdaderos. Todos los errores posicionales son ≤5 mm, pero cada pequeño segmento interior añade hasta 10 mm de oscilación lateral. El `Q` verdadero de la poligonal es `(1,0,0)` en todos los muestreos; el `Q_y` observado sube al aumentar `n`. Es un patrón adverso construido, no un modelo estadístico de error de cámara ni un dato real de 30/120/240 FPS. Con ruido aleatorio correlacionado, filtros o errores menores, la conducta puede ser distinta.

Esto impide interpretar `Q` crudo como característica corporal sin medir error **dinámico** a la cadencia elegida. Un filtro puede atenuar zigzags y también borrar cambios rápidos legítimos; versión, ancho temporal, retardo y sensibilidad se fijan con desarrollo y se comprueban en sesiones reservadas. Para comparar dos intentos, usar igual regla de muestreo/filtro y reportar un análisis de sensibilidad a ambos. Beacon sólo debería recibir un `Q_live` con soporte temporal, cobertura, error de posición/marco y una cota informativa para la distinción sonora prometida. `Invalid` significa falta de identificación instrumental, nunca disonancia humana.
