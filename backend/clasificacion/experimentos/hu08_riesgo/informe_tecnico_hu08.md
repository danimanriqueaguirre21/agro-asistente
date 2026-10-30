# Informe técnico — entrenamiento HU-08

Prototipo académico. Las métricas miden si el clasificador reproduce las etiquetas sintéticas del conjunto de entrenamiento mediante validación cruzada. No miden riesgo agrícola real y no usan `prueba.jsonl`.

## Modelo seleccionado

Configuración: `bosque_aleatorio_profundidad12_hoja1`.

Criterio, aplicado solo a la validación cruzada: mayor macro-F1 media; en empate a seis decimales, mayor accuracy media; si continúa el empate, menor complejidad. La regresión logística se considera más simple que el bosque aleatorio.

Macro-F1 media: 0,8185. Accuracy media: 0,8229.

El pipeline guardado se reajustó con los 576 registros de entrenamiento después de la elección. Ese reajuste no se usó para comparar modelos.

## Variables

Entran, en este orden: `familia_escenario`, `cultivo`, `region`, `etapa_fenologica`, `temperatura_c`, `precipitacion_mm`, `dias_sin_lluvia`, `sintoma_observado`, `proporcion_afectada`, `condicion_suelo`.

No entran `id`, `origen`, `es_observacion_real`, `version_reglas` ni la etiqueta `nivel_riesgo`.

`sintoma_observado` se codifica como texto `true` o `false` antes de la imputación. Esa conversión no sustituye un nulo por cero.

## Valores ausentes

No se eliminó ninguna de las 576 filas. Un nulo de JSON se representa como NaN y el imputador del pliegue lo trata. No se escribe cero en el lugar del dato faltante.

| Variable | Nulos en entrenamiento | Tratamiento dentro del pipeline |
|---|---:|---|
| familia_escenario | 0 | Moda del pliegue y codificación one-hot. En este archivo no hay nulos. |
| cultivo | 0 | Moda del pliegue y codificación one-hot. En este archivo no hay nulos. |
| region | 0 | Moda del pliegue y codificación one-hot. En este archivo no hay nulos. |
| etapa_fenologica | 0 | Moda del pliegue y codificación one-hot. En este archivo no hay nulos. |
| temperatura_c | 93 | Mediana del pliegue de entrenamiento e indicador de ausencia. |
| precipitacion_mm | 77 | Mediana del pliegue de entrenamiento e indicador de ausencia. |
| dias_sin_lluvia | 0 | Mediana del pliegue. En este archivo no hay nulos. |
| sintoma_observado | 0 | Moda del pliegue y codificación one-hot. En este archivo no hay nulos. |
| proporcion_afectada | 0 | Mediana del pliegue. En este archivo no hay nulos. |
| condicion_suelo | 0 | Moda del pliegue y codificación one-hot. En este archivo no hay nulos. |

La mediana y la moda se calculan solo con las filas de entrenamiento de cada pliegue. La regresión logística, además, estandariza sus variables numéricas después de imputar. El bosque aleatorio no las estandariza.

El indicador de ausencia vale 1 cuando el valor original faltaba y 0 cuando estaba presente. No es el valor imputado de la temperatura ni de la precipitación.

## Semilla y configuración

- Semilla: 42.
- Validación: StratifiedKFold de 5 pliegues, con barajado y la misma semilla.
- Regresión logística: solver `lbfgs`, máximo 2000 iteraciones, C en 0,1, 1 y 4.
- Bosque aleatorio: 200 árboles, `n_jobs` 1, profundidad 6, 12 o sin límite, y mínimo de muestras por hoja 1 o 4.
- scikit-learn 1.9.1.

## Comparación

Todas las cifras de esta tabla son medias de los cinco pliegues. Las métricas por categoría salen de las predicciones fuera de pliegue, otra vez solo sobre entrenamiento.

