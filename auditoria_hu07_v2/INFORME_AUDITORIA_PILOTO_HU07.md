# Informe de auditoría de calidad — piloto HU-07 v2

Fecha de la auditoría: 18 de octubre de 2026.
Archivos leídos, sin modificar: `piloto_hu07_v2/aceptadas_v2.jsonl`, `rechazadas_v2.jsonl`, `manifiesto_v2.json`, `fuentes_v2.json`, y la taxonomía, las reglas y el esquema vigentes en `backend/clasificacion/`.
Este archivo es el informe. No es una cola de revisión, no es un dataset y no forma parte del piloto. No se creó `revision_pendiente_v2.jsonl` ni ninguna partición.

## 1. Dictamen

El piloto **sigue pendiente de revisión humana**. Esta auditoría **no lo aprueba** para entrenamiento, validación ni prueba. No se entrenó ningún modelo. No se modificó el PMV1, el backend, el frontend, la base de datos, el RAG, RAGAS, la taxonomía ni `esquema_dataset_v1.json`.

Las 192 consultas son **sintéticas**. No son consultas reales de agricultores. Superar los controles automáticos del manifiesto no las da por buenas.

| Resultado | Cantidad | Qué significa |
|---|---:|---|
| Correctas | 189 | La categoría actual es la decisión que pide el texto. No se propone otra etiqueta. |
| Categoría dudosa | 3 | No hay una sola categoría principal. No se les asigna otra. Salen del conjunto etiquetado hasta que una persona las resuelva. |
| Deben rechazarse, de las 192 | 0 | Ninguna queda cerrada como rechazo en esta auditoría. |
| Corrección de texto, cultivo, región o categoría alternativa | 0 | No se reescribe ninguna frase. |

De las 189 correctas, **57** piden segunda revisión humana: las 48 que ya traen nota de frontera, cuya nota se sostiene, y 9 sin nota en las que la etiqueta se sostiene con reserva. Las otras **132** no mostraron un defecto de etiqueta, cultivo, región ni paráfrasis. Aun así, el conjunto completo sigue sin aprobar: la segunda revisión humana que pide el manifiesto no está hecha, y esta lectura no la reemplaza.

Las **5** filas de `rechazadas_v2.jsonl` se mantienen rechazadas y separadas. No pasan a aceptadas.

## 2. Consultas con categoría dudosa

Quedan descritas aquí, con la estructura conceptual de las reglas: `id`, `text`, candidatas solo de las ocho categorías, `reason`, `status` pendiente y `resolved_category` vacío. No tienen archivo propio.

### piloto-v2-04805c4db9

- Texto: «¿Sirve la ceniza de cocina en el huerto?»
- Categoría actual: `fertilizacion_nutricion`
- Candidatas, sin elección: `fertilizacion_nutricion`, `plagas`, `suelos`
- Motivo: no dice si la ceniza es comida, si va contra un animal o si es para el suelo.
- Estado: pendiente. `resolved_category`: vacío.
- Confianza de esta auditoría: baja.
- Segunda revisión: sí.
- Corrección propuesta: ninguna etiqueta. Retirarla del conjunto etiquetado.

### piloto-v2-99b5624803

- Texto: «¿Lavo el polvo blanco del brote?»
- Categoría actual: `enfermedades_cultivos`
- Candidatas, sin elección: `enfermedades_cultivos`, `plagas`
- Motivo: no hay cultivo ni un animal visto, y «lavo» no pide identificar el polvo. Puede ser un polvo de enfermedad o resto de un insecto, con peso parecido.
- Estado: pendiente. `resolved_category`: vacío.
- Confianza: media.
- Segunda revisión: sí.
- Corrección propuesta: ninguna etiqueta. No fundirla con `piloto-v2-464c8602df`.

### piloto-v2-41bdf8b563

- Texto: «¿El olluco se vende el mismo día?»
- Categoría actual: `cosecha_poscosecha`
- Candidatas de las ocho: solo `cosecha_poscosecha` podría caber, y únicamente si alguien documenta que la decisión es la guarda breve. El texto no dice eso. La venta no es una categoría.
- Motivo: no pide madurez, corte, secado, selección, oreo ni almacenamiento.
- Estado: pendiente. `resolved_category`: vacío.
- Confianza: baja.
- Segunda revisión: sí.
- Corrección propuesta: ninguna etiqueta. Retirarla. Si la revisión humana ve solo una pregunta de venta, rechazarla.

## 3. Consultas que necesitan corrección

No hay una corrección de texto, de `crop`, de `region` ni una categoría de reemplazo que esta auditoría pueda proponer sin incumplir dos reglas: no reescribir la frase para acercarla a una clase, y no etiquetar lo ambiguo.

Lo que sí debe corregirse es el **conjunto**: las tres dudosas no pueden seguir contando como filas etiquetadas. Eso no se hizo en los archivos originales.

## 4. Consultas que deben rechazarse

De las 192, ninguna se cierra como rechazo. `piloto-v2-41bdf8b563` queda dudosa, no rechazada, porque una persona todavía podría sostener la guarda breve si lo deja escrito.

### Anexo ya rechazado

Se leyó aparte. Sigue aparte. Ninguna frase aceptada repite estos textos.

| Id | Por qué se confirma el rechazo |
|---|---|
| `rechazo-v2-001` | cultivo_no_permitido: palto; la lista usa palta; region_no_permitida: Pangoa es un distrito y no entra en region; esqueleto_de_plantilla: preparar el terreno antes de sembrar más un cultivo intercambiable; etiqueta_no_asignada |
| `rechazo-v2-002` | par_de_plantilla_con: rechazo-v2-003; al_enmascarar_el_cultivo_el_esqueleto_coincide; etiqueta_no_asignada |
| `rechazo-v2-003` | par_de_plantilla_con: rechazo-v2-002; al_enmascarar_el_cultivo_el_esqueleto_coincide; etiqueta_no_asignada |
| `rechazo-v2-004` | region_no_mencionada_en_el_texto; etiqueta_no_asignada |
| `rechazo-v2-005` | Un borrador repetía la pregunta q-riego-floracion de backend/evaluation/data/pmv1_baseline.json. El texto no se archiva para no copiar esa pregunta. |

`rechazo-v2-005` no archiva el texto, para no copiar la pregunta de `pmv1_baseline.json`. Eso se mantiene.

## 5. Las 48 fronteras

Las 48 notas se leyeron una por una. **Las 48 se sostienen.** En ninguna la nota contradice el texto ni fuerza una clase que el texto no pide. Por ser fronteras, las 48 quedan con segunda revisión humana aunque el resultado de esta auditoría sea correcta.

Pares que muestran el mismo criterio, bien separados:

- Agua solo por el frío anunciado (`piloto-v2-4d8651680b`, clima) frente al intervalo de riego cuando el viento seca (`piloto-v2-f454b7c529`, riego).
- Sequía como evento (`piloto-v2-59a61015e2`, `piloto-v2-e57aab2fbf`, clima) frente a cómo mojar en la semana seca (`piloto-v2-dacf26a183`, `piloto-v2-18d29e2be0`, riego).
- Tiempo que se deja correr la acequia (`piloto-v2-7f4b6435a7`, riego) frente a la zanja del bajo (`piloto-v2-3f8c9f09bd`, suelos) y frente a limpiar la zanja que embebe (`piloto-v2-80f3cb2f44`, suelos).
- Pudrición de la piña en planta (`piloto-v2-09973b49b9`, enfermedad) frente al color y el olor para cortarla (`piloto-v2-3a3ecfb9c3`, cosecha).
- Kion para sacarlo (`piloto-v2-0e420f3289`, cosecha) frente a pudrición todavía en la era (`piloto-v2-37eabf9a20`, enfermedad).
- Granadilla arrugada como madurez (`piloto-v2-9018b8aefd`, cosecha) frente a mancha aceitosa en planta (`piloto-v2-d9aa2b7030`, enfermedad).
- Semilla el día del recojo (`piloto-v2-c0a9c01736`, cosecha) frente a semilla ya guardada para volver a sembrar (`piloto-v2-6eab714edd`, siembra).
- Tres preguntas de análisis de suelo, todas en suelos y ninguna sobre dosis: si dice la acidez (`piloto-v2-09602c7344`), de cuántos puntos sale la muestra (`piloto-v2-b77cefb95c`) y hasta qué profundidad (`piloto-v2-038ffc061a`).

## 6. Consistencia de las ocho categorías

El criterio usado es el de la taxonomía: la categoría es la decisión pedida, no el cultivo, no la provincia y no la labor que solo se menciona de paso. Ese criterio se mantiene dentro de cada clase.

- **Riego.** Frecuencia, hora, método, turno, reparto y encharcamiento causado por el propio riego. El agua contra una helada no está en esta clase.
- **Fertilización y nutrición.** Fuente, momento, lugar y cantidad de abono, o un síntoma que la pregunta atribuye a falta de comida. Once de 24 dicen «comida». Eso no vuelve falsa la etiqueta, pero deja un atajo léxico. No se reescriben.
- **Plagas.** Animal visto, o un nombre de organismo animal (cochinilla, broca, nematodo, trips, ácaro, babosa). Recoger mazorcas o quitar brotes, cuando el fin es ese organismo, se quedó en plagas.
- **Enfermedades.** Mancha, polvo, pudrición o «mal», sin un animal como causa. El polvo blanco del envés de la papa se sostiene. «¿Lavo el polvo blanco del brote?» no.
- **Siembra y manejo.** Fecha, densidad, semilla para sembrar, variedad, aporque, deshierbo, poda, tutor y raleo. El viento o el frío quedan aquí solo cuando son antecedente o condición de la fecha, no cuando hay que proteger hoy.
- **Clima y heladas.** Helada, granizo, viento, sequía o lluvia tratados como evento, y la protección o el daño de ese evento.
- **Suelos.** Compactación, piedras, cascajo, textura, erosión, terraza, cárcava, drenaje y el análisis cuando la decisión es el terreno.
- **Cosecha y poscosecha.** Madurez, corte, oreo, secado, selección, trilla y guarda en finca.

Problemas de criterio, sin cambiar la taxonomía:

1. Hay fronteras del mismo tipo con nota y sin nota. Sin nota, y aun así correctas con reserva: cortinas vivas ante el viento (`piloto-v2-1d4ef1a7bd`), broca ya en el tendal (`piloto-v2-cae4b79822`), mazorcas picadas para bajar la plaga (`piloto-v2-9c434b0971`), «echar algo al pie» (`piloto-v2-df7f31f7d9`), borde seco atribuido a alimento (`piloto-v2-dc3422090c`), hilos blancos sin picadura (`piloto-v2-86f762efd9`), fruta sin dulce (`piloto-v2-c77fa8da96`), emparejar la era (`piloto-v2-45d1e6b6b2`) y la cochinilla con una pregunta incompleta (`piloto-v2-5d8c063a1b`).
2. «Comida» concentra 11 de las 24 de fertilización. Un clasificador podría aprender esa palabra y no la decisión. No es motivo para reetiquetar ni para reescribir.
3. El equilibrio de 24 por clase es de construcción. No describe cuántas consultas de cada tipo haría un agricultor.
4. El umbral automático (Jaccard de tokens ≥ 0.60, o SequenceMatcher ≥ 0.84 con Jaccard enmascarado ≥ 0.45) dio 0 parejas. La pareja más cercana por dentro del piloto está por debajo: «¿Qué es el polvo blanco del envés de la papa?» y «¿Lavo el polvo blanco del brote?», Jaccard 0.38. El control no vio la etiqueta débil. Por eso no basta el control automático.

No se encontró una consulta compuesta del tipo «cómo riego y qué abono echo» partida en dos o forzada a una sola clase.

Cultivo y región: los 143 `crop` y las 45 `region` están en el texto y en las listas vigentes. Donde hay dos cultivos de la lista, `crop` está omitido (`piloto-v2-a8733a38d2`, `piloto-v2-f68641c5eb`, `piloto-v2-c79efdcc92`). No aparece `palto` ni Pangoa. «Papaya» no se guardó como papa. «Anaranjado» y «empapa» no se tomaron como cultivo. Los identificadores coinciden con los 10 primeros hexadecimales del SHA-256 del texto. No hay duplicado exacto tras normalizar.

Tangelo no aparece. No es un error de fila: la lista de cultivos no obliga a usarlos todos.

## 7. Similitud semántica

No hay paráfrasis evidente que obligue a dejar una sola fila. Estas vecindades deben verse juntas en cualquier revisión futura. Si algún día hubiera particiones, no se separarían sin esa revisión. Esta auditoría no crea particiones.

- `piloto-v2-464c8602df` y `piloto-v2-99b5624803`: el mismo polvo blanco. La primera se sostiene; la segunda queda dudosa.
- `piloto-v2-59a61015e2` y `piloto-v2-e57aab2fbf`: hoja enrollada, seca y un aviso. Una pregunta es qué hacer por el evento; la otra, cómo leer un aviso que no aclara. No son la misma decisión.
- `piloto-v2-2e641787b4` y `piloto-v2-a9b2494770`: «¿La poda de X se hace A o B?». Cultivos y momentos distintos. No es el par de plantilla que ya fue rechazado en el anexo.
- `piloto-v2-dc0403db77` frente a `ilustrativo-014`: las dos preguntan «cuántas» en maíz choclo. La del piloto es después de ralear y lo dice. No es copia.
- `piloto-v2-3b4b3b1aab` frente a `ilustrativo-001`: las dos abren con «cada cuántos días». Una es cuando ya no llueve, sin cultivo; la otra es la papa en floración. No es copia. Tampoco es el par rechazado «cada cuántos días le echo agua al café / a la papa».
- `piloto-v2-4edfdc6c89` frente a `ilustrativo-003`: «seguir regando cuando ya está formado». Otro cultivo y otra frase.
- `piloto-v2-e50652643a` frente a `ilustrativo-016`: haba que recién asoma y madrugada fría. La del piloto pregunta por el humo. No es la misma frase.
- `piloto-v2-cb881ee34d` y `piloto-v2-ec82906d33` no copian las preguntas de riego del PMV1. La más cercana por solapamiento de palabras con el PMV1 fue un falso encuentro por la palabra papa.

## 8. Verificación agronómica

Esta auditoría no responde las consultas y no atribuye dosis, calendarios ni diagnósticos a las fichas de `fuentes_v2.json`. Esas fichas dicen que los PDF no se abrieron. Aquí tampoco se abrieron, y no hacen falta para juzgar la etiqueta.

La etiqueta no depende de que el síntoma sea, en el campo, lo que el texto supone. Sí haría falta una persona con criterio agronómico **para responder**, no para sostener la categoría, en preguntas como los cojines hinchados del cacao (`piloto-v2-0a82b13fc3`), la broca en el tendal (`piloto-v2-cae4b79822`), los nudos atribuidos a nematodos (`piloto-v2-fc0655fb7f`), la helada negra (`piloto-v2-c39737c2a1`) y el aceite en el pelo de la mazorca (`piloto-v2-ef39bdf389`). En todas ellas la categoría se sostiene por la decisión pedida.

## 9. Limitaciones

- Un solo revisor, sin recorrido de campo y sin abrir los manuales. No sustituye la segunda revisión humana del manifiesto.
- La similitud se juzgó por lectura y por solapamiento de palabras. No se usó un modelo de embeddings. Puede quedar alguna paráfrasis que esta lectura no vio. Por dentro del piloto, solo seis parejas alcanzaron Jaccard 0.22, y ninguna llegó a 0.40.
- No se inventó agronomía para desempatar la ceniza, el polvo blanco del brote ni la venta del olluco.
- «Correcta» en este informe quiere decir que la etiqueta aguanta la lectura. No quiere decir aprobada para entrenar.
- Las 132 sin segunda revisión marcada siguen dentro de un conjunto no aprobado.

## 10. Registro de las 192

Orden del archivo `aceptadas_v2.jsonl`.

### 1. `piloto-v2-3b4b3b1aab`

- **Categoría actual:** `riego`
- **Resultado:** correcta
- **Justificación:** Pide cada cuántos días mojar la chacra cuando ya no llueve. Es calendario de riego, sin evento de helada ni obra de drenaje. No nombra cultivo ni provincia.
- **Corrección propuesta:** Ninguna.
- **Confianza:** alta
- **Segunda revisión humana:** no
- **Texto:** ¿Cada cuántos días mojo la chacra cuando ya no llueve?

### 2. `piloto-v2-0ae231115b`

- **Categoría actual:** `fertilizacion_nutricion`
- **Resultado:** correcta
- **Justificación:** Pregunta si a la papa le falta comida. La nota separa bien esa decisión de una identificación de enfermedad o de un insecto. El amarilleo, por sí solo, no cambia la etiqueta.
- **Corrección propuesta:** Ninguna. La nota de frontera se sostiene; no se reescribe el texto.
- **Confianza:** media
- **Segunda revisión humana:** sí
- **Cultivo:** papa
- **Nota de frontera ya presente:** La decisión pedida es si falta alimento. No pide el nombre de una enfermedad ni habla de un insecto.
- **Texto:** Las hojas de abajo de la papa se ponen amarillas y la planta no crece. ¿Le falta comida o espero a ver si reacciona sola?

### 3. `piloto-v2-633bba6f57`

- **Categoría actual:** `plagas`
- **Resultado:** correcta
- **Justificación:** Describe larvas dentro del tallo de la papa, con aserrín, y pide bajar esa población. El daño lo causa un animal visto.
- **Corrección propuesta:** Ninguna.
- **Confianza:** alta
- **Segunda revisión humana:** no
- **Cultivo:** papa
- **Texto:** En la papa encontré larvas dentro del tallo, con aserrín en la entrada del hoyito. ¿Cómo bajo esa población antes de que seque la mata?

