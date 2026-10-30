"""Preprocesamiento del prototipo HU-08.

Convierte ausencias a NaN y deja la imputación a los imputadores del pipeline.
No rellena con cero y no descarta filas.
"""

from __future__ import annotations

import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

ORDEN_VARIABLES = (
    "familia_escenario",
    "cultivo",
    "region",
    "etapa_fenologica",
    "temperatura_c",
    "precipitacion_mm",
    "dias_sin_lluvia",
    "sintoma_observado",
    "proporcion_afectada",
    "condicion_suelo",
)
NUMERICAS_CON_AUSENCIA = ("temperatura_c", "precipitacion_mm")
NUMERICAS_COMPLETAS = ("dias_sin_lluvia", "proporcion_afectada")
ETIQUETA = "nivel_riesgo"
NIVELES = ("bajo", "medio", "alto")


def marcar_ausentes(matriz: np.ndarray) -> np.ndarray:
    """Representa JSON null como NaN. No imputa un número."""
    salida = np.array(matriz, dtype=object, copy=True)
    if salida.ndim != 2 or salida.shape[1] != len(ORDEN_VARIABLES):
        raise ValueError(
            "Se esperaban "
            f"{len(ORDEN_VARIABLES)} variables en este orden: {', '.join(ORDEN_VARIABLES)}."
        )
    for fila in range(salida.shape[0]):
        for columna in range(salida.shape[1]):
            valor = salida[fila, columna]
            if isinstance(valor, (bool, np.bool_)):
                salida[fila, columna] = "true" if bool(valor) else "false"
            elif valor is None:
                salida[fila, columna] = np.nan
            elif isinstance(valor, str) and not valor.strip():
                salida[fila, columna] = np.nan
    return salida


def construir_columnas(escalar_numericas: bool) -> ColumnTransformer:
    transformadores = []
    for nombre in ORDEN_VARIABLES:
        indice = [ORDEN_VARIABLES.index(nombre)]
        if nombre in NUMERICAS_CON_AUSENCIA:
            pasos: list[tuple[str, object]] = [
                ("imputar", SimpleImputer(strategy="median", add_indicator=True)),
            ]
            if escalar_numericas:
                pasos.append(("escalar", StandardScaler()))
            transformadores.append((nombre, Pipeline(pasos), indice))
        elif nombre in NUMERICAS_COMPLETAS:
            pasos = [("imputar", SimpleImputer(strategy="median"))]
            if escalar_numericas:
                pasos.append(("escalar", StandardScaler()))
            transformadores.append((nombre, Pipeline(pasos), indice))
        else:
            transformadores.append(
                (
                    nombre,
                    Pipeline(
                        [
                            ("imputar", SimpleImputer(strategy="most_frequent")),
                            (
                                "codificar",
                                OneHotEncoder(
                                    handle_unknown="ignore",
                                    sparse_output=False,
                                ),
                            ),
                        ]
                    ),
                    indice,
                )
            )
    return ColumnTransformer(transformadores, remainder="drop", verbose_feature_names_out=True)
