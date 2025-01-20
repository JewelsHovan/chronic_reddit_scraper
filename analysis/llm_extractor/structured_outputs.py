import os
from typing import List, Dict, Any, Optional
from litellm import completion
from pydantic import BaseModel, Field, field_validator


class ColloquialTerm(BaseModel):
    term: str = Field(..., description="The colloquial term or phrase")
    context: str = Field(..., description="Brief description of how the term is used")
    category: str = Field(..., description="Basic category: physical, emotional, or intensity")

    @field_validator('category')
    def validate_category(cls, v):
        valid_categories = ['physical', 'emotional', 'intensity']
        if v.lower() not in valid_categories:
            raise ValueError(f'Category must be one of {valid_categories}')
        return v.lower()

class LexiconExtraction(BaseModel):
    terms: List[ColloquialTerm]

class SlangGeneration(BaseModel):
    clinical_term: str = Field(..., description="The formal medical term")
    colloquial_expressions: List[str] = Field(..., description="Natural language expressions")

class SentimentDetails(BaseModel):
    score: float = Field(..., description="Sentiment score from -1.0 to 1.0")
    primary_tone: str = Field(..., description="Primary emotional tone")
    key_phrases: List[str] = Field(..., description="Supporting phrases from the text")

    @field_validator('score')
    def validate_score(cls, v):
        if not -1.0 <= v <= 1.0:
            raise ValueError('Sentiment score must be between -1.0 and 1.0')
        return v

class EmotionalIntensity(BaseModel):
    score: float = Field(..., description="Intensity score from 0.0 to 1.0")
    indicators: List[str] = Field(..., description="Supporting intensity indicators")

    @field_validator('score')
    def validate_score(cls, v):
        if not 0.0 <= v <= 1.0:
            raise ValueError('Intensity score must be between 0.0 and 1.0')
        return v

class PainLevel(BaseModel):
    score: int = Field(..., description="Pain level from 0-10, or -1 if undetermined")
    confidence: float = Field(..., description="Confidence score from 0.0 to 1.0")
    contextual_clues: List[str] = Field(..., description="Supporting context from the text")

    @field_validator('score')
    def validate_score(cls, v):
        if not -1 <= v <= 10:
            raise ValueError('Pain score must be between -1 and 10')
        return v

    @field_validator('confidence')
    def validate_confidence(cls, v):
        if not 0.0 <= v <= 1.0:
            raise ValueError('Confidence score must be between 0.0 and 1.0')
        return v

class Urgency(BaseModel):
    level: str = Field(..., description="Urgency level assessment")
    confidence: float = Field(..., description="Confidence score from 0.0 to 1.0")
    indicators: List[str] = Field(..., description="Supporting urgency indicators")

    @field_validator('level')
    def validate_level(cls, v):
        valid_levels = ['low', 'moderate', 'high', 'critical']
        if v.lower() not in valid_levels:
            raise ValueError(f'Level must be one of {valid_levels}')
        return v.lower()

    @field_validator('confidence')
    def validate_confidence(cls, v):
        if not 0.0 <= v <= 1.0:
            raise ValueError('Confidence score must be between 0.0 and 1.0')
        return v

class TopicClassification(BaseModel):
    primary_topic: str = Field(..., description="Primary topic of the post")
    subtopics: List[str] = Field(..., description="Additional topics covered")
    categories: Dict[str, float] = Field(..., description="Confidence scores for each category")

class ContentAnalysis(BaseModel):
    sentiment: SentimentDetails
    emotional_intensity: EmotionalIntensity
    pain_level: PainLevel
    urgency: Urgency
    topic_classification: TopicClassification

def get_structured_lexicon_extraction(
    model: str, messages: List[Dict[str, str]]
) -> LexiconExtraction:
    """
    Extracts lexicon items using litellm.completion and returns a structured output.
    """
    response = completion(model=model, messages=messages, response_format={"type": "json_object"})
    return LexiconExtraction.model_validate_json(response.choices[0].message.content)

def get_structured_slang_generation(model: str, messages: List[Dict[str, str]]) -> SlangGeneration:
    """
    Generates slang terms using litellm.completion and returns a structured output.
    """
    response = completion(model=model, messages=messages, response_format={"type": "json_object"})
    return SlangGeneration.model_validate_json(response.choices[0].message.content)

def get_structured_content_analysis(
    model: str, messages: List[Dict[str, str]]
) -> ContentAnalysis:
    """
    Analyzes content features using litellm.completion and returns a structured output.
    """
    response = completion(model=model, messages=messages, response_format={"type": "json_object"})
    return ContentAnalysis.model_validate_json(response.choices[0].message.content) 