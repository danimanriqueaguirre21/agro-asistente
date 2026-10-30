# Auditoría de datos — actividades 1 y 2 de HU-07

Fecha: 2026-10-19.

Actividades revisadas:

1. Preparar y organizar el conjunto de datos de consultas agrícolas.
2. Limpiar y preprocesar los datos.

Los controles de esta página son técnicos. Ninguno aprueba el dataset. La taxonomía tiene la lista de ocho códigos en estado aprobado; el conjunto de entrenamiento sigue en `no_aprobado`.

No se modificó `consultas_trabajo.jsonl`, la taxonomía, los modelos v1 y v2, el PMV1, el RAG ni la base de conocimientos. No se generó otro dataset: el archivo existente alcanza para estos controles.

## Origen y organización

| Dato | Valor |
| --- | --- |
| Archivo principal | `backend/clasificacion/preparacion/dataset_trabajo_hu07/consultas_trabajo.jsonl` |
| SHA-256 | `16fd1dfbf3e0589995931b5a42da47bf0ff677ab04cf1fba2c1a7f7536c164fd` |
| Origen | `sintetico_preparacion` en los 1.600 registros |
| Consultas reales | 0 (`is_real_query` es false) |
| Etiqueta | `proposed_category`. Es una propuesta. `review_status` es `pendiente_revision_humana` en los 1.600 |
| Anexo ambiguo | `cola_ambigua.jsonl`, 16 registros, fuera del conteo de 1.600 |
| Anexo fuera de alcance | `fuera_de_alcance.jsonl`, 12 registros, fuera del conteo de 1.600 |
| Notas de frontera | 146 registros con `observations` no vacía. La nota no es una etiqueta |

Distribución de la categoría propuesta: 200 en cada una de las ocho.

Campos presentes en cada fila: `id`, `text`, `proposed_category`, `origin`, `review_status`, `observations`, `is_real_query`, `crop`, `region`. El identificador coincide, en las 1.600 filas, con `trabajo-hu07-` más los primeros 10 hexadecimales del SHA-256 del texto en NFC.

## Partición usada por v1 y v2

Los identificadores de `hu07_tfidf_v2/ids_particiones.json` son los mismos que los de `hu07_tfidf_preliminar/ids_particiones.json`.

| Parte | Registros |
| --- | ---: |
| Entrenamiento | 1.276 |
| Prueba | 319 |
| Suma | 1.595 |
| Fuera de ambas particiones | 5 |

Esas cinco siguen en el archivo original y no entran a las particiones:

- `trabajo-hu07-ead432668d`, `trabajo-hu07-77fa929ec0`, `trabajo-hu07-b7bf806a37`, `trabajo-hu07-7791383f85`: consultas compuestas. Siguen con la propuesta y sin resolución humana.
- `trabajo-hu07-4da2de2e03`: paráfrasis de `ilustrativo-007`. La categoría propuesta se mantiene; el registro queda fuera del experimento.

El par `trabajo-hu07-d6612d79a4` y `trabajo-hu07-628a8b17ab` está entero en entrenamiento. No hay un texto normalizado que aparezca en las dos particiones.

Distribución de la prueba: 40 por categoría, salvo `enfermedades_cultivos` con 39. El entrenamiento queda en 159 o 160.

La semilla de la partición original es 42. La versión 2 eligió sus parámetros con 5 pliegues estratificados dentro de esas 1.276, con la misma semilla. La prueba no entró a esa elección.

## Preprocesamiento que aplica el modelo v2

Se leyó el pipeline guardado en `modelo_tfidf_logreg_v2.joblib`. El archivo no se reescribió. El JSONL tampoco se normaliza en disco: la transformación ocurre al vectorizar.

| Parámetro | Valor en el modelo v2 |
| --- | --- |
| `lowercase` | true |
| `analyzer` | word |
| `ngram_range` | 1 y 2 |
| `min_df` | 2 |
| `sublinear_tf` | true |
| `strip_accents` | `unicode` |
| `stop_words` | null |
| Vocabulario | 3.306 términos |
| Clasificador | `LogisticRegression`, `C=4.0`, `solver=lbfgs` |
| Clases del estimador | las ocho, en orden alfabético interno del estimador |

`strip_accents=unicode` quita las marcas diacríticas al construir el vector. No crea una novena clase. `sin categoría` no está entre las clases: es la abstención de inferencia cuando el margen entre las dos clases punteras es menor que 0,17.

La versión 1, leída del otro joblib, usa `min_df=2`, unigramas y bigramas, `sublinear_tf` y minúsculas, con `strip_accents` vacío y `C=1.0`.

Quitar palabras funcionales se probó en la validación interna de v2 y no fue la configuración elegida. Por eso el modelo guardado tiene `stop_words` vacío.

## Casos que siguen en criterio humano

No se resolvieron en esta revisión.

