import os

import pytest

from app.domain.ports.output.puerto_observaciones_meteorologicas import (
    FiltroObservacionesMeteorologicas,
)
from app.infrastructure.adapters.output.senamhi.adaptador_senamhi_wis2 import (
    AdaptadorSenamhiWis2,
)
from app.infrastructure.config.settings import Settings


@pytest.mark.integration
@pytest.mark.skipif(
    os.environ.get("SENAMHI_WIS2_INTEGRATION") != "1",
    reason="Requiere Internet y SENAMHI WIS2. Ejecutar con SENAMHI_WIS2_INTEGRATION=1.",
)
def test_senamhi_wis2_obtener_recientes_real() -> None:
    settings = Settings(_env_file=None)
    adaptador = AdaptadorSenamhiWis2(
        base_url=settings.senamhi_wis2_base_url,
        coleccion=settings.senamhi_wis2_collection,
        timeout_seconds=settings.senamhi_wis2_timeout_seconds,
    )
    observaciones = adaptador.obtener_recientes(
        FiltroObservacionesMeteorologicas(limite=8, orden="-reportTime")
    )
    assert observaciones
    primera = observaciones[0]
    assert primera.identificador_estacion
    assert primera.fecha_hora
    assert primera.nombre_estacion is None or isinstance(primera.nombre_estacion, str)
