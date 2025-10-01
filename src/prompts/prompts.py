from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# Classification 
classification_prompt = ChatPromptTemplate.from_messages([
    ("system", "Tu es un assistant qui propose une catégorie pertinente pour un texte."),
    
    # Few-shot
    ("human", 
     "Texte : 'Les réseaux de neurones profonds révolutionnent l'apprentissage automatique.'"),
    ("ai", '{{"category": "Intelligence Artificielle", "confidence": 0.95}}'),
    
    ("human", 
     "Texte : 'Docker et Kubernetes facilitent le déploiement d’applications dans le cloud.'"),
    ("ai", '{{"category": "Cloud", "confidence": 0.9}}'),
    
    # Instruction générale
    ("human",
     "Analyse le texte suivant et propose UNIQUEMENT une seule catégorie adaptée :\n\n"
     "Texte : {input}\n\n"
     "{format_instructions}")
])

# Résumé 
summary_prompt = ChatPromptTemplate.from_messages([
    ("system", "Tu es un assistant qui résume des textes en reprenant les mots importants du texte d'origine."),
    
    # Instruction générale
    ("human", 
     "Résume le texte suivant et veille à garder les mots clés les plus importants.\n\n"
     "IMPORTANT : Réponds UNIQUEMENT avec un JSON valide, sans texte en dehors du JSON.\n\n"
     "Texte : {input}\n\n"
     "{format_instructions}")
])

# Traduction
translation_prompt = ChatPromptTemplate.from_messages([
    ("system", "Tu es un traducteur professionnel."),
    
    # Few-shot
    ("human", "Texte : 'Bonjour, comment vas-tu ?'"),
    ("ai", '{{"translated_text": "Hello, how are you?"}}'),
    
    # Instruction générale
    ("human", 
     "Traduis ce texte en anglais : {input}\n\n"
     "{format_instructions}")
])

chat_prompt = ChatPromptTemplate.from_messages([
    ("system", "Tu es un assistant conversationnel utile et amical."),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}")
])