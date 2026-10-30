# Reglas de etiquetado sintético — HU-08

Versión: `sintetica-hu08-v1`.

Estas reglas sirven para construir un ejercicio académico de clasificación. Son supuestos de simulación. No son umbrales agronómicos validados, no describen el clima de Junín y no autorizan una recomendación a un agricultor.

La etiqueta `nivel_riesgo` puede ser `bajo`, `medio` o `alto`. En este archivo esos nombres solo ordenan el puntaje de la simulación. No significan que el prototipo haya aprobado la escala analizada en `docs/HU08_CATEGORIAS_Y_CRITERIOS_RIESGO.md`.

## Alcance

Cada fila pertenece a una sola `familia_escenario`. La etiqueta usa únicamente la regla de esa familia. Un escenario meteorológico no recibe puntos por síntoma ni por suelo. Un escenario de plagas no recibe puntos por temperatura ni por lluvia. Un escenario de suelo no recibe puntos por síntoma.

`cultivo` y `region` se generan para que el conjunto sea variado. No entran en el puntaje. El ejercicio no asigna más riesgo a un cultivo o a un lugar.

Un valor ausente de temperatura o de precipitación suma cero. No se rellena con cero ni se interpreta como riesgo bajo por estar vacío.

## Puntaje y etiqueta

El puntaje es un entero. La etiqueta depende solo de ese entero:

| Puntaje | nivel_riesgo |
|---|---|
| 0 o 1 | bajo |
| 2 o 3 | medio |
| 4 o más | alto |

El puntaje no se guarda en el dataset. Si se guardara, la clasificación sería trivial.

## Meteorológico

Solo usan `temperatura_c`, `precipitacion_mm` y `etapa_fenologica`.

- +2 si la temperatura no es nula, es menor o igual a 4 Celsius simulados, y la etapa es `emergencia` o `floracion`.
- +1 si no aplicó el punto anterior, la temperatura no es nula, es menor o igual a 7, y la etapa es `emergencia`, `floracion` o `llenado`.
- +1 si la temperatura no es nula, es mayor o igual a 25, y la etapa es `floracion`. Este punto no se suma junto con los de frío.
- +2 si la precipitación no es nula, es mayor o igual a 40 mm simulados, y la etapa es `emergencia`, `floracion` o `llenado`.
- +1 si no aplicó el punto anterior, la precipitación no es nula y es mayor o igual a 22.

El frío solo, o la lluvia fuerte sola, llega como máximo a 2 puntos: `medio`. `alto` exige frío o calor de floración junto con lluvia fuerte. Una sola de esas variables no basta para `alto`.

## Plagas y enfermedades

Solo usan `sintoma_observado`, `proporcion_afectada` y `etapa_fenologica`.

Si no hay síntoma, la proporción es 0 y el puntaje es 0.

- +2 si hay síntoma y la proporción es mayor o igual a 0,55.
- +2 si hay síntoma, la proporción es mayor o igual a 0,35 y la etapa es `emergencia` o `floracion`.
- +1 si hay síntoma, la proporción es mayor o igual a 0,25 y la etapa es `llenado`. Este punto no se suma si ya se sumó el punto anterior de etapa.

Ver un síntoma con proporción baja queda en 0: `bajo`. Una proporción alta en `siembra`, `desarrollo_vegetativo` o `maduracion` queda en 2: `medio`. `alto` pide proporción alta y, además, `emergencia` o `floracion`.

## Suelo, agua y manejo

Solo usan `condicion_suelo`, `dias_sin_lluvia`, `precipitacion_mm` y `etapa_fenologica`.

- +2 si el suelo es `encharcado`, la precipitación no es nula y es mayor o igual a 28.
- +1 si el suelo es `encharcado` y no aplicó el punto anterior.
- +2 si el suelo es `seco` y los días sin lluvia son 15 o más.
- +1 si el suelo es `seco`, los días sin lluvia están entre 8 y 14, y no aplicó el punto anterior.
- +2 si el suelo no es `adecuado` y la etapa es `emergencia` o `floracion`.
- +1 si el suelo no es `adecuado`, la etapa es `llenado` y no aplicó el punto anterior.

`adecuado` suma 0 aunque llueva o haya muchos días secos. La lluvia sola, sin suelo encharcado, no etiqueta el escenario. `alto` pide un suelo en condición extrema, con lluvia fuerte o con 15 días o más sin lluvia, y además una etapa sensible.

## Lo que estas reglas no hacen

- No leen SENAMHI ni MySQL.
- No reutilizan consultas, categorías ni modelos de HU-07.
- No declaran una metodología agronómica aprobada.
- No producen medidas preventivas.
