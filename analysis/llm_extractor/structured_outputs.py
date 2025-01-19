import os
from typing import List, Dict, Any, Optional
from litellm import completion
from pydantic import BaseModel, Field, field_validator


class ColloquialTerm(BaseModel):
    reddit_source: str = Field(..., description="The ID of the Reddit post or comment.")
    colloquial_term: str = Field(..., description="The colloquial term or phrase extracted from the post.")
    context: str = Field(..., description="A brief description of the surrounding text in the post.")
    category: str = Field(
        ...,
        description="Categorization of the term (intensity, quality, emotional, location, or other).",
    )
    synonyms: List[str] = Field(
        ..., description="A list of contextually relevant synonyms or alternative phrases."
    )

    @field_validator('category')
    def validate_category(cls, v):
        valid_categories = ['intensity', 'quality', 'emotional', 'location', 'other']
        if v not in valid_categories:
            raise ValueError(f'Category must be one of {valid_categories}')
        return v

class LexiconExtraction(BaseModel):
    terms: List[ColloquialTerm]

class PainContextClassification(BaseModel):
    context: str = Field(..., description="The pain context label.")
    confidence: float = Field(..., description="The confidence score for the classification (0.0 to 1.0).")

    @field_validator('confidence')
    def validate_confidence(cls, v):
        if not 0.0 <= v <= 1.0:
            raise ValueError('Confidence score must be between 0.0 and 1.0')
        return v

class PostClassification(BaseModel):
    post_id: str = Field(
        default="",
        description="The ID of the Reddit post."
    )
    classifications: List[PainContextClassification] = Field(
        default_factory=list,
        description="A list of pain context classifications for the post."
    )

class PainContextClassifications(BaseModel):
    posts: List[PostClassification] = Field(
        default_factory=list,
        description="A list of classified Reddit posts."
    )

class SlangExpression(BaseModel):
    clinical_description: str = Field(
        default="",
        description="The formal or clinical description of pain."
    )
    slang_expressions: List[str] = Field(
        default_factory=list,
        description="A list of nuanced slang expressions or colloquialisms."
    )

class SlangGeneration(BaseModel):
    expressions: List[SlangExpression] = Field(
        default_factory=list,
        description="A list of generated slang expressions."
    )

def get_structured_lexicon_extraction(
    model: str, messages: List[Dict[str, str]]
) -> LexiconExtraction:
    """
    Extracts lexicon items using litellm.completion and returns a structured output.
    """
    response = completion(model=model, messages=messages, response_format={"type": "json_object"})
    return LexiconExtraction.model_validate_json(response.choices[0].message.content)

def get_structured_pain_context_classification(
    model: str, messages: List[Dict[str, str]]
) -> PainContextClassifications:
    """
    Classifies pain context using litellm.completion and returns a structured output.
    """
    response = completion(model=model, messages=messages, response_format={"type": "json_object"})
    return PainContextClassifications.model_validate_json(response.choices[0].message.content)

def get_structured_slang_generation(model: str, messages: List[Dict[str, str]]) -> SlangGeneration:
    """
    Generates slang terms using litellm.completion and returns a structured output.
    """
    response = completion(model=model, messages=messages, response_format={"type": "json_object"})
    return SlangGeneration.model_validate_json(response.choices[0].message.content) 