### 4. `piloto-v2-464c8602df`

- **Categoría actual:** `enfermedades_cultivos`
- **Resultado:** correcta
- **Justificación:** Pide identificar el polvo blanco del envés de la papa y no describe un animal. La nota se sostiene. No es la misma pregunta que piloto-v2-99b5624803, que queda dudosa.
- **Corrección propuesta:** Ninguna. La nota de frontera se sostiene; no se reescribe el texto.
- **Confianza:** media
- **Segunda revisión humana:** sí
- **Cultivo:** papa
- **Nota de frontera ya presente:** La decisión es identificar el polvo de la hoja. No describe un insecto.
- **Texto:** ¿Qué es el polvo blanco del envés de la papa?

### 5. `piloto-v2-cce1fc45cb`

- **Categoría actual:** `siembra_manejo_cultivo`
- **Resultado:** correcta
- **Justificación:** Pregunta en qué semana de octubre, o si en noviembre, poner la semilla de papa en la zona alta. Es ventana de siembra. «Zona alta» no es una provincia y region queda omitida con razón.
- **Corrección propuesta:** Ninguna.
- **Confianza:** alta
- **Segunda revisión humana:** no
- **Cultivo:** papa
- **Texto:** ¿En qué semana de octubre pongo la semilla de papa en la zona alta, o ya es mejor esperar a noviembre?

### 6. `piloto-v2-e50652643a`

- **Categoría actual:** `clima_heladas`
- **Resultado:** correcta
- **Justificación:** Pide si el humo alcanza para la haba que recién asoma ante una madrugada muy fría. Es protección ante el frío. Se parece en el tema a ilustrativo-016, pero la decisión es una práctica concreta y el texto no copia esa frase.
- **Corrección propuesta:** Ninguna.
- **Confianza:** alta
- **Segunda revisión humana:** no
- **Cultivo:** haba
- **Texto:** Anuncian una madrugada muy fría para la haba que recién asoma. ¿Le prendo humo en varios puntos de la chacra o eso no alcanza?

### 7. `piloto-v2-21cfb68647`

- **Categoría actual:** `suelos`
- **Resultado:** correcta
- **Justificación:** Pregunta si un piso compacto de maca se abre con varias pasadas o si hay que buscar otro sitio. El objeto es el terreno. El tema se acerca a ilustrativo-019 sin repetir su frase.
- **Corrección propuesta:** Ninguna.
- **Confianza:** alta
- **Segunda revisión humana:** no
- **Cultivo:** maca
- **Texto:** Para la maca elegí un sitio que suena hueco bajo la lampa, de tan compacto. ¿Ese piso se puede abrir con varias pasadas o busco otro pedazo de chacra?

### 8. `piloto-v2-66283680d0`

- **Categoría actual:** `cosecha_poscosecha`
- **Resultado:** correcta
- **Justificación:** Pregunta si en el café se pasa solo el grano rojo. Es selección de cosecha.
- **Corrección propuesta:** Ninguna.
- **Confianza:** alta
- **Segunda revisión humana:** no
- **Cultivo:** café
- **Texto:** ¿Paso solo el grano rojo del café?

### 9. `piloto-v2-cb881ee34d`

- **Categoría actual:** `riego`
- **Resultado:** correcta
- **Justificación:** La papa está en flor, la tierra está seca y pregunta si echar agua hoy o mañana. Es un turno de riego. No reproduce la pregunta de floración del PMV1 ni la de ilustrativo-001.
- **Corrección propuesta:** Ninguna.
- **Confianza:** alta
- **Segunda revisión humana:** no
- **Cultivo:** papa
- **Texto:** La papa está en flor y la tierra se siente seca. ¿Le echo agua hoy o espero a mañana?

### 10. `piloto-v2-145c42bc6e`

- **Categoría actual:** `fertilizacion_nutricion`
- **Resultado:** correcta
- **Justificación:** Pregunta en qué momento poner gallinaza al maíz choclo. La decisión es la fuente y el momento del abono.
- **Corrección propuesta:** Ninguna.
- **Confianza:** alta
- **Segunda revisión humana:** no
- **Cultivo:** maíz choclo
- **Texto:** ¿En qué momento le pongo gallinaza al maíz choclo, antes de tapar la semilla o cuando ya tiene cuatro hojas?

### 11. `piloto-v2-043f2713a7`

- **Categoría actual:** `plagas`
- **Resultado:** correcta
- **Justificación:** Hay bichos negros en el brote de la haba y pregunta si aplastarlos o si ya pasaron a la vaina. El organismo es un animal.
- **Corrección propuesta:** Ninguna.
- **Confianza:** alta
- **Segunda revisión humana:** no
- **Cultivo:** haba
- **Texto:** La haba está llena de bichos negros en el brote. ¿Los aplasto o ya se pasaron a la vaina?

### 12. `piloto-v2-b57d572039`

- **Categoría actual:** `enfermedades_cultivos`
- **Resultado:** correcta
- **Justificación:** Manchas redondas con centro seco en el café: cortar hojas o ver si ya está en la rama. No hay un animal como causa.
- **Corrección propuesta:** Ninguna.
- **Confianza:** alta
- **Segunda revisión humana:** no
- **Cultivo:** café
- **Texto:** En el café las hojas tienen manchas redondas con el centro seco. ¿Las corto o el problema ya está en la rama?

### 13. `piloto-v2-e70ef2c5ca`

- **Categoría actual:** `siembra_manejo_cultivo`
- **Resultado:** correcta
- **Justificación:** Pregunta si dejar la quinua a un palmo. Es densidad de siembra.
- **Corrección propuesta:** Ninguna.
- **Confianza:** alta
- **Segunda revisión humana:** no
- **Cultivo:** quinua
- **Texto:** ¿Dejo la quinua a un palmo?

### 14. `piloto-v2-f122203a54`

- **Categoría actual:** `clima_heladas`
- **Resultado:** correcta
- **Justificación:** Cayó granizo fino y pregunta si revisar hoy. La categoría es clara. El texto es muy breve y no dice cultivo; eso no abre otra categoría.
- **Corrección propuesta:** Ninguna.
- **Confianza:** media
- **Segunda revisión humana:** no
- **Texto:** Cayó granizo fino. ¿Reviso hoy?

### 15. `piloto-v2-ff4bc93ac0`

- **Categoría actual:** `suelos`
- **Resultado:** correcta
- **Justificación:** Pregunta qué hacer con las piedras grandes. El hoyo de siembra es el uso previsto, como dice la nota, no la decisión.
- **Corrección propuesta:** Ninguna. La nota de frontera se sostiene; no se reescribe el texto.
- **Confianza:** alta
- **Segunda revisión humana:** sí
- **Nota de frontera ya presente:** La decisión es qué hacer con las piedras. El hoyo se menciona solo como el uso previsto del terreno.
- **Texto:** ¿Las piedras grandes se sacan de la melga o se pueden dejar a un lado si el hoyo de siembra cae entre ellas?

### 16. `piloto-v2-0e420f3289`

- **Categoría actual:** `cosecha_poscosecha`
- **Resultado:** correcta
- **Justificación:** Pregunta si el tallo doblado y la hoja amarilla avisan que el rizoma de kion ya está para sacarlo. La nota se sostiene. Esta auditoría no confirma que ese síntoma sea señal de madurez.
- **Corrección propuesta:** Ninguna. La nota de frontera se sostiene; no se reescribe el texto.
- **Confianza:** media
- **Segunda revisión humana:** sí
- **Cultivo:** kion
- **Nota de frontera ya presente:** Pregunta si el rizoma ya está para sacarlo. No pide identificar una enfermedad de la hoja.
- **Texto:** El tallo del kion se está doblando y la hoja amarillea. ¿Eso avisa que el rizoma ya está para sacarlo?

### 17. `piloto-v2-901190ee91`

- **Categoría actual:** `riego`
- **Resultado:** correcta
- **Justificación:** Pregunta si una poza de palta en Chanchamayo se llena una vez o otra vez a mitad de semana. Cultivo y provincia están en el texto y en la lista.
- **Corrección propuesta:** Ninguna.
- **Confianza:** alta
- **Segunda revisión humana:** no
- **Cultivo:** palta
- **Región:** Chanchamayo
- **Texto:** La palta de Chanchamayo está cargada y el pozo rinde poco. ¿Alcanza con mojar la poza una vez o tengo que volver a llenarla a mitad de semana?

### 18. `piloto-v2-6cb18529e8`

- **Categoría actual:** `fertilizacion_nutricion`
- **Resultado:** correcta
- **Justificación:** Después del recojo del café pregunta si alcanza la pulpa descompuesta u otra fuente de comida. La nota separa bien esa decisión del secado y de la guarda.
- **Corrección propuesta:** Ninguna. La nota de frontera se sostiene; no se reescribe el texto.
- **Confianza:** media
- **Segunda revisión humana:** sí
- **Cultivo:** café
- **Nota de frontera ya presente:** La decisión es la fuente de alimento después del recojo. No pide cómo secar ni cómo guardar el grano.
- **Texto:** El café después del recojo queda flaco. ¿Le alcanza con la pulpa descompuesta o hace falta otra fuente de comida?

### 19. `piloto-v2-42ee1ad613`

- **Categoría actual:** `plagas`
- **Resultado:** correcta
- **Justificación:** Telaraña fina, puntitos que caminan y hojas bronceadas: pregunta qué hacer con esos animalitos. No nombra cultivo y crop queda omitido.
- **Corrección propuesta:** Ninguna.
- **Confianza:** alta
- **Segunda revisión humana:** no
- **Texto:** Hay telaraña fina y puntitos que caminan bajo la hoja. Las hojas se ven bronceadas. ¿Qué hago con esos animalitos?

### 20. `piloto-v2-0a82b13fc3`

- **Categoría actual:** `enfermedades_cultivos`
- **Resultado:** correcta
- **Justificación:** Cojines hinchados en el tronco del cacao y secado de una rama: pregunta qué revisar para saber si es un mal del tronco. La etiqueta no exige ponerle nombre a la enfermedad. Responderla sí pediría verificación agronómica, que esta auditoría no hace.
- **Corrección propuesta:** Ninguna.
- **Confianza:** alta
- **Segunda revisión humana:** no
- **Cultivo:** cacao
- **Texto:** Unos cojines del tronco del cacao se ven hinchados y el árbol se seca por una sola rama. ¿Qué reviso para saber si es un mal del tronco?

### 21. `piloto-v2-c40a26bcbb`

- **Categoría actual:** `siembra_manejo_cultivo`
- **Resultado:** correcta
- **Justificación:** Pregunta si el alambre tutor de la granadilla va antes de la flor o cuando el brote trepa. El tutorado entra en siembra y manejo.
- **Corrección propuesta:** Ninguna.
- **Confianza:** alta
- **Segunda revisión humana:** no
- **Cultivo:** granadilla
- **Texto:** Quiero tutor para la granadilla y no sé si el alambre va antes de la flor o cuando el brote ya trepa.

### 22. `piloto-v2-4d8651680b`

- **Categoría actual:** `clima_heladas`
- **Resultado:** correcta
- **Justificación:** En Yauli el agua se menciona solo para el frío anunciado sobre la papa en brote. La nota aplica el criterio de la taxonomía: riego cuyo único fin es atenuar el frío es clima_heladas.
- **Corrección propuesta:** Ninguna. La nota de frontera se sostiene; no se reescribe el texto.
- **Confianza:** alta
- **Segunda revisión humana:** sí
- **Cultivo:** papa
- **Región:** Yauli
- **Nota de frontera ya presente:** El agua se menciona solo como posible protección ante el frío anunciado. No pide el calendario normal de riego.
- **Texto:** En Yauli anuncian frío de varios grados bajo cero y la papa está en brote. ¿Muevo el turno de agua de mañana para esta noche, solo por ese frío, o el agua no sirve en este caso?

### 23. `piloto-v2-3f8c9f09bd`

- **Categoría actual:** `suelos`
- **Resultado:** correcta
- **Justificación:** La yuca amarillea solo en el bajo que no seca y pregunta si el arreglo es una zanja hacia la quebrada. La nota se sostiene: la decisión es sacar el agua estancada.
- **Corrección propuesta:** Ninguna. La nota de frontera se sostiene; no se reescribe el texto.
- **Confianza:** media
- **Segunda revisión humana:** sí
- **Cultivo:** yuca
- **Región:** Satipo
- **Nota de frontera ya presente:** La decisión es sacar el agua estancada del bajo. No pide un turno de riego ni el nombre de una enfermedad.
- **Texto:** La yuca de Satipo amarillea solo en el bajo, donde el barro no seca ni en tres días de sol. ¿El arreglo es sacar esa agua con una zanja hacia la quebrada?

### 24. `piloto-v2-42a7ef097a`

- **Categoría actual:** `cosecha_poscosecha`
- **Resultado:** correcta
- **Justificación:** La naranja pesa y sigue verde: dejarla o cortarla aunque el color no cambie. Es punto de corte.
- **Corrección propuesta:** Ninguna.
- **Confianza:** alta
- **Segunda revisión humana:** no
- **Cultivo:** naranja
- **Texto:** La naranja ya pesa en la mano y sigue verde. ¿La dejo en el árbol o el color no importa para cortarla?

### 25. `piloto-v2-b51869403f`

- **Categoría actual:** `riego`
- **Resultado:** correcta
- **Justificación:** Pregunta si el café en llenado de grano aguanta estirar el riego una semana. Es calendario de riego.
- **Corrección propuesta:** Ninguna.
- **Confianza:** alta
- **Segunda revisión humana:** no
- **Cultivo:** café
- **Texto:** ¿El café en llenado de grano aguanta si estiro el riego una semana?

### 26. `piloto-v2-8a8f4ad51d`

- **Categoría actual:** `fertilizacion_nutricion`
- **Resultado:** correcta
- **Justificación:** Pregunta si la urea quema la hoja del maíz amarillo duro. Es una decisión sobre el fertilizante. No afirma una dosis ni la atribuye a una fuente.
- **Corrección propuesta:** Ninguna.
- **Confianza:** alta
- **Segunda revisión humana:** no
- **Cultivo:** maíz amarillo duro
- **Texto:** ¿La urea quema la hoja del maíz amarillo duro?

### 27. `piloto-v2-263152bdbe`

- **Categoría actual:** `plagas`
- **Resultado:** correcta
- **Justificación:** Hay un gusano vivo en el cogollo del maíz amiláceo en Jauja y pregunta a cuántas plantas revisar. Cultivo, provincia y categoría coinciden con el texto.
- **Corrección propuesta:** Ninguna.
- **Confianza:** alta
- **Segunda revisión humana:** no
- **Cultivo:** maíz amiláceo
- **Región:** Jauja
- **Texto:** En Jauja el maíz amiláceo tiene el cogollo comido y, al abrir la hoja del centro, encuentro un gusano vivo adentro, con restos húmedos alrededor. No es una mata sola: ya vi tres en el mismo surco y otras que todavía parecen sanas. ¿Reviso todas las plantas de la chacra o solo las que ya muestran el daño en el cogollo?

### 28. `piloto-v2-1ffb81b060`

- **Categoría actual:** `enfermedades_cultivos`
- **Resultado:** correcta
- **Justificación:** Polvo anaranjado que mancha los dedos y si se contagia a las plantas de al lado. Es síntoma de enfermedad, sin animal. «Anaranjado» no es el cultivo naranja; omitir crop es correcto.
- **Corrección propuesta:** Ninguna.
- **Confianza:** alta
- **Segunda revisión humana:** no
- **Texto:** Apareció un polvo anaranjado que mancha los dedos al tocar la hoja. ¿Eso se contagia a las plantas de al lado?

### 29. `piloto-v2-dc0403db77`

- **Categoría actual:** `siembra_manejo_cultivo`
- **Resultado:** correcta
- **Justificación:** Pregunta cuántas plantas de maíz choclo dejar por metro después de ralear, y dice que no es al echar la semilla. Es densidad. Se distingue de ilustrativo-014, que pregunta semillas por golpe al sembrar.
- **Corrección propuesta:** Ninguna.
- **Confianza:** alta
- **Segunda revisión humana:** no
- **Cultivo:** maíz choclo
- **Texto:** ¿Cuántas plantas de maíz choclo dejo por metro después de ralear, no al momento de echar la semilla?

### 30. `piloto-v2-1d4ef1a7bd`

- **Categoría actual:** `clima_heladas`
- **Resultado:** correcta
- **Justificación:** En la parte alta de Junín el viento tumba plantas y seca la hoja, y pregunta si amortiguarlo con cortinas vivas o esperar. La decisión es la protección ante ese viento, así que clima_heladas se sostiene. La cortina viva roza siembra y manejo, y esa frontera no tiene nota. Region Junín es válida porque no hay provincia.
- **Corrección propuesta:** Ninguna etiqueta nueva. Conviene una nota de frontera si la fila se conserva. No reescribir el texto para acercarlo a la clase.
- **Confianza:** media
- **Segunda revisión humana:** sí
- **Región:** Junín
- **Texto:** En la parte alta de Junín el viento de agosto tumba las plantas y seca la hoja en un solo día. ¿Ese viento se amortigua con cortinas vivas o espero a que pase la semana y miro qué quedó en pie?

### 31. `piloto-v2-9df9e6a009`

- **Categoría actual:** `suelos`
- **Resultado:** correcta
- **Justificación:** El cascajo menudo deforma la raíz de la zanahoria: zarandearlo o convivir con él. La decisión es sobre el terreno.
- **Corrección propuesta:** Ninguna.
- **Confianza:** alta
- **Segunda revisión humana:** no
- **Cultivo:** zanahoria
- **Texto:** La era de la zanahoria tiene cascajo menudo que deforma la raíz. ¿Lo zarandeo antes de armar la melga o convivo con él?

