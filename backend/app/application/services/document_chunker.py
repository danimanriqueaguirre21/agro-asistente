from dataclasses import dataclass

from app.domain.entities.knowledge_document import KnowledgeDocument


def make_chunk_id(content_hash: str, chunk_index: int) -> str:
    """Identificador determinista: mismo hash e índice producen el mismo id."""
    return f"{content_hash}:chunk:{chunk_index:04d}"


@dataclass(frozen=True)
class DocumentChunk:
    chunk_id: str
    document_id: str
    content_hash: str
    chunk_index: int
    content: str
    title: str
    topic: str
    source_path: str


class DocumentChunker:
    """División simple de Markdown en fragmentos. No es chunking semántico avanzado."""

    def __init__(self, max_chars: int = 500) -> None:
        if max_chars < 1:
            raise ValueError("El tamaño de fragmento debe ser positivo")
        self._max_chars = max_chars

    def chunk(self, content: str, document: KnowledgeDocument) -> list[DocumentChunk]:
        parts = split_markdown(content, self._max_chars)
        chunks: list[DocumentChunk] = []
        content_hash = document.content_hash.value
        for index, part in enumerate(parts):
            chunks.append(
                DocumentChunk(
                    chunk_id=make_chunk_id(content_hash, index),
                    document_id=document.id,
                    content_hash=content_hash,
                    chunk_index=index,
                    content=part,
                    title=document.title,
                    topic=document.topic,
                    source_path=document.source_path,
                )
            )
        return chunks


def split_markdown(content: str, max_chars: int) -> list[str]:
    text = (content or "").replace("\r\n", "\n").strip()
    if not text:
        return []

    paragraphs = [item.strip() for item in text.split("\n\n") if item.strip()]
    chunks: list[str] = []
    current = ""
    for paragraph in paragraphs:
        pieces = _split_long_text(paragraph, max_chars)
        for piece in pieces:
            if not current:
                current = piece
                continue
            candidate = f"{current}\n\n{piece}"
            if len(candidate) <= max_chars:
                current = candidate
            else:
                chunks.append(current)
                current = piece
    if current:
        chunks.append(current)
    return chunks


def _split_long_text(text: str, max_chars: int) -> list[str]:
    if len(text) <= max_chars:
        return [text]
    pieces: list[str] = []
    remaining = text
    while remaining:
        if len(remaining) <= max_chars:
            pieces.append(remaining)
            break
        window = remaining[:max_chars]
        split_at = window.rfind(" ")
        if split_at < max_chars // 2:
            split_at = max_chars
        pieces.append(remaining[:split_at].strip())
        remaining = remaining[split_at:].strip()
    return [piece for piece in pieces if piece]
