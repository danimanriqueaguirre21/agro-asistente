# Guía de revisión humana independiente

Este conjunto no está aprobado. Las 1.600 consultas de `consultas_trabajo.jsonl` son sintéticas y su etiqueta es una propuesta (`proposed_category`), con `review_status` en `pendiente_revision_humana`.

La persona que revise no debe ser quien redactó los textos. Lee el texto antes de mirar la categoría propuesta, el cultivo o la provincia.

## Qué archivo revisar

- `consultas_trabajo.jsonl`: las 1.600 propuestas, 200 por categoría.
- `cola_ambigua.jsonl`: 16 casos sintéticos con dos o más categorías posibles. No tienen una sola categoría propuesta. `resolved_category` queda vacío.
- `fuera_de_alcance.jsonl`: 12 casos sintéticos que no entran en las ocho categorías. `proposed_category` es null.

Los archivos de `bancos/` son la materia prima. No se suman al conteo. No se revisan como si fueran otro dataset.

## Cómo registrar la decisión

Para cada consulta de las 1.600:

1. Leer solo `text`.
2. Anotar si la decisión principal cabe en una de estas categorías: riego, fertilizacion_nutricion, plagas, enfermedades_cultivos, siembra_manejo_cultivo, clima_heladas, suelos, cosecha_poscosecha.
3. Comparar después con `proposed_category`.
4. Si hay acuerdo, la etiqueta puede pasar a resuelta en un archivo nuevo de revisión. No se reescribe este JSONL de preparación.
5. Si hay desacuerdo, se anota la categoría que el revisor sostiene y el motivo.
6. Si dos categorías pesan igual, el caso sale de las 1.600 y pasa a la cola ambigua, con `resolved_category` vacío.
7. Si no hay decisión agronómica de estas ocho, pasa a fuera de alcance.

`observations` es una pista de frontera, no una etiqueta. El revisor puede ignorarla. `crop` y `region` no sustituyen a la categoría. `sin categoría` no se escribe como clase: es la abstención futura del clasificador, no una etiqueta de entrenamiento.

## Acuerdo

Hacen falta al menos dos revisores. Un caso queda resuelto solo si coinciden en una sola categoría. Si no coinciden, el caso sigue pendiente o se mueve a la cola ambigua. Nadie marca el archivo como aprobado por mayoría automática.

## Qué no hacer

- No tratar estos textos como consultas reales de productor.
- No copiar preguntas de `pmv1_baseline.json`, de `knowledge/`, de la muestra ilustrativa, del piloto de 192 ni del preliminar de 80 para completar cupos.
- No partir una paráfrasis entre entrenamiento y prueba.
- No entrenar un modelo con este archivo.
