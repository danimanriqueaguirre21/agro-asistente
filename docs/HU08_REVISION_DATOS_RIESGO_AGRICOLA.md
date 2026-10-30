# HU-08 — Revisión de los datos disponibles para el riesgo agrícola

Actividad 2: preparar y revisar el conjunto de datos.

Esta revisión no entrena un modelo, no crea registros y no modifica el backend, la base de datos, los endpoints ni el flujo de consultas. Una observación meteorológica no es una etiqueta de riesgo.

Fecha de la inspección: 19 de octubre de 2026.

## Conclusión

No existe un conjunto de datos utilizable para entrenar un modelo supervisado de riesgo agrícola.

Lo que hay es estructura y datos de otro propósito:

- MySQL guarda agricultores, contextos, consultas, respuestas, documentos y evidencias. En la base local conectada, esas filas son de desarrollo y de prueba. No describen eventos de daño.
- SENAMHI WIS2 responde con observaciones recientes. El adaptador no las guarda y no conserva la unidad. Una consulta puntual confirma que el payload trae unidad; eso no deja una serie histórica en el repositorio.
- HU-07 tiene consultas sintéticas etiquetadas por tema. Esa etiqueta no es un nivel de riesgo.
- `knowledge/` y la línea base RAGAS son texto de prueba o recomendaciones genéricas, no un catálogo validado ni un registro de eventos.

Por eso no se creó un archivo de registros. Inventar filas o asignar niveles habría simulado evidencia.

## Fuentes inspeccionadas

Diseño de la actividad 1:

- `docs/HU08_VARIABLES_RIESGO_AGRICOLA.md`

Esquema y persistencia:

- `database/schema.sql`
- `backend/app/infrastructure/adapters/output/mysql/repositorio_contexto_agricola.py`
- Base `agro_asistente` abierta con la configuración del backend. La conexión respondió. No se escribió nada.

Contexto y meteorología:

- `backend/app/domain/entities/contexto_agricola.py`
- `backend/app/domain/valueObjects/cultivo.py`
- `backend/app/domain/valueObjects/region.py`
- `backend/app/domain/entities/observacion_meteorologica.py`
- `backend/app/infrastructure/adapters/output/senamhi/adaptador_senamhi_wis2.py`
- `backend/app/infrastructure/adapters/input/http/weather_controller.py`
- `backend/tests/test_adaptador_senamhi_wis2.py`
- `backend/tests/test_senamhi_wis2_integration.py`
- `backend/app/infrastructure/config/settings.py`

Otros archivos de datos que sí están en el repositorio:

- `backend/clasificacion/preparacion/dataset_trabajo_hu07/manifiesto_dataset_trabajo.json` y `consultas_trabajo.jsonl`
- `backend/clasificacion/taxonomia/taxonomia_consultas_v1.json`
- `backend/evaluation/data/pmv1_baseline.json`
- Markdown y metadatos de `knowledge/`

No hay CSV, parquet ni tabla de observaciones, plagas, suelos o niveles de riesgo. `SHOW TABLES` devolvió solo las seis tablas del esquema PMV1.

## MySQL

El esquema tiene seis tablas: `agricultores`, `contextos_agricolas`, `consultas`, `respuestas`, `documentos_conocimiento` y `evidencias`. Ninguna columna guarda estación, temperatura, precipitación, etapa fenológica, síntoma, análisis de suelo ni nivel de riesgo.

Conteo leído en la base local, sin modificarla:

| Tabla | Filas |
|---|---|
| agricultores | 290 |
| contextos_agricolas | 143 |
| consultas | 82 |
| respuestas | 82 |
| documentos_conocimiento | 38 |
| evidencias | 107 |

Esas filas no son un censo de agricultores de Junín. De 290 correos, 285 usan el dominio `example.com`, 4 usan `prueba.com` y 1 usa `agro.com`. No se listan direcciones ni nombres. Hay 148 agricultores sin contexto. Las fechas van del 21 de septiembre de 2026 al 19 de octubre de 2026.

### Contexto agrícola

Campos reales:

