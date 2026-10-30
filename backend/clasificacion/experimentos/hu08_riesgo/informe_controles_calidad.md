# Controles de calidad del dataset sintético HU-08

Este conjunto es un ejercicio académico de clasificación. Todos los registros tienen `es_observacion_real` en false y `origen` en `sintetico_ejercicio_academico`. No salen de MySQL, de SENAMHI ni de HU-07.

Las etiquetas `bajo`, `medio` y `alto` las asignan las reglas de `reglas_etiquetado_sintetico.md`. Son supuestos de simulación. No son umbrales agronómicos validados ni riesgo observado en un predio.

## Controles

- Semilla del generador y de la partición: 42.
- Registros: 720. Duplicados en las variables de clasificación: 0.
- Solape entre entrenamiento y prueba: 0.
- SHA-256: `31d2fa1fca6ab03ae629eef2c7e57e5a45a55c0072199c0d98ec26dbae2a17e6`.

| Variable | Valores nulos | Exactitud de la mejor constante por grupo |
|---|---:|---:|
| familia_escenario | 0 | 0.3333 |
| cultivo | 0 | 0.3611 |
| region | 0 | 0.3653 |
| etapa_fenologica | 0 | 0.6417 |
| temperatura_c | 116 | 0.3986 |
| precipitacion_mm | 95 | 0.4486 |
| dias_sin_lluvia | 0 | 0.3819 |
| sintoma_observado | 0 | 0.3903 |
| proporcion_afectada | 0 | 0.4264 |
| condicion_suelo | 0 | 0.3917 |

La exactitud de una sola variable es la de predecir, en cada grupo de esa variable, la etiqueta más frecuente del grupo. En temperatura, precipitación, días sin lluvia y proporción, los grupos son cuartiles más el grupo nulo. Ninguna variable llega a 0,80. La etiqueta no sale de un umbral sobre una sola columna.

Los nulos están solo en `temperatura_c` y `precipitacion_mm`. El resto de las variables está completo. Un nulo suma cero en la regla y no se sustituye por un número.

## Variedad

Cultivos: cebada 169, haba 135, maíz 139, papa 121, quinua 156.

Regiones de texto: Chupaca 112, Concepción 114, Huancayo 129, Jauja 116, Junín 124, Tarma 125.

Etapas: desarrollo_vegetativo 61, emergencia 199, floracion 195, llenado 91, maduracion 98, siembra 76.

`cultivo` y `region` no entran en la fórmula. Están para que el ejercicio no use un único cultivo ni un único lugar. Los nombres de región no son mediciones hechas en esos distritos.

## Limitaciones

- La etapa es la variable suelta que más se acerca a la etiqueta (exactitud 0.6417) porque varias reglas piden `emergencia` o `floracion` para llegar a `alto`. No la determina: esas etapas también aparecen en `bajo` y `medio`. Por eso el muestreo deja más filas en esas dos etapas.
- `cultivo` y `region` no cambian la etiqueta. Un modelo que se apoye en ellos estará usando variación que esta simulación no relaciona con el nivel.
- No hay observaciones reales ni etiquetas de daño en campo.
- Las unidades Celsius y mm las define la simulación. No fueron leídas del adaptador SENAMHI.
- La etapa pertenece a un vocabulario de ejercicio, no a un calendario validado.
- El síntoma simulado no es un diagnóstico.
- El dataset no debe integrarse al backend ni usarse para aconsejar a un agricultor.
- No se entrenó un modelo en esta generación.
