# Instrucciones para el revisor

Estas consultas son sintéticas. No son consultas reales de agricultores. Esta carpeta no es una revisión ya hecha y no autoriza un entrenamiento.

## Qué archivos usar

- `consultas_57.jsonl` — 57 textos.
- `casos_3.jsonl` — 3 textos.
- `plantilla_registro.jsonl` o `plantilla_registro.md` — para escribir el resultado. Hoy están vacías.

Revise los dos lotes con las mismas reglas. No suponga que uno de los lotes ya tiene un veredicto.

## Qué no abrir

No abra el resto del repositorio mientras revisa. En otros archivos hay etiquetas y justificaciones de una revisión anterior. Verlas anula la independencia.

No use `sellado_hasta_despues/`, `INFORME_PREPARACION.md`, `piloto_hu07_v2/`, `auditoria_hu07_v2/INFORME_AUDITORIA_PILOTO_HU07.md` ni `auditoria_hu07_v2/cierre_revision_humana/`.

No use los 24 ejemplos `ilustrativo-*`, las preguntas de RAGAS, los documentos de `knowledge/` ni las pruebas del backend.

## Qué decidir

La etiqueta es la decisión que pide la pregunta. No es el cultivo ni la provincia. No etiquete por una palabra suelta.

Use solo uno de estos códigos, y solo cuando la decisión sea una:

- `riego`
- `fertilizacion_nutricion`
- `plagas`
- `enfermedades_cultivos`
- `siembra_manejo_cultivo`
- `clima_heladas`
- `suelos`
- `cosecha_poscosecha`

No cree categorías nuevas. No escriba `sin categoría`.

Si dos categorías explican la pregunta con el mismo peso, no elija. Deje `categoria_propuesta` vacía y ponga `estado` en `pendiente`.

Si la pregunta no pide ninguna de las ocho decisiones, deje `categoria_propuesta` vacía y ponga `estado` en `rechazo_propuesto`. Explique el motivo en `justificacion`.

No fuerce una etiqueta.

## Cómo llenar la plantilla

Cada fila de `plantilla_registro.jsonl` corresponde a un `revision_id` de los lotes. El texto no se modifica.

| Campo | Qué escribir |
|---|---|
| `revision_id` | No lo cambie. |
| `categoria_propuesta` | Uno de los ocho códigos, o vacío. |
| `justificacion` | La decisión que vio en el texto, con estas reglas. |
| `estado` | `propuesta`, `pendiente` o `rechazo_propuesto`. |

Coherencia:

- `propuesta`: `categoria_propuesta` lleva exactamente un código de la lista.
- `pendiente`: `categoria_propuesta` queda vacía.
- `rechazo_propuesto`: `categoria_propuesta` queda vacía.

La fila de ejemplo no existe en los lotes. Sirve solo para ver los campos vacíos:

```json
{"revision_id": "rev-000", "categoria_propuesta": "", "justificacion": "", "estado": ""}
```

Devuelva la plantilla llena. No marque este paquete como revisión completada antes de escribir esas tres columnas.

## Las ocho categorías

Taxonomía `consultas-agricolas-junin` 1.0.0. Una consulta tiene una sola categoría principal.

### `riego` — Riego

Decisiones sobre aplicar agua al cultivo: frecuencia, cantidad, método y turnos.

Cabe cuando:

  - Frecuencia o calendario de riego durante el ciclo.
  - Método de riego: gravedad, aspersión, goteo, pozas o manguera.
  - Cómo evitar el encharcamiento causado por el riego.

No cabe cuando:

  - El agua se menciona solo como protección ante una helada: clima_heladas.
  - La dosis o la fuente de abono, aunque viaje en el agua: fertilizacion_nutricion.
  - Drenaje o preparación del terreno, sin preguntar cómo regar: suelos.
  - La pudrición o la mancha como enfermedad a identificar: enfermedades_cultivos.

### `fertilizacion_nutricion` — Fertilización y nutrición

Decisiones sobre abonos, fuentes de nutrientes y carencias nutricionales.

