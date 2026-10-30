# Pruebas de anexos ambiguos y fuera de alcance

Fecha: 2026-10-19.

Se ejecutó el clasificador v2 ya entrenado, con el margen 0,17, sobre los textos originales de los anexos. No se reentrenó el modelo, no se modificaron las etiquetas ni los JSONL, y `sin categoría` no es una clase. Estas consultas son sintéticas. El resultado no describe agricultores reales.

La abstención es un margen menor que 0,17 entre dos de las ocho categorías. No es una detección de fuera de alcance. El modelo no tiene esa clase.

## Prueba

Archivo: `backend/tests/test_anexos_ambiguos_fuera_alcance.py`.

Lee `cola_ambigua.jsonl` (16) y `fuera_de_alcance.jsonl` (12). Comprueba identificador, texto, reproducibilidad de dos pasadas, que las clases punteras sean de las ocho, y que el corte 0,17 decida la abstención. No exige que toda consulta ambigua se abstenga. Comprueba que el SHA-256 del joblib no cambia.

## Ambiguas

Nueve quedaron en `sin categoría`. Siete recibieron una categoría temática. Eso no resuelve el anexo: `resolved_category` sigue vacío.

| Id | Salida | Primera | Segunda | Margen | Categoría forzada |
| --- | --- | --- | --- | ---: | --- |
| ambigua-23d14e1d7f | fertilizacion_nutricion | fertilizacion_nutricion | riego | 0,5757 | Sí |
| ambigua-6f2d0da819 | sin categoría | enfermedades_cultivos | riego | 0,0771 | No |
| ambigua-c3fe6fb00c | enfermedades_cultivos | enfermedades_cultivos | plagas | 0,2645 | Sí |
| ambigua-198e86ea7a | sin categoría | fertilizacion_nutricion | suelos | 0,1554 | No |
| ambigua-45301ad12c | sin categoría | suelos | fertilizacion_nutricion | 0,0932 | No |
| ambigua-276d2f3f16 | sin categoría | enfermedades_cultivos | suelos | 0,0231 | No |
| ambigua-d6551bca95 | riego | riego | clima_heladas | 0,5423 | Sí |
| ambigua-13e8c1f247 | cosecha_poscosecha | cosecha_poscosecha | riego | 0,2082 | Sí |
| ambigua-b3a1b7ff2e | sin categoría | plagas | siembra_manejo_cultivo | 0,0698 | No |
| ambigua-cfa3faca8e | sin categoría | siembra_manejo_cultivo | clima_heladas | 0,1121 | No |
| ambigua-732e076490 | sin categoría | suelos | riego | 0,0976 | No |
| ambigua-6cb985554b | cosecha_poscosecha | cosecha_poscosecha | plagas | 0,5757 | Sí |
| ambigua-8309badc59 | enfermedades_cultivos | enfermedades_cultivos | clima_heladas | 0,3738 | Sí |
| ambigua-bd1a2cc048 | suelos | suelos | siembra_manejo_cultivo | 0,4208 | Sí |
| ambigua-f1f1d621d2 | sin categoría | cosecha_poscosecha | plagas | 0,1300 | No |
| ambigua-abc3fbb2d9 | sin categoría | suelos | fertilizacion_nutricion | 0,0424 | No |

## Fuera de alcance

Nueve quedaron en `sin categoría` por margen bajo. Tres recibieron una categoría de las ocho. Esa categoría no significa que el modelo haya reconocido el fuera de alcance.

| Id | Salida | Primera | Segunda | Margen | Categoría forzada |
| --- | --- | --- | --- | ---: | --- |
| fuera-0e5164f24b | sin categoría | cosecha_poscosecha | plagas | 0,0979 | No |
| fuera-af5096fb20 | fertilizacion_nutricion | fertilizacion_nutricion | riego | 0,6590 | Sí |
| fuera-5c19ffc535 | sin categoría | fertilizacion_nutricion | plagas | 0,0599 | No |
| fuera-eb620d142c | sin categoría | fertilizacion_nutricion | cosecha_poscosecha | 0,1294 | No |
| fuera-8f214c6c3f | sin categoría | cosecha_poscosecha | fertilizacion_nutricion | 0,0296 | No |
| fuera-fcd1b2859b | sin categoría | riego | plagas | 0,0121 | No |
| fuera-80162a511b | sin categoría | riego | fertilizacion_nutricion | 0,0281 | No |
| fuera-e5575b70a5 | riego | riego | siembra_manejo_cultivo | 0,2583 | Sí |
| fuera-b4656c0257 | fertilizacion_nutricion | fertilizacion_nutricion | cosecha_poscosecha | 0,2424 | Sí |
| fuera-b8577dbedf | sin categoría | riego | suelos | 0,0632 | No |
| fuera-3533668bc1 | sin categoría | suelos | clima_heladas | 0,0351 | No |
| fuera-71bf046c3d | sin categoría | fertilizacion_nutricion | enfermedades_cultivos | 0,0739 | No |

## Casos que siguen con categoría forzada

Ambiguas, sin decisión humana:

- `ambigua-23d14e1d7f`, agua y abono el mismo día, fertilizacion_nutricion.
- `ambigua-c3fe6fb00c`, polvo blanco, enfermedades_cultivos.
- `ambigua-d6551bca95`, agua de madrugada, riego.
- `ambigua-13e8c1f247`, papa guardada que se pudre, cosecha_poscosecha.
- `ambigua-6cb985554b`, bicho y humedad en el cuarto, cosecha_poscosecha.
- `ambigua-8309badc59`, hoja comida y manchada, enfermedades_cultivos.
- `ambigua-bd1a2cc048`, preparar terreno y sembrar, suelos.

Fuera de alcance, con una categoría agronómica asignada igual:

- `fuera-af5096fb20`, crédito del banco para abono, fertilizacion_nutricion.
- `fuera-e5575b70a5`, horario de oficina en Huancayo, riego.
- `fuera-b4656c0257`, IGV de un recibo, fertilizacion_nutricion.

Las etiquetas de los anexos no se cambiaron.

## Limitaciones

El modelo solo elige entre ocho clases o se abstiene. Una abstención en una consulta de precio, trámite o ganado no la clasifica como fuera de alcance. Las puntuaciones no están calibradas. El dataset sigue sin aprobación humana. HU-07 no está terminada.
