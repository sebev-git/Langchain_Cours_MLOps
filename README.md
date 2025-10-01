# Langchain_Cours_MLOps

## Version française

Ce dépôt contient l’ensemble du code et des ressources nécessaires pour suivre le cours sur LangChain & MLOps.
Vous y trouverez :

```txt
.
├── Makefile
├── README.md
├── pyproject.toml
├── data
│   ├── md
│   ├── pdf
│   │   ├── 1.pdf
│   │   ├── 2.pdf
│   │   └── 3.pdf
│   └── txt
└── src
    ├── app.py                  # Point d’entrée de l’application
    ├── chap1_fund_components.py  # Chapitre 1 : composants fondamentaux
    ├── chap2_prompt_output.py    # Chapitre 2 : prompts & output parsers
    ├── chap3_docs.py             # Chapitre 3 : gestion des documents
    ├── chap4_memory.py           # Chapitre 4 : gestion de la mémoire
    ├── agents
    │   └── doc_agent.py        # Agent documentaire
    ├── api
    │   └── main.py             # API FastAPI (analyse, tests, chat, etc.)
    ├── core
    │   ├── chains.py           # Chaînes LangChain (analyse, test, chat…)
    │   ├── llm.py              # Configuration du modèle LLM
    │   ├── parsers.py          # Output parsers structurés
    │   └── tools.py            # Outils génériques
    ├── documents
    │   ├── cleaners.py         # Nettoyage des documents
    │   ├── loaders.py          # Chargement des documents
    │   ├── search.py           # Recherche dans les documents
    │   ├── splitters.py        # Découpage en chunks
    │   └── tools.py            # Outils spécifiques aux documents
    ├── memory
    │   ├── memory.py           # Gestion mémoire / historique
    │   └── session.py          # Sessions multi-utilisateurs
    ├── prompts
    │   └── prompts.py          # Prompts structurés
    └── utils
        └── token.py            # Gestion des tokens
```

👉 **Important** : les fichiers de ce dépôt sont une base. Ils sont destinés à être modifiés, enrichis et adaptés au fur et à mesure que vous progressez dans le cours. Chaque chapitre introduit de nouvelles fonctionnalités que vous implémenterez directement dans ces fichiers.

## English version

This repository contains all the code and resources needed to follow the LangChain & MLOps course.
You will find:

```txt
.
├── Makefile
├── README.md
├── pyproject.toml
├── data
│   ├── md
│   ├── pdf
│   │   ├── 1.pdf
│   │   ├── 2.pdf
│   │   └── 3.pdf
│   └── txt
└── src
    ├── app.py                  # Application entry point
    ├── chap1_fund_components.py  # Chapter 1: fundamental components
    ├── chap2_prompt_output.py    # Chapter 2: prompts & output parsers
    ├── chap3_docs.py             # Chapter 3: document management
    ├── chap4_memory.py           # Chapter 4: memory management
    ├── agents
    │   └── doc_agent.py        # Documentation agent
    ├── api
    │   └── main.py             # FastAPI backend (analysis, tests, chat, etc.)
    ├── core
    │   ├── chains.py           # LangChain chains (analysis, test, chat…)
    │   ├── llm.py              # LLM model configuration
    │   ├── parsers.py          # Structured output parsers
    │   └── tools.py            # General utilities
    ├── documents
    │   ├── cleaners.py         # Document cleaning
    │   ├── loaders.py          # Document loading
    │   ├── search.py           # Document search
    │   ├── splitters.py        # Splitting into chunks
    │   └── tools.py            # Document-specific tools
    ├── memory
    │   ├── memory.py           # Memory / history management
    │   └── session.py          # Multi-user session management
    ├── prompts
    │   └── prompts.py          # Structured prompts
    └── utils
        └── token.py            # Token management
```

👉 **Important**: the files in this repository are a starting point. They are meant to be modified, expanded, and adapted as you progress through the course. Each chapter introduces new features that you will implement directly in these files.