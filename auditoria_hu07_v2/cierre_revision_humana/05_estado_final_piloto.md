# Estado final del piloto HU-07 v2

Fecha: 18 de octubre de 2026.

## Dictamen

El piloto **permanece pendiente de aprobación**. No está aprobado para entrenamiento. No se declara cerrado el conjunto.

Falta la revisión humana independiente de las 57 consultas y la decisión humana sobre los dos casos ambiguos. El rechazo del olluco está propuesto y no aplicado. Ninguna de esas salidas es una etiqueta definitiva.

## Cantidades

| Concepto | Cantidad |
|---|---:|
| Consultas originales en `aceptadas_v2.jsonl` | 192 |
| Acuerdos entre revisores | 0 |
| Desacuerdos entre revisores | 0 |
| Pendientes de segundo revisor humano | 57 |
| Casos ambiguos sin resolver | 2 |
| Rechazo propuesto por fuera de las ocho categorías, no aplicado | 1 |
| Correcciones de texto o de etiqueta de reemplazo propuestas | 0 |
| Resoluciones finales | 0 |
| Rechazadas del anexo original, separadas y sin reutilizar | 5 |

## Qué se comprobó

- Los cuatro archivos de `piloto_hu07_v2/` y el informe de auditoría conservan el mismo SHA-256 que al empezar esta fase.
- Las 57 fichas están en `02_segunda_revision_57.md`: 48 con nota de frontera y 9 sin nota.
- Los tres casos dudosos están en `01_tres_casos_dudosos.md`.
- No se emitió ningún código fuera de los ocho. El segundo revisor no emitió códigos.
- Las pendientes y el rechazo propuesto no se incorporaron a un conjunto etiquetado definitivo. No se creó un jsonl de ítems.
- `rechazadas_v2.jsonl` no recibió filas nuevas y no se usó para aceptar nada.
- No se modificó el PMV1, el backend, el frontend, la base de datos, el RAG, RAGAS, la taxonomía ni el esquema.
- No se instalaron dependencias. No se entrenó ningún modelo. No hay particiones.

## Formato que permite el esquema

`esquema_dataset_v1.json` exige `id`, `text` y `category` en cada ítem. `category` tiene que ser una de las ocho. `sin categoría` no es clase de esta versión. La política de ambiguas dice que la cola es una estructura conceptual, sin archivo propio, con `resolved_category` vacío mientras `status` sea pendiente.

Un archivo de ítems con categoría vacía, o con `sin categoría`, contradiría el esquema. Un informe auxiliar en markdown no es un ítem de dataset: no lleva `category` como etiqueta y no entra a entrenamiento. Estos cinco informes usan ese camino.

## Hashes de control

| Archivo | SHA-256 |
|---|---|
| `piloto_hu07_v2/aceptadas_v2.jsonl` | `09b908b4ae89dce38be3e1a9cd1f8bbf479f5b071f22d8501318dfbe9fe6d28a` |
| `piloto_hu07_v2/rechazadas_v2.jsonl` | `0d0590d76f94b6c0b81e6a008d319e12f04ec3afe69e5712ffdc3a3d84425893` |
| `piloto_hu07_v2/manifiesto_v2.json` | `b1f019f562e927a8f7b448ce00e1876507afe7e4b77a7b55fcd3f9359e30e7ba` |
| `piloto_hu07_v2/fuentes_v2.json` | `0e47e14e05a2b1068d6fac805d3dfb0f5c0aff3533b4c21031de87dbb9df919a` |
| `auditoria_hu07_v2/INFORME_AUDITORIA_PILOTO_HU07.md` | `f4f1115a349cf69b39e979d7f9e310f5a1bd4d202990df563b048b2c2883168e` |

## Limitación que deja el piloto abierto

La segunda revisión humana independiente no se pudo hacer en esta herramienta. El agente que auditó las 192 es el mismo que documenta este cierre. Las 57 siguen pendientes. El piloto no queda aprobado.

## Entregables

- `01_tres_casos_dudosos.md`
- `02_segunda_revision_57.md`
- `03_acuerdos_desacuerdos_pendientes.md`
- `04_cambios_propuestos.md`
- `05_estado_final_piloto.md`
