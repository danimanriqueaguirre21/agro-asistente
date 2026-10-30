# HU-08 — Variables candidatas para el riesgo agrícola

Actividad 1: definir las variables que utilizará una evaluación de riesgo agrícola.

Este documento es un diseño. No entrena un modelo, no crea un dataset y no integra una función en el backend. Las variables son candidatas. Ningún umbral, peso ni nivel de riesgo de este texto está validado con datos agronómicos ni con agricultores de Junín.

HU-08 no reutiliza el clasificador de HU-07. Ese clasificador asigna una consulta de texto a una de ocho categorías temáticas. No estima un nivel de riesgo ni explica factores de un evento en el predio.

## Alcance de la actividad

La historia pide tres comportamientos, todavía no implementados:

1. Con datos suficientes, entregar un nivel de riesgo y medidas preventivas.
2. Con datos insuficientes, indicar qué falta y no entregar un nivel.
3. Ante un riesgo ya identificado, mostrar los factores que entraron en esa evaluación.

Esta actividad solo fija qué datos harían falta, cuáles son mínimos y cuáles son contexto, y cómo se decide que el conjunto es suficiente.

## Qué se inspeccionó

Arquitectura y configuración:

- `docs/ARQUITECTURA.md`
- `docs/INSTALACION.md`
- `README.md`
- `backend/app/main.py`
- `backend/app/infrastructure/composition.py`
- `backend/app/infrastructure/config/settings.py`
- `database/schema.sql`

Datos que el sistema ya persiste o consulta:

- `backend/app/domain/entities/contexto_agricola.py`
- `backend/app/domain/valueObjects/cultivo.py`
- `backend/app/domain/valueObjects/region.py`
- `backend/app/domain/entities/observacion_meteorologica.py`
- `backend/app/domain/ports/output/puerto_observaciones_meteorologicas.py`
- `backend/app/application/useCases/obtener_observaciones_meteorologicas.py`
- `backend/app/infrastructure/adapters/output/senamhi/adaptador_senamhi_wis2.py`
- `backend/app/infrastructure/adapters/input/http/weather_controller.py`
- `frontend/src/pages/ContextPage.jsx`

Conocimiento y taxonomía, usados solo como referencia de temas ya nombrados en el proyecto:

- `backend/clasificacion/taxonomia/taxonomia_consultas_v1.json`
- Metadatos y Markdown de `knowledge/`

No se encontró ningún archivo CSV, de series de tiempo, de incidencia de plagas o de análisis de suelo.

## Datos que realmente existen

| Dato | Dónde está | Qué permite | Qué no permite |
|---|---|---|---|
| Cultivo | Contexto agrícola. Texto libre, obligatorio, hasta 50 caracteres en el dominio. | Saber de qué cultivo habla el agricultor. | No es un catálogo cerrado ni una fenología. |
| Región | Contexto agrícola. Texto libre, obligatorio, hasta 120 caracteres. | Un nombre de lugar escrito por el agricultor. | No es latitud, longitud ni distrito geocodificado. |
| Nombre del predio | Contexto. Opcional en el dominio. En `contextos_agricolas.nombre_parcela` la columna es `NOT NULL`. | Identificar la parcela en la interfaz. | No ubica el predio en el mapa. |
| Observaciones del contexto | Texto libre, opcional, hasta 500 caracteres. | Una nota del agricultor. | No es una variable medida. |
| Agricultor | Tabla `agricultores`. | Asociar el contexto al usuario autenticado. | No describe el predio. |
| Observación meteorológica reciente | `GET /api/v1/weather/observations`, adaptador SENAMHI WIS2. No se guarda en MySQL. | Estación, coordenadas, altitud de la geometría, fecha-hora, temperatura del aire, punto de rocío y precipitación, cuando el API las trae. | No hay historial local, pronóstico, humedad relativa, viento, radiación ni temperatura mínima diaria. El adaptador no guarda la unidad del valor. |
| Documentos de conocimiento | Markdown de prueba en `knowledge/`. Temas vistos: heladas y riego de papa. | Texto de ejemplo para RAG. | No es un catálogo validado de medidas ni un registro de eventos. |
| Categoría de una consulta | Clasificador HU-07. | Decir de qué tema habla una pregunta. | No es un nivel de riesgo. |

