from unittest.mock import patch

from src.generation import NO_RELEVANT_INFO_MESSAGE, generate_answer

FAKE_RELEVANT_CHUNK = {
    "text": "# Politique de test\n## Section\nContenu factice.",
    "source": "test.md",
    "document_title": "Politique de test",
    "section": "Section",
    "distance": 0.3,  # en dessous du seuil (0.6) : considere pertinent
}

FAKE_IRRELEVANT_CHUNK = {
    **FAKE_RELEVANT_CHUNK,
    "distance": 0.9,  # au dessus du seuil : considere non pertinent
}


@patch("src.generation.ollama.chat")
@patch("src.generation.retrieve")
def test_generate_answer_skips_ollama_when_no_relevant_chunk(mock_retrieve, mock_chat):
    mock_retrieve.return_value = [FAKE_IRRELEVANT_CHUNK]

    result = generate_answer("question hors sujet")

    assert result == NO_RELEVANT_INFO_MESSAGE
    mock_chat.assert_not_called()  # le point cle : le LLM n'a jamais ete appele


@patch("src.generation.ollama.chat")
@patch("src.generation.retrieve")
def test_generate_answer_uses_ollama_response_and_cites_source(mock_retrieve, mock_chat):
    mock_retrieve.return_value = [FAKE_RELEVANT_CHUNK]
    mock_chat.return_value = {"message": {"content": "Reponse factice du LLM."}}

    result = generate_answer("question dans le sujet")

    assert "Reponse factice du LLM." in result
    assert "Politique de test" in result  # la citation, ajoutee par le code
