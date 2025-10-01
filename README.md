# Langchain_Cours_MLOps

## Résumé Chapitre 4 : État et Mémoire

Dans ce chapitre, nous avons appris à rendre notre assistant stateful (avec état), capable de se souvenir du contexte d’une conversation et de le réutiliser.

1. Problème du stateless
    - Par défaut, un LLM ne se souvient pas des échanges précédents.
    - Cela limite fortement l’expérience utilisateur dans un chatbot ou un agent.

2. Historiques de conversation
    - **InMemoryChatMessageHistory** : stockage en RAM, simple mais non persistant. 
    - **FileChatMessageHistory** : stockage en JSON local, persistant entre redémarrages.  
    - **SQLChatMessageHistory** : stockage en base SQL, adapté au multi-utilisateurs.

3. Gestion de sessions multi-utilisateurs
    - Mise en place d’un SessionManager qui attribue un session_id unique à chaque utilisateur.
    - Chaque utilisateur conserve son propre historique, isolé des autres.

4. RunnableWithMessageHistory
    - Intégration automatique de l’historique dans le prompt.
    - Ajout des nouveaux échanges (humain / IA) directement en mémoire. 
    - Simplifie la gestion de conversations persistantes.

5. Optimisation de la mémoire
    - Problème : un historique complet devient coûteux (tokens, latence, budget).
    - Solution : un wrapper de résumé automatique (SummarizedHistoryWrapper) qui :
        - Utilise l’historique brut tant qu’il reste court.
        - Génère un résumé lorsque l’historique devient trop long.

👉 Grâce à ces briques, nous avons désormais un assistant conversationnel robuste, persistant et scalable, capable de gérer plusieurs utilisateurs et de conserver les informations clés dans la durée.

## Summary Chapter 4: State & Memory

In this chapter, we have learned how to make our assistant stateful (with state), capable of remembering the context of a conversation and reusing.

1. Problem of stateless
    - By default, an LLM does not remember the previous exchanges.
    - This limits the user experience in a chatbot or an agent.

2. Conversation history
    - **InMemoryChatMessageHistory** : in-memory storage, simple but not persistent.
    - **FileChatMessageHistory** : local JSON storage, persistent between restarts.
    - **SQLChatMessageHistory** : SQL-based storage, adapted for multi-user scenarios.

3. Managing multi-user sessions
    - Setting up a SessionManager that assigns a unique session_id to each user.
    - Each user retains their own history, isolated from others.

4. RunnableWithMessage
    - Automatically injects conversation history into prompts.
    - Logs new exchanges (human / AI) directly into memory.
    - Simplifies the management of persistent conversations.

5. Memory optimization
    - Problem: full history grows costly (tokens, latency, budget).
    - Solution: a summarization wrapper (SummarizedHistoryWrapper) that: 
        - Uses the raw history as long as it remains short.
        - Generates a summary when the history becomes too long.

👉 With these components, we now have a robust, persistent, and scalable conversational assistant, able to manage multiple users and retain key details over long interactions.