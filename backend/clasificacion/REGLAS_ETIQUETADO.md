# Reglas de etiquetado — consultas agrícolas v1

Aplican al futuro dataset de entrenamiento. La muestra
`muestras/muestra_ilustrativa_v1.json` solo sirve para revisar estas
reglas. Sus textos son sintéticos: no son consultas reales de agricultores
y no se entrenan.

Taxonomía: `taxonomia/taxonomia_consultas_v1.json`, versión `1.0.0`.

## 1. Una categoría principal

Cada fila etiquetada lleva un solo código de `category`, tomado de la
taxonomía:

- `riego`
- `fertilizacion_nutricion`
- `plagas`
- `enfermedades_cultivos`
- `siembra_manejo_cultivo`
- `clima_heladas`
- `suelos`
- `cosecha_poscosecha`

La categoría es la decisión que la consulta pide resolver, no el cultivo
ni la región. Si la frase menciona agua solo para proteger de una helada,
la categoría es `clima_heladas`. Si pide cómo regar en el ciclo normal del
cultivo, la categoría es `riego`.

`sin categoría` no se escribe en el dataset de esta versión. No es una
clase de entrenamiento ni una predicción válida que se guarde como
etiqueta.

Es una abstención en inferencia. Se produce en tres casos:

- la confianza de una predicción válida no alcanza el umbral configurado;
- el modelo no está disponible (causa operativa, no una clase predicha);
- la salida es inválida o no pertenece a los ocho códigos.

En los tres casos la consulta sigue el flujo general: la recuperación y
la generación no se detienen. Esta regla está documentada aquí y todavía
no está implementada en el backend.

## 2. Nombres normalizados

- `category` usa el código de la taxonomía, en minúsculas y con guion bajo,
  sin tildes.
- El nombre visible (`Riego`, `Fertilización y nutrición`, etc.) vive solo
  en el manifiesto. No se guarda como etiqueta.
- El texto de cada ejemplo ilustrativo vive solo en
  `muestras/muestra_ilustrativa_v1.json`. El manifiesto guarda el
  `sample_id`, no una copia de la frase.
- `crop`, si se informa, usa el nombre de la lista de referencia de la
  taxonomía (`maíz amiláceo`, `kion`, `palta`). No se usan sinónimos
  alternos en la misma versión (`palto` y `palta` no conviven: se usa
  `palta`).
- `region`, si se informa, identifica la región o una provincia. No
  guarda distritos. El valor `Junín` se usa cuando no se precisa
  provincia; en esta versión no se distingue aparte la provincia llamada
  Junín, para no inventar otra marca. Las provincias válidas, con esta
  grafía, son Huancayo, Concepción, Jauja, Tarma, Yauli, Chanchamayo,
  Satipo, Chupaca y Junín. Pangoa no es un valor válido: es un distrito
  de la provincia de Satipo. Si solo se conoce ese distrito, `region`
  queda en `Satipo`.
- El texto de la consulta se conserva como lo diría una persona. No se
  reescribe para “acercarlo” a una categoría.

## 3. Consultas ambiguas

Si dos categorías explicarían la misma pregunta con el mismo peso, la fila
no entra al conjunto etiquetado de la v1. No se anota como
`sin categoría`. Queda pendiente de revisión humana y no se incorpora al
entrenamiento hasta que se resuelva.

La cola de revisión es una regla, no un archivo ni un sistema. Cada caso
pendiente se describe con esta estructura conceptual:

| Campo | Contenido |
|---|---|
| `id` | Identificador del caso, distinto de los `ilustrativo-*` |
| `text` | Consulta, sin reescribirla |
| `candidate_categories` | Códigos en disputa, solo de las ocho categorías |
| `reason` | Por qué no hay una decisión principal |
| `status` | `pendiente` hasta la revisión |
| `resolved_category` | Vacío mientras siga pendiente. Después, un solo código de la taxonomía |

Cuando `resolved_category` tenga un código, la fila ya puede pasar al
conjunto etiquetado y, más adelante, a una partición. Mientras
`status` sea `pendiente`, no entra a entrenamiento, validación ni prueba.

Ejemplos de frontera, resueltos por la decisión pedida:

| Pregunta (criterio, no dato real) | Categoría |
|---|---|
| Cómo regar la papa en floración | `riego` |
| Proteger el cultivo ante una helada anunciada | `clima_heladas` |
| Qué abono aplicar porque las hojas están pálidas | `fertilizacion_nutricion` |
| Cómo preparar un terreno compacto antes de sembrar | `suelos` |
| Qué insecto come las hojas y cómo controlarlo | `plagas` |
| Manchas y pudrición en hojas o frutos, sin un insecto como causa | `enfermedades_cultivos` |
| Fecha, densidad o deshierbo | `siembra_manejo_cultivo` |
| Cuándo cortar y cómo secar o guardar | `cosecha_poscosecha` |

Una consulta compuesta que pide dos acciones a la vez (“cómo riego y qué
abono echo”) no se parte en dos filas ni se fuerza a una clase. Espera
revisión.

Las malezas, el aporque, la poda, el tutorado y la densidad de siembra
entran en `siembra_manejo_cultivo`, salvo que la decisión central sea otra
categoría.

## 4. Duplicados

Antes de asignar una partición:

1. Normalizar una clave interna: Unicode NFC, minúsculas, recortar
   espacios, colapsar espacios repetidos y quitar puntuación de los
   extremos. Esa clave no reemplaza a `text`.
2. Misma clave: es el mismo ejemplo. Se conserva una fila y el resto se
   registra como duplicado exacto.
3. Paráfrasis evidente de una fila ya aceptada: se trata como casi
   duplicado. No recibe otra etiqueta ni otra partición.

En esta versión la detección de casi duplicados es revisión humana al
incorporar cada texto. No hay un umbral automático definido, porque todavía
no existe el corpus real.

## 5. Entrenamiento, validación y prueba

Todavía no se crean esas particiones. Cuando exista el conjunto real:

- Tres particiones disjuntas: entrenamiento, validación y prueba.
- La semilla del reparto se guarda en el manifiesto del dataset.
- Los duplicados exactos y los casi duplicados viajan juntos a la misma
  partición.
- La validación sirve para elegir el umbral de confianza. La prueba no se
  usa para ese ajuste.
- Las proporciones se fijan al conocer el soporte de cada clase. No se
  promete una precisión por el tamaño del conjunto.
- Una clase que no pueda aparecer en entrenamiento y en prueba queda fuera
  de esta versión de la taxonomía, o se agrupa antes de cerrar el archivo.
  No se inventa un mínimo de ejemplos en esta regla.

La muestra ilustrativa no es ninguna de las tres particiones.

## 6. Fuga de información

- No copiar frases de `knowledge/` ni ítems de
  `backend/evaluation/data/pmv1_baseline.json` al dataset de clasificación.
- No usar el `topic` de un documento de conocimiento como etiqueta de una
  consulta.
- No derivar la etiqueta del cultivo o de la provincia.
- No incluir los `id` con prefijo `ilustrativo-` en el futuro archivo de
  entrenamiento.
- No calcular el umbral de `sin categoría` con la partición de prueba.

## 7. Campos que el modelo no debe ver como etiqueta

`crop` y `region` son opcionales y descriptivos. La etiqueta supervisada
de la v1 es solo `category`. Notas de revisión, origen y claves
normalizadas no se entrenan.