| Campo | Tipo en MySQL | Nulo | Qué se observó |
|---|---|---|---|
| cultivo | VARCHAR(100), obligatorio | No | 122 veces `papa` y 21 veces `maiz`. Texto libre, sin catálogo. |
| region | VARCHAR(100), obligatorio | No | 126 `Huancayo`, 12 `Cusco`, 2 `Puno`, 1 `Junín`, 1 `Juniín`, 1 `Sierra de Junin`. |
| nombre_parcela | VARCHAR(150), obligatorio | No | Sobre todo `Parcela 1` (116) y `Parcela RAG` (22). También hay nombres de validación. |
| observaciones | TEXT, opcional | En estas filas, ninguna vacía | 116 `Campana seca`, 22 `Prueba HU-06`, 3 `Zona con riesgo de heladas`, 1 `Zona con riesgo de altas heladas`, 1 `Validacion Ollama`. Longitud máxima: 32. |
| esta_seleccionado | TINYINT | Sí en el esquema | 105 contextos marcados. Ningún agricultor tiene más de uno seleccionado. |
| fecha_creacion | TIMESTAMP | Sí en el esquema | Presente en el rango indicado. |

La frase «riesgo de heladas» aparece dentro de una nota libre. No es una etiqueta verificada ni un nivel. No se usó para etiquetar nada.

Inconsistencias de esquema, sin corregirlas en este paso:

- El dominio limita el cultivo a 50 caracteres y la región a 120. MySQL admite 100 en ambos. El repositorio recorta cultivo y región a 100 al guardar. Una región de más de 100 caracteres se cortaría sin aviso.
- El dominio permite predio vacío. La columna `nombre_parcela` no acepta NULL. Si el dominio no trae nombre, el repositorio guarda cadena vacía.
- Las notas del dominio se limitan a 500 caracteres. La columna es TEXT.

Cultivo y región no están vacíos en las 143 filas. Tampoco hay coordenadas, altitud, etapa ni fecha de siembra.

### Consultas y respuestas

`consultas` guarda la pregunta en texto y la fecha. No guarda una categoría de riesgo. Hay 82 preguntas y solo 22 textos distintos. La más repetida es la pregunta de prueba sobre mejorar el cultivo de papa (48 veces). Las respuestas tienen `metodo_generacion`: 70 `template` y 12 `ollama`. Son ensayos del flujo de consulta, no resultados de daño en campo.

## SENAMHI

Configuración leída en `settings.py`:

- Base: `https://wis.senamhi.gob.pe/oapi`
- Colección: `urn:wmo:md:pe-senamhi:synop-hourly`
- Tiempo de espera: 20 segundos

El adaptador pide ítems OGC y agrupa, por reporte, tres nombres: `air_temperature`, `dewpoint_temperature` y `total_precipitation_or_total_water_equivalent`. El resto de variables se ignora. Si un valor no viene, el campo queda vacío. No se inventa un cero.

Campos del modelo interno:

| Campo | Tipo | Unidad guardada | Comprobación |
|---|---|---|---|
| identificador_estacion | texto | No aplica | Sale de `wigos_station_identifier`. Si falta, la observación se rechaza. |
| nombre_estacion | texto o vacío | No aplica | El adaptador escribe siempre `None`. No lee un nombre de estación. |
| latitud, longitud | número o vacío | Grados decimales, según el orden de la geometría (longitud, latitud) | Si no hay geometría, quedan vacías. |
| altitud | número o vacío | No etiquetada | Solo si la geometría trae una tercera coordenada. |
| fecha_hora | texto o vacío | No aplica | `reportTime` o, si no está, `phenomenonTime`. |
| temperatura | número o vacío | No guardada | Solo si `name` es `air_temperature`. |
| punto_rocio | número o vacío | No guardada | Solo si `name` es `dewpoint_temperature`. |
| precipitacion | número o vacío | No guardada | Solo si `name` es `total_precipitation_or_total_water_equivalent`. |

El endpoint `GET /api/v1/weather/observations` devuelve esa misma forma. El límite HTTP está entre 1 y 50. No hay tabla donde esas filas sobrevivan al cierre del proceso.

La prueba automática `test_adaptador_senamhi_wis2.py` usa un GeoJSON falso. Incluye `"units": "Celsius"` y números de ejemplo. El adaptador no lee `units`, y la prueba no exige que se conserven. Esos números no son observaciones archivadas.

La prueba de integración real está marcada para omitirse salvo que exista la variable de entorno `SENAMHI_WIS2_INTEGRATION=1`. No forma parte de la suite normal y no deja un archivo de datos.

### Comprobación puntual del API

El 19 de octubre de 2026 se consultó la colección, solo para ver claves y unidades. No se guardó el cuerpo ni los valores numéricos.

