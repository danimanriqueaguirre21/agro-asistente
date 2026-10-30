# Distribución del dataset sintético HU-08

Ejercicio académico. Las etiquetas son supuestos de simulación, no riesgo agrícola observado.

- Semilla: 42.
- Reglas: `sintetica-hu08-v1`.
- Registros: 720.
- Entrenamiento: 576. Prueba: 144.
- SHA-256 de `dataset_hu08_sintetico.jsonl`: `31d2fa1fca6ab03ae629eef2c7e57e5a45a55c0072199c0d98ec26dbae2a17e6`.

Cada familia aporta 80 registros a cada nivel. El total de cada nivel es 240.

| Nivel | Total | Entrenamiento | Prueba |
|---|---:|---:|---:|
| bajo | 240 | 192 | 48 |
| medio | 240 | 192 | 48 |
| alto | 240 | 192 | 48 |

La partición es estratificada por familia y nivel, con fracción de prueba 0,2.
Los identificadores están en `ids_particiones.json`.
El entrenamiento posterior debe leer `entrenamiento.jsonl` y evaluar en `prueba.jsonl`.
