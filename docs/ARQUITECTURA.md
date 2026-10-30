# Arquitectura — Agro Asistente PMV1

Arquitectura hexagonal (Ports and Adapters), según la consigna del curso.

## Capas

```text
Frontend (React + Vite)
        │  HTTP REST
        ▼
Adaptadores de entrada (FastAPI)
        │  puertos de entrada
        ▼
Aplicación (casos de uso y servicios)
        │  puertos de salida
        ▼
Dominio (entidades, value objects, ports)
        ▲
        │  implementaciones
Adaptadores de salida
  - MySQL (SQLAlchemy solo aquí)
  - Chroma
  - Seguridad (JWT / bcrypt)
  - Embeddings externos
  - Generación por plantilla (solo pruebas / `GENERATION_PROVIDER=template`)
  - Ollama + Qwen2.5 (PMV1, `GENERATION_PROVIDER=ollama`)
```

## Reglas

1. `domain` no importa FastAPI, SQLAlchemy, Chroma, Ollama, React, httpx ni SDKs de IA.
2. `application` depende de `domain` y de puertos.
3. `infrastructure` implementa los puertos.
4. Los controladores HTTP solo hablan con puertos de entrada / casos de uso (en Fase 1, `/health` es un adaptador de entrada de infraestructura).
5. La composición de dependencias vive en infraestructura (`composition.py`).
6. Los servicios externos se aislan detrás de puertos.

## Embeddings (HU-06 / Sesión 3)

```text
EmbeddingPort          ← dominio
    ├── LocalLexicalEmbeddingAdapter   ← PMV1 (hashing de tokens, no semántico)
    └── ExternalEmbeddingAdapter       ← infraestructura (proveedor concreto pendiente)
```

La API concreta de embeddings no está acoplada al dominio ni a los casos de uso. Las credenciales del futuro proveedor se leen solo desde variables de entorno.

## Generación de texto (PMV1)

Nota de alcance: una planificación anterior dejó el SLM para PMV2 (`SLMGenerationAdapter`). El documento **Uso de herramientas modernas** asigna Ollama y Qwen2.5 1.8B al **PMV1**. El alcance actual del Hito 1 es RAG + SLM base **sin fine-tuning**. LoRA sigue fuera del PMV1.

```text
PuertoGeneracionTexto
    ├── AdaptadorGeneracionOllama     ← PMV1 (Ollama, modelo en OLLAMA_MODEL)
    └── AdaptadorGeneracionPlantilla  ← fallback técnico / pytest
```

`generation_method` refleja el adaptador real: `ollama` o `template`. Nunca se etiqueta como Ollama una respuesta de plantilla.

El identificador del curso es «Qwen2.5 1.8B». La biblioteca de Ollama **no publica** `qwen2.5:1.8b`; la variante oficial más cercana de Qwen2.5 es `qwen2.5:1.5b` (configurable).

HU-04/HU-06 recuperan evidencias RAG y el caso de uso `RegistrarConsulta` llama solo a `PuertoGeneracionTexto`.

## Evaluación RAGAS (línea base PMV1)

RAGAS **no** se importa en `domain` ni en `application`. Vive en `backend/evaluation/`. El script llama a los mismos adaptadores de recuperación y generación que el PMV1 (`ServicioRecuperacionRag` + `AdaptadorGeneracionOllama`). No modifica `PuertoGeneracionTexto`.

Propósito: primera línea base (RAG + Ollama + Qwen2.5 sin fine-tuning). Métricas de `ragas==0.4.3`: `Faithfulness`, `LLMContextRecall`, `ResponseRelevancy`. Las puntuaciones solo existen después de `python -m evaluation.run_baseline`; ver `backend/evaluation/RESULTADOS_PENDIENTES.md` hasta esa corrida. `evaluation/ragas_compat.py` cubre un import de Vertex AI que `langchain-community` 0.4 ya no exporta; no se usa Vertex en el PMV1.

### Matriz de evidencia

| Herramienta | Uso en PMV1 | Estado |
|---|---|---|
| RAGAS | Evaluación de línea base | Preparado; ejecución real pendiente |
| Ollama | Generación | PMV1 |
| Qwen2.5 1.8B | SLM base (tag configurable) | Configurado vía `OLLAMA_MODEL` |
| Python | Script de evaluación | `evaluation.run_baseline` |
| Google Colab Pro | Ejecución opcional | Notebook no ejecutado |

## Persistencia

- **MySQL:** agricultores, contexto agrícola, consultas, respuestas, catálogo de conocimiento y evidencias (`database/schema.sql`).
- **Chroma:** índice vectorial de fragmentos (`agro_knowledge_pmv1`).

MySQL y Chroma no se consideran el servicio de generación. Ese rol lo cubre **Ollama** en el PMV1 (`AdaptadorGeneracionOllama`). `ExternalEmbeddingAdapter` sigue siendo un placeholder de embeddings, no el SLM.

## Composition root

`backend/app/main.py` construye el contenedor de infraestructura y registra los adaptadores de entrada HTTP. El dominio no conoce FastAPI.

