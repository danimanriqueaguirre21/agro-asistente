# Integración del prototipo de riesgo HU-08

La predicción es un ejercicio académico. Usa el modelo entrenado con etiquetas sintéticas de `sintetica-hu08-v1`. No está validada para decidir un riesgo agrícola real, no es un diagnóstico y no es una recomendación.

El endpoint está separado de `POST /api/v1/queries`. No cambia el RAG, el prompt de Ollama ni el clasificador de HU-07.

## Invocación

```text
POST /api/v1/riesgo
Authorization: Bearer <JWT>
Content-Type: application/json
```

El token se obtiene con `POST /api/v1/auth/login`.

## Variables

El cuerpo usa las diez variables del esquema, en cualquier orden JSON. El pipeline las coloca en el orden con el que fue entrenado.

| Campo | Formato |
|---|---|
| familia_escenario | `meteorologico`, `plaga_enfermedad` o `suelo_agua_manejo` |
| cultivo | texto no vacío |
| region | texto no vacío |
| etapa_fenologica | texto no vacío |
| temperatura_c | número o `null` |
| precipitacion_mm | número o `null` |
| dias_sin_lluvia | entero |
| sintoma_observado | `true` o `false` |
| proporcion_afectada | número entre 0 y 1. Si no hay síntoma, debe ser 0 |
| condicion_suelo | `seco`, `adecuado` o `encharcado` |

`null` en temperatura o precipitación lo acepta el preprocesamiento. No se rellena con cero en la petición. Las demás variables son obligatorias.

## Respuesta

HTTP 200. La categoría del ejemplo muestra la forma del contrato, no una medición de campo:

```json
{
  "categoria_predicha": "alto",
  "identificador_modelo": "bosque_aleatorio_profundidad12_hoja1",
  "version_reglas": "sintetica-hu08-v1",
  "naturaleza": "prototipo_academico_sintetico",
  "es_riesgo_agricola_validado": false
}
```

`categoria_predicha` solo puede ser `bajo`, `medio` o `alto`. La respuesta no incluye probabilidades.

Un cuerpo mal formado responde HTTP 422. Si el modelo no puede cargarse o devuelve una categoría ajena, responde HTTP 503 y no inventa una categoría. Sin JWT, responde HTTP 401.

## Pruebas

Desde `backend`:

```text
python -m pytest tests/test_prediccion_riesgo.py tests/test_architecture.py tests/test_health.py -q --tb=short
```

Esas pruebas no leen `prueba.jsonl`.

## Reproducir en local

1. Tener el archivo `modelo_riesgo_hu08.joblib` en esta carpeta, junto con `preprocesamiento_riesgo_hu08.py`.
2. Arrancar el backend como el resto del PMV1, desde `backend`:

```text
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

3. Iniciar sesión y enviar `POST /api/v1/riesgo`.

El pipeline se carga una sola vez, en la primera predicción. No se reentrena.

## Por qué es experimental

Las etiquetas salen de reglas de simulación, no de daños observados en predios. `es_riesgo_agricola_validado` permanece en `false`. El identificador del modelo recuerda que la pieza integrada es el bosque aleatorio del prototipo, no una metodología agronómica aprobada.