- Cinco ítems recientes, sin filtrar por variable: HTTP 200. Todos traían la propiedad `units`. En ese grupo aparecieron las etiquetas `Celsius`, `deg` y `hPa`, y los nombres `air_temperature`, `dewpoint_temperature`, `non_coordinate_pressure`, `pressure_reduced_to_mean_sea_level` y `wind_direction`. Dos de cinco geometrías traían altitud. Este grupo no es un inventario completo de SENAMHI.
- Tres ítems filtrados por `air_temperature`: unidad `Celsius`.
- Tres ítems filtrados por `dewpoint_temperature`: unidad `Celsius`.
- Tres ítems filtrados por `total_precipitation_or_total_water_equivalent`: unidad `kg m-2`.

Esa unidad se vio en esa respuesta. No autoriza a leer los números ya perdidos por el adaptador como grados ni como milímetros. El modelo interno no tiene dónde guardar `units`, así que una observación recuperada hoy no es interpretable de forma segura.

Tampoco hay, en el repositorio, pronóstico, temperatura mínima diaria, humedad relativa, viento ni una serie histórica descargada.

## Otros archivos

| Archivo | Qué es | ¿Sirve para riesgo? |
|---|---|---|
| `consultas_trabajo.jsonl` | 1600 consultas. El manifiesto dice origen `sintetico_preparacion`, `real_queries` 0 y dataset no aprobado. | No. La categoría temática no es un nivel de riesgo. |
| Anexos ambiguos y fuera de alcance | 16 y 12 textos de preparación de HU-07. | No. |
| Taxonomía `consultas-agricolas-junin` 1.0.0 | Lista de ocho temas. El dataset de entrenamiento sigue no aprobado. | No es una escala de riesgo. |
| `pmv1_baseline.json` | Seis preguntas RAGAS. El archivo dice que el texto esperado sale de `knowledge/` y que no inventa agronomía. | No. No hay etiqueta de daño. |
| `knowledge/prueba-*.md`, `ad177d66-….md`, `6e15b823-….md` | El propio Markdown dice que es material de prueba de HU-05 y que no sustituye asistencia técnica. | No. |
| `knowledge/22165791-….md`, `7019602d-….md`, `99d5b3aa-….md`, `af3bb36f-….md` | Notas cortas de papa, heladas o riego, sin fuente institucional ni fecha de un evento. | No son medidas validadas ni registros. |

No se encontró una serie de SENASA, un análisis de suelo ni un registro de incidencia.

## Etiquetas de riesgo

No hay etiquetas históricas verificables.

No existe una columna, un archivo ni un identificador que una una observación con un nivel de daño, una plaga confirmada o un resultado de manejo. Las notas «Zona con riesgo de heladas» y las categorías `clima_heladas`, `plagas` o `suelos` de HU-07 no cumplen ese papel.

## Viabilidad

| Alternativa | ¿La evidencia la permite ahora? | Motivo |
|---|---|---|
| a) Entrenar un modelo supervisado | No | No hay pares de variables y nivel de riesgo real. El clima reciente no está almacenado ni tiene unidad en el modelo interno. Las filas de MySQL son de prueba. |
| b) Dejar solo una estructura de datos | Sí, como especificación | Se puede fijar el esquema y las validaciones. No corresponde llenarlo con filas inventadas. |
| c) Evaluar con reglas agronómicas explícitas | No todavía | No hay umbrales, escala ni método validados. Sin unidad persistida, una regla numérica sobre temperatura o precipitación no se puede aplicar. |

No se elige una de las tres como implementación. La evidencia deja (a) y (c) fuera de alcance hasta que existan datos o un método validado. (b) queda documentada abajo, sin registros, para no simular un dataset.

## Qué faltaría para un entrenamiento supervisado

Para cada familia haría falta una fuente que una las variables mínimas de la actividad 1 con un resultado observado y revisado. Esa fuente no está en el proyecto.

