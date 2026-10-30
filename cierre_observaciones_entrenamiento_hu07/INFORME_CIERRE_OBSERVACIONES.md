# Cierre de observaciones — preparación del entrenamiento HU-07

Fecha: 2026-10-18.

El archivo original `backend/clasificacion/preparacion/dataset_trabajo_hu07/consultas_trabajo.jsonl` no se modificó. SHA-256: `16fd1dfbf3e0589995931b5a42da47bf0ff677ab04cf1fba2c1a7f7536c164fd`.

Las 1.600 consultas son sintéticas. Ninguna es una consulta real de productor.

## Cuántas quedaron aprobadas

Cero.

Las 1.600 tienen `review_status` = `pendiente_revision_humana`. Ninguna tiene etiqueta resuelta ni una aprobación escrita por una persona. Este cierre no aprueba etiquetas por su cuenta.

La copia de trabajo del experimento está en `experimento/consultas_aprobadas.jsonl` y no contiene filas. Su manifiesto deja `is_training_set` en false y `experiment_ran` en false.

## Cuántas se excluyen y por qué

Del conjunto que podría entrenarse, hoy se excluyen las 1.600, porque todas siguen pendientes. Dentro de ese total, la auditoría ya marcó grupos que tampoco entrarían aunque el resto se revisara después:

| Grupo | Cantidad | Motivo | Entran al experimento |
| --- | ---: | --- | --- |
| Consultas compuestas | 4 | Piden dos decisiones con el mismo peso. La regla no las fuerza a una clase. | No, hasta que una persona resuelva una sola etiqueta |
| Revisión humana abierta | 13 | La regla no elige ganador. No se inventa la decisión. | No |
| Resto del archivo | 1.583 | Siguen en `pendiente_revision_humana` | No |
| Cola ambigua | 16 | Anexo, sin categoría resuelta | No |
| Fuera de alcance | 12 | Anexo. No son una categoría temática | No |

Las cuatro compuestas, fuera hasta nueva resolución:

- `trabajo-hu07-ead432668d` (riego o suelos)
- `trabajo-hu07-77fa929ec0` (fertilización o siembra y manejo)
- `trabajo-hu07-b7bf806a37` (enfermedad o plaga)
- `trabajo-hu07-7791383f85` (enfermedad o clima)

Las trece de revisión humana, sin decisión inventada:

- `trabajo-hu07-6310e70aca`
- `trabajo-hu07-d0c408757f`
- `trabajo-hu07-9659612ab0`
- `trabajo-hu07-20392819ed`
- `trabajo-hu07-beb6b836e3`
- `trabajo-hu07-ae638b74f3`
- `trabajo-hu07-5a8d38f56b`
- `trabajo-hu07-4070bf7ab7`
- `trabajo-hu07-33f205f8fe`
- `trabajo-hu07-6493a2ec5e`
- `trabajo-hu07-4cfb645653`
- `trabajo-hu07-fa9a5283d3`
- `trabajo-hu07-3de8a9c50c`

Siguen pendientes, además, dos descripciones sin pregunta (`trabajo-hu07-0caaaf7615`, `trabajo-hu07-02f546802a`), la paráfrasis de `ilustrativo-007` (`trabajo-hu07-4da2de2e03`) y el par de la polilla del olluco (`trabajo-hu07-d6612d79a4`, `trabajo-hu07-628a8b17ab`), que no debe partirse entre particiones.

## Diseño de estados

`fuera_de_alcance` no es una categoría temática. Las únicas categorías son las ocho de la taxonomía. La disposición de la fila es otro campo: pendiente, ambigua, fuera de alcance, excluida o aprobada para experimento.

En el original, `ambigua-198e86ea7a` pone `fuera_de_alcance` dentro de `candidate_categories`. Ese archivo no se reescribió. El diseño corregido, sin aplicarlo al original, está en `diseno_estados.json`.

## Entrenamiento

No es viable. No hay registros aprobados suficientes: hay cero. No se ajustó TF-IDF ni regresión logística. No hay particiones, ni umbral de abstención, ni métricas. Accuracy, precision, recall, F1, macro-F1 y la matriz de confusión no se calcularon.

## Decisiones humanas que siguen pendientes

1. Resolver o dejar fuera las cuatro consultas compuestas.
2. Cerrar las trece revisiones abiertas, con acuerdo de dos personas.
3. Decidir el caso de la ceniza `ambigua-198e86ea7a` sin usar `fuera_de_alcance` como categoría.
4. Aprobar de forma explícita, fila por fila, cualquier consulta que vaya a un experimento. El control de duplicados no sustituye esa aprobación.
5. Recién entonces armar particiones que no separen paráfrasis, y elegir el umbral de abstención solo con validación.

## Limitaciones

El origen sigue siendo sintético. Un resultado futuro sobre estos textos no describe consultas reales de productor. El dataset completo no queda aprobado. El modelo no se integra al flujo de producción ni al PMV1.
