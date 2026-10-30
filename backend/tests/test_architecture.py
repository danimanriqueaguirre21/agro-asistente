from pathlib import Path

FORBIDDEN = (
    "fastapi",
    "sqlalchemy",
    "chromadb",
    "httpx",
    "jwt",
    "bcrypt",
    "pymysql",
    "react",
    "ollama",
    "ragas",
)


def test_domain_does_not_import_frameworks_or_sdks() -> None:
    domain_root = Path(__file__).resolve().parents[1] / "app" / "domain"
    violations: list[str] = []

    for python_file in domain_root.rglob("*.py"):
        content = python_file.read_text(encoding="utf-8").lower()
        for module_name in FORBIDDEN:
            if f"import {module_name}" in content or f"from {module_name}" in content:
                violations.append(f"{python_file}: {module_name}")

    assert violations == []


def test_application_does_not_import_frameworks() -> None:
    application_root = Path(__file__).resolve().parents[1] / "app" / "application"
    violations: list[str] = []
    forbidden = (
        "fastapi",
        "sqlalchemy",
        "chromadb",
        "httpx",
        "bcrypt",
        "pymysql",
        "pydantic",
        "jwt",
        "ollama",
        "ragas",
    )

    for python_file in application_root.rglob("*.py"):
        content = python_file.read_text(encoding="utf-8").lower()
        for module_name in forbidden:
            if f"import {module_name}" in content or f"from {module_name}" in content:
                violations.append(f"{python_file}: {module_name}")

    assert violations == []


def test_bcrypt_stays_inside_security_adapter() -> None:
    backend_root = Path(__file__).resolve().parents[1]
    allowed = backend_root / "app" / "infrastructure" / "adapters" / "output" / "security"
    violations: list[str] = []

    for python_file in (backend_root / "app").rglob("*.py"):
        content = python_file.read_text(encoding="utf-8")
        if "import bcrypt" not in content and "from bcrypt" not in content:
            continue
        if allowed in python_file.parents or python_file.parent == allowed:
            continue
        violations.append(str(python_file.relative_to(backend_root)))

    assert violations == []


def test_pyjwt_stays_inside_security_adapter() -> None:
    backend_root = Path(__file__).resolve().parents[1]
    allowed = backend_root / "app" / "infrastructure" / "adapters" / "output" / "security"
    violations: list[str] = []

    for python_file in (backend_root / "app").rglob("*.py"):
        content = python_file.read_text(encoding="utf-8")
        if "import jwt" not in content and "from jwt" not in content:
            continue
        if allowed in python_file.parents or python_file.parent == allowed:
            continue
        violations.append(str(python_file.relative_to(backend_root)))

    assert violations == []


def test_sqlalchemy_stays_inside_mysql_adapter() -> None:
    backend_root = Path(__file__).resolve().parents[1]
    allowed = backend_root / "app" / "infrastructure" / "adapters" / "output" / "mysql"
    violations: list[str] = []

    for python_file in (backend_root / "app").rglob("*.py"):
        if "sqlalchemy" not in python_file.read_text(encoding="utf-8").lower():
            continue
        if allowed in python_file.parents or python_file.parent == allowed:
            continue
        violations.append(str(python_file.relative_to(backend_root)))

    assert violations == []


def test_httpx_stays_inside_http_output_adapters() -> None:
    backend_root = Path(__file__).resolve().parents[1]
    adapters_root = backend_root / "app" / "infrastructure" / "adapters" / "output"
    allowed = {
        adapters_root / "generation" / "adaptador_generacion_ollama.py",
        adapters_root / "senamhi" / "adaptador_senamhi_wis2.py",
    }
    violations: list[str] = []

    for python_file in (backend_root / "app").rglob("*.py"):
        content = python_file.read_text(encoding="utf-8")
        if "import httpx" not in content and "from httpx" not in content:
            continue
        if python_file not in allowed:
            violations.append(str(python_file.relative_to(backend_root)))

    assert violations == []


def test_chromadb_stays_inside_chroma_adapter() -> None:
    backend_root = Path(__file__).resolve().parents[1]
    allowed = backend_root / "app" / "infrastructure" / "adapters" / "output" / "chroma"
    violations: list[str] = []

    for python_file in (backend_root / "app").rglob("*.py"):
        content = python_file.read_text(encoding="utf-8")
        if "import chromadb" not in content and "from chromadb" not in content:
            continue
        if allowed in python_file.parents or python_file.parent == allowed:
            continue
        violations.append(str(python_file.relative_to(backend_root)))

    assert violations == []


def test_joblib_stays_inside_model_adapters() -> None:
    backend_root = Path(__file__).resolve().parents[1]
    permitidas = {
        backend_root / "app" / "infrastructure" / "adapters" / "output" / "clasificacion",
        backend_root / "app" / "infrastructure" / "adapters" / "output" / "riesgo",
    }
    violations: list[str] = []

    for python_file in (backend_root / "app").rglob("*.py"):
        content = python_file.read_text(encoding="utf-8")
        if "import joblib" not in content and "from joblib" not in content:
            continue
        if any(carpeta in python_file.parents or python_file.parent == carpeta for carpeta in permitidas):
            continue
        violations.append(str(python_file.relative_to(backend_root)))

    assert violations == []