### 32. `piloto-v2-62b417b77a`

- **Categoría actual:** `cosecha_poscosecha`
- **Resultado:** correcta
- **Justificación:** Pregunta si la papa se orea en el surco o se mete a la sombra el mismo día del arranque. Es oreo.
- **Corrección propuesta:** Ninguna.
- **Confianza:** alta
- **Segunda revisión humana:** no
- **Cultivo:** papa
- **Texto:** ¿La papa se orea unas horas en el mismo surco o la meto a la sombra el mismo día del arranque?

### 33. `piloto-v2-18d29e2be0`

- **Categoría actual:** `riego`
- **Resultado:** correcta
- **Justificación:** Pide cómo repartir el agua del surco de quinua para que abajo reciba sin ahogar arriba, en una semana sin lluvia. La nota se sostiene: no pide proteger el cultivo ante una sequía como evento. Region Junín coincide con «parte alta de Junín».
- **Corrección propuesta:** Ninguna. La nota de frontera se sostiene; no se reescribe el texto.
- **Confianza:** media
- **Segunda revisión humana:** sí
- **Cultivo:** quinua
- **Región:** Junín
- **Nota de frontera ya presente:** La decisión es repartir el agua en el surco. No pide proteger el cultivo ante una sequía como evento climático.
- **Texto:** La quinua de la parte alta de Junín tiene el surco de arriba empapado y el de abajo polvoriento. El agua entra de más por la cabecera. Quiero que las plantas de abajo también reciban, sin ahogar las de arriba, mientras siga esta semana sin lluvia. ¿Cómo reparto esa agua en el surco?

### 34. `piloto-v2-137dedd725`

- **Categoría actual:** `fertilizacion_nutricion`
- **Resultado:** correcta
- **Justificación:** La quinua salió despareja y pregunta si dar la misma cantidad de comida a todas. La decisión es el abono.
- **Corrección propuesta:** Ninguna.
- **Confianza:** alta
- **Segunda revisión humana:** no
- **Cultivo:** quinua
- **Texto:** La quinua de la ladera salió despareja: unas plantas verdes y otras pálidas. ¿Les doy la misma cantidad de comida a todas?

### 35. `piloto-v2-6f093fa01c`

- **Categoría actual:** `plagas`
- **Resultado:** correcta
- **Justificación:** Moscas blancas en el frijol y si bajarlas con agua y jabón. El organismo es un animal. El agua es medio de control, no un turno de riego.
- **Corrección propuesta:** Ninguna.
- **Confianza:** alta
- **Segunda revisión humana:** no
- **Cultivo:** frijol
- **Texto:** Unas moscas blancas se levantan cuando sacudo el frijol. ¿Las bajo con agua y jabón o eso no alcanza?

### 36. `piloto-v2-1e2ecdaa68`

- **Categoría actual:** `enfermedades_cultivos`
- **Resultado:** correcta
- **Justificación:** Manchas chocolate en hoja y vaina de haba en Jauja, sin insecto, y si sacar esas hojas. No se le pone nombre de enfermedad. La decisión es el manejo del síntoma.
- **Corrección propuesta:** Ninguna.
- **Confianza:** alta
- **Segunda revisión humana:** no
- **Cultivo:** haba
- **Región:** Jauja
- **Texto:** En Jauja las habas tienen manchas chocolate en la hoja y en la vaina. No hay insecto a la vista. ¿Saco las hojas manchadas de la chacra o las dejo en el surco?

### 37. `piloto-v2-a3e3d16ab5`

- **Categoría actual:** `siembra_manejo_cultivo`
- **Resultado:** correcta
- **Justificación:** En Concepción pregunta si abrir los surcos de haba o poner menos semilla por golpe. La nota se sostiene: el viento del año pasado es antecedente, no un evento a proteger ahora.
- **Corrección propuesta:** Ninguna. La nota de frontera se sostiene; no se reescribe el texto.
- **Confianza:** alta
- **Segunda revisión humana:** sí
- **Cultivo:** haba
- **Región:** Concepción
- **Nota de frontera ya presente:** La decisión es la distancia y la cantidad de semilla. El viento del año pasado se menciona como antecedente, no como un evento que haya que proteger ahora.
- **Texto:** En Concepción las habas del año pasado quedaron muy tupidas, se tumbaron con el viento y casi no se pudo entrar al surco a cosecharlas. Este año no quiero repetir ese trazo. Puedo abrir más la distancia entre surcos o dejar el mismo ancho y poner menos semillas en cada golpe. ¿Cuál de las dos formas evita que se vuelvan a tumbar?

### 38. `piloto-v2-59a61015e2`

- **Categoría actual:** `clima_heladas`
- **Resultado:** correcta
- **Justificación:** La sequía de tres semanas y el aviso de que sigue se consultan como evento. La nota se sostiene. No pide un calendario de riego. Comparte escenario con piloto-v2-e57aab2fbf, pero la decisión es otra: si hay algo que hacer por el evento.
- **Corrección propuesta:** Ninguna. La nota de frontera se sostiene; no se reescribe el texto.
- **Confianza:** media
- **Segunda revisión humana:** sí
- **Cultivo:** maíz amiláceo
- **Nota de frontera ya presente:** La sequía se consulta como evento climático anunciado. No pide un calendario de riego ni una obra en el terreno.
- **Texto:** La sequía ya va tres semanas y el maíz amiláceo enrolla la hoja desde el mediodía. El aviso dice que la seca sigue. ¿Hay algo que hacer por este evento, aparte de mirar el cielo?

### 39. `piloto-v2-60e345941d`

- **Categoría actual:** `suelos`
- **Resultado:** correcta
- **Justificación:** En Huancayo pregunta si frenar la erosión con terrazas o con barreras de pasto. La nota se sostiene: la lluvia es la causa del arrastre, no un evento del que haya que proteger la planta esta noche.
- **Corrección propuesta:** Ninguna. La nota de frontera se sostiene; no se reescribe el texto.
- **Confianza:** alta
- **Segunda revisión humana:** sí
- **Región:** Huancayo
- **Nota de frontera ya presente:** La decisión es frenar la erosión. La lluvia se menciona como la causa del arrastre, no como un evento del que haya que proteger la planta esta noche.
- **Texto:** En Huancayo la ladera se está llevando la capa de arriba cuando llueve fuerte: se ven canalitos y la raíz queda al aire. ¿Eso se frena con terrazas o con barreras de pasto en el bordo?

### 40. `piloto-v2-b7c77ab25c`

- **Categoría actual:** `cosecha_poscosecha`
- **Resultado:** correcta
- **Justificación:** El cacao de Satipo pasa la noche en un balde cerrado y pregunta si esa demora altera el grano. Es guarda breve en finca.
- **Corrección propuesta:** Ninguna.
- **Confianza:** alta
- **Segunda revisión humana:** no
- **Cultivo:** cacao
- **Región:** Satipo
- **Texto:** En Satipo junto el cacao en baldes y, cuando el día se alarga, ese balde pasa la noche cerrado antes de que pueda partir la mazorca. A veces el grano amanece más caliente que al mediodía. No sé si esa espera lo cambia o si puedo abrirlo al día siguiente, apenas tenga sombra y tiempo. ¿La demora de una noche en el balde altera el grano?

### 41. `piloto-v2-02e732247e`

- **Categoría actual:** `riego`
- **Resultado:** correcta
- **Justificación:** El turno de agua es de madrugada y pregunta si alcanza una pasada. Es riego. No nombra cultivo.
- **Corrección propuesta:** Ninguna.
- **Confianza:** alta
- **Segunda revisión humana:** no
- **Texto:** El turno me toca de madrugada. ¿Alcanza una pasada?

### 42. `piloto-v2-6fac5aa3f2`

- **Categoría actual:** `fertilizacion_nutricion`
- **Resultado:** correcta
- **Justificación:** En Concepción pregunta si enterrar los restos de corral junto a la semilla de haba o dejarlos para la flor. Es momento y ubicación del abono.
- **Corrección propuesta:** Ninguna.
- **Confianza:** alta
- **Segunda revisión humana:** no
- **Cultivo:** haba
- **Región:** Concepción
- **Texto:** En Concepción las habas cuajaron poco y el tallo está delgado. El año pasado eché solo restos de corral al voleo. ¿Este año los entierro junto a la semilla o los dejo para cuando aparezcan las flores?

### 43. `piloto-v2-9c434b0971`

- **Categoría actual:** `plagas`
- **Resultado:** correcta
- **Justificación:** Pregunta si la plaga que perfora el cacao baja al recoger las mazorcas picadas. El fin declarado es la plaga, así que la etiqueta se sostiene. Recoger mazorcas roza cosecha y esa frontera no tiene nota.
- **Corrección propuesta:** Ninguna etiqueta nueva. Conviene una nota de frontera si la fila se conserva. No reescribir el texto para acercarlo a la clase.
- **Confianza:** media
- **Segunda revisión humana:** sí
- **Cultivo:** cacao
- **Texto:** ¿La plaga que perfora el fruto del cacao se baja recogiendo las mazorcas picadas?

### 44. `piloto-v2-41a6a3b1fb`

- **Categoría actual:** `enfermedades_cultivos`
- **Resultado:** correcta
- **Justificación:** Llama enfermedad a lo que seca la papa en pocos días y pregunta si se detiene sacando la mata. La decisión es el manejo de esa enfermedad.
- **Corrección propuesta:** Ninguna.
- **Confianza:** alta
- **Segunda revisión humana:** no
- **Cultivo:** papa
- **Texto:** ¿Esta enfermedad de la papa, la que seca la planta entera en pocos días, se detiene sacando la mata enferma?

### 45. `piloto-v2-2e641787b4`

- **Categoría actual:** `siembra_manejo_cultivo`
- **Resultado:** correcta
- **Justificación:** Pregunta si podar el café al terminar el recojo o cuando vuelve a brotar. La nota se sostiene. Comparte el molde «la poda de X se hace A o B» con la palta, pero los momentos y el cultivo son otros; no es paráfrasis.
- **Corrección propuesta:** Ninguna. La nota de frontera se sostiene; no se reescribe el texto.
- **Confianza:** alta
- **Segunda revisión humana:** sí
- **Cultivo:** café
- **Nota de frontera ya presente:** La decisión es el momento de la poda. No pide cómo secar el grano ni qué alimento echar.
- **Texto:** ¿La poda del café se hace apenas termina el recojo o cuando la planta vuelve a brotar?

### 46. `piloto-v2-f2c9713cce`

- **Categoría actual:** `clima_heladas`
- **Resultado:** correcta
- **Justificación:** Pregunta si la helada quema más la papa en flor que la que está en brote. Es efecto del evento climático.
- **Corrección propuesta:** Ninguna.
- **Confianza:** alta
- **Segunda revisión humana:** no
- **Cultivo:** papa
- **Texto:** ¿La helada de esta madrugada quema más la papa en flor que la que todavía está en brote?

### 47. `piloto-v2-09602c7344`

- **Categoría actual:** `suelos`
- **Resultado:** correcta
- **Justificación:** Pregunta si el análisis de suelo dice si la tierra es ácida. La nota se sostiene: no pide dosis de abono.
- **Corrección propuesta:** Ninguna. La nota de frontera se sostiene; no se reescribe el texto.
- **Confianza:** alta
- **Segunda revisión humana:** sí
- **Nota de frontera ya presente:** La pregunta es si la tierra es ácida. No pide una dosis de abono.
- **Texto:** ¿El análisis de suelo me dice si esta tierra es ácida?

### 48. `piloto-v2-e5c82b306a`

- **Categoría actual:** `cosecha_poscosecha`
- **Resultado:** correcta
- **Justificación:** Pregunta si la cosecha de quinua espera a que la panoja esté quebradiza. Es madurez de cosecha.
- **Corrección propuesta:** Ninguna.
- **Confianza:** alta
- **Segunda revisión humana:** no
- **Cultivo:** quinua
- **Texto:** ¿La cosecha de la quinua espera a que la panoja esté quebradiza?

### 49. `piloto-v2-4edfdc6c89`

- **Categoría actual:** `riego`
- **Resultado:** correcta
- **Justificación:** En Jauja pregunta si seguir regando el maíz amiláceo cuando la mazorca ya está formada. Es calendario de riego. El molde se parece a ilustrativo-003 sin copiarlo: otro cultivo y otra frase.
- **Corrección propuesta:** Ninguna.
- **Confianza:** alta
- **Segunda revisión humana:** no
- **Cultivo:** maíz amiláceo
- **Región:** Jauja
- **Texto:** En Jauja, ¿sigo con el riego del maíz amiláceo cuando la mazorca ya está formada?

### 50. `piloto-v2-9fb87f7148`

- **Categoría actual:** `fertilizacion_nutricion`
- **Resultado:** correcta
- **Justificación:** Pregunta si el compost caliente quema la raíz. Es una decisión sobre el abono. No nombra cultivo.
- **Corrección propuesta:** Ninguna.
- **Confianza:** alta
- **Segunda revisión humana:** no
- **Texto:** ¿El compost caliente quema la raíz?

### 51. `piloto-v2-7331c6887f`

- **Categoría actual:** `plagas`
- **Resultado:** correcta
- **Justificación:** Pulgones en la espiga del trigo: esperar mariquitas o intervenir. El organismo es un animal.
- **Corrección propuesta:** Ninguna.
- **Confianza:** alta
- **Segunda revisión humana:** no
- **Cultivo:** trigo
- **Texto:** El trigo tiene pulgones en la espiga. ¿Espero a que aparezcan mariquitas o intervengo yo?

### 52. `piloto-v2-09973b49b9`

- **Categoría actual:** `enfermedades_cultivos`
- **Resultado:** correcta
- **Justificación:** La base de la piña está blanda y con olor agrio, sin mordedura, y pregunta si cortarla para que no pase a las otras. La nota se sostiene. No es el punto de corte de piloto-v2-3a3ecfb9c3.
- **Corrección propuesta:** Ninguna. La nota de frontera se sostiene; no se reescribe el texto.
- **Confianza:** alta
- **Segunda revisión humana:** sí
- **Cultivo:** piña
- **Nota de frontera ya presente:** No hay mordedura. La decisión es la pudrición del fruto en la planta, no el punto de corte para la venta.
- **Texto:** La piña muestra la base del fruto blanda y con olor agrio, sin mordedura. ¿La corto para que no pase a las otras?

### 53. `piloto-v2-90a7ae5e24`

- **Categoría actual:** `siembra_manejo_cultivo`
- **Resultado:** correcta
- **Justificación:** Pregunta si deshierbar cuando la maleza está chica. El deshierbo entra en siembra y manejo.
- **Corrección propuesta:** Ninguna.
- **Confianza:** alta
- **Segunda revisión humana:** no
- **Texto:** ¿Deshierbo cuando la maleza está chica?

### 54. `piloto-v2-5192680295`

- **Categoría actual:** `clima_heladas`
- **Resultado:** correcta
- **Justificación:** Granizada sobre el trigo en espiga: si esas espigas pueden seguir. Es daño del granizo ya ocurrido.
- **Corrección propuesta:** Ninguna.
- **Confianza:** alta
- **Segunda revisión humana:** no
- **Cultivo:** trigo
- **Texto:** Cayó una granizada sobre el trigo en espiga. ¿Esas espigas machucadas pueden seguir o el daño ya no tiene arreglo?

### 55. `piloto-v2-6b80e8ac4f`

- **Categoría actual:** `suelos`
- **Resultado:** correcta
- **Justificación:** Piso de arado del maíz amiláceo en Jauja: si romper esa costra antes de la próxima campaña. Es preparación del terreno.
- **Corrección propuesta:** Ninguna.
- **Confianza:** alta
- **Segunda revisión humana:** no
- **Cultivo:** maíz amiláceo
- **Región:** Jauja
- **Texto:** El terreno del maíz amiláceo en Jauja queda con piso de arado: abajo duro y arriba suelto. ¿Rompo esa costra antes de la próxima campaña?

### 56. `piloto-v2-f3f2c394f1`

- **Categoría actual:** `cosecha_poscosecha`
- **Resultado:** correcta
- **Justificación:** Haba para grano seco: arrancar la planta o ir sacando las vainas negras. Es forma de cosecha.
- **Corrección propuesta:** Ninguna.
- **Confianza:** alta
- **Segunda revisión humana:** no
- **Cultivo:** haba
- **Texto:** Las habas para grano seco, ¿se arrancan con planta entera o se van sacando las vainas negras?

### 57. `piloto-v2-7f4b6435a7`

- **Categoría actual:** `riego`
- **Resultado:** correcta
- **Justificación:** El exceso vino de dejar correr la acequia y pregunta si la próxima vez cerrar antes. La nota se sostiene: no pide una zanja nueva. Encaja en la inclusión de riego sobre encharcamiento causado por el riego.
- **Corrección propuesta:** Ninguna. La nota de frontera se sostiene; no se reescribe el texto.
- **Confianza:** alta
- **Segunda revisión humana:** sí
- **Nota de frontera ya presente:** El exceso de agua lo causó la acequia que abrí. La decisión es cuánto tiempo dejar el agua, no una obra de drenaje.
- **Texto:** Ayer abrí la acequia un buen rato y hoy el piso sigue brilloso. Las plantas amanecieron decaídas, como si hubieran tenido el pie en agua toda la noche. No estoy pidiendo una zanja nueva. ¿La próxima vez cierro antes, o el daño vino de dejar correr el agua demasiado tiempo?

