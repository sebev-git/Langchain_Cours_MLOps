# Langchain_Cours_MLOps

## Résumé Chapitre 3 : Traitement de Documents

Dans ce chapitre, nous avons construit une première boîte à outils documentaire pour manipuler efficacement des fichiers longs et variés avec un LLM.

1. Chargement des documents (Loaders)
    - PDF, TXT, Markdown, Web.
    - Conversion en objets Document standardisés (contenu + métadonnées).

2. Nettoyage du texte
    - Suppression des artefacts (numéros de pages, espaces multiples, pages vides).
    - Normalisation des textes avant découpage.

3. Découpage en chunks (Text Splitters)
    - Segmentation par phrases.
    - Chunks d’environ 600 tokens.
    - Overlap (recouvrement) de 2 phrases pour conserver le contexte.

4. Recherche simple
    - Implémentation d’une recherche par mots-clés dans les chunks.
    - Résultats présentés sous forme de snippets pertinents.
    - Alternative légère au RAG, sans base vectorielle.

5. Exposition en Tools LangChain
    - Conversion des fonctions (load, clean, split, search) en outils avec @tool.
    - Préparation à l’intégration dans un agent (Chapitre 5).

👉 Ce chapitre fournit un pipeline complet de traitement de documents : charger → nettoyer → découper → rechercher.
C’est la base indispensable pour exploiter de longs contenus avec un assistant conversationnel.

## Summary Chapter 3: Document Processing

In this chapter, we built our first document processing toolkit to handle long and diverse files efficiently with an LLM.

1. Loading Documents (Loaders)
    - PDF, TXT, Markdown, Web.
    - Conversion into standardized Document objects (content + metadata).

2. Text Cleaning
    - Removal of artefacts (page numbers, multiple spaces, empty pages).
    - Normalization of text before chunking.

3. Chunking
    - Segmentation by sentences.
    - Chunks of approximately 600 tokens.
    - Overlap of 2 sentences to preserve context.
    
4. Simple Search
    - Keyword-based search across chunks.
    - Returns relevant snippets.
    - Lightweight alternative to RAG, no vector DB needed.

5. LangChain Tools
    - Converted functions (load, clean, split, search) into @tool.
    - Ready for agent integration (Chapter 5).

👉 This chapter provides a complete document pipeline: load → clean → split → search.
It forms the foundation for working with long documents in a conversational assistant.