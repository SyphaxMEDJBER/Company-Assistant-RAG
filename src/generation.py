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
    "Tu es un assistant interne qui aide les employes de NovaTech Solutions "
    "a partir des documents fournis. Reponds UNIQUEMENT a partir des passages "
    "ci-dessous. Si l'information ne s'y trouve pas, dis clairement que tu ne "
    "sais pas, n'invente rien. Reponds de facon claire et directe, sans "
    "mentionner toi-meme tes sources."
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
    answer = response["message"]["content"]

    return f"{answer}\n\nSource(s) : {_format_sources(relevant_chunks)}"


if __name__ == "__main__":
    question = "j'ai perdu mon telephone professionnel, que dois-je faire ?"
    print(generate_answer(question))
