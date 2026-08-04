import re
import sys

import ollama

from src.config import GENERATION_MODEL_NAME, RELEVANCE_THRESHOLD
from src.retrieval import retrieve

NO_RELEVANT_INFO_MESSAGE = (
    "Je n'ai pas trouve d'information pertinente dans les documents internes "
    "pour repondre a cette question."
)

# Contraint le LLM à rester fidèle aux passages fournis (pas de connaissance
# externe) et à ne pas gérer lui-même la citation, qu'on ajoute en code juste
# après pour plus de fiabilité (voir _format_sources).
SYSTEM_PROMPT = (
    "Tu es l'assistant interne IT de NovaTech Solutions. Tu reponds aux "
    "questions des employes UNIQUEMENT a partir des passages de "
    "documentation fournis ci-dessous - jamais avec tes connaissances "
    "generales.\n\n"
    "Si les passages ne couvrent pas la question, en totalite ou en partie, "
    "dis-le clairement. Ne devine et n'invente RIEN : pas d'etape, de menu, "
    "de bouton ou de procedure qui n'est pas ecrit noir sur blanc dans les "
    "passages.\n\n"
    "Reponds en francais, de maniere directe et naturelle. N'ecris jamais "
    "les mots 'passage'/'passage N', ni le nom d'un document, dans ta "
    "reponse.\n\n"
    "Termine TOUJOURS par une derniere ligne exacte :\n"
    "PASSAGES_UTILISES: n,n,n (les numeros des passages dont une "
    "information a vraiment ete reprise dans ta reponse ; si aucun n'a "
    "servi, ecris PASSAGES_UTILISES: aucun)."
)


def _build_user_prompt(question: str, chunks: list[dict]) -> str:
    passages = "\n\n".join(
        f"[Passage {i + 1} - {c['document_title']}, {c['section']}]\n{c['text']}"
        for i, c in enumerate(chunks)
    )
    return f"{passages}\n\nQuestion : {question}"


def _format_sources(chunks: list[dict]) -> str:
    # Dédoublonne en gardant l'ordre d'apparition (donc du plus pertinent
    # au moins pertinent, puisque `chunks` est déjà trié par distance).
    seen = []
    for c in chunks:
        if c["document_title"] not in seen:
            seen.append(c["document_title"])
    return ", ".join(seen)


_USED_PASSAGES_PATTERN = re.compile(
    r"PASSAGES?_UTILIS\w*\s*:\s*(aucun|[\d,\s]+)", re.IGNORECASE
)


def _extract_used_chunks(raw_answer: str, chunks: list[dict]) -> tuple[str, list[dict]]:
    """Separe le texte de reponse de la ligne technique PASSAGES_UTILISES.

    Renvoie (reponse nettoyee, chunks reellement designes par le LLM). Si la
    ligne est absente ou invalide (le LLM peut l'oublier), on retombe sur
    tous les chunks pertinents plutot que de planter.
    """
    match = _USED_PASSAGES_PATTERN.search(raw_answer)
    if not match:
        return raw_answer.strip(), chunks

    clean_answer = raw_answer[: match.start()].strip()
    value = match.group(1).strip().lower()

    if value == "aucun":
        return clean_answer, []

    numbers = [int(n) for n in re.findall(r"\d+", value)]
    used_chunks = [chunks[n - 1] for n in numbers if 1 <= n <= len(chunks)]

    return clean_answer, used_chunks or chunks


def generate_answer(question: str, top_k: int = 5) -> str:
    chunks = retrieve(question, top_k=top_k)

    # Garde-fou : le retrieval renvoie toujours top_k résultats, pertinents ou
    # non. On ne garde que les chunks individuellement assez proches ; s'il
    # n'en reste aucun, on n'appelle même pas le LLM.
    relevant_chunks = [c for c in chunks if c["distance"] <= RELEVANCE_THRESHOLD]
    if not relevant_chunks:
        return NO_RELEVANT_INFO_MESSAGE

    response = ollama.chat(
        model=GENERATION_MODEL_NAME,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": _build_user_prompt(question, relevant_chunks)},
        ],
        options={"temperature": 0.2},
    )
    answer, used_chunks = _extract_used_chunks(response["message"]["content"], relevant_chunks)
    if not used_chunks:
        return answer

    return f"{answer}\n\nSource(s) : {_format_sources(used_chunks)}"


if __name__ == "__main__":
    # Permet de tester une question au choix : `python -m src.generation <question>`.
    # Sans argument, retombe sur une question par défaut.
    default_question = "j'ai perdu mon telephone professionnel, que dois-je faire ?"
    question = " ".join(sys.argv[1:]) or default_question
    print(generate_answer(question))
