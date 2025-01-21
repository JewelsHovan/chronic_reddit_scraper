import os
from typing import List, Dict, Any, Optional, Annotated
from litellm import completion
from pydantic import BaseModel, field_validator


class PainTerm(BaseModel):
    term: Annotated[str, "The term or phrase"]
    context: Annotated[str, "Brief description of how the term is used"]
    category: Annotated[str, "Category: physical, emotional, intensity, location, temporal, or impact"]

    @field_validator('category')
    def validate_category(cls, v):
        valid_categories = ['physical', 'emotional', 'intensity', 'location', 'temporal', 'impact']
        if v.lower() not in valid_categories:
            raise ValueError(f'Category must be one of {valid_categories}')
        return v.lower()

class LexiconExtraction(BaseModel):
    terms: List[PainTerm]

class SlangGeneration(BaseModel):
    clinical_term: Annotated[Optional[str], "The formal medical term"]
    colloquial_expressions: Annotated[List[str], "Natural language expressions"]

class SentimentDetails(BaseModel):
    score: Annotated[float, "Sentiment score from -1.0 to 1.0"]
    primary_tone: Annotated[str, "Primary emotional tone"]
    key_phrases: Annotated[List[str], "Supporting phrases from the text"]

    @field_validator('score')
    def validate_score(cls, v):
        if not -1.0 <= v <= 1.0:
            raise ValueError('Sentiment score must be between -1.0 and 1.0')
        return v

    @field_validator("primary_tone")
    def validate_primary_tone(cls, v):
        valid_tones = ["Negative", "Positive", "Neutral", "Ambivalent"]
        if v not in valid_tones:
            raise ValueError(f"Primary tone must be one of {valid_tones}")
        return v

class EmotionalIntensity(BaseModel):
    score: Annotated[float, "Intensity score from 0.0 to 1.0"]
    indicators: Annotated[List[str], "Supporting intensity indicators"]

    @field_validator('score')
    def validate_score(cls, v):
        if not 0.0 <= v <= 1.0:
            raise ValueError('Intensity score must be between 0.0 and 1.0')
        return v

class PainLevel(BaseModel):
    score: Annotated[int, "Pain level from 0-10, or -1 if undetermined"]
    confidence: Annotated[float, "Confidence score from 0.0 to 1.0"]
    contextual_clues: Annotated[List[str], "Supporting context from the text"]

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
    level: Annotated[str, "Urgency level assessment"]
    confidence: Annotated[float, "Confidence score from 0.0 to 1.0"]
    indicators: Annotated[List[str], "Supporting urgency indicators"]

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
    primary_topic: Annotated[str, "Primary topic of the post"]
    subtopics: Annotated[List[str], "Additional topics covered"]
    categories: Annotated[Dict[str, float], "Confidence scores for each category"]

    @field_validator('primary_topic')
    def validate_primary_topic(cls, v):
        valid_topics = ['Support and Personal Experiences', 'Information and Discussion', 'Community and Social Interaction', 'Humor and Entertainment', 'Reflection and Sentiment', 'Critique and Change', 'Other']
        if v not in valid_topics:
            raise ValueError(f"Primary topic must be one of {valid_topics}")
        return v

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