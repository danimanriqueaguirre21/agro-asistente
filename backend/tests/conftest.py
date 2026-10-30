import os

# Los tests unitarios y HTTP no requieren Ollama. El proveedor activo de PMV1
# sigue siendo ollama en .env.example; pytest fuerza plantilla salvo integración.
_valor_integracion = (
    os.environ.get("RUN_OLLAMA_INTEGRATION_TESTS")
    or os.environ.get("OLLAMA_INTEGRATION")
    or ""
).strip().lower()
if _valor_integracion not in {"1", "true", "yes"}:
    os.environ["GENERATION_PROVIDER"] = "template"