### 58. `piloto-v2-597103e2ad`

- **Categoría actual:** `fertilizacion_nutricion`
- **Resultado:** correcta
- **Justificación:** Zanahoria chica y hoja lavada, sin manchas ni mordeduras: qué darle para que engrose. La nota se sostiene.
- **Corrección propuesta:** Ninguna. La nota de frontera se sostiene; no se reescribe el texto.
- **Confianza:** alta
- **Segunda revisión humana:** sí
- **Cultivo:** zanahoria
- **Nota de frontera ya presente:** Se descartan manchas y mordeduras. La decisión es qué alimento dar para que la raíz engrose.
- **Texto:** La zanahoria sale chica y la hoja se ve lavada, sin manchas ni mordeduras. ¿Qué le puedo dar para que engrose?

### 59. `piloto-v2-c9dc91de32`

- **Categoría actual:** `plagas`
- **Resultado:** correcta
- **Justificación:** Costra con insectos quietos y hormigas en la palta de Chanchamayo: por cuál empezar. Los dos organismos son animales y la categoría sigue siendo una sola.
- **Corrección propuesta:** Ninguna.
- **Confianza:** alta
- **Segunda revisión humana:** no
- **Cultivo:** palta
- **Región:** Chanchamayo
- **Texto:** En la palta de Chanchamayo veo una costra con insectos quietos pegados a la nervadura, y una fila de hormigas que sube por el tronco hasta esa misma hoja. La costra no se va si la lavo con la mano. No sé si el daño lo hacen las hormigas o si ellas solo acompañan a los insectos quietos. ¿Por cuál de los dos empiezo?

### 60. `piloto-v2-c8deeb087d`

- **Categoría actual:** `enfermedades_cultivos`
- **Resultado:** correcta
- **Justificación:** Pregunta qué hacer con las pústulas del tallo. Es síntoma de enfermedad. No nombra cultivo.
- **Corrección propuesta:** Ninguna.
- **Confianza:** alta
- **Segunda revisión humana:** no
- **Texto:** ¿Qué hago con las pústulas del tallo?

### 61. `piloto-v2-c867fa6256`

- **Categoría actual:** `siembra_manejo_cultivo`
- **Resultado:** correcta
- **Justificación:** Pregunta qué variedad de papa aguanta mejor una campaña larga, precoz o tardía. La variedad entra en siembra y manejo.
- **Corrección propuesta:** Ninguna.
- **Confianza:** alta
- **Segunda revisión humana:** no
- **Cultivo:** papa
- **Texto:** ¿Qué variedad de papa aguanta mejor una campaña larga en esta zona, una precoz o una que tarde más?

### 62. `piloto-v2-44037fd77a`

- **Categoría actual:** `clima_heladas`
- **Resultado:** correcta
- **Justificación:** En Jauja anuncian lluvia fuerte con viento y pregunta si amarrar las panojas de quinua. La nota se sostiene. Mirar que el agua no se represé es vigilancia de ese evento, no una obra de drenaje.
- **Corrección propuesta:** Ninguna. La nota de frontera se sostiene; no se reescribe el texto.
- **Confianza:** media
- **Segunda revisión humana:** sí
- **Cultivo:** quinua
- **Región:** Jauja
- **Nota de frontera ya presente:** El evento es la lluvia con viento anunciada. No pide construir un drenaje del terreno.
- **Texto:** En Jauja la quinua está en panoja y anuncian lluvia fuerte con viento para esta noche. ¿Amarro las panojas antes de que llegue o las dejo y solo miro que el agua no se represé en el surco?

### 63. `piloto-v2-b995682db7`

- **Categoría actual:** `suelos`
- **Resultado:** correcta
- **Justificación:** Un manantial empapa una esquina todo el año: drenarla o dejarla fuera de cultivo. Es drenaje del terreno. «Empapa» no nombra el cultivo papa; omitir crop es correcto.
- **Corrección propuesta:** Ninguna.
- **Confianza:** alta
- **Segunda revisión humana:** no
- **Texto:** Hay un manantial que empapa una esquina todo el año. ¿Esa esquina se drena o la dejo fuera de cualquier cultivo?

### 64. `piloto-v2-2ed6d40afa`

- **Categoría actual:** `cosecha_poscosecha`
- **Resultado:** correcta
- **Justificación:** Maíz amiláceo en Jauja con la mazorca doblada: secarlo en la planta o cortarlo y colgarlo. Es secado de cosecha.
- **Corrección propuesta:** Ninguna.
- **Confianza:** alta
- **Segunda revisión humana:** no
- **Cultivo:** maíz amiláceo
- **Región:** Jauja
- **Texto:** En Jauja el maíz amiláceo ya tiene la mazorca doblada hacia abajo. ¿Lo dejo secar en la planta o lo corto y lo cuelgo bajo techo?

### 65. `piloto-v2-fdd583d86e`

- **Categoría actual:** `riego`
- **Resultado:** correcta
- **Justificación:** Pregunta si la haba en flor quiere agua seguido. Es frecuencia de riego.
- **Corrección propuesta:** Ninguna.
- **Confianza:** alta
- **Segunda revisión humana:** no
- **Cultivo:** haba
- **Texto:** ¿La haba en flor quiere agua seguido?

### 66. `piloto-v2-25660f26b2`

- **Categoría actual:** `fertilizacion_nutricion`
- **Resultado:** correcta
- **Justificación:** Pregunta si la cáscara del cacao alrededor del tronco alimenta. La decisión es si esa fuente nutre.
- **Corrección propuesta:** Ninguna.
- **Confianza:** alta
- **Segunda revisión humana:** no
- **Cultivo:** cacao
- **Texto:** ¿Al cacao le pongo la cáscara del mismo fruto alrededor del tronco o eso no alimenta?

### 67. `piloto-v2-93c9f28697`

- **Categoría actual:** `plagas`
- **Resultado:** correcta
- **Justificación:** Pregunta si sirve la trampa amarilla en el almácigo. Es control de insectos. No nombra cultivo.
- **Corrección propuesta:** Ninguna.
- **Confianza:** alta
- **Segunda revisión humana:** no
- **Texto:** ¿Sirve la trampa amarilla en el almácigo?

### 68. `piloto-v2-f4aca3376f`

- **Categoría actual:** `enfermedades_cultivos`
- **Resultado:** correcta
- **Justificación:** Mazorca con granos rayados y planta achaparrada, sin gusano: si puede ser un mal de la planta. La nota se sostiene.
- **Corrección propuesta:** Ninguna. La nota de frontera se sostiene; no se reescribe el texto.
- **Confianza:** alta
- **Segunda revisión humana:** sí
- **Cultivo:** maíz amiláceo
- **Nota de frontera ya presente:** No hay gusano. La decisión es si se trata de un mal de la planta.
- **Texto:** El maíz amiláceo tiene la mazorca con granos rayados y la planta queda achaparrada. No veo gusano. ¿Puede ser un mal de la planta?

### 69. `piloto-v2-a8733a38d2`

- **Categoría actual:** `siembra_manejo_cultivo`
- **Resultado:** correcta
- **Justificación:** En Tarma pregunta si el frijol va en el surco del maíz amiláceo o aparte. Es arreglo de siembra. Hay dos cultivos de la lista, así que omitir crop es lo que pide la regla del piloto. Tarma está en el texto.
- **Corrección propuesta:** Ninguna.
- **Confianza:** alta
- **Segunda revisión humana:** no
- **Región:** Tarma
- **Texto:** En Tarma, ¿el frijol va en el mismo surco del maíz amiláceo o en un surco aparte?

### 70. `piloto-v2-e81e1130dc`

- **Categoría actual:** `clima_heladas`
- **Resultado:** correcta
- **Justificación:** La cebada quedó con la hoja hecha tiras después del granizo: si puede seguir macollando. Es daño del granizo.
- **Corrección propuesta:** Ninguna.
- **Confianza:** alta
- **Segunda revisión humana:** no
- **Cultivo:** cebada
- **Texto:** La cebada quedó con la hoja hecha tiras después del granizo. ¿Esa planta puede seguir macollando o doy la campaña por perdida?

### 71. `piloto-v2-5eb777e476`

- **Categoría actual:** `suelos`
- **Resultado:** correcta
- **Justificación:** Pregunta si la tierra colorada y pegajosa se encostra al perder humedad y si así no le sirve al olluco. La nota se sostiene: el objeto es el suelo, no la fecha de siembra.
- **Corrección propuesta:** Ninguna. La nota de frontera se sostiene; no se reescribe el texto.
- **Confianza:** media
- **Segunda revisión humana:** sí
- **Cultivo:** olluco
- **Nota de frontera ya presente:** La pregunta es si esa tierra se encostra. No pide la fecha de siembra del olluco.
- **Texto:** ¿La tierra colorada y pegajosa se encostra apenas pierde humedad, y así no le sirve al olluco?

### 72. `piloto-v2-1f6c502167`

- **Categoría actual:** `cosecha_poscosecha`
- **Resultado:** correcta
- **Justificación:** Pregunta si la maca se saca con tierra y se lava después, o se limpia en la melga. Es manejo en el momento del arranque.
- **Corrección propuesta:** Ninguna.
- **Confianza:** alta
- **Segunda revisión humana:** no
- **Cultivo:** maca
- **Texto:** ¿La maca se saca con la tierra pegada y se lava después, o se limpia en la misma melga?

### 73. `piloto-v2-e676dde56d`

- **Categoría actual:** `riego`
- **Resultado:** correcta
- **Justificación:** En Tarma el canal llega día por medio: guardar el agua en pozas o soltarla al abrir la compuerta. Es método de riego. No nombra cultivo.
- **Corrección propuesta:** Ninguna.
- **Confianza:** alta
- **Segunda revisión humana:** no
- **Región:** Tarma
- **Texto:** En Tarma el canal llega día por medio. ¿Guardo esa agua en pozas o la suelto apenas abre la compuerta?

### 74. `piloto-v2-df7f31f7d9`

- **Categoría actual:** `fertilizacion_nutricion`
- **Resultado:** correcta
- **Justificación:** El frijol está en flor, quiere que cuaje y pregunta si echar algo al pie ahora. No pide agua, no nombra un animal y no habla del terreno, así que fertilización sigue teniendo más peso que riego. El texto no dice abono. No se reescribe. Un revisor puede retirarla si no ve esa decisión.
- **Corrección propuesta:** Ninguna etiqueta nueva. Conviene una nota de frontera si la fila se conserva. No reescribir el texto para acercarlo a la clase.
- **Confianza:** media
- **Segunda revisión humana:** sí
- **Cultivo:** frijol
- **Texto:** El frijol está en flor y quiero que cuaje. ¿Le echo algo al pie ahora o ya es tarde?

### 75. `piloto-v2-3458d186c1`

- **Categoría actual:** `plagas`
- **Resultado:** correcta
- **Justificación:** Un gusano corta la quinua al ras y pregunta qué buscar junto al tallo. La nota se sostiene: no pide preparar ni drenar el terreno.
- **Corrección propuesta:** Ninguna. La nota de frontera se sostiene; no se reescribe el texto.
- **Confianza:** alta
- **Segunda revisión humana:** sí
- **Cultivo:** quinua
- **Nota de frontera ya presente:** El corte lo hace un gusano. No pide preparar ni drenar el terreno.
- **Texto:** La quinua tiene un gusano que corta la plantita al ras, de noche. ¿Qué busco al amanecer junto al tallo cortado?

### 76. `piloto-v2-d4c5653567`

- **Categoría actual:** `enfermedades_cultivos`
- **Resultado:** correcta
- **Justificación:** La palta de Chanchamayo tiene una mancha oscura que llora savia y pregunta si el mal está en el tronco o en la raíz. Es identificación de un mal del tronco.
- **Corrección propuesta:** Ninguna.
- **Confianza:** alta
- **Segunda revisión humana:** no
- **Cultivo:** palta
- **Región:** Chanchamayo
- **Texto:** En Chanchamayo la palta tiene el tronco con una mancha oscura que llora savia y la copa se pone triste. ¿El mal está en el tronco o tengo que mirar la raíz?

### 77. `piloto-v2-2d59493e39`

- **Categoría actual:** `siembra_manejo_cultivo`
- **Resultado:** correcta
- **Justificación:** La arveja se enreda por el piso y pregunta si ponerle tutor. La nota se sostiene.
- **Corrección propuesta:** Ninguna. La nota de frontera se sostiene; no se reescribe el texto.
- **Confianza:** alta
- **Segunda revisión humana:** sí
- **Cultivo:** arveja
- **Nota de frontera ya presente:** La decisión es el tutor. No pide corregir el terreno.
- **Texto:** La arveja se me enreda por el piso. ¿Le pongo ramas de tutor o la dejo rastrera?

### 78. `piloto-v2-113babe101`

- **Categoría actual:** `clima_heladas`
- **Resultado:** correcta
- **Justificación:** Tras una noche bajo cero la hoja está oscura, como cocida, sin polvo ni bicho, y pregunta si el daño es del frío y qué plantas mirar. La nota se sostiene.
- **Corrección propuesta:** Ninguna. La nota de frontera se sostiene; no se reescribe el texto.
- **Confianza:** alta
- **Segunda revisión humana:** sí
- **Nota de frontera ya presente:** Pide reconocer el daño del frío ya ocurrido. No pide el nombre de una enfermedad.
- **Texto:** Esta noche el termómetro del pueblo marcó bajo cero y al amanecer la hoja está oscura, como cocida, sin polvo ni bicho encima. ¿Ese daño es del frío de anoche, y qué plantas miro primero para ver si rebrotan?

### 79. `piloto-v2-52c6b645ad`

- **Categoría actual:** `suelos`
- **Resultado:** correcta
- **Justificación:** Café de Chanchamayo en pendiente lavada, con la raíz a la vista: devolver tierra sin tapar el cuello o si el problema es la pendiente. Es erosión y el terreno.
- **Corrección propuesta:** Ninguna.
- **Confianza:** alta
- **Segunda revisión humana:** no
- **Cultivo:** café
- **Región:** Chanchamayo
- **Texto:** En Chanchamayo el café está en una pendiente lavada y se ve la raíz en la superficie. ¿Puedo devolver tierra al pie sin tapar el cuello, o el problema es la pendiente misma?

### 80. `piloto-v2-c0a9c01736`

- **Categoría actual:** `cosecha_poscosecha`
- **Resultado:** correcta
- **Justificación:** Apartar semilla el mismo día del recojo o después de secarla bajo techo. La nota se sostiene: es selección y secado de lo recién recogido. No es la semilla ya guardada de piloto-v2-6eab714edd.
- **Corrección propuesta:** Ninguna. La nota de frontera se sostiene; no se reescribe el texto.
- **Confianza:** media
- **Segunda revisión humana:** sí
- **Nota de frontera ya presente:** La decisión es la selección y el secado de lo recién recogido. No pide cómo ni cuándo volver a sembrarlo.
- **Texto:** Quiero apartar semilla para la otra campaña, distinta de lo que voy a vender. ¿La escogo el mismo día del recojo o después de que seque bajo techo?

### 81. `piloto-v2-dacf26a183`

- **Categoría actual:** `riego`
- **Resultado:** correcta
- **Justificación:** Yuca de Satipo en un lomito: en una semana sin lluvias, mojar el pie o empapar el camellón. La nota se sostiene. No es la sequía consultada como evento en piloto-v2-59a61015e2.
- **Corrección propuesta:** Ninguna. La nota de frontera se sostiene; no se reescribe el texto.
- **Confianza:** media
- **Segunda revisión humana:** sí
- **Cultivo:** yuca
- **Región:** Satipo
- **Nota de frontera ya presente:** Pregunta por cómo mojar la yuca en la época seca. No pide proteger el cultivo ante una sequía anunciada.
- **Texto:** La yuca de Satipo está en un lomito. Cuando deja de llover, el agua pasa de largo y no se queda junto a la planta. En la época seca dudo si basta con mojar el pie o si tengo que empapar el camellón entero para que la raíz de verdad reciba. ¿Qué hago en una semana sin lluvias?

### 82. `piloto-v2-a392235b7a`

- **Categoría actual:** `fertilizacion_nutricion`
- **Resultado:** correcta
- **Justificación:** Guano de isla guardado: mezclarlo con tierra o echarlo directo en el hoyo. Es forma de aplicar el abono. «Huerto» no es un cultivo de la lista.
- **Corrección propuesta:** Ninguna.
- **Confianza:** alta
- **Segunda revisión humana:** no
- **Texto:** Guardé guano de isla en un saco desde el año pasado. Antes de usarlo en el huerto, ¿lo mezclo con tierra o lo aplico directo en el hoyo?

### 83. `piloto-v2-cae4b79822`

- **Categoría actual:** `plagas`
- **Resultado:** correcta
- **Justificación:** Hueco redondo y polvillo en el grano de café, ya en el tendal, y pregunta cómo bajar esa broca sin perder lo sano. El organismo es una plaga y la etiqueta se sostiene. El lugar es de poscosecha y esa frontera no tiene nota. «Me dijeron» no aparece; el texto nombra la broca. No se atribuye ningún manejo a las fichas de fuentes.
- **Corrección propuesta:** Ninguna etiqueta nueva. Conviene una nota de frontera si la fila se conserva. No reescribir el texto para acercarlo a la clase.
- **Confianza:** media
- **Segunda revisión humana:** sí
- **Cultivo:** café
- **Texto:** En el grano del café hay un hueco redondo y, al abrirlo, sale un polvillo claro. No es un grano suelto: ya encontré varios en el mismo tendal, unos con el hueco fresco y otros vacíos. No quiero botar el lote entero si el daño está solo en una parte. ¿Cómo bajo esa broca sin perder lo que todavía está sano?

