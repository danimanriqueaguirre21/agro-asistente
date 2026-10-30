# Prueba ilustrativa de inferencia — HU-07

Esta prueba no evalúa el rendimiento del modelo. Las consultas son nuevas y sintéticas. El modelo no se volvió a entrenar y no entra al PMV1, al RAG ni a producción.

Puntuación: máximo de `predict_proba`. Por debajo de 0.55 se marca solo para leer esta prueba. Ese corte no se eligió con validación.

Consultas claras: 16. Coincidencias con la categoría esperada: 13.

| Id | Esperada | Predicha | Puntuación | Segunda | Margen | Lectura |
| --- | --- | --- | ---: | --- | ---: | --- |
| inf-01 | riego | riego | 0.5126 | cosecha_poscosecha | 0.3704 | Coincide con la categoría esperada. Baja puntuación. |
| inf-02 | riego | riego | 0.4160 | cosecha_poscosecha | 0.3062 | Coincide con la categoría esperada. Baja puntuación. |
| inf-03 | fertilizacion_nutricion | cosecha_poscosecha | 0.2793 | fertilizacion_nutricion | 0.0209 | No coincide con la categoría esperada. Baja puntuación. Confusión. |
| inf-04 | fertilizacion_nutricion | fertilizacion_nutricion | 0.2613 | enfermedades_cultivos | 0.1013 | Coincide con la categoría esperada. Baja puntuación. |
| inf-05 | plagas | plagas | 0.4763 | enfermedades_cultivos | 0.3769 | Coincide con la categoría esperada. Baja puntuación. |
| inf-06 | plagas | plagas | 0.6258 | enfermedades_cultivos | 0.5235 | Coincide con la categoría esperada. |
| inf-07 | enfermedades_cultivos | enfermedades_cultivos | 0.4563 | plagas | 0.2898 | Coincide con la categoría esperada. Baja puntuación. |
| inf-08 | enfermedades_cultivos | plagas | 0.1903 | enfermedades_cultivos | 0.0166 | No coincide con la categoría esperada. Baja puntuación. Confusión. |
| inf-09 | siembra_manejo_cultivo | siembra_manejo_cultivo | 0.5566 | riego | 0.4553 | Coincide con la categoría esperada. |
| inf-10 | siembra_manejo_cultivo | cosecha_poscosecha | 0.3179 | siembra_manejo_cultivo | 0.1236 | No coincide con la categoría esperada. Baja puntuación. Confusión. |
| inf-11 | clima_heladas | clima_heladas | 0.3774 | riego | 0.2496 | Coincide con la categoría esperada. Baja puntuación. |
| inf-12 | clima_heladas | clima_heladas | 0.4956 | plagas | 0.3937 | Coincide con la categoría esperada. Baja puntuación. |
| inf-13 | suelos | suelos | 0.4938 | fertilizacion_nutricion | 0.3880 | Coincide con la categoría esperada. Baja puntuación. |
| inf-14 | suelos | suelos | 0.3189 | riego | 0.1700 | Coincide con la categoría esperada. Baja puntuación. |
| inf-15 | cosecha_poscosecha | cosecha_poscosecha | 0.2109 | suelos | 0.0456 | Coincide con la categoría esperada. Baja puntuación. |
| inf-16 | cosecha_poscosecha | cosecha_poscosecha | 0.7215 | siembra_manejo_cultivo | 0.6476 | Coincide con la categoría esperada. |
| inf-17 | riego | riego | 0.2585 | clima_heladas | 0.0123 | Coincide con una de las dos lecturas. Baja puntuación. |
| inf-18 | suelos | riego | 0.3621 | suelos | 0.0679 | Coincide con una de las dos lecturas. Baja puntuación. |
| inf-19 | clima_heladas | clima_heladas | 0.1926 | cosecha_poscosecha | 0.0052 | Coincide con una de las dos lecturas. Baja puntuación. |
| inf-20 | plagas | plagas | 0.3365 | enfermedades_cultivos | 0.1230 | Coincide con una de las dos lecturas. Baja puntuación. |
| inf-21 | ninguna de las ocho | riego | 0.2827 | siembra_manejo_cultivo | 0.1022 | El modelo igual asignó una de las ocho. No puede devolver sin categoría. Baja puntuación. |

## Consultas

