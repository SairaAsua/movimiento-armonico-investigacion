# Separación 3D entre proxies de muñeca en una toma pública de danza

**Ensayo de factibilidad offline, 03-10-2026.** Se reutiliza **sólo** la toma pública [CMU 05_02](CMU_DANZA_BANCO_REAL.md): 1.123 cuadros de marcadores a 120 Hz, auditados por SHA-256. El [script reproducible](cmu_relacion_manos.py) exige `numpy` y `ezc3d`, lee el C3D desde `research/sources/cmu_mocap/` (ignorado por Git) y no publica marcadores ni imágenes. El [contraejemplo matemático anterior](https://github.com/SairaAsua/movimiento-armonico-investigacion/blob/0d27a64/research/RELACION_ESPACIAL_MIEMBROS.md) mostró que `Q`, rapidez y fase individuales no determinan una relación espacial 3D. Esta toma **no tiene soga, Nico, valoración estética, fase de tarea, fuerza ni referencia anatómica independiente**.

## Punto, marco y denominador

La mano izquierda se representa por la media de `LWRA/LWRB`; la derecha, por `RWRA/RWRB`, **proxies de marcadores** y no centros articulares verificados. Los cuatro marcadores, hombros, cintura y dos etiquetas de control de orientación tienen residual no negativo y coordenadas finitas en los 1.123 cuadros; ello sólo señala disponibilidad según el archivo. La escala fija `L=303,531939 mm` es la mediana del ancho entre marcadores de hombros durante los **primeros 120 cuadros**, calculada antes de resumir el resto. No se optimiza a un resultado estético ni usa la toma completa para calibrar retrospectivamente una señal que se quiera llamar live.

El vector `Δp(t)=p_R(t)−p_L(t)` se expresa en sala y en ejes corporales derivados de hombros/cintura. La norma da la misma distancia en ambos marcos hasta precisión numérica, como debe ocurrir bajo rotación rígida. El **signo de la componente vertical**, en cambio, depende de la convención corporal. La proyección lateral–vertical elimina la componente delante–detrás de ese marco móvil: es una **proyección ortográfica construida**, no un video de una Reolink ni el resultado de un detector 2D.

| Resultado en anchos de hombros `L` | Mínimo | P5 | Mediana | P95 | Máximo |
|---|---:|---:|---:|---:|---:|
| Distancia 3D entre medias de pares de muñeca | 0,596430 | 1,150451 | 2,061350 | 3,731890 | 4,177092 |
| Componente vertical firmada, derecha menos izquierda | −1,346327 | −1,244535 | −0,023209 | 1,498940 | 2,537216 |
| Distancia 3D menos distancia proyectada lateral–vertical | 0,000000 | 0,000104 | 0,008188 | 0,388544 | 0,654193 |
| Diferencia absoluta de distancia al usar `LWR0/RWR0` | 0,000418 | 0,012803 | 0,185295 | 0,411231 | 0,450459 |

La proyección reduce la distancia en más de `0,1 L` en **283/1123 cuadros (25,2 %)**. Esto comprueba que la profundidad de esta toma puede importar para ese descriptor; no estima el error de ninguna cámara propia. `LWR0/RWR0` son **otros puntos del mismo archivo**, posiblemente derivados (sus residuales son exactamente cero en todos los cuadros), no una verdad externa. La discrepancia mediana entre elecciones de proxy, `0,185 L` (~56 mm), demuestra sensibilidad a la definición operacional de «muñeca», **no** error anatómico ni sesgo del primer proxy. Los cuantiles por cuadro son descripciones de una sola toma autocorrelacionada, no intervalos de confianza ni 1.123 personas independientes.

## Decisión para el estudio y Beacon

Conservar `Δp` firmado y `D=||Δp||` **por par nombrado**, marco, escala, reloj y estado de calidad. La distancia permite una comprobación de invariancia al marco rígido; su resumen escalar pierde quién pasó arriba, adelante o primero. Si el piloto sólo recupera una proyección, publicar `D_proj` con vista y unidades, sin renombrarlo `D_3d`. Si se quiere medir el orden vertical o contramovimiento histórico, hará falta además profundidad y orientación corporal validadas, tarea definida y acuerdo con especialista Laban.

En el banco técnico propio, una separación dinámica conocida entre dos marcadores/objetos debe servir de **referencia física** a velocidades, giros y oclusiones representativas; después se medirá error y cobertura por par sobre intentos completos. La toma CMU carece de esa referencia y por ello no valida exactitud. Para comparar frases de Nico, el par, el proxy, el marco, la escala y un margen mínimo de diferencia se fijarán en desarrollo antes de sesiones reservadas. `Q`, `R` HIT y la separación son preguntas distintas; ninguna de las tres prueba belleza o eficiencia. Una señal Beacon de separación sólo sería elegible después de verificar disponibilidad causal, latencia, expiración y audibilidad de su mapeo, sin iniciar ahora la cadena live.
