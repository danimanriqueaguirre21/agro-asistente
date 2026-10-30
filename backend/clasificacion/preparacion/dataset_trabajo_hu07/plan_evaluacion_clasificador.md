# Plan de evaluación del clasificador

Este plan no entrena un modelo y no calcula métricas. El archivo de trabajo no está aprobado y no tiene particiones.

## Cuándo se podrá evaluar

Solo después de que una revisión humana independiente deje un conjunto con etiquetas resueltas, con `approval_status` puesto por una persona y con `is_training_set` todavía en false hasta ese cierre. Las consultas que sigan pendientes, ambiguas o fuera de alcance no entran a entrenamiento, validación ni prueba.

Los resultados sobre texto sintético no se extienden a consultas reales de productor.

## Partición

No hay partición en este directorio. Cuando exista un conjunto aprobado:

1. Agrupar duplicados exactos, esqueletos iguales y pares cercanos (como el par de la polilla del olluco). El grupo entero va a una sola partición.
2. Estratificar por la categoría ya resuelta.
3. Guardar la semilla en el manifiesto. Hoy `split_seed` es null.
4. Usar tres particiones disjuntas. La validación elige el umbral de abstención. La prueba no se usa para elegirlo.
5. Las proporciones se fijan cuando se conozca el tamaño del conjunto aprobado. Este plan no las promete.

El modelo, si algún día se entrena, usa solo el texto. No usa el id, la nota, el origen, el cultivo ni la región como rasgos.

## Métricas previstas

Sobre la partición de prueba, y solo entonces:

- accuracy
- precision, recall y F1 por clase
- macro-F1
- matriz de confusión
- evaluación de la abstención

La abstención responde «sin categoría» cuando la confianza no alcanza el umbral elegido en validación, cuando el modelo no está disponible o cuando la salida no es una de las ocho categorías. «sin categoría» no es una clase de entrenamiento.

Esas métricas no se presentan en este informe porque el modelo no se entrenó.
