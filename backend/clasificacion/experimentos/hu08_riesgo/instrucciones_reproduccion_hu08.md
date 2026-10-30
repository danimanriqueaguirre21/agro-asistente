# Reproducir el entrenamiento HU-08

Prototipo académico. El comando vuelve a entrenar con `entrenamiento.jsonl` y la semilla 42. No lee `prueba.jsonl` y no modifica los JSONL.

Requisitos ya usados por el proyecto: Python 3.13, scikit-learn 1.9 y joblib. No hace falta pandas.

```text
python "backend/clasificacion/experimentos/hu08_riesgo/entrenar_modelo_riesgo_hu08.py"
```

También se puede ejecutar desde esta carpeta:

```text
python entrenar_modelo_riesgo_hu08.py
```

El script sobrescribe solo los artefactos de entrenamiento de HU-08: el joblib, las métricas, la configuración, este instructivo y el informe técnico.

Para cargar después el pipeline hace falta que este directorio esté en la ruta de importación, porque el preprocesamiento vive en `preprocesamiento_riesgo_hu08.py`:

```text
import sys
from pathlib import Path
import joblib

carpeta = Path("backend/clasificacion/experimentos/hu08_riesgo")
sys.path.insert(0, str(carpeta))
pipeline = joblib.load(carpeta / "modelo_riesgo_hu08.joblib")
```

La entrada de `predict` es una matriz con las diez variables en el orden guardado en `configuracion_seleccionada_hu08.json`. Un valor ausente se pasa como `None` o como NaN. No se rellena con cero antes de llamar al pipeline.
