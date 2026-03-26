from .llm import llm
from src.prompts.prompts import classification_prompt
from src.core.parsers import classification_parser

classification_chain = classification_prompt | llm | classification_parser