La colección configurada es `urn:wmo:md:pe-senamhi:synop-hourly`, base `https://wis.senamhi.gob.pe/oapi`. El adaptador lee tres nombres de variable: `air_temperature`, `dewpoint_temperature` y `total_precipitation_or_total_water_equivalent`. Si el API no envía una de ellas, el campo queda vacío. No se inventa el valor.

La taxonomía `consultas-agricolas-junin` 1.0.0 tiene la lista de ocho temas aprobada y una lista de cultivos de referencia. El dataset de entrenamiento de esa taxonomía no está aprobado. Esa lista de cultivos no está conectada al campo `cultivo` del contexto: hoy se acepta cualquier texto no vacío.

## Familias de riesgo

No hay evidencia en el repositorio para un solo modelo que cubra clima, plagas y suelo. Las tres familias se evalúan por separado. Un resultado de una familia no se convierte en resultado de otra.

| Familia | Pregunta que intenta responder | Evidencia actual |
|---|---|---|
| Meteorológica | Si las condiciones de temperatura o precipitación observadas justifican un aviso para el cultivo y la etapa indicados. | Hay observaciones recientes de SENAMHI. No hay umbrales por cultivo ni pronóstico. |
| Plagas y enfermedades | Si un organismo o un síntoma declarado, junto con el cultivo, basta para señalar un riesgo y sus factores. | No hay registros de incidencia, trampas ni diagnósticos. |
| Suelo, agua y manejo | Si una condición declarada de suelo, agua o labor basta para señalar un riesgo de manejo. | No hay análisis de suelo ni láminas de riego medidas. |

Mientras no exista una serie etiquetada y revisada para una familia, esa familia no tiene un modelo entrenable. Una regla explícita de suficiencia puede decir «faltan datos» sin fingir una predicción.

## Regla de suficiencia

Una evaluación tiene un identificador de familia. Solo usa variables de esa familia.

- **Mínimas.** Si falta cualquiera, no hay nivel de riesgo. La respuesta lista los nombres de las que faltan.
- **De contexto.** Mejoran la explicación. Su ausencia no bloquea la evaluación si las mínimas están presentes. La respuesta debe decir que el factor no se usó.
- **De salida.** El nivel, los factores y las medidas preventivas no son entradas. No se piden al agricultor para «completar» el cálculo.

Una variable presente con valor vacío, ilegible o fuera de un rango todavía no definido cuenta como ausente.

El nivel, cuando más adelante se emita, tiene que nombrar los factores usados. Esos factores son las variables mínimas y de contexto que sí entraron. No se presentan como causa demostrada si el método solo las asoció por una regla o por un modelo no validado.

No se usa la abstención `sin categoría` de HU-07 como sustituto de «datos insuficientes». Son mecanismos distintos.

## Variables del cultivo

### cultivo

- Descripción: nombre del cultivo del predio que se evalúa.
- Tipo: texto.
- Unidad: no aplica.
- Obligatoria: mínima en las tres familias.
- Fuente prevista: contexto agrícola ya guardado. El agricultor puede corregirlo en la solicitud de riesgo si el contexto no corresponde a la parcela evaluada.
- Utilidad: los umbrales y las medidas, si algún día se validan, dependen del cultivo.
- Si no está: no se emite nivel. Se pide el cultivo.

### variedad

- Descripción: variedad o cultivar, si el agricultor la conoce.
- Tipo: texto.
- Unidad: no aplica.
- Obligatoria: contexto. No es mínima.
- Fuente prevista: declaración del agricultor. No existe en el contexto actual.
- Utilidad: algunas variedades toleran frío o enfermedades de forma distinta. Esa diferencia no está medida en este proyecto.
- Si no está: la evaluación sigue con el cultivo. El factor «variedad» no se usa.

### area_predio

- Descripción: superficie de la parcela evaluada.
- Tipo: número.
- Unidad: hectárea. Pendiente de confirmar con el equipo agronómico si conviene otra unidad.
- Obligatoria: contexto.
- Fuente prevista: declaración del agricultor. No está en MySQL.
- Utilidad: orden de magnitud del predio. No cambia por sí sola un nivel meteorológico.
- Si no está: se omite. No se estima.

### fecha_siembra