### 84. `piloto-v2-65b37803aa`

- **Categoría actual:** `enfermedades_cultivos`
- **Resultado:** correcta
- **Justificación:** Polvo gris en el frijol y hojas que se caen: si juntarlas lejos de la chacra. No hay un animal como causa.
- **Corrección propuesta:** Ninguna.
- **Confianza:** alta
- **Segunda revisión humana:** no
- **Cultivo:** frijol
- **Texto:** Las hojas del frijol se llenan de un polvo gris y se caen. ¿Junto esas hojas lejos de la chacra?

### 85. `piloto-v2-6eab714edd`

- **Categoría actual:** `siembra_manejo_cultivo`
- **Resultado:** correcta
- **Justificación:** Semilla de la campaña pasada, ya en el costal: quedarse con las más gordas o usar todo antes de volver a ponerla. Es la semilla que se va a sembrar, no el secado del recojo de hoy. Por eso no es cosecha.
- **Corrección propuesta:** Ninguna.
- **Confianza:** alta
- **Segunda revisión humana:** no
- **Texto:** Guardé semilla de la campaña pasada en un costal, sin escoger, y ahí se mezclaron granos grandes, chicos y algunos partidos. Antes de volver a ponerla en la chacra quiero saber si vale la pena abrir el costal y quedarme solo con las más gordas, o si uso todo porque separarlas me quita varios días. ¿Qué hago con ese costal?

### 86. `piloto-v2-7d7389ae50`

- **Categoría actual:** `clima_heladas`
- **Resultado:** correcta
- **Justificación:** Pregunta si el viento de Chanchamayo tumba el plátano con racimo y si apuntalarlo antes del ventarrón. Es protección ante el viento anunciado.
- **Corrección propuesta:** Ninguna.
- **Confianza:** alta
- **Segunda revisión humana:** no
- **Cultivo:** plátano
- **Región:** Chanchamayo
- **Texto:** ¿El viento fuerte de Chanchamayo tumba el plátano cuando está con racimo, y conviene apuntalarlo antes de que llegue el ventarrón?

### 87. `piloto-v2-9f43588f66`

- **Categoría actual:** `suelos`
- **Resultado:** correcta
- **Justificación:** Pregunta si un suelo arenoso pierde la reserva de humedad más rápido y si eso cambia la preparación. La nota se sostiene: no pide el calendario de riego.
- **Corrección propuesta:** Ninguna. La nota de frontera se sostiene; no se reescribe el texto.
- **Confianza:** alta
- **Segunda revisión humana:** sí
- **Nota de frontera ya presente:** La decisión es la preparación según la textura. No pide un calendario de riego.
- **Texto:** ¿Un suelo arenoso se queda sin reserva de humedad más rápido que uno negro, y eso cambia cómo lo preparo antes de usar la chacra?

### 88. `piloto-v2-d733f0b0d1`

- **Categoría actual:** `cosecha_poscosecha`
- **Resultado:** correcta
- **Justificación:** Frijol ya arrancado se mancha en la era porque llueve, y pregunta si terminar de secarlo bajo techo. La nota se sostiene.
- **Corrección propuesta:** Ninguna. La nota de frontera se sostiene; no se reescribe el texto.
- **Confianza:** alta
- **Segunda revisión humana:** sí
- **Cultivo:** frijol
- **Nota de frontera ya presente:** Las plantas ya están arrancadas. El problema es el secado en la era, no un mal en planta en pie.
- **Texto:** El frijol seco se está manchando en la era porque todavía llueve sobre las plantas ya arrancadas. ¿Lo termino de secar bajo techo?

### 89. `piloto-v2-3c573bcd02`

- **Categoría actual:** `riego`
- **Resultado:** correcta
- **Justificación:** Pregunta si parar el riego cuando las hojas amanecen mojadas por el sereno. El sereno no se consulta como helada.
- **Corrección propuesta:** Ninguna.
- **Confianza:** alta
- **Segunda revisión humana:** no
- **Texto:** ¿Paro el riego si las hojas amanecen mojadas por el sereno?

### 90. `piloto-v2-967f4ea269`

- **Categoría actual:** `fertilizacion_nutricion`
- **Resultado:** correcta
- **Justificación:** La cebada amarillea desde la punta, no hay bichos, y pregunta si le falta comida. La nota se sostiene.
- **Corrección propuesta:** Ninguna. La nota de frontera se sostiene; no se reescribe el texto.
- **Confianza:** media
- **Segunda revisión humana:** sí
- **Cultivo:** cebada
- **Nota de frontera ya presente:** No hay un animal a la vista. La consulta atribuye el amarillamiento a falta de comida.
- **Texto:** La cebada está amarillenta desde la punta. No veo bichos. ¿Será que le falta comida?

### 91. `piloto-v2-a9cbaf32da`

- **Categoría actual:** `plagas`
- **Resultado:** correcta
- **Justificación:** Orugas comen el borde de la hoja de yuca y pregunta si buscarlas de día o de noche. El organismo es un animal.
- **Corrección propuesta:** Ninguna.
- **Confianza:** alta
- **Segunda revisión humana:** no
- **Cultivo:** yuca
- **Texto:** Unas orugas están comiendo el borde de la hoja de la yuca y dejan solo las venas. ¿Las busco de día o de noche?

### 92. `piloto-v2-f68641c5eb`

- **Categoría actual:** `enfermedades_cultivos`
- **Resultado:** correcta
- **Justificación:** Pregunta si la roya que deja polvo en el dedo pasa del trigo a la cebada. Es una enfermedad. Hay dos cultivos y crop queda omitido con razón.
- **Corrección propuesta:** Ninguna.
- **Confianza:** alta
- **Segunda revisión humana:** no
- **Texto:** ¿La roya que deja polvo en el dedo pasa del trigo a la cebada si están en surcos vecinos?

### 93. `piloto-v2-c79efdcc92`

- **Categoría actual:** `siembra_manejo_cultivo`
- **Resultado:** correcta
- **Justificación:** Pregunta si sembrar cebada después de la papa en el mismo surco, esta campaña. Es sucesión de siembra. Hay dos cultivos y crop queda omitido. No es la misma pregunta que ilustrativo-015.
- **Corrección propuesta:** Ninguna.
- **Confianza:** alta
- **Segunda revisión humana:** no
- **Texto:** ¿Puedo sembrar cebada después de la papa en el mismo surco, esta misma campaña?

### 94. `piloto-v2-d5d0c2cad6`

- **Categoría actual:** `clima_heladas`
- **Resultado:** correcta
- **Justificación:** Pregunta si recoger los plantines cuando anuncian granizo. Es protección ante el granizo.
- **Corrección propuesta:** Ninguna.
- **Confianza:** alta
- **Segunda revisión humana:** no
- **Texto:** ¿Recojo los plantines si anuncian granizo?

### 95. `piloto-v2-e304a544db`

- **Categoría actual:** `suelos`
- **Resultado:** correcta
- **Justificación:** Hay pie de arado y quiere armar surcos de haba: roturar hondo o rastrear la superficie. La decisión es cómo romper ese piso, no la fecha de siembra.
- **Corrección propuesta:** Ninguna.
- **Confianza:** alta
- **Segunda revisión humana:** no
- **Cultivo:** haba
- **Texto:** Quiero armar surcos para haba y el piso tiene pie de arado. ¿Primero roturo hondo o solo rastreo la superficie?

### 96. `piloto-v2-c997997e42`

- **Categoría actual:** `cosecha_poscosecha`
- **Resultado:** correcta
- **Justificación:** Pregunta si la cebada está lista cuando el grano no marca. Es madurez de cosecha.
- **Corrección propuesta:** Ninguna.
- **Confianza:** alta
- **Segunda revisión humana:** no
- **Cultivo:** cebada
- **Texto:** ¿La cebada está lista si el grano no marca?

### 97. `piloto-v2-6041f5b673`

- **Categoría actual:** `riego`
- **Resultado:** correcta
- **Justificación:** La zanahoria engrosa, la tierra se cuartea y pregunta si dar un poco de agua o esperar. La decisión es el riego, no corregir la estructura del suelo. No es la misma pregunta que piloto-v2-0a55dcc9ff.
- **Corrección propuesta:** Ninguna.
- **Confianza:** alta
- **Segunda revisión humana:** no
- **Cultivo:** zanahoria
- **Texto:** La zanahoria está engrosando y la tierra se cuartea. ¿Le doy un poco de agua o espero a que se asiente?

### 98. `piloto-v2-b3b049a316`

- **Categoría actual:** `fertilizacion_nutricion`
- **Resultado:** correcta
- **Justificación:** La palta bota fruta chica y pregunta si dar más comida en la flor o cuando el fruto cuajó. La decisión es el momento del abono.
- **Corrección propuesta:** Ninguna.
- **Confianza:** alta
- **Segunda revisión humana:** no
- **Cultivo:** palta
- **Texto:** La palta bota fruta chica. ¿Le doy más comida cuando florece o refuerzo cuando el fruto ya cuajó?

### 99. `piloto-v2-9ba31869f2`

- **Categoría actual:** `plagas`
- **Resultado:** correcta
- **Justificación:** Pregunta cómo apartar las babosas del almácigo. Son animales. No nombra cultivo.
- **Corrección propuesta:** Ninguna.
- **Confianza:** alta
- **Segunda revisión humana:** no
- **Texto:** ¿Cómo aparto las babosas del almácigo?

### 100. `piloto-v2-a00996c1e8`

- **Categoría actual:** `enfermedades_cultivos`
- **Resultado:** correcta
- **Justificación:** Mosaico en la yuca, sin bicho, y si ese mal se queda en la rama que se corta para la próxima campaña. La nota se sostiene: no pide fecha ni distancia de siembra.
- **Corrección propuesta:** Ninguna. La nota de frontera se sostiene; no se reescribe el texto.
- **Confianza:** alta
- **Segunda revisión humana:** sí
- **Cultivo:** yuca
- **Nota de frontera ya presente:** La decisión es si el mal pasa con la rama que se guarda para sembrar. No pide fecha ni distancia de siembra.
- **Texto:** La yuca tiene las hojas con mosaico, unas partes verdes y otras amarillas, y no encuentro bicho. ¿Ese mal se queda en la rama que corto para la próxima campaña?

### 101. `piloto-v2-4f494d618e`

- **Categoría actual:** `siembra_manejo_cultivo`
- **Resultado:** correcta
- **Justificación:** Pregunta a qué distancia dejar los hijuelos de plátano al separarlos de la madre. Es densidad de siembra.
- **Corrección propuesta:** Ninguna.
- **Confianza:** alta
- **Segunda revisión humana:** no
- **Cultivo:** plátano
- **Texto:** ¿A qué distancia dejo los hijuelos de plátano cuando los separo de la madre?

### 102. `piloto-v2-b0c7ad356c`

- **Categoría actual:** `clima_heladas`
- **Resultado:** correcta
- **Justificación:** Pregunta si la flor de la arveja cuaja después del hielo. Es efecto de la helada.
- **Corrección propuesta:** Ninguna.
- **Confianza:** alta
- **Segunda revisión humana:** no
- **Cultivo:** arveja
- **Texto:** ¿La flor de la arveja cuaja tras el hielo?

### 103. `piloto-v2-758adade0a`

- **Categoría actual:** `suelos`
- **Resultado:** correcta
- **Justificación:** En Yauli la chacra es cascajera: traer tierra o trabajar solo con lo que hay. Es preparación del terreno.
- **Corrección propuesta:** Ninguna.
- **Confianza:** alta
- **Segunda revisión humana:** no
- **Región:** Yauli
- **Texto:** En Yauli la chacra es casi pura cascajera. ¿Traigo tierra de otro lado para armar eras o trabajo solo con lo que hay?

### 104. `piloto-v2-5b5b04cf02`

- **Categoría actual:** `cosecha_poscosecha`
- **Resultado:** correcta
- **Justificación:** Las mandarinas se ablandan a los tres días en el cajón: si faltó punto de corte o si el cajón está cerrado. Las dos lecturas son de cosecha y poscosecha.
- **Corrección propuesta:** Ninguna.
- **Confianza:** alta
- **Segunda revisión humana:** no
- **Cultivo:** mandarina
- **Texto:** Las mandarinas se ponen blandas a los tres días en un cajón. ¿Les faltó punto de corte o el cajón está muy cerrado?

### 105. `piloto-v2-217291845c`

- **Categoría actual:** `riego`
- **Resultado:** correcta
- **Justificación:** Sube el agua con balde al plátano y pregunta si alcanza para madre e hijo o si el hijo se lleva toda el agua de la semana. Es reparto del riego.
- **Corrección propuesta:** Ninguna.
- **Confianza:** alta
- **Segunda revisión humana:** no
- **Cultivo:** plátano
- **Texto:** Tengo el plátano en una ladera y subo el agua con balde, de a pocos, porque no hay canal hasta esa altura. El hijo está creciendo y la planta madre sigue con hoja grande. No sé si el balde alcanza para los dos o si el hijo, que es el que va a producir, debe llevarse toda el agua de esta semana.

### 106. `piloto-v2-734718f290`

- **Categoría actual:** `fertilizacion_nutricion`
- **Resultado:** correcta
- **Justificación:** Pregunta qué abono le sienta mejor a la arveja, el de corral o uno comprado. La decisión es la fuente.
- **Corrección propuesta:** Ninguna.
- **Confianza:** alta
- **Segunda revisión humana:** no
- **Cultivo:** arveja
- **Texto:** ¿Qué abono le sienta mejor a la arveja, el de corral o uno comprado?

### 107. `piloto-v2-94bdd9fa4c`

- **Categoría actual:** `plagas`
- **Resultado:** correcta
- **Justificación:** Trips en la flor de la granadilla y si quitar los brotes cargados. La nota se sostiene: quitar brotes es un medio de ese control, no una poda de manejo.
- **Corrección propuesta:** Ninguna. La nota de frontera se sostiene; no se reescribe el texto.
- **Confianza:** alta
- **Segunda revisión humana:** sí
- **Cultivo:** granadilla
- **Nota de frontera ya presente:** La decisión es qué hacer con los trips de la flor. Quitar brotes se menciona solo como medio posible de ese control.
- **Texto:** Al sacudir la granadilla caen unos trips diminutos de la flor. ¿Puedo quitar los brotes cargados de esos trips o me quedo sin cuaje?

### 108. `piloto-v2-5585a9b353`

- **Categoría actual:** `enfermedades_cultivos`
- **Resultado:** correcta
- **Justificación:** Naranjas que caen con mancha hundida y dura, sin larva, todavía referidas al árbol. La nota se sostiene: no es guarda ni insecto.
- **Corrección propuesta:** Ninguna. La nota de frontera se sostiene; no se reescribe el texto.
- **Confianza:** alta
- **Segunda revisión humana:** sí
- **Cultivo:** naranja
- **Nota de frontera ya presente:** El fruto sigue en el árbol y no hay larva. No es una consulta de guarda ni de insecto.
- **Texto:** Unos frutos de naranja caen con una mancha hundida y dura. No hay larva adentro. ¿Qué puede estar pudriendo la cáscara todavía en el árbol?

### 109. `piloto-v2-a1cc90a7ad`

- **Categoría actual:** `siembra_manejo_cultivo`
- **Resultado:** correcta
- **Justificación:** Pregunta si la estaca de yuca se entierra inclinada o parada. Es forma de siembra.
- **Corrección propuesta:** Ninguna.
- **Confianza:** alta
- **Segunda revisión humana:** no
- **Cultivo:** yuca
- **Texto:** ¿La estaca de yuca se entierra inclinada o parada?

### 110. `piloto-v2-3c89f4e5b1`

- **Categoría actual:** `clima_heladas`
- **Resultado:** correcta
- **Justificación:** Pasó la helada y pregunta si esperar para ver qué habas rebrotan. Es el daño del frío ya ocurrido.
- **Corrección propuesta:** Ninguna.
- **Confianza:** alta
- **Segunda revisión humana:** no
- **Cultivo:** haba
- **Texto:** Pasó la helada y algunas habas siguen verdes mientras otras quedaron negras. ¿Espero unos días para ver cuáles rebrotan?

### 111. `piloto-v2-80f3cb2f44`

- **Categoría actual:** `suelos`
- **Resultado:** correcta
- **Justificación:** Pregunta si limpiar la zanja que embebe la papa. La nota se sostiene: no pide cómo regar. La taxonomía manda el drenaje, cuando no se pregunta cómo regar, a suelos. El texto es muy breve.
- **Corrección propuesta:** Ninguna. La nota de frontera se sostiene; no se reescribe el texto.
- **Confianza:** media
- **Segunda revisión humana:** sí
- **Cultivo:** papa
- **Nota de frontera ya presente:** La decisión es limpiar la zanja que embebe la chacra. No pide cómo regar la papa.
- **Texto:** ¿Limpio la zanja que embebe la papa?

### 112. `piloto-v2-969a7f3f3e`

- **Categoría actual:** `cosecha_poscosecha`
- **Resultado:** correcta
- **Justificación:** Pregunta si cosechar la palta cuando la fruta ya no brilla, aunque siga verde. Es punto de corte.
- **Corrección propuesta:** Ninguna.
- **Confianza:** alta
- **Segunda revisión humana:** no
- **Cultivo:** palta
- **Texto:** ¿Conviene cosechar la palta cuando la fruta ya no brilla, aunque siga verde?

### 113. `piloto-v2-ec82906d33`