## HU-01 — Registro de agricultor

Componentes:

| Capa | Componente |
|---|---|
| Dominio | `Farmer`, `Email`, `PasswordHash` |
| Puerto de entrada | `RegisterFarmerPort` |
| Caso de uso | `RegisterFarmer` |
| Puertos de salida | `FarmerRepositoryPort`, `PasswordHasherPort` |
| Adaptadores | `MysqlFarmerRepository`, `BcryptPasswordHasher` |
| HTTP | `POST /api/v1/auth/register` |
| Frontend | `/register` |

```text
POST /api/v1/auth/register
        ↓
auth_controller (adaptador de entrada)
        ↓
RegisterFarmerPort / RegisterFarmer
        ↓
FarmerRepositoryPort          PasswordHasherPort
        ↓                              ↓
MysqlFarmerRepository         BcryptPasswordHasher
        ↓
tabla farmers (MySQL/MariaDB)
```

La tabla `farmers` reutiliza el esquema de Fase 1: `id` (UUID), `full_name` (nombres y apellidos concatenados), `email` único y `password_hash` bcrypt.

## HU-02 — Inicio de sesión

Componentes:

| Capa | Componente |
|---|---|
| Dominio | `LoginFarmerPort`, `TokenIssuerPort`, `InvalidCredentialsError` |
| Caso de uso | `LoginFarmer` |
| Puertos de salida | `FarmerRepositoryPort`, `PasswordHasherPort`, `TokenIssuerPort` |
| Adaptadores | `MysqlFarmerRepository`, `BcryptPasswordHasher`, `JwtTokenIssuer` |
| HTTP | `POST /api/v1/auth/login` |
| Frontend | `/login` |

```text
POST /api/v1/auth/login
        ↓
auth_controller
        ↓
LoginFarmerPort / LoginFarmer
        ↓
FarmerRepositoryPort     PasswordHasherPort     TokenIssuerPort
        ↓                       ↓                     ↓
MysqlFarmerRepository    BcryptPasswordHasher    JwtTokenIssuer
```

El JWT se firma en infraestructura con PyJWT. Claims: `sub` (id del agricultor), `email`, `exp`. Configuración: `JWT_SECRET`, `JWT_ALGORITHM`, `JWT_EXPIRE_MINUTES`.

## HU-03 — Contexto agrícola

Componentes:

| Capa | Componente |
|---|---|
| Dominio | `AgriculturalContext`, `Crop`, `Region`, `ManageContextPort` |
| Casos de uso | `CreateAgriculturalContext`, `ListAgriculturalContexts`, `SelectAgriculturalContext` |
| Puertos de salida | `AgriculturalContextRepositoryPort`, `TokenVerifierPort` |
| Adaptadores | `MysqlAgriculturalContextRepository`, `JwtTokenVerifier` |
| HTTP | `GET/POST /api/v1/contexts`, `POST /api/v1/contexts/{id}/select` |
| Frontend | `/context` |

```text
Authorization: Bearer JWT
        ↓
JwtTokenVerifier (sub = farmer_id)
        ↓
Create / List / Select
        ↓
AgriculturalContextRepositoryPort
        ↓
tabla agricultural_contexts
```

Campos persistidos (esquema de Fase 1, sin migración): `plot_name`, `crop`, `region`, `notes`, `is_selected`. La selección es persistente: un solo contexto `is_selected` por agricultor. El aislamiento es por `farmer_id` del JWT, no por un id enviado en el body.

## HU-04 — Consulta agrícola

Componentes:

| Capa | Componente |
|---|---|
| Dominio | `Query`, `Response`, `QueryText` |
| Puerto de entrada | `SubmitQueryPort` |
| Caso de uso | `SubmitQuery` |
| Puertos de salida | `QueryRepositoryPort`, `PuertoGeneracionTexto` |
| Adaptadores | `MysqlQueryRepository`, `AdaptadorGeneracionOllama` (PMV1) |
| HTTP | `POST /api/v1/queries` |
| Frontend | `/query` |

```text
Authorization: Bearer JWT
        ↓
JwtTokenVerifier (sub = farmer_id)
        ↓
SubmitQuery
        ↓
contexto seleccionado del agricultor
        ↓
QueryRepositoryPort                 PuertoGeneracionTexto
        ↓                                   ↓
MysqlQueryRepository                AdaptadorGeneracionOllama
        ↓
tablas queries y responses
```

La consulta queda asociada al agricultor autenticado, al contexto `is_selected` de ese agricultor y a `created_at`. Si no hay contexto seleccionado, el caso de uso responde con error controlado (`SelectedContextNotFoundError` → HTTP 409).

HU-06 extiende `RegistrarConsulta` con recuperación RAG. El método de generación del PMV1 es `ollama` cuando el SLM responde. Si Ollama falla: HTTP 503, sin fingir éxito.

`ListQueryHistoryPort` no formaba parte del diseño implementado de HU-04; no se agregó `GET /api/v1/queries`.

El esquema de Fase 1 (`queries.question_text`, `responses.answer_text`, `responses.generation_method`) se reutilizó sin cambios.

