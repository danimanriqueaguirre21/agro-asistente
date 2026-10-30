# Informe técnico — experimento preliminar HU-07

Experimento técnico sobre categorías propuestas. El dataset no está aprobado. Las consultas son sintéticas. Las métricas no son un resultado definitivo ni describen consultas reales de productores.

## Datos

- Archivo leído, sin modificar: `backend/clasificacion/preparacion/dataset_trabajo_hu07/consultas_trabajo.jsonl`.
- Registros leídos: 1600.
- Usados en el experimento: 1595.
- Entrenamiento: 1276. Prueba: 319. Semilla: 42.
- Partición del par de la polilla del olluco: El par ya quedó en la misma partición.

Excluidos del entrenamiento:

- `trabajo-hu07-ead432668d` (riego): Consulta compuesta. El informe pide sacarla de las 1600.
- `trabajo-hu07-77fa929ec0` (fertilizacion_nutricion): Consulta compuesta. El informe pide sacarla de las 1600.
- `trabajo-hu07-4da2de2e03` (plagas): El informe pide excluirla de entrenamiento por paráfrasis de ilustrativo-007.
- `trabajo-hu07-b7bf806a37` (enfermedades_cultivos): Consulta compuesta. El informe pide sacarla de las 1600.
- `trabajo-hu07-7791383f85` (enfermedades_cultivos): Consulta compuesta. El informe pide sacarla de las 1600.

No se cargaron los anexos: cola ambigua (16) y fuera de alcance (12).

Distribución usada, por categoría propuesta:

- riego: 199 (entrenamiento 159, prueba 40)
- fertilizacion_nutricion: 199 (entrenamiento 159, prueba 40)
- plagas: 199 (entrenamiento 159, prueba 40)
- enfermedades_cultivos: 198 (entrenamiento 159, prueba 39)
- siembra_manejo_cultivo: 200 (entrenamiento 160, prueba 40)
- clima_heladas: 200 (entrenamiento 160, prueba 40)
- suelos: 200 (entrenamiento 160, prueba 40)
- cosecha_poscosecha: 200 (entrenamiento 160, prueba 40)

## Modelo

Pipeline de `TfidfVectorizer` (palabras y bigramas, `min_df=2`, `sublinear_tf`) y `LogisticRegression` (`C=1.0`, `solver=lbfgs`, `max_iter=2000`). No hubo búsqueda de parámetros. El conjunto de prueba no se usó para elegir la configuración.

## Métricas en prueba

- Accuracy: 0.9467
- Precision macro: 0.9474
- Recall macro: 0.9466
- F1 macro: 0.9463
- F1 ponderado: 0.9463

| Categoría | Precision | Recall | F1 | Soporte |
| --- | ---: | ---: | ---: | ---: |
| riego | 0.9444 | 0.8500 | 0.8947 | 40 |
| fertilizacion_nutricion | 0.9474 | 0.9000 | 0.9231 | 40 |
| plagas | 0.9048 | 0.9500 | 0.9268 | 40 |
| enfermedades_cultivos | 0.9730 | 0.9231 | 0.9474 | 39 |
| siembra_manejo_cultivo | 0.9750 | 0.9750 | 0.9750 | 40 |
| clima_heladas | 0.9756 | 1.0000 | 0.9877 | 40 |
| suelos | 0.9524 | 1.0000 | 0.9756 | 40 |
| cosecha_poscosecha | 0.9070 | 0.9750 | 0.9398 | 40 |

Matriz de confusión (filas: etiqueta propuesta; columnas: predicción), en el orden de las ocho categorías:

```
  34    2    1    0    0    0    1    2
   1   36    1    0    1    0    0    1
   0    0   38    1    0    1    0    0
   0    0    2   36    0    0    0    1
   0    0    0    0   39    0    1    0
   0    0    0    0    0   40    0    0
   0    0    0    0    0    0   40    0
   1    0    0    0    0    0    0   39
```

Categorías con F1 más bajo en esta prueba: riego (0.8947), fertilizacion_nutricion (0.9231), plagas (0.9268).

## Limitaciones

- Las etiquetas son propuestas. No hay aprobación humana registrada.
- El texto es sintético. El resultado no dice cómo respondería el modelo a consultas reales.
- El modelo no está integrado al PMV1, al RAG ni a producción.
- No se calculó un umbral de abstención.
- La división es estratificada y reproducible, con el par cercano de la polilla del olluco forzado a la misma partición. No se rehizo una búsqueda general de paráfrasis.

Versiones: python 3.13.7, plataforma Windows-11-10.0.26200-SP0, scikit-learn 1.9.1, numpy 2.5.3, joblib 1.6.0.
