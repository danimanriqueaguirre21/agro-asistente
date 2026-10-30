# HU-08 — Categorías de riesgo y criterios de aceptación

Este documento analiza cómo podrían definirse los niveles de riesgo agrícola. No aprueba una escala, no fija umbrales y no implementa reglas ni un modelo.

Ningún nivel de este archivo es válido para mostrarlo a un agricultor. Un nivel solo podría emitirse cuando exista una metodología de esa familia, revisada y aprobada, y cuando los datos de esa evaluación sean suficientes e interpretables.

Se apoya en `docs/HU08_VARIABLES_RIESGO_AGRICOLA.md` y `docs/HU08_REVISION_DATOS_RIESGO_AGRICOLA.md`. No modifica el backend, los modelos, la base de datos ni el flujo RAG. No usa las filas locales de prueba, las consultas sintéticas de HU-07 ni las notas «Zona con riesgo de heladas» como ejemplos de un nivel.

## Qué queda definido y qué no

| Se puede fijar ahora, como regla de diseño | Sigue siendo propuesta, no criterio validado |
|---|---|
| Hay tres familias y no se mezclan en un solo nivel. | Que los nombres visibles sean bajo, medio y alto. |
| Sin datos mínimos, el sistema se abstiene y lista lo que falta. | Qué situación de campo corresponde a cada nombre. |
| Sin metodología aprobada para esa familia, también se abstiene. | Cualquier corte numérico de temperatura, lluvia, síntoma o suelo. |
| Cada factor cita si es observación verificada o declaración del agricultor. | Las medidas preventivas. No hay catálogo con fuente. |
| Una abstención no es el nivel bajo ni la etiqueta `sin categoría` de HU-07. | Un modelo único para las tres familias. |

## Familias y metodologías

Las familias ya separadas en la actividad 1 se mantienen:

| Familia | Qué evaluaría | Por qué no comparte el criterio de las otras |
|---|---|---|
| Meteorológica | Temperatura o precipitación, con unidad, fecha y estación o medición declarada, para un cultivo y una etapa. | El criterio, cuando exista, será una comparación numérica. Hoy el adaptador no guarda la unidad y no hay umbral por cultivo. |
| Plagas y enfermedades | Un organismo o un síntoma declarado, con cultivo y etapa. | Un relato no es un diagnóstico. Hace falta un protocolo de registro o una incidencia verificada. La presencia de una palabra no asigna un nivel. |
| Suelo, agua y manejo | Un problema declarado o una medición con método y fecha. | La lluvia de una estación no describe el suelo. El pH o la humedad sin método no se interpretan. |

Pueden compartir el vocabulario de la pantalla y la forma de abstenerse. No pueden compartir la regla que elige el nivel. Un resultado meteorológico no se copia a plagas ni a suelo, y no se promedia con ellos.

Un solo modelo, o una sola tabla de cortes, queda fuera hasta que haya datos y un método que lo justifiquen. La revisión de datos no encontró esa evidencia.

## Nombres propuestos para el nivel

Bajo, medio y alto son nombres posibles para hablar con el agricultor. No son clases agronómicas aprobadas. Mientras no haya metodología, el sistema no debe mostrarlos.

El sentido que se propone revisar, todavía sin números, es este:

| Nombre propuesto | Sentido que habría que validar | Lo que no significa |
|---|---|---|
| Bajo | Según el método aprobado de esa familia, la situación registrada no pide una acción inmediata. | No significa «no hay peligro», ni «dato ausente», ni «la consulta no encaja en una categoría de HU-07». |
| Medio | Según ese método, conviene vigilar el factor citado o revisar una ficha preventiva ya registrada. | No significa un promedio entre familias ni un síntoma sin protocolo. |
| Alto | Según ese método, el cultivo y la etapa indicados requieren atención prioritaria por los factores citados. | No significa un diagnóstico de laboratorio ni un pronóstico si el dato es una observación ya pasada. |

Esos sentidos tienen que reescribirse por familia, cultivo y etapa cuando alguien con responsabilidad agronómica los apruebe. Hasta entonces son texto de trabajo.

