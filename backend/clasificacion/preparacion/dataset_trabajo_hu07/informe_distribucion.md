# Informe de distribución

Fuente: `controles.json`, generado junto con `consultas_trabajo.jsonl`. SHA-256 del JSONL: `16fd1dfbf3e0589995931b5a42da47bf0ff677ab04cf1fba2c1a7f7536c164fd`.

La meta de preparación era 200 consultas por categoría, 1.600 en total. Esa meta se cumplió como conteo de preparación. No es una prueba de suficiencia estadística ni una aprobación.

| Categoría | Registros | Menos de 12 palabras | De 12 a 30 | Más de 30 | Coincidencias con el patrón léxico de la clase |
| --- | ---: | ---: | ---: | ---: | ---: |
| riego | 200 | 12 | 180 | 8 | 81 |
| fertilizacion_nutricion | 200 | 15 | 177 | 8 | 139 |
| plagas | 200 | 12 | 180 | 8 | 96 |
| enfermedades_cultivos | 200 | 12 | 180 | 8 | 126 |
| siembra_manejo_cultivo | 200 | 12 | 180 | 8 | 90 |
| clima_heladas | 200 | 12 | 180 | 8 | 152 |
| suelos | 200 | 12 | 180 | 8 | 120 |
| cosecha_poscosecha | 200 | 12 | 180 | 8 | 34 |

El patrón léxico es un conteo automático de palabras típicas de cada clase. No valida la etiqueta. En cosecha y poscosecha el conteo es bajo (34 de 200) porque muchas consultas dicen «corto», «guardo» o «saco» y el patrón busca «cosecha», «secado», «almacén» u «oreo».

Otras cifras del mismo control:

- 1.300 registros nombran un solo cultivo de la lista de referencia. Los otros 300 nombran ninguno o más de uno, y `crop` queda null.
- 1.227 nombran una sola región válida (Junín o una provincia). Los otros 373 dejan `region` en null.
- 146 llevan una observación de frontera.
- 1.600 siguen pendientes de revisión humana.
- 0 son consultas reales.
- 16 casos ambiguos y 12 fuera de alcance van en anexos y no entran en las 1.600.

Estado: no aprobado. `is_training_set` permanece en false.
