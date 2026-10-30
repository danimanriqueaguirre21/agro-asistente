# Tareas pendientes para la aprobación

El dataset de trabajo no está aprobado. Estas condiciones tienen que cumplirse antes de llamar a un archivo «dataset de entrenamiento». Ninguna está cumplida hoy.

1. Revisión humana independiente, con el texto leído antes que la categoría propuesta. Quien redactó los ejemplos no cierra solo la revisión.
2. Regla de acuerdo entre al menos dos revisores. Sin coincidencia, el caso sigue pendiente o pasa a la cola ambigua.
3. Casos ambiguos resueltos en una sola categoría, o excluidos. `resolved_category` no se llena por defecto.
4. Casos fuera de alcance excluidos del entrenamiento.
5. Cero consultas pendientes dentro del archivo que se proponga para entrenar.
6. Paráfrasis, esqueletos iguales y pares cercanos en la misma partición. La semilla queda escrita en el manifiesto.
7. Sin cruce, al umbral ya usado, con la muestra ilustrativa, el preliminar de 80, el piloto, las preguntas RAGAS, `knowledge/` ni las frases de prueba del backend.
8. Cruce explícito contra las 800 consultas sintéticas anteriores, cuando ese archivo exista. Hoy no está en el repositorio y el cruce no se hizo.
9. Una persona asigna `approval_status`. No se asigna por script.
10. `is_training_set` sigue en false hasta ese acto. El origen sintético no se borra aunque la etiqueta se revise: revisar una etiqueta no convierte el texto en una consulta real.
11. Consultas reales solo si hay procedencia verificable. Hoy hay cero, y no se inventan.
12. La meta de 200 por categoría no se usa como argumento de suficiencia estadística.

Mientras eso no ocurra, no se entrena TF-IDF con regresión logística y no se integra un clasificador en el flujo de consultas.
