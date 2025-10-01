# Langchain_Cours_MLOps

## Version française

Dans ce premier chapitre, nous avons posé les bases pour travailler avec LangChain et amorcer la construction d’un assistant intelligent.

1. Environnement de travail
    - Mise en place d’une arborescence claire (src/, data/, etc.).
    - Gestion des dépendances avec uv et configuration via pyproject.toml.
    - Création d’un environnement reproductible et isolé.

2. Composants fondamentaux de LangChain
    - Utilisation de LiteLLM pour appeler différents modèles (Groq, GPT, Claude…) avec fallback automatique.
    - Introduction aux Messages :
        - **SystemMessage** (rôle du modèle),
        - **HumanMessage** (demande utilisateur),
        - **AIMessage** (réponse générée).

3. Interface Runnable
    - ``.invoke()`` : exécution simple.
    - ``.batch()`` : exécution en parallèle.
    - ``.stream()`` : génération en continu (streaming).
    - ``.with_retry()`` : robustesse avec relance automatique.

4. Création de Tools personnalisés
    - Implémentation de ``word_count`` (compte de mots) et ``char_count`` (compte de caractères).
    - Découverte du décorateur @tool pour exposer des fonctions au modèle.

5. Première application pratique
    - Combinaison d’un modèle (ChatLiteLLM), de messages et de tools.
    - Analyse des réponses du LLM avec nos outils personnalisés.

👉 En résumé, nous avons construit les fondations de LangChain : Messages, Runnables et Tools. Ces briques serviront de socle pour développer un assistant complet dans les chapitres suivants.

## English version

In this first chapter, we laid the foundations to work with LangChain and start building an intelligent assistant.

1. Environment setup
    - Setting up a clear directory structure (src/, data/, etc.).
    - Managing dependencies
    - Creating a reproducible and isolated environment.

2. Fundamental components of LangChain
    - Using LiteLLM to call different models (Groq, GPT, Claude…) with automatic fallback.
    - Introduction to Messages :
        - **SystemMessage** (role of the model),
        - **HumanMessage** (user request),
        - **AIMessage** (generated response).

3. Runnable interface
    - ``.invoke()`` : simple execution.
    - ``.batch()`` : parallel execution.
    - ``.stream()`` : continuous generation (streaming).
    - ``.with_retry()`` : robustness with automatic retry.

4. Creating custom Tools
    - Implementation of ``word_count`` (word count) and ``char_count`` (character count).
    - Discovery of the @tool decorator to expose functions to the model.

5. First practical application
    - Combination of a model (ChatLiteLLM), messages and tools.
    - Analysis of the LLM responses with our custom tools.

👉 In short, we built the core building blocks of LangChain: Messages, Runnables, and Tools. These foundations will support the development of a complete assistant in the next chapters.