No se asigna ninguno de estos nombres a los contextos de `example.com`, a las preguntas repetidas de la base local ni a los 1600 textos de HU-07.

## Criterios de aceptación propuestos

Un nivel solo sería aceptable si se cumplen todas las condiciones siguientes. Hoy fallan las que dependen de una metodología aprobada, así que ninguna evaluación de HU-08 es aceptable todavía.

1. La familia está declarada: `meteorologico`, `plaga_enfermedad` o `suelo_agua_manejo`.
2. Existe un documento de metodología de esa familia, con versión, fecha, cultivos y etapas cubiertos, y un responsable que lo haya aprobado. Este archivo no cuenta como esa aprobación.
3. Los datos mínimos de esa familia están presentes y se pueden interpretar. Un número sin unidad no se interpreta.
4. El método aprobado, y no una suposición de este documento, es el que relaciona esos datos con bajo, medio o alto.
5. La respuesta lista los factores usados y marca el origen de cada uno.
6. La respuesta dice la versión del método. No presenta el nivel como un hecho medido en el predio si el dato vino de una estación o de una declaración.
7. Si el método no cubre ese cultivo o esa etapa, el sistema se abstiene.
8. Los registros de prueba no producen un nivel.

La aceptación es por familia. Aprobar el criterio meteorológico no acepta el de plagas ni el de suelo.

## Evidencia necesaria para validar cada familia

Sin esta evidencia, el criterio de esa familia sigue en propuesta.

### Meteorológica

- Decisión de si el aviso usa temperatura del aire, mínima del predio, precipitación, o una combinación, y en qué unidad se compara.
- Umbrales escritos por cultivo y etapa, con la fuente de donde salen. Este documento no los inventa.
- Criterio de distancia o de diferencia de altitud entre el predio y la estación. Mientras no exista, la estación se cita como estación, no como medición del predio.
- Casos reales en los que se sepa si hubo daño por helada, granizo, sequía o exceso de lluvia. Las observaciones recientes de SENAMHI, solas, no traen ese resultado.
- Qué hacer con una observación pasada cuando el agricultor pregunta por un evento futuro. Un dato ya ocurrido no es un pronóstico.

### Plagas y enfermedades

- Lista de síntomas u organismos que el sistema puede registrar, y la advertencia de que registrarlos no es un diagnóstico de laboratorio.
- Protocolo que diga qué relato corresponde a vigilancia y cuál a atención prioritaria, o una serie de incidencia verificada. Una sola frase del agricultor no basta para fijar ese protocolo.
- Etapa del cultivo en la que el mismo síntoma cambia de importancia.
- Separación explícita entre un insecto visto y un signo de enfermedad. HU-07 ya separa esos temas en las consultas; esa separación no etiqueta el riesgo del predio.

### Suelo, agua y manejo

- Definición del problema que el agricultor puede declarar, sin convertir la declaración en un análisis de suelo.
- Unidad y método cuando haya humedad, pH u otra medición, y la fecha del análisis.
- Criterio que diga si un problema declarado puede llegar a «alto» o si, sin medición, el sistema solo puede mostrar el relato y abstenerse de un nivel.
- Confirmación de que la precipitación de SENAMHI no completa esta familia.

## Cuándo evaluar y cuándo abstenerse

La información mínima para intentar una evaluación es la de la actividad 1, más la unidad cuando el factor es numérico, más una metodología aprobada de esa familia.

| Familia | Mínimo de datos | Abstención aunque esos datos existan |
|---|---|---|
| Meteorológica | Familia, cultivo, etapa declarada, fecha de la observación, y temperatura o precipitación según el aviso, con estación identificada o con una declaración de predio que traiga ubicación y unidad. | Falta la unidad. El método no está aprobado para ese cultivo y etapa. No hay criterio de distancia y se pretendería tratar la estación como el predio. El dato es anterior y la pregunta es un pronóstico. |
| Plagas y enfermedades | Familia, cultivo, etapa declarada y organismo o síntoma. | No hay protocolo aprobado. El texto solo pide identificar una plaga sin decir qué se vio. Se intenta usar la categoría de HU-07 como diagnóstico. |
| Suelo, agua y manejo | Familia, cultivo, etapa declarada, y un problema declarado o una medición con método y fecha. | Solo hay lluvia de estación. El pH o la humedad no traen método. El método aprobado exige medición y solo hay un relato, o al revés, según quede escrito en ese método. |

