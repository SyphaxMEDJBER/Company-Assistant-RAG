import re
from dataclasses import dataclass
from pathlib import Path

SECTION_PATTERN = re.compile(r"^## (.+)$", re.MULTILINE)


@dataclass
class Chunk:
    text: str
    source: str
    document_title: str
    section: str


def _extract_title(content: str) -> str:
    first_line = content.strip().splitlines()[0]
    return first_line.lstrip("# ").strip()


def chunk_markdown_document(content: str, source: str) -> list[Chunk]:
    """Découpe un document Markdown en chunks, un par section de niveau 2 (##).

    Chaque chunk est préfixé par le titre du document (H1) pour rester
    compréhensible même une fois extrait de son contexte d'origine.
    """
    document_title = _extract_title(content)
    matches = list(SECTION_PATTERN.finditer(content))

    chunks: list[Chunk] = []

    preamble = content[: matches[0].start()] if matches else content
    preamble_body = "\n".join(
        line for line in preamble.splitlines() if not line.startswith("# ")
    ).strip()
    if preamble_body:
        chunks.append(
            Chunk(
                text=f"# {document_title}\n## Métadonnées\n{preamble_body}",
                source=source,
                document_title=document_title,
                section="Métadonnées",
            )
        )

    for i, match in enumerate(matches):
        section_title = match.group(1).strip()
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(content)
        section_body = content[start:end].strip()
        chunks.append(
            Chunk(
                text=f"# {document_title}\n## {section_title}\n{section_body}",
                source=source,
                document_title=document_title,
                section=section_title,
            )
        )

    return chunks


def chunk_documents_dir(documents_dir: Path) -> list[Chunk]:
    chunks: list[Chunk] = []
    for md_file in sorted(documents_dir.glob("*.md")):
        content = md_file.read_text(encoding="utf-8")
        chunks.extend(chunk_markdown_document(content, source=md_file.name))
    return chunks