- **Categoría actual:** `riego`
- **Resultado:** correcta
- **Justificación:** Pregunta si echar el agua al mediodía o cuando baja el sol. Es horario de riego. No menciona helada, así que no es la pregunta del PMV1 sobre riego contra heladas.
- **Corrección propuesta:** Ninguna.
- **Confianza:** alta
- **Segunda revisión humana:** no
- **Texto:** ¿Echo el agua al mediodía o cuando baja el sol?

### 114. `piloto-v2-46f92a88fc`

- **Categoría actual:** `fertilizacion_nutricion`
- **Resultado:** correcta
- **Justificación:** El maíz amiláceo en Jauja hace mucha hoja y poca mazorca, y pregunta si le está dando comida de más. La decisión es la cantidad de abono.
- **Corrección propuesta:** Ninguna.
- **Confianza:** alta
- **Segunda revisión humana:** no
- **Cultivo:** maíz amiláceo
- **Región:** Jauja
- **Texto:** El maíz amiláceo en Jauja crece mucha hoja y poca mazorca. El color es verde oscuro, casi azul, y los tallos están gruesos, pero la mazorca no llena. Vengo repitiendo la misma cantidad de comida desde que salió la planta. ¿Será que le estoy dando de más y por eso solo hace hoja?

### 115. `piloto-v2-ef39bdf389`

- **Categoría actual:** `plagas`
- **Resultado:** correcta
- **Justificación:** Le dijeron que un poco de aceite en el pelo frena al gusano del maíz choclo y pregunta si hacerlo cuando el pelo sale. La decisión es el control de ese gusano. «Me dijeron» no se toma como fuente ni se confirma el método.
- **Corrección propuesta:** Ninguna.
- **Confianza:** alta
- **Segunda revisión humana:** no
- **Cultivo:** maíz choclo
- **Texto:** Me dijeron que un poco de aceite en el pelo de la mazorca frena al gusano del maíz choclo. ¿Eso se hace cuando el pelo recién sale?

### 116. `piloto-v2-0216a38b4f`

- **Categoría actual:** `enfermedades_cultivos`
- **Resultado:** correcta
- **Justificación:** Tras una semana de llovizna hay manchas aceitosas y quiere saber qué mal es, sin bicho ni mordedura. La nota se sostiene: no pide riego ni protección ante la lluvia.
- **Corrección propuesta:** Ninguna. La nota de frontera se sostiene; no se reescribe el texto.
- **Confianza:** alta
- **Segunda revisión humana:** sí
- **Nota de frontera ya presente:** Pide identificar el mal aparecido después de la lluvia. No pide una labor de riego ni protección ante el evento de lluvia.
- **Texto:** Después de una semana de llovizna salieron manchas aceitosas en las hojas de abajo, con un borde amarillo. No encuentro bicho ni mordedura. Quiero saber qué mal es antes de tocar las plantas de al lado.

### 117. `piloto-v2-b1e74e0e1f`

- **Categoría actual:** `siembra_manejo_cultivo`
- **Resultado:** correcta
- **Justificación:** Pregunta si el aporque del maíz amiláceo se hace una vez a la rodilla o se repite. El aporque entra en siembra y manejo.
- **Corrección propuesta:** Ninguna.
- **Confianza:** alta
- **Segunda revisión humana:** no
- **Cultivo:** maíz amiláceo
- **Texto:** El aporque del maíz amiláceo, ¿lo hago una vez cuando está a la rodilla o repito más adelante?

### 118. `piloto-v2-a6b2b2f6d5`

- **Categoría actual:** `clima_heladas`
- **Resultado:** correcta
- **Justificación:** En la puna de Junín el sereno se congela sobre la melga de maca y pregunta si taparla o esperar al sol. Es protección ante el hielo. Region Junín es válida: no nombra provincia.
- **Corrección propuesta:** Ninguna.
- **Confianza:** alta
- **Segunda revisión humana:** no
- **Cultivo:** maca
- **Región:** Junín
- **Texto:** La maca en la puna de Junín está en las primeras hojas y el sereno de la noche se congela sobre la melga. ¿Ese hielo de madrugada pide tapar la melga o basta con que el sol de la mañana lo levante?

### 119. `piloto-v2-70687727e3`

- **Categoría actual:** `suelos`
- **Resultado:** correcta
- **Justificación:** La piña pasa días con el cuello en barro: camas altas o una salida hacia la quebrada. Es drenaje y preparación del terreno.
- **Corrección propuesta:** Ninguna.
- **Confianza:** alta
- **Segunda revisión humana:** no
- **Cultivo:** piña
- **Texto:** La piña quedó en un plano donde la lluvia no tiene por dónde salir y el cuello pasa días en barro. ¿Levanto camas altas o abro una salida hacia la quebrada, aunque eso me lleve toda la semana?

### 120. `piloto-v2-70d99abe63`

- **Categoría actual:** `cosecha_poscosecha`
- **Resultado:** correcta
- **Justificación:** Racimo verde de plátano en Chanchamayo, a la sombra, y cuántos días puede quedar así. Es guarda en finca.
- **Corrección propuesta:** Ninguna.
- **Confianza:** alta
- **Segunda revisión humana:** no
- **Cultivo:** plátano
- **Región:** Chanchamayo
- **Texto:** En Chanchamayo corto el racimo de plátano cuando todavía está verde y lo apoyo en el piso del acopio, a la sombra, sin apilar otro racimo encima. El cuarto ventila, pero de día entra calor y de noche baja. No lo tapo con plástico. Quiero saber cuántos días puede quedar así, en esas condiciones, antes de que se pase y ya no sirva para llevar al mercado.

### 121. `piloto-v2-89c82efb59`

- **Categoría actual:** `riego`
- **Resultado:** correcta
- **Justificación:** El cacao de Chanchamayo bota flores si se deja seco y pregunta cuánta agua poner en el platón sin sumergir la raíz. Es riego, incluida la precaución de no encharcar con ese riego. No afirma una cifra.
- **Corrección propuesta:** Ninguna.
- **Confianza:** alta
- **Segunda revisión humana:** no
- **Cultivo:** cacao
- **Región:** Chanchamayo
- **Texto:** El cacao de Chanchamayo bota flores si lo dejo seco varios días. ¿Cuánta agua le pongo en el platón para que la raíz no quede sumergida?

### 122. `piloto-v2-83896490d1`

- **Categoría actual:** `fertilizacion_nutricion`
- **Resultado:** correcta
- **Justificación:** Kion de Chanchamayo con hoja clara y rizoma delgado: incorporar hoja de monte u otra fuente de comida. La nota se sostiene. Juntar tierra es el momento, no la decisión.
- **Corrección propuesta:** Ninguna. La nota de frontera se sostiene; no se reescribe el texto.
- **Confianza:** media
- **Segunda revisión humana:** sí
- **Cultivo:** kion
- **Región:** Chanchamayo
- **Nota de frontera ya presente:** La decisión es la fuente de comida. Juntar tierra al tallo se menciona solo como el momento de incorporarla.
- **Texto:** En Chanchamayo el kion de la sombra salió con hoja clara y el rizoma delgado. ¿Le incorporo hoja de monte descompuesta al juntar tierra al tallo, o busco otra fuente de comida?

### 123. `piloto-v2-c9f90d3ff3`

- **Categoría actual:** `plagas`
- **Resultado:** correcta
- **Justificación:** Minador con caminos plateados en la hoja nueva de naranja en Satipo: quitar esas hojas o dejarlas. El organismo es un animal.
- **Corrección propuesta:** Ninguna.
- **Confianza:** alta
- **Segunda revisión humana:** no
- **Cultivo:** naranja
- **Región:** Satipo
- **Texto:** En Satipo la naranja tiene minador haciendo caminos plateados en la hoja nueva. ¿Quito esas hojas o dejo que la planta las bote solas?

### 124. `piloto-v2-bf34bcde5e`

- **Categoría actual:** `enfermedades_cultivos`
- **Resultado:** correcta
- **Justificación:** Pregunta si la enfermedad que pudre el cuello de la papaya se nota antes de que la planta se caiga. El texto dice papaya, no papa. Crop papaya es correcto.
- **Corrección propuesta:** Ninguna.
- **Confianza:** alta
- **Segunda revisión humana:** no
- **Cultivo:** papaya
- **Texto:** ¿La enfermedad que pudre el cuello de la papaya se nota antes de que la planta se caiga?

### 125. `piloto-v2-66a778a6c9`

- **Categoría actual:** `siembra_manejo_cultivo`
- **Resultado:** correcta
- **Justificación:** Cacao de Satipo con mucha sombra: ralear árboles o abrir la copa con poda. Las dos opciones son manejo del cultivo.
- **Corrección propuesta:** Ninguna.
- **Confianza:** alta
- **Segunda revisión humana:** no
- **Cultivo:** cacao
- **Región:** Satipo
- **Texto:** En Satipo el cacao da mucha sombra entre plantas. ¿Raleo árboles o solo abro la copa con poda?

### 126. `piloto-v2-e57aab2fbf`

- **Categoría actual:** `clima_heladas`
- **Resultado:** correcta
- **Justificación:** Lleva un mes sin llover, la zanahoria enrolla la hoja y el aviso no aclara si la seca sigue: si guiarse por el aviso o por el día. La nota se sostiene. No es la misma decisión que piloto-v2-59a61015e2.
- **Corrección propuesta:** Ninguna. La nota de frontera se sostiene; no se reescribe el texto.
- **Confianza:** media
- **Segunda revisión humana:** sí
- **Cultivo:** zanahoria
- **Nota de frontera ya presente:** La decisión es cómo leer el aviso de seca. No pide abrir una acequia ni cambiar el terreno.
- **Texto:** Lleva un mes sin llover y la zanahoria enrolla la hoja desde el mediodía. El aviso de la radio no aclara si la seca sigue. ¿Me guío por ese aviso o solo miro el día de hoy?

### 127. `piloto-v2-d7a1c0bbcd`

- **Categoría actual:** `suelos`
- **Resultado:** correcta
- **Justificación:** Pregunta si el suelo gredoso se trabaja húmedo. Es labor sobre el terreno.
- **Corrección propuesta:** Ninguna.
- **Confianza:** alta
- **Segunda revisión humana:** no
- **Texto:** ¿El suelo gredoso se trabaja húmedo?

### 128. `piloto-v2-2a932027dd`

- **Categoría actual:** `cosecha_poscosecha`
- **Resultado:** correcta
- **Justificación:** Pregunta si trillar el trigo en la era apenas cortado o esperar un día más de sol. Es secado y trilla.
- **Corrección propuesta:** Ninguna.
- **Confianza:** alta
- **Segunda revisión humana:** no
- **Cultivo:** trigo
- **Texto:** ¿El trigo se trilla en la era apenas lo corto o espero a que el sol lo seque un día más?

### 129. `piloto-v2-d2433d5acd`

- **Categoría actual:** `riego`
- **Resultado:** correcta
- **Justificación:** El olluco cerró el follaje y pregunta si seguir mojando la melga o dejarla secar. Es calendario de riego.
- **Corrección propuesta:** Ninguna.
- **Confianza:** alta
- **Segunda revisión humana:** no
- **Cultivo:** olluco
- **Texto:** El olluco ya cerró el follaje. ¿Sigo mojando la melga o ya la dejo secar?

### 130. `piloto-v2-04805c4db9`

- **Categoría actual:** `fertilizacion_nutricion`
- **Resultado:** categoria_dudosa
- **Justificación:** «¿Sirve la ceniza de cocina en el huerto?» no dice para qué. Con el mismo peso puede ser abono, manejo de un animal o enmienda del suelo. No hay una decisión principal. Candidatas, sin elección: fertilizacion_nutricion, plagas y suelos. Estado: pendiente.
- **Corrección propuesta:** No asignar otra categoría. Retirar del conjunto etiquetado hasta revisión humana. resolved_category queda vacío.
- **Confianza:** baja
- **Segunda revisión humana:** sí
- **Texto:** ¿Sirve la ceniza de cocina en el huerto?

### 131. `piloto-v2-43487aba32`

- **Categoría actual:** `plagas`
- **Resultado:** correcta
- **Justificación:** Pregunta si juntar al amanecer los escarabajos de la arveja. El organismo es un animal.
- **Corrección propuesta:** Ninguna.
- **Confianza:** alta
- **Segunda revisión humana:** no
- **Cultivo:** arveja
- **Texto:** ¿Junto al amanecer los escarabajos de la arveja?

### 132. `piloto-v2-37eabf9a20`

- **Categoría actual:** `enfermedades_cultivos`
- **Resultado:** correcta
- **Justificación:** Pudrición acuosa del rizoma de kion todavía en la era, sin arrancar: sacarlo entero o cortar solo lo dañado. La nota se sostiene. No es el oreo ni la venta.
- **Corrección propuesta:** Ninguna. La nota de frontera se sostiene; no se reescribe el texto.
- **Confianza:** alta
- **Segunda revisión humana:** sí
- **Cultivo:** kion
- **Nota de frontera ya presente:** El rizoma sigue en la era. La decisión es la pudrición en planta, no el oreo ni la venta.
- **Texto:** El kion tiene el rizoma con una pudrición acuosa y olor fuerte, y todavía está en la era, sin arrancar. ¿Lo saco entero o corto solo la parte dañada?

### 133. `piloto-v2-21531f6c69`

- **Categoría actual:** `siembra_manejo_cultivo`
- **Resultado:** correcta
- **Justificación:** Pregunta si sacar la maleza a mano o esperar a que el cultivo cierre. Es deshierbo.
- **Corrección propuesta:** Ninguna.
- **Confianza:** alta
- **Segunda revisión humana:** no
- **Texto:** ¿Saco la maleza a mano alrededor de la planta chica o espero a que el cultivo cierre y la ahogue?

### 134. `piloto-v2-aff7084cd4`

- **Categoría actual:** `clima_heladas`
- **Resultado:** correcta
- **Justificación:** Un viento frío, que el texto distingue de la helada de la puna, y si puede quemar el brote tierno del café. Es el evento de viento.
- **Corrección propuesta:** Ninguna.
- **Confianza:** alta
- **Segunda revisión humana:** no
- **Cultivo:** café
- **Texto:** En la zona del café bajó un viento frío que no es la helada de la puna. ¿Ese viento puede quemar el brote tierno igual?

### 135. `piloto-v2-45d1e6b6b2`

- **Categoría actual:** `suelos`
- **Resultado:** correcta
- **Justificación:** Pregunta si emparejar ya la era de la zanahoria. Emparejar el terreno es preparación del suelo y la etiqueta se sostiene. El texto es breve y roza el armado de la era de siembra; esa frontera no tiene nota.
- **Corrección propuesta:** Ninguna etiqueta nueva. Conviene una nota de frontera si la fila se conserva. No reescribir el texto para acercarlo a la clase.
- **Confianza:** media
- **Segunda revisión humana:** sí
- **Cultivo:** zanahoria
- **Texto:** ¿Emparejo ya la era de la zanahoria?

### 136. `piloto-v2-f67aed0bc0`

- **Categoría actual:** `cosecha_poscosecha`
- **Resultado:** correcta
- **Justificación:** Pregunta si apartar los frutos golpeados del saco. Es selección de poscosecha. No nombra cultivo.
- **Corrección propuesta:** Ninguna.
- **Confianza:** alta
- **Segunda revisión humana:** no
- **Texto:** ¿Aparto los frutos golpeados del saco?

### 137. `piloto-v2-d6d8ea08a2`

- **Categoría actual:** `riego`
- **Resultado:** correcta
- **Justificación:** Pregunta si alcanza más la manguera gota a gota o soltar el agua por el surco. Es método de riego.
- **Corrección propuesta:** Ninguna.
- **Confianza:** alta
- **Segunda revisión humana:** no
- **Texto:** Entre llevar el agua con manguera, gota a gota, y soltarla por el surco, ¿qué alcanza para más plantas sin dejarlas con sed?

### 138. `piloto-v2-dc3422090c`

- **Categoría actual:** `fertilizacion_nutricion`
- **Resultado:** correcta
- **Justificación:** La granadilla tiene el borde de las hojas viejas seco y el cogollo verde, y pregunta si le falta alimento en la raíz. La decisión pedida es la nutrición y la etiqueta se sostiene. El borde seco también se asocia a falta de agua; esa frontera no tiene nota. No se responde si el síntoma es carencia.
- **Corrección propuesta:** Ninguna etiqueta nueva. Conviene una nota de frontera si la fila se conserva. No reescribir el texto para acercarlo a la clase.
- **Confianza:** media
- **Segunda revisión humana:** sí
- **Cultivo:** granadilla
- **Texto:** La granadilla tiene las hojas viejas con el borde seco y el cogollo todavía verde. ¿Le falta alimento en la raíz?

### 139. `piloto-v2-2642f924ad`

- **Categoría actual:** `plagas`
- **Resultado:** correcta
- **Justificación:** Escarabajos nocturnos en Tarma dejan la hoja como encaje y pregunta cómo encontrarlos. La nota se sostiene. No pide trabajar el terreno. No nombra cultivo y crop queda omitido.
- **Corrección propuesta:** Ninguna. La nota de frontera se sostiene; no se reescribe el texto.
- **Confianza:** alta
- **Segunda revisión humana:** sí
- **Región:** Tarma
- **Nota de frontera ya presente:** La decisión es cómo encontrar al escarabajo que come la hoja. No pide trabajar el terreno.
- **Texto:** En Tarma unos escarabajos nocturnos dejan la hoja de la chacra hecha encaje. ¿Reviso de noche con linterna o busco larvas donde la tierra sigue húmeda?

### 140. `piloto-v2-d71570f104`