## HU-05 — Base de conocimiento agrícola

Componentes:

| Capa | Componente |
|---|---|
| Dominio | `KnowledgeDocument`, `ContentHash` |
| Puerto de entrada | `IngestKnowledgePort`, `ListKnowledgeDocumentsPort` |
| Caso de uso | `IngestKnowledge`, `ListKnowledgeDocuments` |
| Puerto de salida | `KnowledgeDocumentRepositoryPort` |
| Adaptador | `MysqlKnowledgeDocumentRepository` |
| HTTP | `POST /api/v1/knowledge/ingest`, `GET /api/v1/knowledge/documents` |
| Frontend | `/knowledge` |

```text
Authorization: Bearer JWT
        ↓
Knowledge controller
        ↓
IngestKnowledge
        ↓
validación → SHA-256 → detección de duplicado
        ↓
KnowledgeDocumentRepositoryPort
        ↓
MysqlKnowledgeDocumentRepository
        ↓
tabla knowledge_documents + knowledge/{id}.md
```

El esquema de Fase 1 no tiene columna de contenido: el Markdown se guarda en `knowledge/` y `source_path` apunta al archivo. `content_hash` es SHA-256 (64 hex) y es único. `chunk_count` se persiste en 0 en la ingesta; la indexación de HU-06 lo actualiza.

`EmbeddingPort` y Chroma no se usan en la ingesta. La indexación es un caso de uso aparte (`IndexKnowledge`).

La ingesta requiere JWT, sin roles de administrador: cualquier agricultor autenticado puede incorporar o listar documentos del catálogo compartido.

## HU-06 — RAG básico

Componentes:

| Capa | Componente |
|---|---|
| Dominio | `Evidence`, `EmbeddingPort`, `VectorStorePort`, `EvidenceRepositoryPort` |
| Aplicación | `DocumentChunker`, `RagRetrievalService`, `IndexKnowledge`, `SubmitQuery` |
| Adaptadores | `LocalLexicalEmbeddingAdapter`, `ChromaVectorStoreAdapter`, `MysqlEvidenceRepository`, `AdaptadorGeneracionOllama` |
| HTTP | `POST /api/v1/queries`, `POST /api/v1/knowledge/index` |
| Frontend | `/query` (consulta, contexto, respuesta y evidencias) |

```text
Authorization: Bearer JWT
        ↓
SubmitQuery
        ↓
contexto seleccionado
        ↓
RagRetrievalService
        ↓
EmbeddingPort                 VectorStorePort
        ↓                             ↓
LocalLexicalEmbeddingAdapter   ChromaVectorStoreAdapter
                                      ↓
                           colección agro_knowledge_pmv1
        ↓
evidencias (si hay similitud suficiente)
        ↓
PuertoGeneracionTexto / AdaptadorGeneracionOllama
        ↓
QueryRepositoryPort + EvidenceRepositoryPort
        ↓
tablas queries, responses, evidences
```

### Embeddings

- **Implementado en PMV1:** `LocalLexicalEmbeddingAdapter`. Genera vectores deterministas por hashing de tokens. Sirve para recuperar fragmentos con solapamiento de términos. **No es un embedding semántico** ni una llamada a un proveedor externo.
- **Pendiente (Sesión 3):** `ExternalEmbeddingAdapter` + `EMBEDDING_API_URL` / `EMBEDDING_API_KEY` / `EMBEDDING_MODEL`. El dominio solo habla con `EmbeddingPort`.

`EMBEDDING_PROVIDER=local` (por defecto) usa el adaptador léxico. `EMBEDDING_PROVIDER=external` deja el placeholder de Fase 1, que aún no invoca un proveedor.

### Chroma

Colección única del PMV1: `agro_knowledge_pmv1` (`CHROMA_COLLECTION`). Persistencia local en `CHROMA_PERSIST_DIR` (por defecto `./chroma_data`). MySQL y Chroma no sustituyen al servicio externo de IA exigido por la consigna.

### Chunking e IDs

Troceo simple por párrafos Markdown, con recorte por `CHUNK_SIZE` (500 caracteres por defecto). El id de cada fragmento es determinista:

```text
{content_hash}:chunk:{índice:04d}
```

Reindexar el mismo documento hace `upsert` sobre los mismos ids: no duplica chunks. Si el contenido cambia, el hash cambia y se generan ids nuevos.

### Recuperación

`RAG_TOP_K` (3) y `RAG_MIN_SIMILARITY` (0.12) son configurables. No hay ranking avanzado. Si no hay resultados por encima del umbral, no se inventa evidencia y el SLM debe indicar que no hay información suficiente (el prompt se lo exige).

### Indexación

La ingesta (HU-05) no indexa. Para demostrar HU-06:

```text
POST /api/v1/knowledge/index
Authorization: Bearer <JWT>
```

Cualquier agricultor autenticado puede indexar (sin roles nuevos). El endpoint recorre los documentos registrados, lee `knowledge/{id}.md`, genera chunks, embeddings y los envía a Chroma.
