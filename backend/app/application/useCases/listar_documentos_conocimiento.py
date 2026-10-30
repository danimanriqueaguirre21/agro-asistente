from app.domain.ports.input.incorporar_conocimiento_port import (
    PuertoListarDocumentosConocimiento,
    ResultadoDocumentoConocimiento,
    documento_a_resultado,
)
from app.domain.ports.output.repositorio_documento_conocimiento_port import (
    PuertoRepositorioDocumentoConocimiento,
)


class ListarDocumentosConocimiento(PuertoListarDocumentosConocimiento):
    def __init__(self, repositorio_conocimiento: PuertoRepositorioDocumentoConocimiento) -> None:
        self._repositorio_conocimiento = repositorio_conocimiento

    def ejecutar(self) -> list[ResultadoDocumentoConocimiento]:
        documentos = self._repositorio_conocimiento.listar_todos()
        return [documento_a_resultado(documento, estado="registered") for documento in documentos]