- **Categoría actual:** `enfermedades_cultivos`
- **Resultado:** correcta
- **Justificación:** La panoja de quinua sale con polvo oscuro y no granea: si es un mal de la panoja. No hay un animal como causa.
- **Corrección propuesta:** Ninguna.
- **Confianza:** alta
- **Segunda revisión humana:** no
- **Cultivo:** quinua
- **Texto:** La panoja de la quinua sale cubierta de un polvo oscuro y no granea. ¿Es un mal de la panoja?

### 141. `piloto-v2-9870443304`

- **Categoría actual:** `siembra_manejo_cultivo`
- **Resultado:** correcta
- **Justificación:** En Huancayo pregunta si juntar el surco de zanahoria por el tiempo frío o solo cuidar la fecha de mayo. La nota se sostiene: el frío es condición de esa fecha, no una helada a la que haya que proteger hoy.
- **Corrección propuesta:** Ninguna. La nota de frontera se sostiene; no se reescribe el texto.
- **Confianza:** alta
- **Segunda revisión humana:** sí
- **Cultivo:** zanahoria
- **Región:** Huancayo
- **Nota de frontera ya presente:** La decisión es la fecha y la distancia de siembra. El frío se menciona como condición de esa fecha, no como protección ante una helada.
- **Texto:** En Huancayo quiero la zanahoria para agosto. Si la pongo en mayo, ¿el surco va más junto porque el tiempo frío la atrasa, o mantengo el mismo trazo de siempre y solo cuido la fecha?

### 142. `piloto-v2-63c243ee65`

- **Categoría actual:** `clima_heladas`
- **Resultado:** correcta
- **Justificación:** El granizo partió hojas de papaya y pregunta si esas heridas se atienden como daño del clima de ayer. La nota se sostiene. El cultivo es papaya, no papa.
- **Corrección propuesta:** Ninguna. La nota de frontera se sostiene; no se reescribe el texto.
- **Confianza:** alta
- **Segunda revisión humana:** sí
- **Cultivo:** papaya
- **Nota de frontera ya presente:** La decisión es el daño del granizo ya ocurrido. No pide identificar una enfermedad.
- **Texto:** El granizo golpeó la papaya y partió varias hojas grandes. ¿Esas heridas se atienden como daño del clima de ayer?

### 143. `piloto-v2-b77cefb95c`

- **Categoría actual:** `suelos`
- **Resultado:** correcta
- **Justificación:** En Concepción pregunta si la muestra para saber si la tierra está ácida sale de un hoyo o de varios. La nota se sostiene: no pide la dosis de abono.
- **Corrección propuesta:** Ninguna. La nota de frontera se sostiene; no se reescribe el texto.
- **Confianza:** alta
- **Segunda revisión humana:** sí
- **Región:** Concepción
- **Nota de frontera ya presente:** La decisión es cómo muestrear el terreno. No se pregunta la dosis de abono.
- **Texto:** En Concepción quiero saber si la tierra está ácida antes de decidir cualquier cultivo. ¿La muestra se saca de un solo hoyo o de varios puntos de la chacra?

### 144. `piloto-v2-9018b8aefd`

- **Categoría actual:** `cosecha_poscosecha`
- **Resultado:** correcta
- **Justificación:** Pregunta si la granadilla arrugada ya pasó de madura o si así se recoge. Es punto de corte. Se distingue de piloto-v2-d9aa2b7030, que añade manchas aceitosas en la planta.
- **Corrección propuesta:** Ninguna.
- **Confianza:** alta
- **Segunda revisión humana:** no
- **Cultivo:** granadilla
- **Texto:** La granadilla arrugada, ¿ya pasó de madura o así se recoge del parral?

### 145. `piloto-v2-bbafa50942`

- **Categoría actual:** `riego`
- **Resultado:** correcta
- **Justificación:** Maíz choclo en Huancayo, semana sin llovizna: una pasada hoy con el reservorio o esperar el turno del domingo. Es calendario de riego, no la sequía como evento climático.
- **Corrección propuesta:** Ninguna.
- **Confianza:** alta
- **Segunda revisión humana:** no
- **Cultivo:** maíz choclo
- **Región:** Huancayo
- **Texto:** En Huancayo el maíz choclo está a la altura de la rodilla y esta semana no cayó ni una llovizna sobre la chacra. El turno del canal recién abre el domingo. ¿Le doy hoy una pasada ligera con lo que queda en el reservorio o espero ese turno aunque la tierra ya esté polvorienta?

### 146. `piloto-v2-6bb324c09c`

- **Categoría actual:** `fertilizacion_nutricion`
- **Resultado:** correcta
- **Justificación:** El trigo macolló poco y pregunta si dar una segunda comida al encañar. Es momento del abono.
- **Corrección propuesta:** Ninguna.
- **Confianza:** alta
- **Segunda revisión humana:** no
- **Cultivo:** trigo
- **Texto:** El trigo macolló poco. ¿Le doy una segunda comida cuando empiece a encañar?

### 147. `piloto-v2-5d8c063a1b`

- **Categoría actual:** `plagas`
- **Resultado:** correcta
- **Justificación:** Pregunta si empezar por la cochinilla de la piña. La cochinilla es un animal y la categoría se sostiene. La pregunta no dice empezar qué; la claridad es baja y no alcanza para retirarla.
- **Corrección propuesta:** Ninguna etiqueta nueva. Conviene una nota de frontera si la fila se conserva. No reescribir el texto para acercarlo a la clase.
- **Confianza:** media
- **Segunda revisión humana:** sí
- **Cultivo:** piña
- **Texto:** ¿Empiezo por la cochinilla de la piña?

### 148. `piloto-v2-86f762efd9`

- **Categoría actual:** `enfermedades_cultivos`
- **Resultado:** correcta
- **Justificación:** Hilos blancos en la base del plátano, la mata se troncha y no hay picadura: cómo evitar que pase a los hijuelos. Niega la picadura y la etiqueta de enfermedad se sostiene. Un hilo blanco también puede leerse como otro organismo; esa frontera no tiene nota. No se le pone nombre.
- **Corrección propuesta:** Ninguna etiqueta nueva. Conviene una nota de frontera si la fila se conserva. No reescribir el texto para acercarlo a la clase.
- **Confianza:** media
- **Segunda revisión humana:** sí
- **Cultivo:** plátano
- **Texto:** Veo hilos blancos en la base del plátano y la mata se troncha. No hay picadura de insecto. ¿Cómo evito que pase a los hijuelos?

### 149. `piloto-v2-21b6d2701c`

- **Categoría actual:** `siembra_manejo_cultivo`
- **Resultado:** correcta
- **Justificación:** Pregunta si ralear el maíz amarillo duro con tres hojas o cuando ya se ve la planta débil. Es raleo.
- **Corrección propuesta:** Ninguna.
- **Confianza:** alta
- **Segunda revisión humana:** no
- **Cultivo:** maíz amarillo duro
- **Texto:** Para el maíz amarillo duro, ¿conviene ralear cuando la planta tiene tres hojas o cuando ya se ve cuál quedó débil?

### 150. `piloto-v2-af95af001d`

- **Categoría actual:** `clima_heladas`
- **Resultado:** correcta
- **Justificación:** En Chupaca el aviso habla de bajo cero el viernes y pregunta si proteger solo lo que está en flor o también lo recién emergido. Es protección ante la helada anunciada.
- **Corrección propuesta:** Ninguna.
- **Confianza:** alta
- **Segunda revisión humana:** no
- **Región:** Chupaca
- **Texto:** En Chupaca el aviso de la radio habla de temperaturas bajo cero para el viernes. ¿Protejo solo lo que está en flor o también lo que recién emergió?

### 151. `piloto-v2-0a55dcc9ff`

- **Categoría actual:** `suelos`
- **Resultado:** correcta
- **Justificación:** La tierra de la yuca se agrieta en la época seca: buscar un sitio más franco o cerrar la grieta trabajando el piso. Es el terreno, no un turno de riego.
- **Corrección propuesta:** Ninguna.
- **Confianza:** alta
- **Segunda revisión humana:** no
- **Cultivo:** yuca
- **Texto:** La tierra de la yuca se abre en grietas profundas en la época seca. ¿Busco un sitio más franco o esa grieta se puede cerrar trabajando el piso?

### 152. `piloto-v2-0d6dbaf3e4`

- **Categoría actual:** `cosecha_poscosecha`
- **Resultado:** correcta
- **Justificación:** Pregunta si arrancar toda la yuca el mismo día o ir sacando según se venda. El ritmo es el del arranque. No es la pregunta comercial suelta de piloto-v2-41bdf8b563.
- **Corrección propuesta:** Ninguna.
- **Confianza:** alta
- **Segunda revisión humana:** no
- **Cultivo:** yuca
- **Texto:** ¿La yuca se arranca toda la mata el mismo día o puedo ir sacando según vaya vendiendo?

### 153. `piloto-v2-bb0982ea87`

- **Categoría actual:** `riego`
- **Resultado:** correcta
- **Justificación:** La arveja está en vaina y pregunta si la tierra debe quedar húmeda o casi seca entre riegos. Es calendario de riego.
- **Corrección propuesta:** Ninguna.
- **Confianza:** alta
- **Segunda revisión humana:** no
- **Cultivo:** arveja
- **Texto:** La arveja está en vaina. ¿La tierra debe quedar húmeda o casi seca entre una vez y otra?

### 154. `piloto-v2-8079fbca13`

- **Categoría actual:** `fertilizacion_nutricion`
- **Resultado:** correcta
- **Justificación:** Pregunta si la comida de la piña va al hijo. Es dónde aplicar el abono.
- **Corrección propuesta:** Ninguna.
- **Confianza:** alta
- **Segunda revisión humana:** no
- **Cultivo:** piña
- **Texto:** ¿La comida de la piña va al hijo?

### 155. `piloto-v2-0fe9653a2a`

- **Categoría actual:** `plagas`
- **Resultado:** correcta
- **Justificación:** Larvas chicas dejan ventanitas en la hoja del kion y pregunta cómo controlarlas antes de que pasen al rizoma. El organismo es un animal.
- **Corrección propuesta:** Ninguna.
- **Confianza:** alta
- **Segunda revisión humana:** no
- **Cultivo:** kion
- **Texto:** Veo larvas chicas y la hoja del kion queda con ventanitas transparentes, como raspada. ¿Cómo las controlo antes de que pasen al rizoma?

### 156. `piloto-v2-a5e7330c55`

- **Categoría actual:** `enfermedades_cultivos`
- **Resultado:** correcta
- **Justificación:** Pregunta si la raíz enferma de la zanahoria contagia. El texto ya la presenta como enferma y no describe un animal.
- **Corrección propuesta:** Ninguna.
- **Confianza:** alta
- **Segunda revisión humana:** no
- **Cultivo:** zanahoria
- **Texto:** ¿La raíz enferma de la zanahoria contagia?

### 157. `piloto-v2-3ded03e2d7`

- **Categoría actual:** `siembra_manejo_cultivo`
- **Resultado:** correcta
- **Justificación:** Pregunta si la maca se pone en melgas angostas o en un solo tablón. Es trazo de siembra.
- **Corrección propuesta:** Ninguna.
- **Confianza:** alta
- **Segunda revisión humana:** no
- **Cultivo:** maca
- **Texto:** ¿La maca se pone en melgas angostas o en un solo tablón?

### 158. `piloto-v2-31849ca42b`

- **Categoría actual:** `clima_heladas`
- **Resultado:** correcta
- **Justificación:** Pregunta si una lluvia torrencial obliga a revisar el cultivo al día siguiente por el golpe del agua. La nota se sostiene: no pide nombrar un mal ni abrir un drenaje.
- **Corrección propuesta:** Ninguna. La nota de frontera se sostiene; no se reescribe el texto.
- **Confianza:** media
- **Segunda revisión humana:** sí
- **Nota de frontera ya presente:** Pide revisar el golpe de esa lluvia. No pide identificar un mal de las hojas ni abrir un drenaje definitivo.
- **Texto:** ¿La lluvia torrencial de una noche, la que deja el camino como río, obliga a revisar el cultivo al día siguiente por el golpe del agua?

### 159. `piloto-v2-47fa623464`

- **Categoría actual:** `suelos`
- **Resultado:** correcta
- **Justificación:** El agua se comió el bordo de la cebada y dejó una cárcava: si taparla esta semana. Es reparar el terreno.
- **Corrección propuesta:** Ninguna.
- **Confianza:** alta
- **Segunda revisión humana:** no
- **Cultivo:** cebada
- **Texto:** El camino del agua se comió el bordo del surco de la cebada y dejó una cárcava chica. ¿Esa cárcava se tapa esta semana?

### 160. `piloto-v2-2ca48be747`

- **Categoría actual:** `cosecha_poscosecha`
- **Resultado:** correcta
- **Justificación:** En Huancayo quiere el maíz choclo tierno y pregunta qué color del pelo marca el corte. Es madurez de cosecha, no grano seco.
- **Corrección propuesta:** Ninguna.
- **Confianza:** alta
- **Segunda revisión humana:** no
- **Cultivo:** maíz choclo
- **Región:** Huancayo
- **Texto:** En Huancayo el maíz choclo lo quiero tierno para vender en el mercado del sábado, no para dejarlo secar. Si lo dejo un día de más en la planta, el grano se pone duro y ya no me lo reciben como choclo. El pelo de la mazorca cambia de color, pero no sé cuál de esos colores marca el punto. ¿Hay una señal segura en ese pelo para cortarlo a tiempo?

### 161. `piloto-v2-3cff8cbcf3`

- **Categoría actual:** `riego`
- **Resultado:** correcta
- **Justificación:** En Concepción el reservorio no alcanza y pregunta a cuáles plantas dar el agua de hoy. La nota se sostiene: no pide qué sembrar ni qué fecha elegir.
- **Corrección propuesta:** Ninguna. La nota de frontera se sostiene; no se reescribe el texto.
- **Confianza:** alta
- **Segunda revisión humana:** sí
- **Región:** Concepción
- **Nota de frontera ya presente:** La decisión es el reparto del agua del reservorio. No pide qué cultivo sembrar ni qué fecha elegir.
- **Texto:** En Concepción el reservorio familiar alcanza para pocas horas. Hay plantas recién salidas y otras ya cargadas, todas con sed el mismo día, y el agua no va a alcanzar para el huerto entero. ¿A cuáles les doy el agua de hoy y cuáles pueden esperar al siguiente turno?

### 162. `piloto-v2-ee8406d7b7`

- **Categoría actual:** `fertilizacion_nutricion`
- **Resultado:** correcta
- **Justificación:** En Huancayo pregunta si madurar el estiércol de cuy un mes o enterrarlo esta semana. Es manejo del abono. No nombra cultivo.
- **Corrección propuesta:** Ninguna.
- **Confianza:** alta
- **Segunda revisión humana:** no
- **Región:** Huancayo
- **Texto:** En Huancayo quiero aprovechar el estiércol del cuy antes de que se seque al sol. ¿Lo dejo madurar un mes bajo sombra o lo puedo enterrar esta semana en los surcos que ya están con plantas?

### 163. `piloto-v2-a5ef8415c6`

- **Categoría actual:** `plagas`
- **Resultado:** correcta
- **Justificación:** Un chinche pica la mazorca del maíz amarillo duro en grano lechoso y pregunta cómo evitar que siga. El organismo es un animal.
- **Corrección propuesta:** Ninguna.
- **Confianza:** alta
- **Segunda revisión humana:** no
- **Cultivo:** maíz amarillo duro
- **Texto:** Un chinche apesta la mazorca del maíz amarillo duro mientras el grano está lechoso. ¿Cómo evito que siga picando?

### 164. `piloto-v2-1a86fd7779`

- **Categoría actual:** `enfermedades_cultivos`
- **Resultado:** correcta
- **Justificación:** Pregunta si dejar en el campo las arvejas secas con manchas violáceas en el tallo. Es manejo del síntoma, sin un animal como causa.
- **Corrección propuesta:** Ninguna.
- **Confianza:** alta
- **Segunda revisión humana:** no
- **Cultivo:** arveja
- **Texto:** ¿Puedo dejar en el campo las plantas de arveja que se secaron con manchas violáceas en el tallo?

### 165. `piloto-v2-fd27b8a188`

- **Categoría actual:** `siembra_manejo_cultivo`
- **Resultado:** correcta
- **Justificación:** Pregunta si al renovar el café viejo se replantan solo los huecos o hileras completas. Es forma de replante.
- **Corrección propuesta:** Ninguna.
- **Confianza:** alta
- **Segunda revisión humana:** no
- **Cultivo:** café
- **Texto:** Quiero renovar las plantas viejas de café. ¿Replanto solo los huecos vacíos o cambio hileras completas?

### 166. `piloto-v2-701c189be5`

- **Categoría actual:** `clima_heladas`
- **Resultado:** correcta
- **Justificación:** En Tarma el olluco cierra hoja y vienen madrugadas con escarcha: si el daño se acumula. Es el evento de frío.
- **Corrección propuesta:** Ninguna.
- **Confianza:** alta
- **Segunda revisión humana:** no
- **Cultivo:** olluco
- **Región:** Tarma
- **Texto:** En Tarma el olluco está cerrando hoja y vienen varias madrugadas seguidas con escarcha. ¿La escarcha repetida se acumula como daño o una sola noche fría no cambia nada?

### 167. `piloto-v2-c47ba89df0`

- **Categoría actual:** `suelos`
- **Resultado:** correcta
- **Justificación:** Un pedazo que fue corral está suelto y otro apelmazado: si prepararlos distinto. Es preparación del terreno. No nombra cultivo.
- **Corrección propuesta:** Ninguna.
- **Confianza:** alta
- **Segunda revisión humana:** no
- **Texto:** Tengo un pedazo que fue corral y está suelto, y al lado uno que nunca se movió y está apelmazado. ¿Los preparo de forma distinta antes de usarlos, o los dos aguantan la misma labor de roturado?