| Configuración | Macro-F1 | Accuracy | F1 bajo | F1 medio | F1 alto |
|---|---:|---:|---:|---:|---:|
| regresion_logistica_C0.1 | 0,6594 | 0,6736 | 0,6895 | 0,5106 | 0,7810 |
| regresion_logistica_C1.0 | 0,6648 | 0,6753 | 0,6963 | 0,5282 | 0,7714 |
| regresion_logistica_C4.0 | 0,6651 | 0,6736 | 0,7016 | 0,5318 | 0,7642 |
| bosque_aleatorio_profundidad6_hoja1 | 0,7688 | 0,7778 | 0,8213 | 0,6563 | 0,8282 |
| bosque_aleatorio_profundidad6_hoja4 | 0,7361 | 0,7500 | 0,8170 | 0,5890 | 0,8026 |
| bosque_aleatorio_profundidad12_hoja1 | 0,8185 | 0,8229 | 0,8640 | 0,7283 | 0,8631 |
| bosque_aleatorio_profundidad12_hoja4 | 0,7749 | 0,7830 | 0,8373 | 0,6605 | 0,8256 |
| bosque_aleatorio_profundidadsin_limite_hoja1 | 0,8116 | 0,8159 | 0,8602 | 0,7230 | 0,8513 |
| bosque_aleatorio_profundidadsin_limite_hoja4 | 0,7783 | 0,7865 | 0,8427 | 0,6646 | 0,8264 |

### Categorías del modelo seleccionado

Predicciones fuera de pliegue. El orden de la matriz es bajo, medio, alto. Cada fila es la etiqueta sintética y cada columna es la predicción.

| Categoría | Precisión | Recall | F1 | Soporte |
|---|---:|---:|---:|---:|
| bajo | 0,8852 | 0,8438 | 0,8640 | 192 |
| medio | 0,8182 | 0,6562 | 0,7283 | 192 |
| alto | 0,7782 | 0,9688 | 0,8631 | 192 |

```text
162 22 8
21 126 45
0 6 186
```

## Salida del preprocesamiento

El pipeline conservó el orden de entrada de las diez variables. La codificación one-hot y los indicadores de ausencia amplían esa entrada. Los nombres de salida del modelo guardado son:

- `familia_escenario__x0_meteorologico`
- `familia_escenario__x0_plaga_enfermedad`
- `familia_escenario__x0_suelo_agua_manejo`
- `cultivo__x1_cebada`
- `cultivo__x1_haba`
- `cultivo__x1_maíz`
- `cultivo__x1_papa`
- `cultivo__x1_quinua`
- `region__x2_Chupaca`
- `region__x2_Concepción`
- `region__x2_Huancayo`
- `region__x2_Jauja`
- `region__x2_Junín`
- `region__x2_Tarma`
- `etapa_fenologica__x3_desarrollo_vegetativo`
- `etapa_fenologica__x3_emergencia`
- `etapa_fenologica__x3_floracion`
- `etapa_fenologica__x3_llenado`
- `etapa_fenologica__x3_maduracion`
- `etapa_fenologica__x3_siembra`
- `temperatura_c__x4`
- `temperatura_c__missingindicator_x4`
- `precipitacion_mm__x5`
- `precipitacion_mm__missingindicator_x5`
- `dias_sin_lluvia__x6`
- `sintoma_observado__x7_false`
- `sintoma_observado__x7_true`
- `proporcion_afectada__x8`
- `condicion_suelo__x9_adecuado`
- `condicion_suelo__x9_encharcado`
- `condicion_suelo__x9_seco`

## Limitaciones

- Las etiquetas son supuestos de simulación de `reglas_etiquetado_sintetico.md`. Un macro-F1 alto solo diría que el modelo se acerca a esas reglas, no que predice daño en un predio.
- No hay observaciones reales de agricultores ni unidades leídas de SENAMHI.
- `cultivo` y `region` no definen la etiqueta sintética. Si el modelo les da peso, está usando variación que la simulación no relacionó con el nivel.
- La etapa pesa en las reglas. Parte del resultado puede venir de esa variable y no de una relación agronómica.
- La mediana no reproduce la regla de simulación, que trata el nulo como ausencia de puntos y no como el valor típico.
- Esta corrida no evalúa `prueba.jsonl`. Esa evaluación queda fuera de esta actividad.
- El modelo no está integrado al backend.

## Archivos de esta actividad

- `preprocesamiento_riesgo_hu08.py`
- `entrenar_modelo_riesgo_hu08.py`
- `configuracion_seleccionada_hu08.json`
- `metricas_validacion_cruzada_hu08.json`
- `modelo_riesgo_hu08.joblib`
- `informe_tecnico_hu08.md`
- `instrucciones_reproduccion_hu08.md`

## Reproducir

```text
python entrenar_modelo_riesgo_hu08.py
```

El comando se ejecuta en `backend/clasificacion/experimentos/hu08_riesgo`. También funciona con la ruta absoluta del script, porque lee y escribe junto a ese archivo.