- Descripción: fecha en que se sembró o plantó el ciclo actual.
- Tipo: fecha.
- Unidad: día calendario.
- Obligatoria: contexto. Pasa a ser mínima solo si, en una validación posterior, una familia exige etapa fenológica y la etapa no fue declarada.
- Fuente prevista: declaración del agricultor. No está en el contexto.
- Utilidad: permite estimar la etapa solo cuando exista un calendario validado para ese cultivo y esa zona. Ese calendario no existe en el repositorio.
- Si no está: no se calcula una etapa. No se inventa el día de siembra.

## Ubicación y condiciones ambientales

### region_texto

- Descripción: lugar escrito por el agricultor, tal como está en el contexto.
- Tipo: texto.
- Unidad: no aplica.
- Obligatoria: contexto. No sustituye a las coordenadas.
- Fuente prevista: campo `region` del contexto agrícola.
- Utilidad: mostrar el lugar en la explicación y, más adelante, intentar asociarlo a una estación si existe un directorio de lugares. Ese directorio no existe.
- Si no está: el contexto actual no permite guardarlo vacío. Si en una solicitud de riesgo llegara vacío, se pide. No se geocodifica a partir del nombre.

### latitud y longitud

- Descripción: posición usada para elegir una estación o una observación.
- Tipo: número.
- Unidad: grados decimales. El adaptador SENAMHI lee la latitud en la segunda coordenada de la geometría y la longitud en la primera.
- Obligatoria: mínima para la familia meteorológica, salvo que el agricultor indique directamente `identificador_estacion` o entregue él mismo `temperatura_aire` y `fecha_hora_observacion`.
- Fuente prevista: geometría de la estación SENAMHI. El predio del agricultor no tiene coordenadas guardadas.
- Utilidad: acerca la observación a un lugar. Una estación no es el predio.
- Si no están y tampoco hay estación o medición declarada: no hay nivel meteorológico. Se pide ubicación de la parcela o una estación.

### altitud

- Descripción: altitud asociada a la geometría de la estación.
- Tipo: número.
- Unidad: no está etiquetada en `ObservacionMeteorologica`. No se afirma que sea metros hasta leer la unidad de la fuente.
- Obligatoria: contexto.
- Fuente prevista: coordenada de altitud de SENAMHI WIS2, si viene.
- Utilidad: en la sierra, la altitud cambia la exposición al frío. Sin una curva validada, solo es contexto.
- Si no está: se omite. No se completa con un modelo de elevación que el proyecto no tiene.

### identificador_estacion

- Descripción: identificador WIGOS de la estación usada.
- Tipo: texto.
- Unidad: no aplica.
- Obligatoria: mínima meteorológica cuando la temperatura proviene de SENAMHI.
- Fuente prevista: `wigos_station_identifier` del adaptador actual.
- Utilidad: permite repetir la consulta y citar la fuente del factor.
- Si no está: no se usa una observación anónima. Se pide la estación o una medición declarada por el agricultor, marcada como declaración y no como estación.

### fecha_hora_observacion

- Descripción: momento de la observación meteorológica usada.
- Tipo: fecha y hora, texto tal como llega de la fuente.
- Unidad: no aplica.
- Obligatoria: mínima meteorológica.
- Fuente prevista: `reportTime` o `phenomenonTime` del adaptador.
- Utilidad: una temperatura sin momento no dice si corresponde al evento consultado.
- Si no está: la observación no entra. No se usa «la última» sin fecha.

### temperatura_aire

- Descripción: temperatura del aire de la observación.
- Tipo: número.
- Unidad: el adaptador guarda `value` y no el campo de unidad. El nombre WMO es `air_temperature`. La unidad queda pendiente de lectura en el payload.
- Obligatoria: mínima para un aviso de frío o calor. No es mínima para un aviso que solo dependa de precipitación.
- Fuente prevista: SENAMHI WIS2, o declaración explícita del agricultor.
- Utilidad: es el dato meteorológico que el sistema ya sabe pedir.
- Si no está: no hay nivel de riesgo por temperatura. Se indica que falta. No se interpola.

### punto_rocio

- Descripción: temperatura de punto de rocío de la misma observación.
- Tipo: número.
- Unidad: misma reserva que `temperatura_aire`. Nombre WMO `dewpoint_temperature`.
- Obligatoria: contexto.
- Fuente prevista: SENAMHI WIS2.
- Utilidad: se relaciona con la humedad del aire. Convertirlo a humedad relativa exige una fórmula y una validación que este proyecto no ha hecho.
- Si no está: no se calcula humedad. El factor no se usa.

### precipitacion

