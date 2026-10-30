# Auditoría de etiquetas — dataset de trabajo HU-07

Fecha de la auditoría: 2026-10-18.

Archivo auditado: `backend/clasificacion/preparacion/dataset_trabajo_hu07/consultas_trabajo.jsonl`.
SHA-256 sin cambios: `16fd1dfbf3e0589995931b5a42da47bf0ff677ab04cf1fba2c1a7f7536c164fd`.

Este informe no aprueba el dataset, no cambia etiquetas y no entrena un modelo. Las 1.600 consultas siguen siendo sintéticas (`origin`: `sintetico_preparacion`, `is_real_query`: false, `review_status`: `pendiente_revision_humana`).

Criterio usado: la categoría es la decisión que la consulta pide resolver, según `REGLAS_ETIQUETADO.md`. El cultivo, la provincia y la nota de frontera no son la etiqueta. Una consulta que pide dos acciones con el mismo peso no se fuerza a una clase.

## Resultado

No aparece un bloque de etiquetas invertidas. La mayor parte de las 1.600 propuestas coincide con la decisión que el texto pide. Los controles de duplicados no se toman como aprobación.

Quedan casos que la regla ya saca del conjunto etiquetado, casos que un revisor tiene que dirimir, y dos problemas de calidad que no son un cambio de categoría.

## Resumen por categoría

| Categoría | Registros | Con nota de frontera | La nota sostiene la propuesta | Revisión humana de etiqueta | Lectura de la auditoría |
| --- | ---: | ---: | ---: | ---: | --- |
| riego | 200 | 23 | 21 | 2 | El agua es la decisión, aunque se nombre la cosecha o la helada como momento. |
| fertilizacion_nutricion | 200 | 36 | 33 | 3 | El abono o la carencia es la decisión. El aporque o la cosecha solo ubican el momento. |
| plagas | 200 | 21 | 20 | 1 | Hay un animal que daña. Ardilla, nematodo y babosa caben en la taxonomía. |
| enfermedades_cultivos | 200 | 22 | 18 | 4 | La mancha o la pudrición es la decisión. Mencionar un insecto para descartarlo no cambia la clase. |
| siembra_manejo_cultivo | 200 | 20 | 18 | 2 | Fecha, distancia, poda, tutor y aporque. La helada o la cosecha aparecen como contexto. |
| clima_heladas | 200 | 10 | 7 | 3 | Helada, granizo, sequía, viento o lluvia como evento. |
| suelos | 200 | 8 | 8 | 0 | Erosión, drenaje, costra, profundidad o compactación. |
| cosecha_poscosecha | 200 | 6 | 5 | 1 | Corte, secado, oreo, selección, guarda y beneficio en finca. |
| Total | 1600 | 146 | 130 | 16 | |

Las 16 de la última columna están listadas abajo. No se les cambió la etiqueta.

Cosecha y poscosecha, revisada aparte: las 200 hablan de madurez, corte, secado, fermentado del cacao, oreo o guarda. El patrón léxico automático solo marca 34 de 200 porque el texto dice «corto», «guardo» o «saco» y el patrón busca «cosecha», «secado» o «almacén». Eso no es un error de clase. Hay una sola frontera que sigue abierta (lluvia sobre el secado de la quinua).

## Lista de posibles errores

No se encontró una etiqueta que la regla invierta de forma unívoca hacia otra clase. Lo que sí hay son consultas compuestas metidas en las 1.600. La regla dice que esas filas no entran al conjunto etiquetado hasta que una persona elija una sola decisión. Forzarlas a la categoría propuesta es el error de disposición, no una corrección automática de código.

| ID | Etiqueta actual | Alternativa | Por qué es un error de disposición |
| --- | --- | --- | --- |
| trabajo-hu07-ead432668d | riego | suelos | Pregunta las dos cosas: si el agua entra o si primero se rompe la costra. |
| trabajo-hu07-77fa929ec0 | fertilizacion_nutricion | siembra_manejo_cultivo | Pregunta si el estiércol y el deshierbo son decisiones distintas. |
| trabajo-hu07-b7bf806a37 | enfermedades_cultivos | plagas | Pregunta si la fumagina se mira como enfermedad o si primero se busca el insecto. |
| trabajo-hu07-7791383f85 | enfermedades_cultivos | clima_heladas | Pregunta si el borde morado es enfermedad y no el frío. |

Esas cuatro salen de las 1.600 y quedan pendientes. No se les asigna la alternativa por script.

En el anexo, no en las 1.600:

| ID | Problema | Corrección por regla |
| --- | --- | --- |
| ambigua-198e86ea7a | `candidate_categories` incluye `fuera_de_alcance`. Ese valor no es una de las ocho categorías. | Si la ceniza no es un abono, la fila va a `fuera_de_alcance.jsonl`. No entra a las 1.600. |

## Lista de casos que requieren revisión humana

La regla no elige un ganador. Siguen con la propuesta actual y con `resolved_category` vacío.