- 4 consultas compuestas, listadas arriba.
- 13 revisiones abiertas y 2 descripciones sin pregunta, en `auditoria_etiquetas_dataset_trabajo/lista_casos_dudosos.jsonl`, grupo `revision_humana`.
- 16 de la cola ambigua, con `resolved_category` vacío.
- 12 fuera de alcance, con `disposition` igual a `fuera_de_alcance` y `proposed_category` nulo. Ese valor es la disposición del anexo, no una categoría temática.
- `ambigua-198e86ea7a` incluye `fuera_de_alcance` dentro de `candidate_categories`. Las candidatas temáticas solo pueden ser las ocho. La corrección queda propuesta: dejar `fertilizacion_nutricion` como única candidata temática, o pasar la fila al anexo de fuera de alcance si una persona decide que no hay decisión agrícola. No se aplicó.

## Tabla de controles

| Control realizado | Resultado | Evidencia | Problemas encontrados | Acción pendiente | Estado de aprobación humana |
| --- | --- | --- | --- | --- | --- |
| Origen y marca de consulta real | 1.600 sintéticas; 0 reales | `origin` y `is_real_query` en `consultas_trabajo.jsonl` | Ninguno técnico | Mantener la marca sintética en cualquier uso posterior | No aprobado |
| Ocho categorías, grafía exacta | 200 por código; 0 códigos ajenos | Conteo de `proposed_category` frente a la taxonomía 1.0.0 | Ninguno | Ninguna sobre la grafía | No aprobado. La lista de códigos sí está aprobada; las etiquetas de las filas no |
| Campos obligatorios y textos vacíos | 0 faltantes; 0 textos vacíos | Lectura de las 1.600 filas y de los nueve campos del esquema de trabajo | Ninguno | Ninguna | No aprobado |
| Identificador estable | 0 identificadores repetidos; 0 hashes distintos del texto NFC | SHA-256 de cada texto, 10 hex | Ninguno | Ninguna | No aprobado |
| Duplicados exactos | 0 | Conteo del texto tal como está | Ninguno | Ninguna | No aprobado |
| Duplicados normalizados | 0 | Minúsculas, sin acentos y con espacios colapsados | Ninguno en esa normalización | El par de la polilla del olluco queda bajo el umbral de paráfrasis y debe seguir en la misma partición | No aprobado |
| Anexos separados del conjunto de 1.600 | 16 ambiguas y 12 fuera de alcance, sin mezclarse | `cola_ambigua.jsonl`, `fuera_de_alcance.jsonl`, `controles.json` | `ambigua-198e86ea7a` usa `fuera_de_alcance` como candidata | Una persona decide si esa fila sigue ambigua o pasa al anexo de fuera de alcance | No aprobado |
| Consultas compuestas y revisión humana | Siguen sin resolución | `lista_casos_dudosos.jsonl` | 4 compuestas, 15 de revisión humana, 1 paráfrasis excluida del experimento | Acuerdo de dos revisores. No asignar la alternativa por script | No aprobado |
| Separación entrenamiento y prueba | 1.276 y 319; 0 identificadores en común; 0 textos normalizados en común; las 5 exclusiones fuera de ambas | `ids_particiones.json` de v1 y de v2, listas idénticas | Ninguno de filtración exacta o normalizada | Conservar estas listas si se vuelve a entrenar | No aprobado |
| Preprocesamiento reproducible de v2 | Minúsculas, palabra, n-gramas 1-2, `min_df=2`, `sublinear_tf`, acentos `unicode`, sin stop words, `C=4` | Parámetros leídos del joblib v2; semilla 42 en `entrenar_v2.py` | El JSONL original no guarda el texto ya normalizado. La normalización vive en el vectorizador | Reutilizar el pipeline guardado o el script, con la misma semilla y los mismos identificadores | No aprobado |
| Abstención | `sin categoría` si el margen es menor que 0,17 | `manifiesto_experimento.json` y las clases del estimador | No es un control de limpieza del archivo | No escribir `sin categoría` como etiqueta del dataset | No aprobado |

## Condiciones pendientes para cerrar las actividades 1 y 2

La organización del archivo y la comprobación de limpieza ya están hechas sobre el conjunto existente. Las actividades no quedan cerradas como conjunto aprobado mientras falte esto:

1. Revisión de dos personas, distintas de quien redactó los textos, sobre las categorías propuestas.
2. Decisión humana de las 4 consultas compuestas: una sola categoría, o salida del conjunto etiquetado.
3. Decisión humana de los 15 casos de `revision_humana` y de la paráfrasis que ya está fuera del experimento.
4. Decisión humana de `ambigua-198e86ea7a`, sin usar `fuera_de_alcance` como código de categoría.
5. Un archivo futuro de entrenamiento que copie solo las filas con etiqueta resuelta y aprobación explícita. Este informe no es ese archivo.

Hasta entonces, el conjunto de trabajo permanece sintético, pendiente y no aprobado. El clasificador no se integra al backend.