- Descripción: precipitación o equivalente en agua de la observación.
- Tipo: número.
- Unidad: no guardada. Nombre WMO `total_precipitation_or_total_water_equivalent`.
- Obligatoria: mínima solo para un aviso de exceso o falta de lluvia. No es mínima para un aviso de helada.
- Fuente prevista: SENAMHI WIS2, o declaración del agricultor con la fuente marcada.
- Utilidad: distingue un evento de lluvia de una decisión de riego.
- Si no está: no hay nivel por lluvia. No se rellena con cero.

### temperatura_minima_declarada

- Descripción: mínima que el agricultor observó en el predio, si la declara.
- Tipo: número.
- Unidad: pendiente de fijar junto con la unidad de SENAMHI. No mezclar números de distinta unidad.
- Obligatoria: contexto. Puede reemplazar a `temperatura_aire` de estación solo si la regla de esa evaluación lo dice de forma explícita y la declaración trae fecha.
- Fuente prevista: agricultor. No existe en el sistema.
- Utilidad: la estación puede estar lejos del predio.
- Si no está: se usa la estación, si la estación cumple las mínimas. No se fabrica una mínima de predio.

Estas variables meteorológicas no incluyen pronóstico, rachas de viento, granizo medido, humedad relativa ni radiación. Pedirlas ahora sería inventar una fuente.

## Etapa de desarrollo del cultivo

### etapa_fenologica

- Descripción: etapa declarada del ciclo, por ejemplo emergencia, tuberización o floración.
- Tipo: texto de una lista cerrada por cultivo. Esa lista no existe todavía y debe salir de validación agronómica, no de este documento.
- Unidad: no aplica.
- Obligatoria: mínima en las tres familias. El mismo dato numérico no significa lo mismo en siembra que en cosecha.
- Fuente prevista: declaración del agricultor. No está en el contexto ni se puede derivar sin `fecha_siembra` y un calendario validado.
- Utilidad: condiciona qué factor se considera relevante.
- Si no está: no se emite nivel. Se pide la etapa. No se infiere del mes actual.

### dias_desde_siembra

- Descripción: días entre `fecha_siembra` y la fecha de la evaluación.
- Tipo: número entero.
- Unidad: día.
- Obligatoria: contexto, y solo se calcula si ambas fechas existen.
- Fuente prevista: cálculo interno. No es un dato que el agricultor deba teclear si ya dio la fecha de siembra.
- Utilidad: acompaña a la etapa. No la reemplaza hasta que un calendario validado lo autorice.
- Si no está: se omite.

## Amenazas o eventos observados

### familia_riesgo

- Descripción: cuál de las tres familias se evalúa.
- Tipo: texto enumerado: `meteorologico`, `plaga_enfermedad`, `suelo_agua_manejo`.
- Unidad: no aplica.
- Obligatoria: mínima en toda evaluación.
- Fuente prevista: la solicitud. Puede proponerla la interfaz según la pregunta, pero la familia elegida tiene que quedar registrada. La categoría de HU-07 no se copia como familia sin una correspondencia revisada.
- Utilidad: evita mezclar factores de familias distintas en un solo nivel.
- Si no está: no hay evaluación. Se pregunta qué tipo de riesgo quiere revisar.

### evento_meteorologico_declarado

- Descripción: evento que el agricultor dice haber visto o espera: helada, granizo, sequía, viento o lluvia fuerte.
- Tipo: texto de una lista corta, más un campo libre de detalle.
- Unidad: no aplica.
- Obligatoria: contexto para la familia meteorológica. No reemplaza temperatura o precipitación.
- Fuente prevista: agricultor.
- Utilidad: explica el motivo de la consulta. Un aviso de helada sin temperatura sigue siendo insuficiente para un nivel.
- Si no está: la evaluación meteorológica puede seguir si temperatura o precipitación, cultivo, etapa y ubicación cumplen las mínimas. El relato del evento no se inventa.

### organismo_o_sintoma

- Descripción: plaga vista o síntoma descrito por el agricultor: insecto, mancha, pudrición, polvo u otro signo.
- Tipo: texto.
- Unidad: no aplica.
- Obligatoria: mínima para la familia de plagas y enfermedades.
- Fuente prevista: agricultor. El conocimiento RAG puede citar un documento recuperado, pero ese documento de prueba no diagnostica.
- Utilidad: sin un signo o un organismo no hay factores de esta familia.
- Si no está: no hay nivel. Se pide qué se observó en la planta. No se clasifica la consulta de HU-07 como diagnóstico.

