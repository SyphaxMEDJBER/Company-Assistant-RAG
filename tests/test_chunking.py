from src.chunking import chunk_markdown_document

SAMPLE_DOCUMENT = """# Guide de Test

**Reference** : TEST-001

## 1. Premiere section
Contenu de la premiere section.

## 2. Deuxieme section
Contenu de la deuxieme section.
"""


def test_chunk_markdown_document_returns_one_chunk_per_section():
    chunks = chunk_markdown_document(SAMPLE_DOCUMENT, source="test.md")

    # 3 chunks attendus : le preambule (Reference) + les 2 sections "##".
    assert len(chunks) == 3


def test_chunk_markdown_document_extracts_correct_section_titles():
    chunks = chunk_markdown_document(SAMPLE_DOCUMENT, source="test.md")

    sections = [c.section for c in chunks]
    assert sections == ["Métadonnées", "1. Premiere section", "2. Deuxieme section"]


def test_chunk_markdown_document_prefixes_each_chunk_with_document_title():
    chunks = chunk_markdown_document(SAMPLE_DOCUMENT, source="test.md")

    for chunk in chunks:
        assert chunk.text.startswith("# Guide de Test")
