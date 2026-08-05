# Company Assistant RAG

![Tests](https://github.com/SyphaxMEDJBER/Company-Assistant-RAG/actions/workflows/tests.yml/badge.svg)
![CD](https://github.com/SyphaxMEDJBER/Company-Assistant-RAG/actions/workflows/docker-publish.yml/badge.svg)

Assistant RAG (Retrieval-Augmented Generation) qui répond aux questions des employés à partir de
documents internes d'entreprise : découpage et indexation vectorielle des documents, recherche
sémantique, génération de réponse par un LLM local (Ollama) avec citation de la source, interface
Streamlit, tests automatisés, containerisation Docker et pipeline CI/CD (GitHub Actions).

Corpus : 6 documents Markdown fictifs mais réalistes pour une entreprise fictive (NovaTech
Solutions) — politique de sécurité IT, gestion des incidents, guide VPN/accès distant, onboarding
IT, gestion des mots de passe, procédure de perte de matériel.

## Sommaire

- [Pipeline](#pipeline)
- [Pourquoi un RAG "souverain" (100% local)](#pourquoi-un-rag-souverain-100-local)
- [Limites connues](#limites-connues)
- [Stack technique](#stack-technique)
- [Structure du projet](#structure-du-projet)
- [Installation et utilisation](#installation-et-utilisation)
- [Tests](#tests)
- [Docker](#docker)
- [CI/CD](#cicd)

## Pipeline

1. **Corpus & découpage** — les documents Markdown sont découpés en chunks (un par section `##`),
   chacun préfixé par le titre du document pour rester compréhensible isolément (`src/chunking.py`).
2. **Indexation vectorielle** — chaque chunk est transformé en embedding (Sentence-Transformers,
   modèle multilingue) et stocké dans ChromaDB avec la métrique de similarité cosinus
   (`src/indexing.py`).
3. **Retrieval** — la question de l'employé est encodée avec le même modèle, puis ChromaDB renvoie
   les `top_k` chunks les plus proches (`src/retrieval.py`).
4. **Génération** — les chunks jugés pertinents (seuil de distance calibré empiriquement) sont
   injectés dans un prompt envoyé à Ollama (LLM local), qui génère une réponse fidèle aux passages
   fournis. La citation de la ou des source(s) est déterminée par un mécanisme dédié
   (`PASSAGES_UTILISES`) plutôt que laissée au LLM, pour rester fiable (`src/generation.py`).
5. **Interface** — Streamlit permet de poser une question et d'afficher la réponse + sa source
   (`app.py`).
6. **Qualité & déploiement** — tests automatisés (pytest, avec mock pour isoler la logique du vrai
   appel au LLM), containerisation (Docker Compose : app + Ollama), pipeline CI/CD (GitHub Actions)
   qui teste puis publie une image Docker à chaque push sur `main`.

## Pourquoi un RAG "souverain" (100% local)

Ce projet utilise **Ollama en local**, volontairement, sans aucune API LLM externe (pas d'OpenAI,
pas de Groq). Dans un contexte d'entreprise où les documents indexés sont sensibles (procédures de
sécurité, accès VPN, gestion des mots de passe...), envoyer ces contenus à un service tiers pour
générer une réponse pose un problème de confidentialité et de conformité. En gardant tout le
pipeline — embeddings, base vectorielle, génération — sur l'infrastructure locale, aucune donnée
ne sort jamais.

## Limites connues

Le modèle utilisé est volontairement petit, car la machine sur laquelle tourne ce projet n'est pas
assez puissante (pas de GPU) — les réponses ne sont donc pas toujours excellentes.

| Modèle | Taille | Comportement observé |
|---|---|---|
| **llama3.2:3b** (retenu) | ~2 Go | Bon compromis global ; quelques citations sur-inclusives sur certaines questions |
| qwen2.5:3b | ~2 Go | Meilleur respect du mécanisme de citation, mais peut inventer une procédure détaillée sur des questions génériques (ex : "comment activer la 2FA ?") |
| mistral:7b | ~4 Go | ❌ Fait planter la machine (8 Go de RAM, pas de GPU) — écarté définitivement |

## Stack technique

**RAG** : Python, ChromaDB, Sentence-Transformers, Ollama (llama3.2:3b)
**Interface** : Streamlit
**Qualité & déploiement** : pytest, Docker Compose, GitHub Actions

## Structure du projet

```
├── data/
│   └── documents/            # Corpus : 6 documents Markdown fictifs
├── src/
│   ├── config.py              # Chemins, modèles, seuil de pertinence
│   ├── chunking.py            # Découpage des documents en chunks
│   ├── indexing.py            # Construction de l'index ChromaDB
│   ├── retrieval.py           # Recherche des chunks pertinents (top-k)
│   └── generation.py          # Prompt, appel Ollama, citation des sources
├── tests/
│   ├── test_chunking.py       # Test unitaire (sans dépendance externe)
│   └── test_generation.py     # Tests avec mock (Ollama, retrieval)
├── .github/workflows/
│   ├── tests.yml               # CI : tests automatisés
│   └── docker-publish.yml      # CD : build + publication de l'image Docker
├── app.py                     # Interface Streamlit
├── Dockerfile
├── docker-compose.yml          # app + Ollama
└── requirements.txt
```

## Installation et utilisation

```bash
git clone https://github.com/SyphaxMEDJBER/Company-Assistant-RAG.git
cd Company-Assistant-RAG
```

### Option rapide : Docker Compose

```bash
docker compose up --build
docker compose exec ollama ollama pull llama3.2:3b   # une seule fois
```

Puis ouvrir [http://localhost:8501](http://localhost:8501). Voir [Docker](#docker) pour le détail.

### Installation manuelle

Prérequis : [Ollama](https://ollama.com/download) installé localement.

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # macOS/Linux

pip install -r requirements.txt
ollama pull llama3.2:3b
```

**1. Construire l'index vectoriel**
```bash
python -m src.indexing
```

**2. Lancer l'interface**
```bash
streamlit run app.py
```

**3. Ou interroger le RAG en ligne de commande**
```bash
python -m src.generation "j'ai oublie mon mot de passe"
```

## Tests

```bash
pytest
```

Les tests de `generation.py` utilisent `unittest.mock` pour remplacer le retrieval et l'appel à
Ollama par des réponses factices — ils vérifient ainsi la logique du code (garde-fou de
pertinence, construction de la citation) sans dépendre d'un vrai modèle ni d'un index déjà
construit, ce qui les rend exécutables de façon fiable en CI.

## Docker

```bash
docker compose up --build
```

Lance 2 conteneurs : l'application (Streamlit + RAG, index reconstruit à la fabrication de
l'image) et Ollama (image officielle, modèle à télécharger une fois via
`docker compose exec ollama ollama pull llama3.2:3b`). Communication entre les deux via le réseau
interne de Docker Compose.

## CI/CD

Deux workflows GitHub Actions, un pour la CI, un pour la CD :

- **`tests.yml` (CI)** — à chaque push et pull request : reconstruit l'index et exécute la suite
  de tests.
- **`docker-publish.yml` (CD)** — à chaque push sur `main` : construit l'image Docker et la
  publie sur GitHub Container Registry (`ghcr.io/syphaxmedjber/company-assistant-rag`), avec cache
  GitHub Actions pour accélérer les builds suivants.