### parte_planta_afectada

- Descripción: hoja, tallo, raíz, flor, fruto u otra parte.
- Tipo: texto.
- Unidad: no aplica.
- Obligatoria: contexto en plagas y enfermedades.
- Fuente prevista: agricultor.
- Utilidad: precisa el factor mostrado al consultar el riesgo.
- Si no está: se omite.

### proporcion_afectada

- Descripción: parte del cultivo que el agricultor estima afectada.
- Tipo: número, o una escala ordinal aún no definida.
- Unidad: porcentaje, si se usa número. La escala ordinal queda pendiente.
- Obligatoria: contexto.
- Fuente prevista: estimación del agricultor, no un muestreo del sistema.
- Utilidad: separa un hallazgo aislado de un daño extendido. Sin un protocolo de muestreo no es una incidencia medida.
- Si no está: se omite. No se pone cero ni «todo el campo».

### problema_suelo_agua_manejo

- Descripción: condición declarada de terreno, agua o labor: encharcamiento, sequedad del suelo, compactación, erosión, falta de riego o riego excesivo.
- Tipo: texto.
- Unidad: no aplica.
- Obligatoria: mínima para la familia de suelo, agua y manejo, salvo que exista una medición de esa familia (`humedad_suelo` o `ph_suelo`).
- Fuente prevista: agricultor.
- Utilidad: es el único dato de esta familia que alguien puede aportar hoy, porque no hay laboratorio ni sensores.
- Si no está y tampoco hay medición: no hay nivel. Se pide cuál es el problema observado.

### humedad_suelo

- Descripción: humedad del suelo medida o estimada con un método nombrado.
- Tipo: número.
- Unidad: pendiente. No se elige una unidad sin el método de medición.
- Obligatoria: no. Si existe y el método está nombrado, puede cumplir el mínimo de la familia de suelo y agua junto con cultivo y etapa.
- Fuente prevista: no hay sensor ni análisis en el sistema. Solo una declaración futura con método explícito.
- Utilidad: distingue el relato de una medición.
- Si no está: no se calcula a partir de la precipitación de la estación.

### ph_suelo

- Descripción: pH de un análisis de suelo, con fecha del análisis.
- Tipo: número.
- Unidad: unidades de pH.
- Obligatoria: contexto. No es mínima.
- Fuente prevista: análisis aportado por el agricultor. No hay tabla de análisis.
- Utilidad: contexto para nutrición y suelo. Un pH sin cultivo y etapa no produce un nivel.
- Si no está: se omite.

## Medidas preventivas disponibles

Las medidas no entran al cálculo del nivel. Se consultan después, y solo si la evaluación emitió un nivel.

### medida_preventiva

- Descripción: acción sugerida, ligada a la familia, el cultivo y la etapa.
- Tipo: texto, con un identificador de la ficha de origen.
- Unidad: no aplica.
- Obligatoria: no es entrada. Es salida condicionada.
- Fuente prevista: fichas que todavía no existen. Los Markdown de `knowledge/` son material de prueba y dicen de forma explícita que no sustituyen asistencia técnica local. No se copian como medidas de HU-08.
- Utilidad: cumple la parte de «medidas preventivas» del criterio de aceptación cuando el nivel sí se emite.
- Si no hay ficha para esa combinación: se entrega el nivel y los factores, y se dice que no hay una medida registrada. No se redacta una recomendación agronómica para llenar el hueco.

### medida_ya_aplicada

- Descripción: acción que el agricultor ya hizo en este ciclo.
- Tipo: texto.
- Unidad: no aplica.
- Obligatoria: contexto.
- Fuente prevista: agricultor.
- Utilidad: evita repetir como sugerencia algo que ya se hizo. No demuestra que la medida haya funcionado.
- Si no está: las fichas se muestran sin filtrar por lo ya hecho, y la respuesta lo indica.

## Qué es mínimo y qué es contexto

