# Validación final de HU-07

Fecha: 2026-10-19.

Esta revisión no cierra la historia. No modifica el modelo, el dataset, el umbral ni el flujo RAG. Las métricas siguen siendo de textos sintéticos con etiquetas propuestas.

## Actividad 6

En el repositorio no hay un checklist ni criterios de aceptación con el nombre «actividad 6». Las actividades que sí quedaron escritas son la preparación y limpieza de datos, la integración del modelo y el uso de la categoría dentro de la consulta.

Esta verificación puede darse por ejecutada. No puede darse por cumplido el cierre de HU-07.

## Controles

| Control | Resultado |
| --- | --- |
| Partición documentada | 1.276 entrenamiento y 319 prueba. Cero identificadores en común. Las listas de v1 y v2 son las mismas. |
| Métricas v2 | Accuracy 0,9655 y macro-F1 0,9652 en esas 319. La suma de soportes por categoría es 319. |
| Métricas v1 guardadas | Accuracy 0,9467 y macro-F1 0,9463. Coinciden con la copia que guarda el archivo de v2. La diferencia del F1 ponderado es 2,2e-16, un redondeo de archivo. |
| Modelo v2 en disco | Ocho clases. `sin categoría` no está entre ellas. `min_df=2`, acentos `unicode`, `C=4`, sin palabras funcionales. |
| Umbral | 0,17 en el manifiesto, en la validación cruzada interna y como valor predeterminado de `CLASIFICADOR_MARGEN_MINIMO`. |
| Abstención en la prueba bloqueada | 34 de 319 (10,7 %). Entre las 285 clasificadas, accuracy 0,9930 y 2 errores. El corte no se eligió con esa prueba. |
| Dataset | Sigue `no_aprobado`. Origen sintético. Cero consultas reales. |
| RAG y Ollama | El caso de uso recupera y genera con el texto original. El archivo del prompt de Ollama no menciona al clasificador ni a `sin categoría`. |
| Fallo del clasificador | No inventa categoría. La respuesta de PMV1 sigue. `classification.available` queda en false y `category` en null. |
| Frontend | Interpreta los tres estados del contrato actual. No hay prueba automatizada de la pantalla. |
| RAGAS | Dos pruebas fallan porque falta el módulo `ragas`. El fallo ya estaba y no depende de este cierre. |

## Pruebas ejecutadas

`python -m pytest tests/test_clasificacion_en_consulta.py tests/test_clasificador_consulta.py tests/test_submit_query.py tests/test_query_endpoint.py tests/test_rag_endpoint.py tests/test_settings.py tests/test_generacion_ollama.py -q -m "not integration"`

Resultado: todas pasaron (55 pruebas).

Cubren las ocho categorías como conjunto permitido, la abstención con puntuaciones fijas por debajo de 0,17, el margen igual o mayor que el corte, una sola llamada al clasificador, el texto original hacia el RAG, la respuesta generada sin la categoría, el JWT y el error controlado.

No cubren, como prueba automatizada, las 16 consultas de la cola ambigua ni las 12 fuera de alcance. La sonda experimental ya guardada, que no ajustó el modelo, dejó 7 de 16 ambiguas y 3 de 12 fuera de alcance con una categoría forzada. Esa sonda no se volvió a ejecutar en este cierre.

## Métricas y limitaciones

| Versión | Accuracy | Macro-F1 | Conjunto |
| --- | ---: | ---: | --- |
| v1 | 0,9467 | 0,9463 | 319, etiquetas propuestas |
| v2, sin abstención | 0,9655 | 0,9652 | las mismas 319 |
| v2, con abstención | 0,9930 entre clasificadas | 0,9925 entre clasificadas | 285 de 319 |

Riego sigue siendo la clase más débil de v2 (F1 0,9091). Esas cifras no describen agricultores reales. `predict_proba` no está calibrada. El modelo no está validado para producción.

## Frontend

Con el contrato actual de `classification`:

- `available` true y una de las ocho categorías: muestra el código.
- `available` true y `category` igual a `sin categoría`: muestra «sin categoría (abstención experimental)».
- `available` false y `category` null: muestra «No disponible» y, si viene, el texto de `error`.
- Si falta el objeto, la pantalla no se rompe y muestra «No disponible».

La respuesta y las evidencias se pintan igual que antes.

## Criterios de aceptación

No hay un documento de criterios de aceptación de HU-07 en el repositorio. El diseño de datos aprueba la lista de ocho códigos y deja el dataset de entrenamiento en no aprobado. `backend/clasificacion/README.md` todavía dice que el flujo de consultas no lee esa carpeta; el adaptador sí carga el modelo desde ahí. Ese README no se cambió en este cierre.

Criterios verificables para un cierre formal:

| Criterio | Estado |
| --- | --- |
| Ocho categorías de la taxonomía, y `sin categoría` solo como abstención | Cumplido |
| Umbral 0,17 fijado fuera del conjunto de prueba | Cumplido en el experimento |
| Clasificación una vez por consulta, sin filtrar el RAG ni cambiar el prompt de Ollama | Cumplido |
| Error del clasificador sin categoría inventada, y PMV1 sigue respondiendo | Cumplido |
| La interfaz muestra categoría, abstención e indisponibilidad | Cumplido por lectura del componente. Sin prueba de interfaz |
| Etiquetas resueltas por dos personas y dataset aprobado | No cumplido |
| Consultas compuestas, ambiguas y fuera de alcance resueltas por una persona | No cumplido |
| Entrenamiento solo con filas aprobadas | No cumplido. Se usaron propuestas |
| Evaluación con consultas reales de productores | No cumplido |
| Pruebas automatizadas de ambiguas y fuera de alcance en el flujo de consultas | No cumplido |
| RAGAS ejecutable en este entorno | No cumplido por dependencia ausente, ajena a este cambio |

## Recomendación

La actividad de verificación queda registrada en este informe. HU-07 no puede cerrarse. Falta la aprobación humana del dataset, una evaluación que no dependa solo de textos sintéticos, y pruebas del flujo para ambiguas y fuera de alcance. El modelo permanece experimental.
