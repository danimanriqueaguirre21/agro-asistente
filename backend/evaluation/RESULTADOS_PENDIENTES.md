# RESULTADOS PENDIENTES — línea base RAGAS PMV1

**EVALUACIÓN PENDIENTE**

**NO HAY RESULTADOS TODAVÍA**

No se generó ningún archivo de puntuaciones. No se inventaron métricas.

## Qué falta

1. **Ollama en ejecución** (`ollama serve`) y el modelo de `OLLAMA_MODEL` instalado (`ollama pull qwen2.5:1.5b` o el tag de su laboratorio).
2. **Índice Chroma** con la base de conocimiento. Si la colección está vacía, hay que indexar (`POST /api/v1/knowledge/index`), y eso **sí requiere MySQL** operativo con documentos ingeridos.
3. Confirmar `GENERATION_PROVIDER=ollama` en `backend/.env`. El script **no** cae a plantilla.
4. Juez RAGAS: por defecto el mismo Ollama (`/v1`). Si usa `RAGAS_LLM_PROVIDER=openai`, hace falta `OPENAI_API_KEY` en el entorno (nunca en git).

MySQL no es necesario para puntuar si Chroma ya tiene fragmentos. En este entorno de desarrollo MySQL ha fallado con `Access denied for user 'root'@'localhost'`; si el índice está vacío, hay que corregir credenciales y reindexar.

## Cómo ejecutar

```powershell
cd backend
.\.venv\Scripts\Activate.ps1
# .env: GENERATION_PROVIDER=ollama
python -m evaluation.run_baseline
```

## Variables

| Variable | Rol |
|---|---|
| `GENERATION_PROVIDER` | Debe ser `ollama` |
| `OLLAMA_BASE_URL` | p. ej. `http://127.0.0.1:11434` |
| `OLLAMA_MODEL` | Tag instalado (default documentado `qwen2.5:1.5b`) |
| `OLLAMA_TIMEOUT_SECONDS` | Timeout de generación |
| `CHROMA_PERSIST_DIR` / `CHROMA_COLLECTION` | Índice real del PMV1 |
| `RAGAS_LLM_PROVIDER` | `ollama` (defecto) u `openai` |
| `RAGAS_EMBEDDING_MODEL` | Embeddings del juez (opcional) |
| `OPENAI_API_KEY` | Solo si el juez es OpenAI |

## Comando

`python -m evaluation.run_baseline` desde `backend/`.
