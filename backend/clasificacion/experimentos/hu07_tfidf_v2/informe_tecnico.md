# Segunda versión experimental — HU-07

El dataset sigue sin aprobación humana. Las consultas son sintéticas. Esta comparación no describe agricultores reales y la versión no entra en producción.

## Errores de la prueba ilustrativa

Esos tres textos no se usaron para entrenar ni para elegir esta configuración.

- Sulfato de potasio en el cafeto. `potasio`, `sulfato`, `cafeto` y `llenando` no aparecen en el entrenamiento, así que no están en el vocabulario. El modelo vio `grano`, y esa palabra cae sobre todo en cosecha (20 de 44 usos en entrenamiento). `abono` empujaba a fertilización, pero no alcanzó.
- Tallo seco de granadilla. `pudrición` sí empuja a enfermedades. `tallo` pesa más hacia plagas y está repartido (9 y 9). La puntuación quedó en un casi empate, 0,19 frente a 0,17.
- Palo del frijol. `palo` y `trepe` no están en el entrenamiento. `tutor` y `amarro` aparecen una sola vez y la versión 1 los descartó con `min_df=2`. El aporte mayor hacia cosecha fue la palabra funcional `lo`.
- Fuera de alcance. El modelo solo conoce ocho clases y siempre elige una. Una puntuación baja no identifica una consulta fuera de alcance.
- Empates. Un margen pequeño indica dos categorías agrícolas próximas, no una consulta ajena al cultivo.
- Las puntuaciones de `predict_proba` no están calibradas.

En la prueba bloqueada de la versión 1, riego fue la clase con más confusiones: 6 de 40, sobre todo con fertilización y cosecha. El patrón encaja con palabras compartidas (`grano`, `seco`), no con un fallo de lectura del archivo.

## Qué se cambió

Se buscó, solo dentro de las 1.276 consultas de entrenamiento de la versión 1, entre `min_df` 1 o 2, `C` 1 o 4, quitar o no las palabras funcionales, y unir o no los acentos. El criterio fue el macro-F1 medio de 5 pliegues estratificados, semilla 42. La prueba de 319 consultas quedó cerrada.

Configuración elegida: min_df=2, C=4.0, sin palabras funcionales=False, sin acentos=True. Macro-F1 de validación: 0.9408.

Abstención: devolver `sin categoría` si el margen entre las dos clases punteras es menor que 0.17. Ese corte salió del barrido sobre las probabilidades fuera de pliegue del entrenamiento, exigiendo al menos 85% de consultas clasificadas. `sin categoría` es abstención. No es `fuera_de_alcance` y no es una novena clase.

No se añadieron frases para cubrir potasio, cafeto o el palo del frijol. Habría sido usar la prueba de inferencia para forzar el acierto.

## Comparación en la misma prueba

- Versión 1. Accuracy 0.9467. Macro-F1 0.9463.
- Versión 2, sin abstención. Accuracy 0.9655. Macro-F1 0.9652.

Versión 2:

| Categoría | Precision | Recall | F1 | Soporte |
| --- | ---: | ---: | ---: | ---: |
| riego | 0.9459 | 0.8750 | 0.9091 | 40 |
| fertilizacion_nutricion | 0.9302 | 1.0000 | 0.9639 | 40 |
| plagas | 0.9286 | 0.9750 | 0.9512 | 40 |
| enfermedades_cultivos | 0.9730 | 0.9231 | 0.9474 | 39 |
| siembra_manejo_cultivo | 1.0000 | 1.0000 | 1.0000 | 40 |
| clima_heladas | 1.0000 | 1.0000 | 1.0000 | 40 |
| suelos | 1.0000 | 0.9750 | 0.9873 | 40 |
| cosecha_poscosecha | 0.9512 | 0.9750 | 0.9630 | 40 |

Con el umbral ya fijado, en esa misma prueba:

- Clasificadas: 285 de 319 (89.3%).
- Abstenciones: 34 (10.7%).
- Accuracy entre las clasificadas: 0.9930.
- Macro-F1 entre las clasificadas: 0.9925.
- Errores entre las clasificadas: 2.

Esas cifras de abstención en prueba no se usaron para mover el corte.

## Sondas que no ajustaron el modelo

- Anexo fuera de alcance, 12 consultas: 9 abstenidas y 3 siguieron recibiendo una de las ocho.
- Cola ambigua, 16 consultas: 9 abstenidas y 7 recibieron una categoría.

Lectura posterior de las 21 consultas ilustrativas, también sin usarla para ajustar:

| Id | v1 | v2 | Salida v2 | Margen |
| --- | --- | --- | --- | ---: |
| inf-01 | riego | riego | riego | 0.6903 |
| inf-02 | riego | riego | riego | 0.6313 |
| inf-03 | cosecha_poscosecha | fertilizacion_nutricion | sin categoría | 0.1101 |
| inf-04 | fertilizacion_nutricion | fertilizacion_nutricion | fertilizacion_nutricion | 0.2426 |
| inf-05 | plagas | plagas | plagas | 0.6485 |
| inf-06 | plagas | plagas | plagas | 0.8107 |
| inf-07 | enfermedades_cultivos | enfermedades_cultivos | enfermedades_cultivos | 0.5083 |
| inf-08 | plagas | plagas | sin categoría | 0.0680 |
| inf-09 | siembra_manejo_cultivo | siembra_manejo_cultivo | siembra_manejo_cultivo | 0.7294 |
| inf-10 | cosecha_poscosecha | cosecha_poscosecha | sin categoría | 0.1074 |
| inf-11 | clima_heladas | clima_heladas | clima_heladas | 0.4626 |
| inf-12 | clima_heladas | clima_heladas | clima_heladas | 0.6480 |
| inf-13 | suelos | suelos | suelos | 0.6313 |
| inf-14 | suelos | suelos | suelos | 0.2431 |
| inf-15 | cosecha_poscosecha | cosecha_poscosecha | cosecha_poscosecha | 0.1907 |
| inf-16 | cosecha_poscosecha | cosecha_poscosecha | cosecha_poscosecha | 0.9083 |
| inf-17 | riego | riego | sin categoría | 0.0649 |
| inf-18 | riego | riego | riego | 0.1925 |
| inf-19 | clima_heladas | clima_heladas | sin categoría | 0.0290 |
| inf-20 | plagas | plagas | plagas | 0.2624 |
| inf-21 | riego | riego | riego | 0.2546 |

## Datos que faltan para evaluar la abstención

- Consultas fuera de alcance confirmadas por una persona, separadas de las agrícolas ambiguas, y que no entren al entrenamiento. Doce ejemplos sintéticos no alcanzan.
- Consultas agrícolas con dos decisiones de igual peso, marcadas como ambiguas y no forzadas a una clase. Dieciséis ejemplos pendientes no alcanzan.
- Etiquetas resueltas del conjunto principal. Hoy siguen siendo propuestas.
- Consultas reales de productores, en otro conjunto, antes de hablar de uso en chacra.

## Limitaciones

- El macro-F1 alto sigue midiendo textos sintéticos con la etiqueta propuesta.
- Quitar palabras funcionales o bajar `min_df` no crea las palabras que el entrenamiento nunca vio.
- El corte se calculó con modelos de pliegues y se aplica al modelo reajustado con todo el entrenamiento. La escala del margen puede moverse un poco.
- Una puntuación baja no se traduce a fuera de alcance.
- `predict_proba` no está calibrada.
- El PMV1, el RAG, RAGAS, la taxonomía y la base de conocimientos no se modificaron.

Versiones: python 3.13.7, plataforma Windows-11-10.0.26200-SP0, scikit-learn 1.9.1, numpy 2.5.3, joblib 1.6.0.
