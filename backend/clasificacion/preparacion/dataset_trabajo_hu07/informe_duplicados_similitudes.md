# Informe de duplicados y similitudes

Control aplicado al archivo aceptado `consultas_trabajo.jsonl` (1.600 registros).

## Dentro del archivo

- Duplicados exactos tras normalizar (NFC, minúsculas, espacios colapsados, puntuación de los extremos): 0.
- Esqueletos repetidos al enmascarar cultivo y provincia: 0. Una misma frase con otro cultivo o otra provincia no se contó dos veces.
- Pares con Jaccard de tokens mayor o igual a 0,60, o SequenceMatcher mayor o igual a 0,84: 0.

El par más cercano, todavía bajo esos umbrales, está en plagas:

- `trabajo-hu07-d6612d79a4`: «¿La polilla del olluco de Yauli se busca de noche en el follaje o en el tubérculo?»
- `trabajo-hu07-628a8b17ab`: «¿La polilla del olluco se confunde con la de la papa. En Yauli, en el olluco, ¿busco la larva en la hoja o en el tubérculo?»
- Jaccard 0,55. SequenceMatcher 0,597.

Ese par debe viajar junto en una partición futura. No se separa entre entrenamiento y prueba.

## Frente a fuentes que no se pueden reutilizar

Se compararon 363 textos: 24 de la muestra ilustrativa, 80 del preliminar, las aceptadas y rechazadas del piloto, 6 preguntas RAGAS de `pmv1_baseline.json`, las líneas de `knowledge/` de al menos 25 caracteres y las frases de prueba del backend.

Umbral de cruce: Jaccard mayor o igual a 0,55 o SequenceMatcher mayor o igual a 0,80.

En una pasada anterior el control marcó tres consultas. Esas tres líneas se reescribieron y el control se volvió a ejecutar. En la corrida aceptada los cruces son 0.

## Lo que no se pudo cruzar

No hay en el repositorio un archivo con las 800 consultas sintéticas anteriores. Un glob que buscaba «800» en el nombre encontraba archivos del entorno virtual y objetos de git, y eso no es ese conjunto. El cruce contra esas 800 no se ejecutó.

## Anexos

Las 16 ambiguas y las 12 de fuera de alcance no entran en el conteo de duplicados de las 1.600. También son sintéticas y pendientes. No copian las frases ambiguas del piloto ni la frase rechazada sobre la venta de olluco.
