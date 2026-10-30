# Evaluación en el conjunto de prueba — HU-08

Esta evaluación compara las predicciones del modelo ya entrenado con las etiquetas sintéticas de `prueba.jsonl`. No mide riesgo agrícola real ni valida una metodología agronómica.

No se reentrenó el modelo. No se usaron estos registros para elegir parámetros, umbrales ni reglas. No se calcularon probabilidades.

## Resultado

- Registros evaluados: 144.
- Predicciones correctas: 117.
- Predicciones incorrectas: 27.
- Accuracy: 0,8125.
- Macro-F1: 0,8084.

| Categoría real | Registros | Predichos como esa categoría | Precisión | Recall | F1 |
|---|---:|---:|---:|---:|---:|
| bajo | 48 | 40 | 0,9000 | 0,7500 | 0,8182 |
| medio | 48 | 40 | 0,8250 | 0,6875 | 0,7500 |
| alto | 48 | 64 | 0,7500 | 1,0000 | 0,8571 |

## Matriz de confusión

Filas: etiqueta sintética. Columnas: predicción. Orden: bajo, medio, alto.

| Real \ Predicha | bajo | medio | alto |
|---|---:|---:|---:|
| bajo | 36 | 7 | 5 |
| medio | 4 | 33 | 11 |
| alto | 0 | 0 | 48 |

## Lectura de las cifras

La F1 más alta es la de `alto` (0,8571). La más baja es la de `medio` (0,7500).

Los errores están fuera de la diagonal: 7 de `bajo` se predijeron como `medio`; 5 de `bajo` se predijeron como `alto`; 4 de `medio` se predijeron como `bajo`; 11 de `medio` se predijeron como `alto`.

De las 27 predicciones incorrectas, 12 tienen etiqueta real `bajo`, 15 tienen etiqueta real `medio`, 0 tienen etiqueta real `alto`.

La confusión más numerosa es `medio` predicho como `alto` (11 registros).

La diferencia entre la F1 más alta y la más baja es 0,1071. El desempeño no es equilibrado.

Esas cifras describen el acuerdo con la etiqueta sintética. No identifican una causa agronómica.

## Limitaciones

- Las etiquetas de referencia salen de `reglas_etiquetado_sintetico.md`. Acertarlas no demuestra un riesgo observado en un predio.
- El conjunto tiene 144 registros sintéticos, 48 por categoría. No representa agricultores de Junín.
- El preprocesamiento imputa temperatura y precipitación ausentes con la mediana aprendida en el entrenamiento. La regla de simulación, en cambio, no suma puntos cuando el dato falta.
- No se informa una probabilidad. El bosque puede calcular puntuaciones, y esta evaluación no las trata como confianza calibrada.

## Reproducir

```text
python backend/clasificacion/experimentos/hu08_riesgo/evaluar_modelo_riesgo_hu08.py
```

SHA-256 de `prueba.jsonl`: `d49fe09c32f0dc937b6a7892e8c1de644f96b28c87eaa65ffddd97122f4d8223`.

SHA-256 de `modelo_riesgo_hu08.joblib`: `2f3997c1101433c24f4ebdf7f62ecefaa83d782cb34b86a3484705e8bde133bb`.