Si falta un dato mínimo, la respuesta nombra ese dato y no entrega bajo, medio ni alto.

Si los datos mínimos están, pero la metodología de la familia no está aprobada, la respuesta tampoco entrega un nivel. El motivo es la falta de método, no un nivel intermedio. Hoy este es el caso de las tres familias.

Otras abstenciones:

- Valor vacío, ilegible o de una unidad distinta a la que el método aprobado espera.
- Familia no indicada.
- Etapa no declarada. No se calcula con la fecha de siembra mientras no exista un calendario validado.
- Fila de prueba, consulta sintética de HU-07 o nota libre del contexto usada como si fuera una etiqueta.

La abstención no muestra medidas preventivas. No hay un nivel al que asociarlas, y no hay fichas con fuente.

## Factores que se muestran

Cuando más adelante exista una evaluación aceptada, los factores son solo los datos que entraron. Cada factor lleva:

| Dato del factor | Qué debe decir |
|---|---|
| Nombre | La variable usada, por ejemplo temperatura del aire o síntoma declarado. |
| Valor y unidad | El número o el texto, y la unidad si es numérico. Sin unidad, ese número no aparece como evidencia. |
| Origen | `observacion_verificada` o `declaracion_agricultor`. |
| Referencia | Estación, fecha y hora, o la fecha de la declaración. |
| Papel | Si entró en el nivel o si solo se muestra como contexto no usado. |

Origen `observacion_verificada`: una medición de una fuente identificada, con unidad y fecha, o un registro marcado como verificado por alguien responsable. Una lectura de SENAMHI solo califica así cuando la unidad quede guardada junto al valor. El adaptador actual no hace eso, de modo que sus números de hoy no se presentan como observación verificada de HU-08.

Origen `declaracion_agricultor`: cultivo y región escritos en el contexto, etapa, síntoma, problema de suelo, temperatura que el propio agricultor dice haber visto, y cualquier nota libre. Guardar la frase en MySQL no la vuelve una medición.

La pantalla debe poder leerse así: qué se midió en una estación, qué dijo el agricultor y qué no se usó. Un factor de contexto no se redacta como causa del nivel.

Si el agricultor abre un riesgo ya identificado, se muestran los factores guardados con esa evaluación y la versión del método. No se recalcula con otros datos ni se rellena con una respuesta del modelo de lenguaje.

## Medidas preventivas

Las medidas no definen el nivel. Solo podrían acompañar a un nivel ya aceptado, y solo citando una ficha con identificador y fuente. Los Markdown de `knowledge/` no son esa ficha.

Si no hay ficha para el cultivo, la etapa y la familia, se muestra el nivel y los factores, y se dice que no hay una medida registrada. No se redacta una recomendación para completar el vacío.

## Estado

Quedó definida la forma de la evaluación: familias separadas, abstención sin datos o sin método, y factores con origen explícito.

No quedó validado el significado de bajo, medio y alto. No hay umbrales, protocolo de síntomas, criterio de suelo ni catálogo de medidas.

La implementación sigue bloqueada porque:

- no hay metodología aprobada para ninguna familia;
- no hay umbrales ni una escala aceptada;
- no hay etapas fenológicas validadas, y la etapa depende de una declaración que el sistema aún no pide;
- el adaptador de SENAMHI no conserva la unidad ni deja historial;
- no hay eventos de campo etiquetados;
- no hay catálogo de medidas con fuente;
- no hay regla de distancia entre predio y estación.

Hasta cerrar eso, HU-08 no debe mostrar un nivel de riesgo.
