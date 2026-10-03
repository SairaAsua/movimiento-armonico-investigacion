# Proyección oblicua: ritmo aparente de una órbita uniforme

**Contraejemplo geométrico reproducible del 3 de octubre de 2026**, con [script](fase_proyeccion_oblicua_sintetica.py). No usa video humano, cámara física ni el software de HarMoCAP. Precisa el alcance de la advertencia sobre `atan2` de píxeles en el [banco de fase intracíclo](BANCO_FASE_INTRACICLO_CAMARAS.md).

Sea una mano ideal que describe una circunferencia con fase física `θ(t)=ωt` a rapidez angular **constante**. Bajo proyección ortográfica de un plano inclinado, su imagen centrada puede ser `x=cos θ`, `y=c sin θ`, con `c=cos(inclinación)` y `0<c≤1`. El ángulo medido directamente en píxeles es `ψ=atan2(c sin θ, cos θ)`, no `θ`. Su derivada, tras desenvolver la vuelta, es

`dψ/dt = ω c/(cos² θ+c² sin² θ)`.

En los cruces del eje horizontal parece ir a `cω`; en los del eje vertical, a `ω/c`. Con `c=0,25`, la relación entre rapidez angular aparente máxima y mínima es **16**, aunque la mano física nunca cambie de rapidez. Los cierres de vuelta siguen en los mismos tiempos: una verificación que sólo mira hitos no detecta este sesgo intracíclo.

Para mostrar la consecuencia relacional, suponemos dos puntos con **la misma fase física**: uno visto frontalmente (`c=1`) y otro en un plano oblicuo. Su `R₁:₁` físico es `1`. Si se toman sus dos ángulos de imagen como fases segmentarias, el [banco](fase_proyeccion_oblicua_sintetica.py) da:

| Factor `c` del segundo plano | `R₁:₁` de ángulos 2D | Rapidez angular aparente / real |
|---:|---:|---:|
| 1,00 | 1,000000 | 1,00–1,00 |
| 0,50 | 0,971615 | 0,50–2,00 |
| 0,25 | 0,902780 | 0,25–4,00 |

El número `0,902780` no indica coordinación biológica imperfecta: es el resultado de aplicar `atan2` a dos proyecciones distintas. La hipótesis ortográfica y los centros conocidos hacen el ejemplo **más favorable** que un video real; perspectiva, centro móvil, oclusión y error de pose añaden otras dependencias. Tampoco significa que una homografía corrija cualquier mano 3D: sólo rectifica un **plano físico fijo** si su geometría y calibración se verifican.

## Consecuencia de diseño para Laban, HIT y Beacon

Laban motiva estudiar orientación/planos y HIT motiva estudiar fase entre señales; aquí una diferencia **espacial de planos** cambia la fase 2D estimada aunque el tiempo físico sea idéntico. Por tanto, en el contraste `base → +Laban → +HIT`, la fase calculada de una elipse proyectada puede volver a introducir información sobre el plano y confundir los bloques si no se declara el marco, la vista y la rectificación. El ejemplo no demuestra que esto ocurra en Nico, pero da una prueba técnica concreta:

1. Antes de la captura humana, filmar una trayectoria de referencia con fase temporal conocida en planos frontal y oblicuo; medir el error de `atan2` crudo por sector y después de una rectificación calibrada. Conservar PTS, orientación del plano y estado de visibilidad.
2. Si no existe una corrección validada, nombrar la señal `projected_image_angle_phase`, usarla sólo dentro del subdominio de vistas/planos comprobados y tratar cambios de frente corporal como cambio de dominio. No llamar `R` de esos ángulos coordinación 3D ni sonificarlo como tal.
3. Para el análisis de Nico, comprobar por separado cómo cambian el descriptor espacial `Q` y el error de fase bajo la misma orientación. El control factorial matemático Laban–HIT supone fases intrínsecas conocidas; el **estimador óptico** necesita su propia validación antes de que esa separación se transfiera al video.

La demostración es determinista. No establece precisión de Reolink, «logicam», Moto G, ni calibración de HarMoCAP/Beacon; esos resultados dependen del [piloto instrumental](PROTOCOLO_PILOTO_V0.md).
