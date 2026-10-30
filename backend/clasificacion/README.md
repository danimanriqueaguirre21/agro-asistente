# Clasificación de consultas (PMV2-HU-07) — diseño de datos

Esta carpeta guarda el diseño de la taxonomía y del futuro dataset de
consultas agrícolas etiquetadas. No contiene un modelo, un entrenamiento
ni un conjunto definitivo de entrenamiento, validación o prueba.

## Qué no es esta carpeta

| Ruta | Uso | Relación con esta carpeta |
|---|---|---|
| `knowledge/` | Documentos de la base de conocimiento RAG | No etiquetar consultas con el campo `topic` de esos documentos |
| `backend/evaluation/data/pmv1_baseline.json` | Línea base RAGAS | No reutilizar sus preguntas como dataset de clasificación |
| `backend/evaluation/results/` | Puntuaciones RAGAS | No mezclar métricas del clasificador aquí |

El flujo de consultas del PMV1 (`RegistrarConsulta`, RAG y Ollama) no lee
esta carpeta.

## Contenido

| Archivo | Rol |
|---|---|
| `taxonomia/taxonomia_consultas_v1.json` | Manifiesto versionado de las ocho categorías |
| `esquema/esquema_dataset_v1.json` | Campos del dataset y qué no entra al entrenamiento |
| `REGLAS_ETIQUETADO.md` | Cómo etiquetar, deduplicar y partir los datos |
| `muestras/muestra_ilustrativa_v1.json` | Ejemplos sintéticos para revisión |

Los identificadores `ilustrativo-*` no deben copiarse a un futuro archivo
de entrenamiento. Los ejemplos del manifiesto no repiten el texto: apuntan
al `id` de la muestra.

## Versión y aprobación

Taxonomía `1.0.0` (2026-10-18).

| Qué | Estado |
|---|---|
| Lista de ocho categorías | Aprobada |
| Diseño documental | Aprobado con observaciones; las observaciones de esa auditoría quedaron corregidas en estos documentos |
| Dataset para entrenamiento | No aprobado. No existe |

`sin categoría` es una abstención en inferencia, no una clase de esta
versión. Ocurre si la confianza no alcanza el umbral, si el modelo no
está disponible o si la salida no pertenece a la taxonomía. La falta del
modelo y la salida inválida son causas operativas, no predicciones
válidas. En los tres casos la consulta sigue el flujo general. Una
consulta ambigua no usa ese valor: queda pendiente de revisión humana,
como describe `REGLAS_ETIQUETADO.md`.