| ID | Etiqueta actual | Alternativa | Razón de la duda |
| --- | --- | --- | --- |
| trabajo-hu07-6310e70aca | riego | suelos | Después de regar aparece costra y la duda es si el agua volverá a entrar. |
| trabajo-hu07-d0c408757f | riego | clima_heladas | Regar en una mañana de helada seca. La nota dice que la decisión es la humedad. La helada sigue en la frase. |
| trabajo-hu07-9659612ab0 | fertilizacion_nutricion | cola ambigua | Ceniza de cocina «solo como aporte». La nota admite dejarla ambigua. No es la frase del piloto. |
| trabajo-hu07-20392819ed | fertilizacion_nutricion | suelos | El análisis de fósforo se usa para abonar, o el fin era conocer el terreno. El tema ya está en `ambigua-45301ad12c`. |
| trabajo-hu07-beb6b836e3 | plagas | enfermedades_cultivos | Pelusa blanca: ¿insecto o hongo? |
| trabajo-hu07-ae638b74f3 | enfermedades_cultivos | plagas | Polvo blanco que no se mueve. La nota dice que un ácaro la volvería ambigua. |
| trabajo-hu07-5a8d38f56b | enfermedades_cultivos | cosecha_poscosecha | Pudrición del kion en pie, frente a un rizoma que se malogró después de sacarlo. |
| trabajo-hu07-4070bf7ab7 | siembra_manejo_cultivo | clima_heladas | Aporque de la papa y helada de la mañana. La nota dice que, si pesan igual, se mueve. |
| trabajo-hu07-33f205f8fe | siembra_manejo_cultivo | cosecha_poscosecha | Quitar el fruto bajo de la papaya: manejo de la planta o cosecha. |
| trabajo-hu07-6493a2ec5e | clima_heladas | suelos o riego | La lluvia encharcó la flor del café. La nota abre drenaje o riego. |
| trabajo-hu07-4cfb645653 | clima_heladas | cosecha_poscosecha | El viento partió un racimo de plátano que estaba por madurar. |
| trabajo-hu07-fa9a5283d3 | clima_heladas | enfermedades_cultivos | El viento dejó la hoja del café sucia de polvo. |
| trabajo-hu07-3de8a9c50c | cosecha_poscosecha | clima_heladas | Tapar el secado de la quinua si viene lluvia. |

No son cambio de categoría. Sí impiden entrenar tal cual:

| ID | Etiqueta actual | Problema |
| --- | --- | --- |
| trabajo-hu07-4da2de2e03 | plagas | Paráfrasis de `ilustrativo-007` (gusanos verdes en la papa). Quedó bajo el umbral automático de Jaccard 0,55. No entra a entrenamiento. |
| trabajo-hu07-d6612d79a4 y trabajo-hu07-628a8b17ab | plagas | Par más cercano del archivo (Jaccard 0,55). La segunda frase está mal cerrada y nombra papa y olluco, por eso `crop` quedó null. Misma clase. Van juntas en cualquier partición futura. |
| trabajo-hu07-0caaaf7615, trabajo-hu07-02f546802a | enfermedades_cultivos | Describen un síntoma y no formulan la decisión. La clase propuesta es coherente con la mancha. Un revisor decide si sirven como consulta. |

## Anexos, sin incorporarlos a las 1.600

Cola ambigua, 16 registros. `status` pendiente y `resolved_category` vacío. No tienen una sola categoría propuesta. Los temas (riego y abono a la vez, hoja amarilla sin causa, polvo blanco, ceniza, análisis de suelo, mancha después de la lluvia, agua de helada o de riego, pudrición en guarda, maleza y gusano, siembra con helada anunciada, charco de riego o de suelo, bicho y humedad en almacén, hoja comida y manchada, preparar terreno y sembrar, grano húmedo con polvillo) coinciden con la regla de empate. No se resolvieron.

Fuera de alcance, 12 registros. Precio, crédito, receta, vacuna de ganado, licencia, camioneta, aduana, horario de oficina, IGV, escuela, multa por quemar rastrojo y día de feria. La multa nombra la terraza, pero la decisión es la sanción, no el suelo. No pasan al conjunto principal.

## Recomendaciones para cerrar la revisión

1. Dos personas, distintas de quien redactó los textos, leen primero el texto y después la propuesta.
2. Las cuatro consultas compuestas salen de las 1.600 y quedan en la cola, sin categoría resuelta, hasta que haya acuerdo en una sola.
3. Las trece de revisión humana se cierran una por una. Si no hay acuerdo, siguen pendientes.
4. `ambigua-198e86ea7a` no usa `fuera_de_alcance` como si fuera una categoría de la taxonomía.
5. `trabajo-hu07-4da2de2e03` no se usa en entrenamiento. El par de la polilla del olluco no se separa entre particiones.
6. Cosecha no se reetiqueta por el conteo léxico de 34 sobre 200.
7. Pasar el control de duplicados no aprueba ninguna fila.
8. No se entrena TF-IDF ni regresión logística, y no se integra un clasificador, mientras `approval_status` siga en `no_aprobado`.

Estado final: dataset no aprobado. Sin entrenamiento. Sin integración en producción.