- **inf-01** (clara): ¿Dejo correr el agua por el surco del ajo en Concepción hasta el final del cantero, o corto la toma antes para que no se encharque?
- **inf-02** (clara): El aspersor de la alfalfa en Jauja moja solo media parcela. ¿Lo cambio de sitio o abro más la llave del ramal?
- **inf-03** (clara): ¿Echo sulfato de potasio al cafeto de Satipo cuando el grano ya está llenando, o ese abono va más temprano?
- **inf-04** (clara): Las hojas viejas del maíz de Chupaca amarillean parejo desde la punta y la planta sigue en pie. ¿Le falta nitrógeno en este momento?
- **inf-05** (clara): En el brote del cacao de Satipo hay insectos negros chupando la hoja tierna. ¿Los aplasto hoy o busco primero si ya dejaron huevos?
- **inf-06** (clara): El choclo de Tarma tiene un gusano metido en la mazorca. ¿Abro la panca para sacarlo o dejo la mazorca cerrada?
- **inf-07** (clara): La hoja de la quinua en Jauja muestra pústulas anaranjadas y no hay insecto caminando. ¿La miro como roya y corto esas hojas?
- **inf-08** (clara): El tallo de la granadilla en Chanchamayo se raja y por dentro está café y seco. ¿Es pudrición del tallo la que tengo que atender?
- **inf-09** (clara): ¿Siembro el tarwi de Yauli a chorro seguido en el surco, o dejo un palmo entre cada golpe de semilla?
- **inf-10** (clara): El frijol de Huancayo ya largó guía. ¿Le amarro un palo para que trepe o lo dejo arrastrado en el suelo?
- **inf-11** (clara): Esta noche anuncian helada en la puna de Tarma y la papa todavía está chica. ¿Humear la chacra con paja alcanza para cubrir esa helada?
- **inf-12** (clara): El granizo de ayer en Concepción agujereó la hoja del haba. ¿Reviso hoy el golpe del granizo o espero a que la hoja seque sola?
- **inf-13** (clara): En la ladera de Chupaca la tierra se va con cada lluvia y ya se abrió una cárcava. ¿Levanto una barrera de piedra para frenar ese suelo?
- **inf-14** (clara): Donde está la pituca en Satipo el suelo es tan suelto y arenoso que no retiene nada. ¿Le mezclo tierra más fina antes de seguir con el cultivo?
- **inf-15** (clara): ¿Saco la oca de Jauja cuando el follaje ya se secó, o el tubérculo sigue creciendo bajo tierra?
- **inf-16** (clara): El café pergamino de Satipo ya pasó por el tendedero. ¿Lo encierro en saco hoy o lo dejo aireando unos días más?
- **inf-17** (frontera): ¿Mojar la haba de Yauli al amanecer, con helada en el pasto, es el riego del día o es para proteger la planta del frío?
- **inf-18** (frontera): La costra del terreno de la papa en Huancayo no deja entrar el agua del surco. ¿Rompo esa costra o cambio la forma de regar?
- **inf-19** (frontera): El ventarrón de anoche rajó un racimo de plátano en Satipo que ya estaba pintón. ¿Lo corto ahora por el golpe del viento?
- **inf-20** (frontera): Hay una pelusa blanca en el brote del frijol de Tarma. No distingo si es un insecto quieto o un hongo.
- **inf-21** (sin_categoria_tematica): ¿A qué hora atiende la ventanilla del banco en Huancayo para cobrar un depósito?

## Confusiones en las consultas claras

- `inf-03`: se esperaba fertilizacion_nutricion y el modelo respondió cosecha_poscosecha (0.2793), con fertilizacion_nutricion en segundo lugar.
- `inf-08`: se esperaba enfermedades_cultivos y el modelo respondió plagas (0.1903), con enfermedades_cultivos en segundo lugar.
- `inf-10`: se esperaba siembra_manejo_cultivo y el modelo respondió cosecha_poscosecha (0.3179), con siembra_manejo_cultivo en segundo lugar.

## Puntuación baja en esta lectura

- `inf-01`: riego con 0.5126. Segunda opción: cosecha_poscosecha (0.1423).
- `inf-02`: riego con 0.4160. Segunda opción: cosecha_poscosecha (0.1098).
- `inf-03`: cosecha_poscosecha con 0.2793. Segunda opción: fertilizacion_nutricion (0.2584).
- `inf-04`: fertilizacion_nutricion con 0.2613. Segunda opción: enfermedades_cultivos (0.1601).
- `inf-05`: plagas con 0.4763. Segunda opción: enfermedades_cultivos (0.0994).
- `inf-07`: enfermedades_cultivos con 0.4563. Segunda opción: plagas (0.1665).
- `inf-08`: plagas con 0.1903. Segunda opción: enfermedades_cultivos (0.1737).
- `inf-10`: cosecha_poscosecha con 0.3179. Segunda opción: siembra_manejo_cultivo (0.1943).
- `inf-11`: clima_heladas con 0.3774. Segunda opción: riego (0.1278).
- `inf-12`: clima_heladas con 0.4956. Segunda opción: plagas (0.1019).
- `inf-13`: suelos con 0.4938. Segunda opción: fertilizacion_nutricion (0.1058).
- `inf-14`: suelos con 0.3189. Segunda opción: riego (0.1489).
- `inf-15`: cosecha_poscosecha con 0.2109. Segunda opción: suelos (0.1654).
- `inf-17`: riego con 0.2585. Segunda opción: clima_heladas (0.2462).
- `inf-18`: riego con 0.3621. Segunda opción: suelos (0.2943).
- `inf-19`: clima_heladas con 0.1926. Segunda opción: cosecha_poscosecha (0.1875).
- `inf-20`: plagas con 0.3365. Segunda opción: enfermedades_cultivos (0.2135).
- `inf-21`: riego con 0.2827. Segunda opción: siembra_manejo_cultivo (0.1805).

## Límite

El pipeline siempre devuelve una de las ocho categorías. La consulta del banco no tiene categoría temática y aun así recibió una predicción. Estas coincidencias no aprueban el dataset ni sustituyen una evaluación con consultas reales.