### 168. `piloto-v2-41bdf8b563`

- **Categoría actual:** `cosecha_poscosecha`
- **Resultado:** categoria_dudosa
- **Justificación:** «¿El olluco se vende el mismo día?» no pide madurez, corte, secado, selección, oreo ni guarda. La única categoría que podría caber es cosecha_poscosecha, y solo con una lectura de vida útil que el texto no hace. No hay una segunda categoría de las ocho en empate. Estado: pendiente.
- **Corrección propuesta:** No asignar otra categoría. Retirar del conjunto etiquetado hasta revisión humana. resolved_category queda vacío. Si el revisor lee solo una decisión de venta, rechazarla: la venta no es una de las ocho categorías. Si documenta que la decisión es la guarda breve en finca, podría volver como cosecha_poscosecha.
- **Confianza:** baja
- **Segunda revisión humana:** sí
- **Cultivo:** olluco
- **Texto:** ¿El olluco se vende el mismo día?

### 169. `piloto-v2-17eb4d974a`

- **Categoría actual:** `riego`
- **Resultado:** correcta
- **Justificación:** Papaya de Satipo: si el agua está demasiado cerca del cuello o no llega a la raíz de afuera. Es cómo regar. El cultivo es papaya, no papa.
- **Corrección propuesta:** Ninguna.
- **Confianza:** alta
- **Segunda revisión humana:** no
- **Cultivo:** papaya
- **Región:** Satipo
- **Texto:** La papaya de Satipo tiene el hoyo siempre fresco, casi frío al tacto, y aun así las hojas de abajo se arrugan cuando el sol pega de lleno. Dudo si estoy mojando demasiado cerca del cuello o si el agua no llega a la raíz que está más afuera. ¿Cómo lo distingo antes de echarle otro balde?

### 170. `piloto-v2-c77fa8da96`

- **Categoría actual:** `fertilizacion_nutricion`
- **Resultado:** correcta
- **Justificación:** La papaya sale sin dulce y pregunta si cambiar la comida cuando aparece la flor. La decisión pedida es la comida y la etiqueta se sostiene. «Sin dulce» también se asocia al punto de corte; esa frontera no tiene nota y no pesa lo mismo que la pregunta por la comida.
- **Corrección propuesta:** Ninguna etiqueta nueva. Conviene una nota de frontera si la fila se conserva. No reescribir el texto para acercarlo a la clase.
- **Confianza:** media
- **Segunda revisión humana:** sí
- **Cultivo:** papaya
- **Texto:** La papaya se ve vigorosa arriba y la fruta sale sin dulce. ¿Cambio la comida cuando aparece la flor?

### 171. `piloto-v2-70c8a1aad0`

- **Categoría actual:** `plagas`
- **Resultado:** correcta
- **Justificación:** Pregunta si los pulgones del almácigo se van al soltar mariquitas del maizal. Es control de un animal. «Maizal» no es uno de los tres maíces de la lista; omitir crop es correcto.
- **Corrección propuesta:** Ninguna.
- **Confianza:** alta
- **Segunda revisión humana:** no
- **Texto:** ¿Los pulgones del almácigo se van si suelto mariquitas que junto en el maizal?

### 172. `piloto-v2-fd825deb98`

- **Categoría actual:** `enfermedades_cultivos`
- **Resultado:** correcta
- **Justificación:** Maíz choclo en Huancayo amaneció seco, con la base oscura y olor a podrido, sin gusano: si arrancar esas matas. Es un mal del tallo, no un insecto.
- **Corrección propuesta:** Ninguna.
- **Confianza:** alta
- **Segunda revisión humana:** no
- **Cultivo:** maíz choclo
- **Región:** Huancayo
- **Texto:** En Huancayo varias matas de maíz choclo amanecieron secas, con la base del tallo oscura y olor a podrido. No encontré gusano. ¿Arranco esas matas antes de que se moje otra vez el surco?

### 173. `piloto-v2-c7e8e93ece`

- **Categoría actual:** `siembra_manejo_cultivo`
- **Resultado:** correcta
- **Justificación:** En Chupaca pregunta si esperar la primera lluvia de verdad para poner la semilla o si hay un día del que ya no pasar. La nota se sostiene: es la ventana de siembra, no un evento de lluvia ya anunciado.
- **Corrección propuesta:** Ninguna. La nota de frontera se sostiene; no se reescribe el texto.
- **Confianza:** alta
- **Segunda revisión humana:** sí
- **Región:** Chupaca
- **Nota de frontera ya presente:** Pregunta por la ventana para poner la semilla. No pide qué hacer ante un evento de lluvia ya anunciado.
- **Texto:** En Chupaca la campaña de lluvias se atrasa algunos años y otras veces cae antes de que yo tenga la semilla lista. No quiero ponerla en seco, tampoco quiero pasarme de la fecha y perder el ciclo. ¿La dejo preparada y espero la primera lluvia de verdad, o hay un día del calendario del que ya no debo pasar aunque el cielo siga despejado?

### 174. `piloto-v2-c39737c2a1`

- **Categoría actual:** `clima_heladas`
- **Resultado:** correcta
- **Justificación:** Pregunta si hay helada negra aunque no se vea hielo. Es una pregunta de clima. La etiqueta no exige definir el fenómeno ni citar un boletín.
- **Corrección propuesta:** Ninguna.
- **Confianza:** alta
- **Segunda revisión humana:** no
- **Texto:** ¿Hay helada negra aunque no se vea hielo?

### 175. `piloto-v2-226b8b322c`

- **Categoría actual:** `suelos`
- **Resultado:** correcta
- **Justificación:** Pregunta si rehacer las terrazas de Tarma cuando el muro se venció. La nota se sostiene: no pide una fecha de siembra.
- **Corrección propuesta:** Ninguna. La nota de frontera se sostiene; no se reescribe el texto.
- **Confianza:** alta
- **Segunda revisión humana:** sí
- **Región:** Tarma
- **Nota de frontera ya presente:** La decisión es reparar la terraza. No pide una fecha de siembra.
- **Texto:** ¿Las terrazas que ya existen en la ladera de Tarma hay que rehacerlas si el muro se venció, o puedo seguir usándolas así?

### 176. `piloto-v2-043cae6a91`

- **Categoría actual:** `cosecha_poscosecha`
- **Resultado:** correcta
- **Justificación:** Después de cosechar arveja verde, pregunta si la vaina va en costal cerrado o necesita aire. Es guarda breve.
- **Corrección propuesta:** Ninguna.
- **Confianza:** alta
- **Segunda revisión humana:** no
- **Cultivo:** arveja
- **Texto:** Después de la cosecha de arveja verde, ¿la vaina se guarda en costal cerrado o necesita aire?

### 177. `piloto-v2-f856963a81`

- **Categoría actual:** `riego`
- **Resultado:** correcta
- **Justificación:** Pregunta si el trigo en espiga se malogra al mojarlo encima. Es método de riego.
- **Corrección propuesta:** Ninguna.
- **Confianza:** alta
- **Segunda revisión humana:** no
- **Cultivo:** trigo
- **Texto:** ¿El trigo en espiga se malogra si lo mojo encima?

### 178. `piloto-v2-f41202baee`

- **Categoría actual:** `fertilizacion_nutricion`
- **Resultado:** correcta
- **Justificación:** Pregunta si el fertilizante granulado del maíz choclo va en banda o encima del surco. Es forma de aplicar el abono.
- **Corrección propuesta:** Ninguna.
- **Confianza:** alta
- **Segunda revisión humana:** no
- **Cultivo:** maíz choclo
- **Texto:** ¿El fertilizante granulado del maíz choclo se pone en banda al costado o encima del surco?

### 179. `piloto-v2-b1df0fe24f`

- **Categoría actual:** `plagas`
- **Resultado:** correcta
- **Justificación:** Costra en el fruto de mandarina y ácaros vistos con lupa: si el manejo va en el fruto grande o en el brote siguiente. El organismo es un animal.
- **Corrección propuesta:** Ninguna.
- **Confianza:** alta
- **Segunda revisión humana:** no
- **Cultivo:** mandarina
- **Texto:** La mandarina tiene el fruto con una costra levantada y, con lupa, se ven ácaros moviéndose. ¿El manejo va en el fruto que ya está grande o en el brote de la campaña que viene?

### 180. `piloto-v2-99b5624803`

- **Categoría actual:** `enfermedades_cultivos`
- **Resultado:** categoria_dudosa
- **Justificación:** «¿Lavo el polvo blanco del brote?» no dice cultivo ni si el polvo es de una enfermedad o resto de un animal. Enfermedades y plagas explican la frase con peso parecido. No pide el nombre del polvo, a diferencia de piloto-v2-464c8602df. Candidatas, sin elección: enfermedades_cultivos y plagas. Estado: pendiente.
- **Corrección propuesta:** No asignar otra categoría. Retirar del conjunto etiquetado hasta revisión humana. resolved_category queda vacío. No unirla a piloto-v2-464c8602df: aquella pide identificar el polvo del envés de la papa.
- **Confianza:** media
- **Segunda revisión humana:** sí
- **Texto:** ¿Lavo el polvo blanco del brote?

### 181. `piloto-v2-a9b2494770`

- **Categoría actual:** `siembra_manejo_cultivo`
- **Resultado:** correcta
- **Justificación:** Pregunta si la poda de la palta va en la época seca o con flor. Es momento de poda. No es paráfrasis de la poda del café.
- **Corrección propuesta:** Ninguna.
- **Confianza:** alta
- **Segunda revisión humana:** no
- **Cultivo:** palta
- **Texto:** ¿La poda de la palta se hace en la época seca o cuando la planta está cargada de flor?

### 182. `piloto-v2-b1897ea4fe`

- **Categoría actual:** `clima_heladas`
- **Resultado:** correcta
- **Justificación:** El viento se llevó flor de la palta en Chanchamayo y pregunta si la caída es del ventarrón o de la planta. La decisión es el efecto de ese viento.
- **Corrección propuesta:** Ninguna.
- **Confianza:** alta
- **Segunda revisión humana:** no
- **Cultivo:** palta
- **Región:** Chanchamayo
- **Texto:** El viento de ayer se llevó mucha flor de la palta en Chanchamayo. ¿Esa caída es por el ventarrón o la planta ya estaba por botar flor?

### 183. `piloto-v2-038ffc061a`

- **Categoría actual:** `suelos`
- **Resultado:** correcta
- **Justificación:** Pregunta si el análisis de suelo alcanza con los primeros veinte centímetros. La nota se sostiene: no pide interpretar una dosis.
- **Corrección propuesta:** Ninguna. La nota de frontera se sostiene; no se reescribe el texto.
- **Confianza:** alta
- **Segunda revisión humana:** sí
- **Nota de frontera ya presente:** Pregunta por la profundidad de la muestra de tierra. No pide interpretar una dosis.
- **Texto:** ¿Un análisis de suelo alcanza con la capa de los primeros veinte centímetros?

### 184. `piloto-v2-ea5c1fc816`

- **Categoría actual:** `cosecha_poscosecha`
- **Resultado:** correcta
- **Justificación:** La papaya suena sordo al golpearla y pregunta si con eso basta para cortarla. Es madurez de cosecha. El cultivo es papaya.
- **Corrección propuesta:** Ninguna.
- **Confianza:** alta
- **Segunda revisión humana:** no
- **Cultivo:** papaya
- **Texto:** La papaya da un sonido sordo cuando le doy un golpecito con los nudillos. ¿Con eso basta para cortarla?

### 185. `piloto-v2-f454b7c529`

- **Categoría actual:** `riego`
- **Resultado:** correcta
- **Justificación:** En Yauli el viento seca la chacra y pregunta si acortar los días entre riegos o alargar la acequia. La nota se sostiene. No es la protección ante el viento de piloto-v2-1d4ef1a7bd ni el agua usada solo contra el frío de piloto-v2-4d8651680b.
- **Corrección propuesta:** Ninguna. La nota de frontera se sostiene; no se reescribe el texto.
- **Confianza:** alta
- **Segunda revisión humana:** sí
- **Región:** Yauli
- **Nota de frontera ya presente:** El viento se menciona como causa de que la chacra se seque. La decisión pedida es el intervalo y la duración del agua, no una protección ante un evento de viento.
- **Texto:** En Yauli el viento seca la chacra en un día. ¿Acorto los días entre cada riego o alargo la hora que dejo abierta la acequia?

### 186. `piloto-v2-e7cca92a8f`

- **Categoría actual:** `fertilizacion_nutricion`
- **Resultado:** correcta
- **Justificación:** Hojas nuevas del olluco pequeñas, sin mordeduras, y si reforzar la comida a mitad del ciclo. La nota se sostiene.
- **Corrección propuesta:** Ninguna. La nota de frontera se sostiene; no se reescribe el texto.
- **Confianza:** media
- **Segunda revisión humana:** sí
- **Cultivo:** olluco
- **Nota de frontera ya presente:** No hay daño de un animal. La decisión es si se refuerza la comida a mitad del ciclo.
- **Texto:** Las hojas nuevas del olluco salen pequeñas. No hay mordeduras. ¿Refuerzo la comida a mitad del ciclo?

### 187. `piloto-v2-fc0655fb7f`

- **Categoría actual:** `plagas`
- **Resultado:** correcta
- **Justificación:** La raíz de papaya tiene nudos y le dijeron que son nematodos: sacar las plantas o seguir. La taxonomía incluye los nematodos en plagas. «Me dijeron» no se toma como fuente ni se confirma el diagnóstico.
- **Corrección propuesta:** Ninguna.
- **Confianza:** alta
- **Segunda revisión humana:** no
- **Cultivo:** papaya
- **Texto:** La raíz de la papaya está con nudos y me dijeron que son nematodos. ¿Saco esas plantas o puedo seguir con ellas?

### 188. `piloto-v2-d9aa2b7030`

- **Categoría actual:** `enfermedades_cultivos`
- **Resultado:** correcta
- **Justificación:** Manchas aceitosas en el fruto de granadilla, que se arruga en la planta: retirar esos frutos o esperar. La nota se sostiene. No es el punto de recolección de piloto-v2-9018b8aefd.
- **Corrección propuesta:** Ninguna. La nota de frontera se sostiene; no se reescribe el texto.
- **Confianza:** alta
- **Segunda revisión humana:** sí
- **Cultivo:** granadilla
- **Nota de frontera ya presente:** El fruto sigue en la planta. La decisión es la mancha, no el punto de recolección.
- **Texto:** La granadilla tiene manchas aceitosas en el fruto y se arruga en la planta. ¿Retiro los frutos así o espero a ver si maduran?

### 189. `piloto-v2-f9c10157b9`

- **Categoría actual:** `siembra_manejo_cultivo`
- **Resultado:** correcta
- **Justificación:** Pregunta si sembrar el olluco entero o partido. Es forma de la semilla.
- **Corrección propuesta:** Ninguna.
- **Confianza:** alta
- **Segunda revisión humana:** no
- **Cultivo:** olluco
- **Texto:** ¿Siembro el olluco entero o partido?

### 190. `piloto-v2-550177d516`

- **Categoría actual:** `clima_heladas`
- **Resultado:** correcta
- **Justificación:** Anuncian noche clara y sin viento después de un día caliente, y pregunta si prepararse por el frío sobre la papa chiquita. Es protección ante el riesgo anunciado.
- **Corrección propuesta:** Ninguna.
- **Confianza:** alta
- **Segunda revisión humana:** no
- **Cultivo:** papa
- **Texto:** Anuncian una noche clara y sin viento después de un día caliente. En la sierra eso a veces termina en frío fuerte sobre la papa chiquita. ¿Me preparo desde hoy?

### 191. `piloto-v2-45b44ad4dc`

- **Categoría actual:** `suelos`
- **Resultado:** correcta
- **Justificación:** El hoyo de la palta junta agua contra el tronco cuando llueve y pregunta si abrirlo para que el agua salga. La nota se sostiene: es salida del agua del terreno, no un mal del tronco ni un turno de riego.
- **Corrección propuesta:** Ninguna. La nota de frontera se sostiene; no se reescribe el texto.
- **Confianza:** alta
- **Segunda revisión humana:** sí
- **Cultivo:** palta
- **Nota de frontera ya presente:** La decisión es abrir el hoyo para que salga el agua. No pide diagnosticar un mal del tronco ni un turno de riego.
- **Texto:** El hoyo de la palta junta agua contra el tronco cada vez que llueve. ¿Lo abro a un lado para que el agua salga?

### 192. `piloto-v2-3a3ecfb9c3`

- **Categoría actual:** `cosecha_poscosecha`
- **Resultado:** correcta
- **Justificación:** La piña cambió el color de la base y el olor, y pregunta si cortarla hoy o esperar porque el centro sigue verde. Es punto de corte. Se distingue de la pudrición en planta de piloto-v2-09973b49b9.
- **Corrección propuesta:** Ninguna.
- **Confianza:** alta
- **Segunda revisión humana:** no
- **Cultivo:** piña
- **Texto:** La piña cambió el color de la base y el olor es más fuerte que la semana pasada. ¿La corto hoy mismo o el centro todavía está verde y conviene esperar un par de días?

## 11. Cierre

Conteo de resultados en el registro: {'correcta': 189, 'categoria_dudosa': 3}. Filas con segunda revisión: 60.
El piloto permanece `pendiente_de_revision_humana`. `training_dataset` sigue en `no_aprobado`. No hay particiones ni modelo entrenado.
