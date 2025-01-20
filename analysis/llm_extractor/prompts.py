lexicon_expansion_prompt = """
Analyze this Reddit post and identify key pain-related expressions. Focus on how people naturally describe their experiences.

Return a JSON object with this simplified format:

{
  "terms": [
    {
      "term": "feels like fire in my joints",
      "context": "describing intense inflammatory pain",
      "category": "physical"
    },
    {
      "term": "at my breaking point",
      "context": "expressing emotional distress from chronic pain",
      "category": "emotional"
    }
  ]
}

Categories are limited to: physical, emotional, intensity

Please analyze the following input:
{input_text}
"""

content_analysis_prompt = """
Analyze this Reddit post and extract key content-based features about the author's experience. Focus on emotional and contextual indicators.

Return a JSON object with this format:

{
  "sentiment": {
    "score": -0.8,        // range: -1.0 (very negative) to 1.0 (very positive)
    "primary_tone": "frustrated",
    "key_phrases": [
      "can't take it anymore",
      "feeling hopeless",
      "at my wit's end"
    ]
  },
  "emotional_intensity": {
    "score": 0.9,         // range: 0.0 (minimal) to 1.0 (extreme)
    "indicators": [
      "extremely",
      "desperately",
      "!!!"
    ]
  },
  "pain_level": {
    "score": 8,           // range: 0-10, use -1 if cannot determine
    "confidence": 0.7,    // range: 0.0 to 1.0
    "contextual_clues": [
      "can barely walk",
      "worst pain ever",
      "completely debilitating"
    ]
  },
  "urgency": {
    "level": "high",      // options: low, moderate, high, critical
    "confidence": 0.85,
    "indicators": [
      "need help immediately",
      "emergency situation",
      "can't wait any longer"
    ]
  },
  "topic_classification": {
    "primary_topic": "support_seeking",
    "subtopics": [
      "medication_advice",
      "coping_strategies"
    ],
    "categories": {
      // Confidence scores for each possible category
      "support_seeking": 0.8,
      "medication": 0.4,
      "symptoms": 0.6,
      "rant": 0.2,
      "success_story": 0.0,
      "research": 0.0,
      "advice": 0.5
    }
  }
}

Important: 
- Use contextual clues to make educated guesses, but indicate lower confidence when uncertain
- For pain_level, only provide a score if there are clear contextual indicators
- Multiple subtopics can be present in a single post
- Sentiment should consider the overall tone, not just individual words

Please analyze the following input (reddit post and comments):
{input_text}
"""

slang_generation_prompt = """
Convert this medical term into natural expressions that people might use on Reddit.

Return a JSON object with this format:

{
  "clinical_term": "cervical radiculopathy",
  "colloquial_expressions": [
    "my neck is doing its best Vader force choke impression",
    "feels like my spine is trying to escape",
    "neck.exe has stopped working"
  ]
}

Focus on vivid, relatable expressions that real people would use.

Please analyze the following input:
{input_text}
"""