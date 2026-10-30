# Revisión de los tres casos dudosos

Fecha: 18 de octubre de 2026.
Fuente de los textos: `piloto_hu07_v2/aceptadas_v2.jsonl`, leído y no modificado.
Criterio: `backend/clasificacion/taxonomia/taxonomia_consultas_v1.json` 1.0.0 y `backend/clasificacion/REGLAS_ETIQUETADO.md`.

Esta fase la cierra el mismo agente que escribió `auditoria_hu07_v2/INFORME_AUDITORIA_PILOTO_HU07.md`. No es un segundo revisor. No se añade contexto que la pregunta no trae. No se cambia el registro original.

El esquema 1.0.0 exige `category` en todo ítem de dataset y prohíbe guardar `sin categoría`. La cola de ambiguas es una estructura conceptual, sin archivo de ítems. Por eso estos tres casos viven solo en este informe.

## piloto-v2-04805c4db9

- **Texto original:** ¿Sirve la ceniza de cocina en el huerto?
- **Categoría original:** `fertilizacion_nutricion`
- **Cultivo y región:** no constan. El texto tampoco los nombra.
- **Intención que el texto expresa:** pregunta si la ceniza de cocina sirve en el huerto. No dice para nutrir, para un animal ni para el terreno.
- **Categoría defendible:** no.
- **Aplicación de la regla:** fertilización incluye compost, guano o fertilizante cuando el fin es nutrir. Plagas exige un organismo que come, pica o daña. Suelos exige una decisión sobre el terreno. El texto no elige ninguno de esos fines. Las tres lecturas pesan lo mismo porque todas añaden un fin que la frase no trae.
- **Candidatas, sin elección:** `fertilizacion_nutricion`, `plagas`, `suelos`
- **Resultado de esta fase:** ambiguo. `status`: pendiente. `resolved_category`: vacío.
- **Resolución final:** no existe.
- **Evaluación del primer revisor:** categoría dudosa, confianza baja, sin etiqueta nueva.
- **Evaluación del segundo revisor:** no realizada.

## piloto-v2-99b5624803

- **Texto original:** ¿Lavo el polvo blanco del brote?
- **Categoría original:** `enfermedades_cultivos`
- **Cultivo y región:** no constan.
- **Intención que el texto expresa:** pregunta si lavar un polvo blanco que está en el brote. No pide el nombre del polvo, no nombra un animal y no dice que sea una enfermedad.
- **Categoría defendible:** no.
- **Aplicación de la regla:** enfermedades incluye polvo de roya, manchas, pudrición y el manejo de una enfermedad. Plagas exige un animal visto. Aquí no hay animal visto, y «polvo blanco» tampoco es el polvo de roya nombrado en la taxonomía. Decir que es un hongo, o que es cera de un insecto, sería inventar la causa. Las dos lecturas quedan con el mismo peso.
- **Candidatas, sin elección:** `enfermedades_cultivos`, `plagas`
- **No se funde con** `piloto-v2-464c8602df`, que pregunta qué es el polvo del envés de la papa. Esa otra frase pide identificar y está fuera de estos tres casos.
- **Resultado de esta fase:** ambiguo. `status`: pendiente. `resolved_category`: vacío.
- **Resolución final:** no existe.
- **Evaluación del primer revisor:** categoría dudosa, confianza media, sin etiqueta nueva.
- **Evaluación del segundo revisor:** no realizada.

## piloto-v2-41bdf8b563

- **Texto original:** ¿El olluco se vende el mismo día?
- **Categoría original:** `cosecha_poscosecha`
- **Cultivo:** olluco, nombrado en el texto. **Región:** no consta.
- **Intención que el texto expresa:** pregunta si el olluco se vende el mismo día. No pregunta cuándo arrancarlo, cómo saber que está maduro, cómo secarlo, seleccionarlo, orearlo, guardarlo o beneficiarlo.
- **Categoría defendible dentro de las ocho:** no.
- **Aplicación de la regla:** cosecha y poscosecha cubre madurez, corte o arranque, secado, selección, oreo, almacenamiento y beneficio en finca. La venta no está en esa lista ni en las otras siete. Leer la frase como vida útil o guarda breve añade un problema de almacenamiento que la pregunta no formula.
- **Candidatas de las ocho:** ninguna con apoyo en el texto. No se deja `cosecha_poscosecha` como resolución.
- **Resultado de esta fase:** fuera de las ocho categorías.
- **Motivo del rechazo propuesto:** la decisión expresada es comercial. No es una de las ocho decisiones de la taxonomía 1.0.0.
- **Resolución final:** no existe. El rechazo queda propuesto en este informe y no se escribe en `aceptadas_v2.jsonl` ni en `rechazadas_v2.jsonl`.
- **Evaluación del primer revisor:** la dejó dudosa, por si alguien documentaba una guarda breve. Esta fase no usa esa lectura, porque el encargo prohíbe inventar contexto ausente.
- **Evaluación del segundo revisor:** no realizada. Un revisor humano puede todavía confirmar el rechazo o, si deja escrito otro sentido que el texto sí tenga, resolverlo. Este informe no anticipa esa decisión.

## Cierre de los tres

| Id | Etiqueta original | Esta fase | Resolución final |
|---|---|---|---|
| `piloto-v2-04805c4db9` | `fertilizacion_nutricion` | Ambiguo, pendiente | No existe |
| `piloto-v2-99b5624803` | `enfermedades_cultivos` | Ambiguo, pendiente | No existe |
| `piloto-v2-41bdf8b563` | `cosecha_poscosecha` | Fuera de las ocho; rechazo propuesto, no aplicado | No existe |

Ninguno entra a un conjunto etiquetado definitivo.
