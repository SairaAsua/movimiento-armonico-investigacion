# Sensibilidad del contraste `C` a error temporal del marco corporal

Fecha: 24 de septiembre de 2026. El [cambio de signo según marco](CMU_MARCOS_C_CONTRASTE.md) motivó probar una causa instrumental posible. Este ensayo usa los 1.123 cuadros de la [toma CMU 05_02](CMU_DANZA_BANCO_REAL.md), verificada por SHA-256 al cargarla, y el [script reproducible](cmu_orientacion_sensibilidad.py). Es **Monte Carlo hipotético**, no una medición de error de las cámaras disponibles, ni un cálculo de belleza o eficiencia.

## Intervención simulada

Se conservan las posiciones observadas de muñeca y cintura y la escala causal del [replay](ACOPLE_CAUSAL_REPLAY.md), fijada con el primer segundo (303,532 mm). Tras obtener el vector de muñeca en ejes corporales, se le aplica una rotación pequeña aleatoria distinta para cada cuadro: esto equivale a perturbar la orientación estimada del torso mientras la posición relativa en sala se mantiene. La rotación se aplica con Rodrigues, no como suma lineal de coordenadas. El desvío RMS del **vector angular** se fija en 0,25°, 0,5°, 1° o 2°; cada componente normal tiene desvío `σ/√3`. Se comparan tres estructuras temporales del error: independiente por cuadro, autoregresiva con `ρ=0,95`, y sesgo angular constante en toda la toma. Son 200 réplicas por condición, semilla `20260924`; se recalculan tanto rapidez como pertenencia delante/detrás. El baseline con esta escala es `C_izq=+2,241`, `C_der=+2,762 L/s`, ligeramente distinto del análisis con escala mediana de la toma completa.

| Error RMS | Estructura | `C` izquierda p5 / med / p95, L/s | `C` derecha p5 / med / p95, L/s | Signo derecho opuesto |
|---:|---|---:|---:|---:|
| 0,5° | Independiente | +2,505 / +2,647 / +2,787 | +2,604 / +2,704 / +2,809 | 0/200 |
| 0,5° | `ρ=0,95` | +2,270 / +2,311 / +2,361 | +2,766 / +2,795 / +2,825 | 0/200 |
| 1,0° | Independiente | +2,689 / +3,079 / +3,451 | +1,720 / +2,017 / +2,347 | 0/200 |
| 1,0° | `ρ=0,95` | +2,353 / +2,427 / +2,507 | +2,779 / +2,840 / +2,894 | 0/200 |
| 2,0° | Independiente | +3,400 / +4,339 / +5,245 | −0,005 / +0,802 / +1,490 | 10/200 |
| 2,0° | `ρ=0,95` | +2,478 / +2,625 / +2,750 | +2,646 / +2,773 / +2,908 | 0/200 |

El sesgo **constante** hasta 2° altera poco el resultado en este caso: la mediana de la desviación absoluta respecto del baseline es 0,018 L/s izquierda y 0,009 L/s derecha a 2°. Un error independiente cuadro a cuadro de igual amplitud fabrica longitud de recorrido al diferenciar posiciones proyectadas; puede elevar o reducir `C` porque ese recorrido falso se reparte desigualmente entre regiones. Con 1° independiente la mediana izquierda sube 0,838 L/s y la derecha baja 0,745 L/s. A 2° aparece inversión de signo derecho en 5 % de réplicas. La diferencia entre el contraste co-rotante y el centrado en cintura de la toma **no queda atribuida** al ruido: no conocemos el error real del marco, y la perturbación mantiene la orientación nominal como si fuera verdadera.

La simulación tampoco da un umbral universal de grados: el efecto depende de FPS, tamaño/distancia de la mano al origen, distribución de regiones, segmentación y rapidez verdadera. `ρ=0,95` aquí es correlación **entre cuadros a 120 Hz**, no una propiedad de un filtro HarMoCAP. Un [ensayo posterior de promedio causal del marco](CMU_FILTRO_MARCO_CAUSAL.md) cuantifica cómo bajar el jitter hipotético cambia también la orientación durante giros y el propio `C`, sin establecer exactitud física ni validar una versión live. Los percentiles son entre réplicas hipotéticas sobre **una toma**, no intervalos de confianza poblacionales.

## Gate para el banco de cámaras y el estudio

Antes de fijar `C` para Nico, el [piloto de video](PILOTO_VALIDACION_VIDEO.md) debe medir por separado error angular estático, fluctuación cuadro a cuadro y error durante giros en cada montaje 2D/3D. Se necesita una referencia física o multivista de orientación y una secuencia de cuerpo/objeto rígido que permita separar giro real de jitter; registrar además FPS y timestamps originales. El pipeline deberá propagar esa incertidumbre a cada tramo y al contraste por región, y comparar filtrado causal con referencia offline, reportando retardo. Un umbral de validez basado sólo en error angular medio ocultaría precisamente la diferencia temporal que revela este ensayo. El [diccionario de señales](DICCIONARIO_SENALES_V0.md) deberá exigir una calidad de marco por ventana para `spacetime_c_live` antes de convertirlo en sonido.
