from src.core.chains import classification_chain
from src.core.parsers import classification_parser

text = """
Artificial intelligence is a concept coined in the mid-1950s, following the reflections of mathematician Alan Turing, 
who wondered whether a computer would one day be able to think, or if it was only capable of an imitation game.
"""

response = classification_chain.invoke({
    "input": text,
    "format_instructions": classification_parser.get_format_instructions()
})
print("Category:", response.category)
print("Confidence:", response.confidence)

from src.core.chains import summary_chain, translation_chain
from src.core.parsers import summary_parser, translation_parser

# Summary
print("\n--- Summary ---")
response = summary_chain.invoke({
    "input": text,
    "format_instructions": summary_parser.get_format_instructions()
})
print("Summary:", response.summary)

# Translation 
print("\n--- Translation ---")
response = translation_chain.invoke({
    "input": text,
    "format_instructions": translation_parser.get_format_instructions()
})

print("\nTranslated text:", response.translated_text)