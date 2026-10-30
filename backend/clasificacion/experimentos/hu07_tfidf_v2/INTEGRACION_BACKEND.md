# Integración del clasificador v2 en el backend

El dataset sigue sin aprobación humana. Las puntuaciones no están calibradas y no describen consultas reales de productores. La HU-07 no está terminada.

## Flujo de una consulta

`POST /api/v1/queries` sigue exigiendo el JWT del agricultor. `RegistrarConsulta` hace, en este orden:

1. Valida el texto y busca el contexto agrícola seleccionado.
2. Clasifica ese mismo texto una sola vez, con `ClasificarConsulta` y el modelo v2.
3. Recupera fragmentos RAG con el texto original, sin filtrar por categoría.
4. Genera la respuesta con el texto original, el cultivo, la región y esos fragmentos. El prompt de Ollama no recibe la categoría.
5. Guarda la consulta, la respuesta y las evidencias como antes.
6. Devuelve la respuesta de PMV1 y, además, el objeto `classification`.

`POST /api/v1/clasificacion` sigue existiendo. No sustituye a la ruta de consultas.

## Categoría

`classification.category` es una de las ocho categorías o `sin categoría`. `sin categoría` aparece cuando el margen es menor que `CLASIFICADOR_MARGEN_MINIMO` (0,17 si no se cambia). No es una clase del modelo. La abstención no se reemplaza por otra categoría.

`classification.scores_are_calibrated` queda en false.

## Error del clasificador

Si el modelo no carga o devuelve una clase fuera de las ocho, no se inventa una categoría y no se usa `sin categoría` para tapar el fallo. `classification.available` queda en false, `classification.category` en null y `classification.error` trae el mensaje. La consulta sigue recuperando documentos y generando la respuesta de PMV1. El estado HTTP sigue siendo 201 cuando la generación sí ocurrió. Un fallo de Ollama sigue respondiendo 503, como antes.

## Dónde se ve

La respuesta JSON de `POST /api/v1/queries` incluye `classification` sin quitar `answer`, `evidences` ni el resto de campos. La pantalla de consulta muestra la categoría debajo del método. El texto de la respuesta no cambia.

## Pruebas

Desde `backend`:

```text
python -m pytest tests/test_clasificacion_en_consulta.py tests/test_clasificador_consulta.py tests/test_submit_query.py tests/test_query_endpoint.py tests/test_rag_endpoint.py -q
```

Esas pruebas pasaron el 2026-10-19. Comprueban la categoría, la abstención, el texto original hacia el RAG, la respuesta generada, una sola llamada al clasificador, el JWT y el error controlado.

`python -m pytest tests -q -m "not integration"` deja dos fallos previos en `test_ragas_baseline.py`: el entorno no tiene el módulo `ragas`. No los provoca este cambio.

## Limitaciones

El modelo es experimental y sintético. La categoría no selecciona documentos ni modifica la respuesta. No está guardada en la base de datos. La HU-07 no queda cerrada.