| Familia | Datos que faltan | Fuente necesaria |
|---|---|---|
| Meteorológica | Serie de observaciones con unidad, estación, fecha y ubicación del predio o distancia conocida a la estación. Resultado revisado: hubo o no daño por helada, granizo, sequía o exceso de lluvia, en un cultivo y una etapa declarados. | Historial meteorológico con unidad (SENAMHI u otra red identificada) más un registro de daño en predio, revisado por alguien responsable. Un pronóstico, si se quisiera avisar a futuro, sería otra fuente. |
| Plagas y enfermedades | Síntoma u organismo, cultivo, etapa y un diagnóstico o una incidencia confirmada. Hoy solo existiría el relato del agricultor, y no está guardado como dato de riesgo. | Registro fitosanitario verificable, por ejemplo una ficha de campo revisada o una fuente institucional identificada. El clasificador de consultas no lo reemplaza. |
| Suelo, agua y manejo | Problema declarado o medición con método y fecha, más un resultado de campo revisado. | Análisis de suelo, sensor o lámina de riego con método escrito, y un resultado observado. La precipitación de una estación no sustituye la humedad del suelo. |

En los tres casos falta también la etapa fenológica, que el agricultor tendría que declarar, y una escala de niveles acordada antes de etiquetar.

## Esquema previsto, sin registros

No se creó un JSONL ni una tabla. Si más adelante se recoge evidencia real, cada fila debería poder validarse así:

| Campo | Tipo | Validación |
|---|---|---|
| id_registro | texto | Obligatorio, único. |
| origen | texto | Obligatorio. Valores previstos: `contexto_agricultor`, `senamhi_wis2`, `declaracion_agricultor`, `registro_verificado`. |
| es_observacion_real | booleano | Obligatorio. `false` en pruebas. Una fila de prueba no entra a entrenamiento. |
| familia_riesgo | texto | Obligatoria si la fila se usa en una evaluación: `meteorologico`, `plaga_enfermedad`, `suelo_agua_manejo`. |
| cultivo | texto | Obligatorio, no vacío. |
| etapa_fenologica | texto | Obligatoria para emitir un nivel. Lista cerrada aún no validada: mientras no exista, la fila no está completa. |
| region_texto | texto | Opcional. No se geocodifica sola. |
| latitud, longitud | número | Opcionales. Si una está, la otra también. |
| identificador_estacion | texto | Obligatorio cuando el valor meteorológico viene de SENAMHI. |
| fecha_hora_observacion | fecha y hora | Obligatoria para cualquier medición. |
| nombre_variable | texto | Obligatorio para una medición. |
| valor | número | Obligatorio si hay variable. No se rellena con cero. |
| unidad | texto | Obligatoria junto al valor. Sin unidad, el valor no se interpreta. |
| organismo_o_sintoma | texto | Obligatorio para la familia de plagas y enfermedades. |
| problema_suelo_agua_manejo | texto | Obligatorio para suelo y agua si no hay medición con método. |
| metodo_medicion | texto | Obligatorio si el valor no viene de una estación identificada. |
| nivel_riesgo | texto o vacío | Vacío hasta que una fuente verificada lo aporte. Prohibido asignarlo por regla no validada o por similitud con una nota. |
| factores | lista | Solo los campos que sí entraron. No se agregan causas no medidas. |
| id_ficha_medida | texto o vacío | Vacío mientras no exista una ficha con fuente. El Markdown de prueba no se cita como ficha. |

Validaciones de conjunto:

- Una fila meteorológica sin unidad, sin fecha o sin estación o declaración identificada queda incompleta.
- Una fila de `example.com`, de `knowledge/` o de HU-07 no se marca `es_observacion_real`.
- La ausencia de `nivel_riesgo` no se convierte en un nivel «bajo» ni en `sin categoría`.
- No se mezcla en la misma etiqueta un tema de consulta y un daño de cultivo.

Hoy ese esquema tiene cero filas reales completas.

## Estado de la actividad 2

La revisión técnica está hecha. El conjunto de datos para HU-08 no está preparado, porque no hay registros reales etiquetados que preparar sin inventarlos.

La actividad 2 no queda cerrada como dataset listo. El entrenamiento no comienza.

## Decisiones pendientes antes de seguir

1. No usar la base local ni las consultas de HU-07 como si fueran observaciones de predios.
2. Decidir si el siguiente paso será recoger eventos reales etiquetados o definir una metodología de reglas con validación agronómica. Las dos vías están bloqueadas con la evidencia actual.
3. Si se usa SENAMHI, persistir la unidad junto al valor antes de comparar números. La comprobación puntual vio `Celsius` y `kg m-2` en esas respuestas; el adaptador actual las tira.
4. No interpretar las notas «Zona con riesgo de heladas» como niveles.
5. Acordar la escala de riesgo y la lista de etapas antes de etiquetar o de escribir reglas.
6. Separar el predio de la estación. La estación no es el predio mientras no haya coordenadas del predio y un criterio de distancia.
