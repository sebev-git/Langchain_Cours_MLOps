''' Avant pipeline

from src.prompts.prompts import classification_prompt

text = """
Artificial intelligence is a concept coined in the mid-1950s, following the reflections of mathematician Alan Turing, 
who wondered whether a computer would one day be able to think, or if it was only capable of an imitation game.
"""

response = classification_prompt.format_messages(
    input=text
)
print("\n--- Classification Prompt ---")
print(response)
__________________________________________________________
'''
''' Avant le formatage d'output
from src.core.chains import classification_chain

text = """
Artificial intelligence is a concept coined in the mid-1950s, following the reflections of mathematician Alan Turing, 
who wondered whether a computer would one day be able to "think", or if it was only capable of an "imitation game".
"""

print("\n--- Classification Chain ---")
response = classification_chain.invoke({
    "input": text
})

print(response.content)
__________________________________________________________
'''

from src.core.parsers import classification_parser
from src.core.chains import classification_chain

text = """
Artificial intelligence is a concept coined in the mid-1950s, following the reflections of mathematician Alan Turing, 
who wondered whether a computer would one day be able to "think", or if it was only capable of an "imitation game"."""

response = classification_chain.invoke({
    "input": text,
    "format_instructions": classification_parser.get_format_instructions()
})
print("Category:", response.category)
print("Confidence:", response.confidence)