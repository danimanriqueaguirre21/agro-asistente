from dataclasses import dataclass

from app.domain.entities.documento_conocimiento import DocumentoConocimiento


def crear_id_fragmento(hash_contenido: str, indice_fragmento: int) -> str:
    """Identificador determinista: mismo hash e índice producen el mismo id."""
    return f"{hash_contenido}:chunk:{indice_fragmento:04d}"


@dataclass(frozen=True)
class FragmentoDocumento:
    fragmento_id: str
    documento_id: str
    hash_contenido: str
    indice_fragmento: int
    contenido: str
    titulo: str
    tema: str
    ruta_origen: str


class FragmentadorDocumentos:
    """División simple de Markdown en fragmentos. No es chunking semántico avanzado."""

    def __init__(self, max_chars: int = 500) -> None:
        if max_chars < 1:
            raise ValueError("El tamaño de fragmento debe ser positivo")
        self._max_chars = max_chars

    def fragmentar(
        self, contenido: str, documento: DocumentoConocimiento
    ) -> list[FragmentoDocumento]:
        partes = dividir_markdown(contenido, self._max_chars)
        fragmentos: list[FragmentoDocumento] = []
        hash_contenido = documento.hash_contenido.value
        for indice, parte in enumerate(partes):
            fragmentos.append(
                FragmentoDocumento(
                    fragmento_id=crear_id_fragmento(hash_contenido, indice),
                    documento_id=documento.id,
                    hash_contenido=hash_contenido,
                    indice_fragmento=indice,
                    contenido=parte,
                    titulo=documento.titulo,
                    tema=documento.tema,
                    ruta_origen=documento.ruta_origen,
                )
            )
        return fragmentos


def dividir_markdown(contenido: str, max_chars: int) -> list[str]:
    texto = (contenido or "").replace("\r\n", "\n").strip()
    if not texto:
        return []

    parrafos = [item.strip() for item in texto.split("\n\n") if item.strip()]
    fragmentos: list[str] = []
    actual = ""
    for parrafo in parrafos:
        piezas = _dividir_texto_largo(parrafo, max_chars)
        for pieza in piezas:
            if not actual:
                actual = pieza
                continue
            candidato = f"{actual}\n\n{pieza}"
            if len(candidato) <= max_chars:
                actual = candidato
            else:
                fragmentos.append(actual)
                actual = pieza
    if actual:
        fragmentos.append(actual)
    return fragmentos


def _dividir_texto_largo(texto: str, max_chars: int) -> list[str]:
    if len(texto) <= max_chars:
        return [texto]
    piezas: list[str] = []
    restante = texto
    while restante:
        if len(restante) <= max_chars:
            piezas.append(restante)
            break
        ventana = restante[:max_chars]
        corte = ventana.rfind(" ")
        if corte < max_chars // 2:
            corte = max_chars
        piezas.append(restante[:corte].strip())
        restante = restante[corte:].strip()
    return [pieza for pieza in piezas if pieza]
