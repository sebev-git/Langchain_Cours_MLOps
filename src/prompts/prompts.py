''' Avant le formatage de sortie
from langchain_core.prompts import ChatPromptTemplate

# 1) Content classification
classification_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an assistant that analyzes text and suggests a relevant category."),

    ("human", "Text: 'The neural network was trained on medical images.'"),
    ("ai", "AI"),

    ("human", "Text: 'We stored patient data on a Hadoop cluster.'"),
    ("ai", "Databases"),

    ("human", "Text: 'AWS provides computing and storage services.'"),
    ("ai", "Cloud"),

    ("human", "Text: {input}")
])
'''

from langchain_core.prompts import ChatPromptTemplate

classification_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an assistant that suggests a relevant category for a text."),

    # Few-shot
    ("human", 
     "Text: 'Deep neural networks are revolutionizing machine learning.'"),
    ("ai", '{{"category": "Artificial Intelligence", "confidence": 0.95}}'),

    ("human", 
     "Text: 'Docker and Kubernetes make it easier to deploy applications in the cloud.'"),
    ("ai", '{{"category": "Cloud", "confidence": 0.9}}'),

    # General instruction
    ("human",
     "Analyze the following text and propose ONLY one suitable category:\n\n"
     "Text: {input}\n\n"
     "{format_instructions}")    # <------ HERE
])