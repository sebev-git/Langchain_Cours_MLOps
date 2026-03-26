from pydantic import BaseModel, Field
from langchain_core.output_parsers import PydanticOutputParser

class ClassificationResult(BaseModel):
    category: str = Field(..., description="Category assigned to the text (e.g., AI, Cloud, etc.)")
    confidence: float = Field(..., description="Confidence score between 0 and 1")

classification_parser = PydanticOutputParser(pydantic_object=ClassificationResult)