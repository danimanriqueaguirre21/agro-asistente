# Preparación para la revisión independiente

No entregar este informe al revisor. Contiene el estado de las revisiones anteriores. El revisor solo debe recibir `INSTRUCCIONES_REVISOR.md`, `consultas_57.jsonl`, `casos_3.jsonl` y la plantilla vacía.

Fecha: 18 de octubre de 2026.

## Estado actual del piloto

`piloto_hu07_v2` sigue `pendiente_de_revision_humana`. `training_dataset` sigue `no_aprobado`. `is_training_set` es false. No hay particiones. No hay modelo entrenado.

Las 192 consultas aceptadas son sintéticas. No son consultas reales de agricultores. Las 5 rechazadas del anexo siguen rechazadas y no entran en este paquete.

La auditoría y el cierre los hizo un mismo agente. Eso no cuenta como revisión humana independiente. Este paquete no inventa un segundo dictamen y no deja la plantilla llena.

## Consultas pendientes

| Grupo | Cantidad | Situación |
|---|---:|---|
| Segunda revisión, aún sin otro revisor | 57 | Van en `consultas_57.jsonl` |
| Casos que el cierre dejó sin etiqueta definitiva | 3 | Van en `casos_3.jsonl` |
| Total en este paquete, sin dictamen independiente | 60 | La plantilla está vacía |
| Resto de las 192, fuera de este paquete | 132 | El primer agente no pidió segunda lectura. Eso no las aprueba. |
| Rechazadas del anexo original | 5 | Siguen aparte |

De los 3, el cierre propuso mantener 2 como ambiguas y 1 como rechazo por quedar fuera de las ocho categorías. Esas propuestas no están en los archivos del revisor y no se aplicaron a los originales. El detalle está solo en `sellado_hasta_despues/correspondencia_ids.json`.

## Archivos preparados

Para el revisor:

- `INSTRUCCIONES_REVISOR.md`
- `consultas_57.jsonl`
- `casos_3.jsonl`
- `plantilla_registro.jsonl`
- `plantilla_registro.md`

Sellado, para después de la revisión:

- `sellado_hasta_despues/correspondencia_ids.json`
- `sellado_hasta_despues/LEEME_NO_ENTREGAR.md`

Los textos del revisor no llevan categoría, cultivo como campo, región como campo, nota de frontera ni identificador `piloto-v2-`. El orden de los `revision_id` sale de una semilla guardada en el archivo sellado. Esa semilla no reparte entrenamiento, validación ni prueba.

## Procedimiento para comparar las dos revisiones

1. Recibir la plantilla llena por otra persona, no por el agente que hizo la auditoría.
2. Comprobar que hay 60 `revision_id`, de `rev-001` a `rev-060`, sin repetidos y sin filas nuevas.
3. Comprobar cada `estado`:
   - `propuesta` trae un solo código de las ocho categorías;
   - `pendiente` trae la categoría vacía;
   - `rechazo_propuesto` trae la categoría vacía.
4. Rechazar la plantilla si aparece `sin categoría`, un código nuevo, o una categoría junto a `pendiente` o `rechazo_propuesto`.
5. Abrir entonces `sellado_hasta_despues/correspondencia_ids.json` y unir por `revision_id`.
6. Clasificar, sin cambiar los originales:
   - acuerdo: `estado` es `propuesta` y el código es igual a `categoria_original`;
   - desacuerdo: `estado` es `propuesta` y el código es otro de los ocho;
   - ambiguo: `estado` es `pendiente`;
   - rechazo propuesto: `estado` es `rechazo_propuesto`.
7. Escribir esa comparación en una carpeta nueva. No sobrescribir `piloto_hu07_v2/` ni esta plantilla vacía.
8. Un desacuerdo o un pendiente no se cierra por mayoría automática. Lo arbitra una persona. Mientras tanto, `resolved_category` sigue vacío y la fila no entra a un conjunto etiquetado definitivo.

## Condiciones para aprobar el dataset

