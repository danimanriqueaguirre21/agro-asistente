# Categorías de riesgo del prototipo HU-08

Actividad 4: definir las categorías de riesgo utilizadas por el prototipo académico.

Este documento no modifica el modelo, no lo reentrena y no lo integra al backend. No abre `prueba.jsonl`. Las tres categorías son etiquetas de la simulación `sintetica-hu08-v1`. No son niveles validados de riesgo agrícola.

## Clases que el modelo guardó

Se leyó `modelo_riesgo_hu08.joblib` sin modificarlo. El clasificador es el bosque aleatorio `bosque_aleatorio_profundidad12_hoja1`. Su atributo `classes_` contiene tres cadenas:

| Posición en `classes_` | Cadena exacta | Puntos Unicode |
|---|---|---|
| 0 | `alto` | U+0061 U+006C U+0074 U+006F |
| 1 | `bajo` | U+0062 U+0061 U+006A U+006F |
| 2 | `medio` | U+006D U+0065 U+0064 U+0069 U+006F |

Son de tipo `str`, en minúsculas, sin espacios y sin acentos. El orden de `classes_` es el orden alfabético de scikit-learn. No es una escala de gravedad y no debe mostrarse como ranking.

## Correspondencia con las categorías previstas

Las tres cadenas coinciden, como conjunto, con:

- `nivel_riesgo` de `reglas_etiquetado_sintetico.md`: `bajo`, `medio`, `alto`.
- `niveles` de `configuracion_seleccionada_hu08.json`, en el orden `bajo`, `medio`, `alto`.
- Las etiquetas de `entrenamiento.jsonl`: 192 filas de cada cadena, sin variantes.

| Prevista | En el modelo | ¿Misma cadena? |
|---|---|---|
| `bajo` | `bajo` | Sí |
| `medio` | `medio` | Sí |
| `alto` | `alto` | Sí |

No aparecieron `Bajo`, `BAJO`, `bajo `, `médio` ni ninguna otra forma.

El orden de presentación del prototipo es `bajo`, `medio`, `alto`, porque así ordena el puntaje de la simulación. El orden de `classes_` no cambia ese contrato.

## Tres lecturas que no se mezclan

| Lectura | Qué es | Qué no es |
|---|---|---|
| Categoría predicha | La cadena que devuelve el pipeline: `bajo`, `medio` o `alto`. | Una medición hecha en el predio. |
| Etiqueta de la simulación | El nombre que las reglas asignan a un puntaje entero. | Un umbral agronómico aprobado. |
| Interpretación agronómica real | No existe en este prototipo. | No se completa con los textos de `knowledge/` ni con la taxonomía de HU-07. |

`docs/HU08_CATEGORIAS_Y_CRITERIOS_RIESGO.md` dejó `bajo`, `medio` y `alto` como nombres posibles, pendientes de una metodología aprobada. Este prototipo reutiliza esas palabras solo como etiquetas sintéticas. No aprueba aquel documento.

## Significado dentro de la simulación

La versión de las reglas es `sintetica-hu08-v1`. El puntaje no se guarda en el dataset ni lo devuelve el modelo. La etiqueta sale solo de ese puntaje:

| Puntaje simulado | Categoría |
|---|---|
| 0 o 1 | `bajo` |
| 2 o 3 | `medio` |
| 4 o más | `alto` |

Cada fila usa una sola familia. Los puntos de otra familia no se suman. `cultivo` y `region` no entran en el puntaje. Un dato ausente de temperatura o de precipitación suma cero puntos. No significa, por sí solo, la categoría `bajo`.

### `bajo`

En la simulación, el escenario suma 0 o 1 punto.

- Meteorológico: no se junta un frío o un calor de floración con una lluvia fuerte. Puede no haber ningún punto.
- Plagas y enfermedades: no hay síntoma, o el síntoma tiene una proporción que no alcanza los puntos de la regla.
- Suelo, agua y manejo: el suelo es `adecuado`, o la condición extrema no se junta con la etapa y la lluvia o los días sin lluvia que la regla pide para subir de 1 punto.

### `medio`

En la simulación, el escenario suma 2 o 3 puntos. Una sola señal fuerte de la familia, o dos señales débiles, puede bastar. En meteorología, el frío solo o la lluvia fuerte sola quedan como máximo en `medio`. En plagas, una proporción alta fuera de `emergencia` y `floracion` también queda en `medio`.

### `alto`

En la simulación, el escenario suma 4 puntos o más. Hacen falta al menos dos condiciones de la misma familia. Una sola variable no alcanza esta etiqueta.

- Meteorológico: frío, o calor en floración, junto con lluvia fuerte.
- Plagas y enfermedades: proporción alta y, además, etapa `emergencia` o `floracion`.
- Suelo, agua y manejo: suelo encharcado con lluvia fuerte, o suelo seco con 15 días o más sin lluvia, y además una etapa que la regla trata como sensible.

Esos cortes pertenecen a la simulación. No se trasladan a grados, milímetros ni porcentajes de un cultivo real.

## Contrato de salida propuesto

Todavía no hay un endpoint. Cuando el backend lo exponga, la respuesta de este prototipo debería limitarse a lo siguiente:

| Campo | Tipo | Valor |
|---|---|---|
| `categoria` | texto | Exactamente `bajo`, `medio` o `alto`, como en `classes_`. |
| `modelo_id` | texto | `bosque_aleatorio_profundidad12_hoja1`. |
| `artefacto` | texto | `modelo_riesgo_hu08.joblib`. |
| `version_reglas` | texto | `sintetica-hu08-v1`. |
| `naturaleza` | texto | `prototipo_academico_sintetico`. |
| `es_riesgo_agricola_validado` | booleano | `false`. |

Ejemplo de forma, no de una predicción ejecutada:

```json
{
  "categoria": "medio",
  "modelo_id": "bosque_aleatorio_profundidad12_hoja1",
  "artefacto": "modelo_riesgo_hu08.joblib",
  "version_reglas": "sintetica-hu08-v1",
  "naturaleza": "prototipo_academico_sintetico",
  "es_riesgo_agricola_validado": false
}
```

El contrato no incluye probabilidades ni una escala de confianza. El bosque tiene `predict_proba`, pero esas cifras no están calibradas y no se definen como probabilidad de daño. No forman parte de la salida.

Tampoco incluye medidas preventivas. Las reglas de simulación no las producen.

`categoria` no se traduce a mayúsculas, no se acentúa y no se sustituye por «riesgo bajo», «riesgo medio» o «riesgo alto» dentro del campo. Un texto explicativo puede acompañar la respuesta, siempre que repita la cadena exacta y diga que el resultado es del prototipo sintético.

## Limitaciones

- La categoría predicha aproxima la etiqueta sintética. En la validación cruzada del entrenamiento, `medio` fue la clase con menor F1, 0,7283. Eso no se reevaluó con `prueba.jsonl`.
- El modelo puede usar `cultivo` y `region` aunque las reglas no les dan puntos.
- La imputación por mediana del pipeline no es la regla que asigna cero puntos a un valor ausente.
- No hay metodología agronómica aprobada para estas tres palabras.
- Esta actividad no crea el endpoint ni cambia el flujo de consultas.

## Estado de la actividad 4

Para el prototipo, la actividad queda definida: el modelo usa `bajo`, `medio` y `alto`, con el significado de la simulación y con el contrato de salida anterior.

No queda definida una escala de riesgo agrícola real. La integración al backend no forma parte de esta actividad.