| Familia | Mínimas para emitir nivel | Solo contexto |
|---|---|---|
| Meteorológica | `familia_riesgo`, `cultivo`, `etapa_fenologica`, `fecha_hora_observacion`, y al menos una de `temperatura_aire` o `precipitacion` según el aviso, con `identificador_estacion` o una declaración de predio que traiga ubicación. | `region_texto`, `altitud`, `punto_rocio`, `variedad`, `area_predio`, `fecha_siembra`, `evento_meteorologico_declarado`, `temperatura_minima_declarada` cuando no sustituye a la temperatura de la fuente. |
| Plagas y enfermedades | `familia_riesgo`, `cultivo`, `etapa_fenologica`, `organismo_o_sintoma`. | `parte_planta_afectada`, `proporcion_afectada`, `variedad`, `region_texto`, `fecha_siembra`. |
| Suelo, agua y manejo | `familia_riesgo`, `cultivo`, `etapa_fenologica`, y `problema_suelo_agua_manejo` o una medición con método (`humedad_suelo` o `ph_suelo` con fecha). | `area_predio`, `region_texto`, `precipitacion` de la estación, `medida_ya_aplicada`. |

La precipitación de una estación no completa, por sí sola, el mínimo de suelo y agua: describe el tiempo, no el estado del terreno.

## Fuentes de datos identificadas

1. Contexto agrícola del agricultor autenticado: cultivo, región, predio y notas.
2. SENAMHI WIS2, observaciones recientes ya integradas en el backend: temperatura, punto de rocío, precipitación, estación, coordenadas, altitud y fecha. No persistidas.
3. Declaración del agricultor en una futura solicitud de riesgo: etapa, síntomas, problema de suelo o agua, medidas ya aplicadas.
4. Fichas de medidas preventivas: fuente aún inexistente. La base RAG actual no califica.

No hay una quinta fuente de incidencia fitosanitaria, SENASA, análisis de suelo ni pronóstico dentro del repositorio.

## Información que falta

- Coordenadas del predio y un modo de elegir la estación más cercana sin afirmar que la estación es el predio.
- Unidad de temperatura, precipitación y altitud guardada junto al número.
- Historial meteorológico local. El endpoint actual pide observaciones recientes, con límite entre 1 y 50.
- Pronóstico. Un aviso de helada «para mañana» no se puede calcular con una observación pasada.
- Lista fenológica por cultivo, validada para Junín.
- Umbrales por cultivo, etapa y familia. No se proponen en este documento.
- Registros reales de daño, plaga o enfermedad con etiqueta revisada.
- Análisis de suelo y humedad de suelo con método.
- Catálogo de medidas preventivas con autor y alcance.
- Directorio que traduzca el texto de `region` a una caja geográfica.

## Supuestos y decisiones pendientes de validación

Supuestos de trabajo, no resultados:

- El riesgo se evalúa por familia. Un modelo único queda descartado hasta que haya datos y un método que lo justifiquen.
- La etapa fenológica la declara el agricultor. Calcularla desde la fecha de siembra queda bloqueado hasta tener un calendario validado.
- Una observación de estación es un factor citado, no una medición del predio.
- El valor numérico de SENAMHI no se interpreta hasta confirmar y guardar su unidad.
- Las medidas preventivas salen de fichas identificadas. El modelo de lenguaje del PMV1 no las redacta como si fueran evidencia.
- «Datos insuficientes» no produce un nivel intermedio ni la etiqueta `sin categoría`.

Decisiones que un responsable agronómico debe cerrar antes de entrenar o de implementar reglas:

- Lista de etapas por cultivo de la agricultura familiar de Junín.
- Si el aviso meteorológico usa temperatura del aire, mínima diaria, o ambas.
- Distancia o diferencia de altitud aceptable entre predio y estación.
- Escala del nivel de riesgo: cuántos niveles, y qué significa cada uno para el agricultor.
- Qué síntomas puede registrar el sistema sin presentarlos como diagnóstico de laboratorio.
- Qué medidas se pueden mostrar y con qué fuente institucional.

## Estado de la actividad 1

La actividad «Definir las variables que utilizará el modelo» queda documentada en este archivo.

Cumple el encargo de diseño: variables, tipo, unidad cuando ya se conoce, obligatoriedad, fuente, utilidad, ausencia, mínimos, contexto y separación por familia.

No cumple los criterios de aceptación de la historia. Esos criterios exigen que el sistema entregue un nivel, señale datos faltantes en la interfaz y muestre factores de un riesgo identificado. Nada de eso está implementado.

No hay dataset real para entrenar ni para evaluar un modelo de riesgo. La siguiente actividad no se inicia desde este documento.