Todas hacen falta. Cumplir una sola no aprueba el piloto.

1. Otra persona, distinta de quien escribió la auditoría y este paquete, completa la plantilla.
2. Los acuerdos, desacuerdos, pendientes y rechazos quedan escritos en un informe de comparación.
3. Cada desacuerdo tiene arbitraje humano y una sola categoría, o sale del conjunto etiquetado.
4. Cada `pendiente` sigue fuera del dataset etiquetado. No se guarda como `sin categoría`.
5. Cada `rechazo_propuesto` confirmado queda fuera de las aceptadas y no se mezcla con el anexo original sin dejar constancia en un archivo nuevo.
6. Los 3 casos de `casos_3.jsonl` no entran al dataset etiquetado mientras sigan ambiguos o fuera de las ocho categorías.
7. Las 5 rechazadas de `rechazadas_v2.jsonl` no se reutilizan como aceptadas.
8. No entran los 24 `ilustrativo-*`, las 800 consultas sintéticas anteriores, ni textos de RAGAS, `knowledge/` o pruebas del backend.
9. No se crean particiones de entrenamiento, validación o prueba antes de esa aprobación.
10. No se entrena un modelo antes de esa aprobación.
11. La taxonomía y el esquema 1.0.0 siguen sin cambios. La etiqueta, si llega a existir, es solo `category`.

Hasta que eso ocurra, el piloto permanece pendiente de aprobación.

## Control de integridad

Estos SHA-256 se calcularon antes de escribir el paquete y seguían iguales al cerrarlo.

| Archivo | SHA-256 |
|---|---|
| `piloto_hu07_v2/aceptadas_v2.jsonl` | `09b908b4ae89dce38be3e1a9cd1f8bbf479f5b071f22d8501318dfbe9fe6d28a` |
| `piloto_hu07_v2/rechazadas_v2.jsonl` | `0d0590d76f94b6c0b81e6a008d319e12f04ec3afe69e5712ffdc3a3d84425893` |
| `piloto_hu07_v2/manifiesto_v2.json` | `b1f019f562e927a8f7b448ce00e1876507afe7e4b77a7b55fcd3f9359e30e7ba` |
| `piloto_hu07_v2/fuentes_v2.json` | `0e47e14e05a2b1068d6fac805d3dfb0f5c0aff3533b4c21031de87dbb9df919a` |
| `auditoria_hu07_v2/INFORME_AUDITORIA_PILOTO_HU07.md` | `f4f1115a349cf69b39e979d7f9e310f5a1bd4d202990df563b048b2c2883168e` |
| `auditoria_hu07_v2/cierre_revision_humana/01_tres_casos_dudosos.md` | `c127dd8c75597717e09e108f00850d1ab7629760e36266ea47c8b01877ad9cc5` |
| `auditoria_hu07_v2/cierre_revision_humana/02_segunda_revision_57.md` | `70ebef4bdc80d4e8dafc4429be293dcb33c2babb46017d337d4df28d71bbc875` |
| `auditoria_hu07_v2/cierre_revision_humana/03_acuerdos_desacuerdos_pendientes.md` | `ae662ffeb9b7d12c552c731fa35ab12a03bdfd1604980ba85ef933c67a182399` |
| `auditoria_hu07_v2/cierre_revision_humana/04_cambios_propuestos.md` | `d5bd839214634db3e266ba1e60aec526a28c3ce01fd5793335ea005be0e73b25` |
| `auditoria_hu07_v2/cierre_revision_humana/05_estado_final_piloto.md` | `be68e22999d12fdb890d48776106580526b922670e8b8927909c0f83acac1c4c` |
| `backend/clasificacion/taxonomia/taxonomia_consultas_v1.json` | `688e33afdaca178a845c1a28e8349c2aec5c2c972b3fa5da0dd1aa335067f806` |
| `backend/clasificacion/esquema/esquema_dataset_v1.json` | `5ff9c5cc5588dd58c068a68066416332da962ca18dc01e663b15bce6b5be7abc` |
