# Cambios propuestos, no aplicados

Ningún cambio de esta lista se escribió en `piloto_hu07_v2/`. Las etiquetas originales siguen como estaban.

## No se propone

- No se propone otra categoría para la ceniza ni para el polvo blanco.
- No se reescribe ninguna frase.
- No se cambia ningún `crop` ni ninguna `region`.
- No se propone partir ni fusionar filas.
- No se propone pasar las cinco rechazadas del anexo a aceptadas.
- No se propone una partición de entrenamiento, validación o prueba.

## Disposición propuesta para el conjunto, cuando una persona cierre la revisión

1. Mantener fuera de todo conjunto etiquetado definitivo, hasta una decisión humana, a `piloto-v2-04805c4db9` y `piloto-v2-99b5624803`.
2. No usar `piloto-v2-41bdf8b563` como ejemplo de `cosecha_poscosecha`. La disposición propuesta es rechazarla por quedar fuera de las ocho categorías. Sigue sin aplicarse.
3. No dar por cerradas las 57. Su etiqueta original permanece, y el informe de auditoría no cuenta como segunda firma.

Si una persona resuelve un caso ambiguo, `resolved_category` tendrá que ser un solo código de los ocho. Mientras esté vacío, la fila no entra a entrenamiento, validación ni prueba. `sin categoría` no se escribe.

## Notas de frontera que el primer revisor mencionó y no se añadieron

El primer revisor dijo que convenía una nota, si la fila se conservaba, en las nueve sin `review_note`. No se añadió ninguna nota al piloto. La lista es:

- `piloto-v2-1d4ef1a7bd` — categoría original `clima_heladas`
- `piloto-v2-9c434b0971` — categoría original `plagas`
- `piloto-v2-cae4b79822` — categoría original `plagas`
- `piloto-v2-df7f31f7d9` — categoría original `fertilizacion_nutricion`
- `piloto-v2-dc3422090c` — categoría original `fertilizacion_nutricion`
- `piloto-v2-86f762efd9` — categoría original `enfermedades_cultivos`
- `piloto-v2-c77fa8da96` — categoría original `fertilizacion_nutricion`
- `piloto-v2-45d1e6b6b2` — categoría original `suelos`
- `piloto-v2-5d8c063a1b` — categoría original `plagas`