Cabe cuando:

  - Qué abono aplicar, en qué momento y con qué fuente.
  - Hojas pálidas u otro síntoma que la consulta atribuye a falta de nutriente.
  - Compost, guano o fertilizante cuando el fin es nutrir el cultivo.

No cabe cuando:

  - Preparar, drenar o descompactar el terreno sin hablar de abono: suelos.
  - Un insecto visible como causa del daño: plagas.
  - Manchas o pudriciones que se quieren identificar como enfermedad: enfermedades_cultivos.

### `plagas` — Plagas

Organismos que comen, pican o dañan el cultivo, y su control: insectos, ácaros, nematodos u otros animales.

Cabe cuando:

  - Gusanos, pulgones, ácaros u otros animales vistos en la planta.
  - Cómo controlar ese organismo sin cambiar el tema a otra labor.

No cabe cuando:

  - Hongos, bacterias, virus, manchas o pudriciones sin un animal como causa: enfermedades_cultivos.
  - Malezas, aporque o densidad de siembra: siembra_manejo_cultivo.
  - Carencia de nutriente como explicación del síntoma: fertilizacion_nutricion.

### `enfermedades_cultivos` — Enfermedades de cultivos

Identificación o manejo de enfermedades del cultivo: hongos, bacterias, virus y síntomas de pudrición o mancha.

Cabe cuando:

  - Manchas, polvo de roya, pudrición de hojas, tallos o frutos.
  - Preguntas por el nombre o el manejo de una enfermedad del cultivo.

No cabe cuando:

  - El daño lo causa un insecto u otro animal visto: plagas.
  - El síntoma se consulta como falta de abono: fertilizacion_nutricion.
  - Cómo guardar la cosecha para que no se malogre, sin identificar una enfermedad: cosecha_poscosecha.

### `siembra_manejo_cultivo` — Siembra y manejo del cultivo

Época y forma de siembra, semilla, densidad y labores culturales que no son riego, abono, suelo, clima, plaga, enfermedad ni cosecha.

Cabe cuando:

  - Mes o ventana de siembra, surcos, golpes y cantidad de semilla.
  - Aporque, deshierbo, poda, tutorado o variedad a sembrar.

No cabe cuando:

  - La labor central es regar, abonar, cosechar o proteger de una helada.
  - Preparación física del terreno o drenaje: suelos.
  - Control de un insecto o de una enfermedad.

### `clima_heladas` — Clima y heladas

Riesgo meteorológico para el cultivo: heladas, granizo, sequía, viento o lluvia como evento, y la protección ante ese evento.

Cabe cuando:

  - Qué hacer ante una helada anunciada o recién ocurrida.
  - Granizo, viento o una sequía tratados como evento del clima.
  - Una práctica de riego cuyo único fin, en la pregunta, es atenuar la helada.

No cabe cuando:

  - Calendario normal de riego, sin evento climático: riego.
  - La pregunta pide identificar la enfermedad que apareció después de la lluvia: enfermedades_cultivos.
  - La fecha habitual de siembra, sin un evento de clima: siembra_manejo_cultivo.

### `suelos` — Suelos

El terreno como objeto de la decisión: textura, piedras, compactación, erosión, drenaje, pH o preparación del suelo.

Cabe cuando:

  - Cómo preparar un suelo compacto, pedregoso o encharcado.
  - Drenaje, terrazas o análisis de suelo cuando la decisión es sobre el terreno.

No cabe cuando:

  - El análisis se usa solo para decidir la dosis de abono: fertilizacion_nutricion.
  - Cómo y cuándo regar un suelo que ya está en producción: riego.
  - Fecha o densidad de siembra, si el suelo no es el problema: siembra_manejo_cultivo.

### `cosecha_poscosecha` — Cosecha y poscosecha

Madurez, corte o arranque, secado, selección, oreo, almacenamiento y beneficio en finca.

Cabe cuando:

  - Cómo saber que el producto ya está para cosechar.
  - Secado, fermentación, oreo o guarda de corta duración en la finca.

No cabe cuando:

  - Cuándo sembrar: siembra_manejo_cultivo.
  - Identificar la enfermedad que pudre el fruto en planta: enfermedades_cultivos.
  - Abonar después de cosechar, si la decisión es el abono: fertilizacion_nutricion.

