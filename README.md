# Company Assistant RAG

Assistant RAG (Retrieval-Augmented Generation) qui répond aux questions des employés à partir de documents internes fictifs d'entreprise (sécurité IT, gestion des incidents, VPN, onboarding, mots de passe, perte de matériel).

## Pourquoi un RAG "souverain" (100% local) ?

Ce projet utilise **Ollama en local**, volontairement, sans aucune API LLM externe (pas d'OpenAI, pas de Groq). Dans un contexte d'entreprise où les documents indexés sont sensibles (procédures de sécurité, accès VPN, gestion des mots de passe...), envoyer ces contenus à un service tiers pour générer une réponse pose un problème de confidentialité et de conformité. En gardant tout le pipeline — embeddings, base vectorielle, génération — sur l'infrastructure locale, aucune donnée ne sort jamais. C'est ce qu'on appelle un RAG souverain.

## Architecture

```
Question employé
      │
      ▼
[1] Embedding de la question (Sentence-Transformers)
      │
      ▼
[2] Recherche de similarité dans ChromaDB → top-k passages pertinents
      │
      ▼
[3] Construction du prompt (question + passages + instructions)
      │
      ▼
[4] Génération de la réponse par Ollama (LLM local)
      │
      ▼
Réponse + citation du/des document(s) source
```

## Stack

- **Corpus** : documents Markdown fictifs mais réalistes
- **Embeddings** : Sentence-Transformers
- **Base *vectorielle* : ChromaDB
- **LLM** : Ollama (local)
- **Interface** : Streamlit
- **Conteneurisation** : Docker
- **CI/CD** : GitHub Actions

## Statut du projet

Construit étape par étape, une branche Git par étape (voir historique des commits). Ce README sera complété au fur et à mesure (installation, lancement, structure du repo).
