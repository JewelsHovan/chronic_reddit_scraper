lexicon_expansion_prompt = """
Analyze this Reddit post and extract all pain-related terms and expressions. Focus on how people naturally describe their experiences.

Categorize each term into one of these categories:
- Physical: descriptors of the pain sensation (e.g., burning, stabbing)
- Intensity: words indicating severity (e.g., mild, severe)
- Location: body parts or spatial descriptions
- Temporal: time-related patterns or duration
- Impact: effects on daily life or functioning

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
      "category": "intensity"
    },
    {
        "term": "my lower back",
        "context": "describing the location of the pain",
        "category": "location"
    },
    {
        "term": "it's been constant for weeks",
        "context": "describing the duration of the pain",
        "category": "temporal"
    },
    {
        "term": "can't even get out of bed",
        "context": "describing the impact of the pain on daily life",
        "category": "impact"
    }
  ]
}

Categories are limited to: physical, emotional, intensity, location, temporal, impact

Please analyze the following input:
{input_text}
"""

content_analysis_prompt = """
Analyze this Reddit post and extract key content-based features about the author's experience. Focus on emotional and contextual indicators.

For the primary tone, use only the following options: Negative, Positive, Neutral, Ambivalent

For the primary topic, use only the following options: Support and Personal Experiences, Information and Discussion, Community and Social Interaction, Humor and Entertainment, Reflection and Sentiment, Critique and Change, Other

Return a JSON object with this format:

{
  "sentiment": {
    "score": -0.8,        // range: -1.0 (very negative) to 1.0 (very positive)
    "primary_tone": "Negative", // options: Negative, Positive, Neutral, Ambivalent
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
    "primary_topic": "Support and Personal Experiences", // options: Support and Personal Experiences, Information and Discussion, Community and Social Interaction, Humor and Entertainment, Reflection and Sentiment, Critique and Change, Other
    "subtopics": [
      "medication_advice",
      "coping_strategies"
    ],
    "categories": {
      // Confidence scores for each possible category
      "support_and_personal_experiences": 0.8,
      "information_and_discussion": 0.4,
      "community_and_social_interaction": 0.6,
      "humor_and_entertainment": 0.2,
      "reflection_and_sentiment": 0.0,
      "critique_and_change": 0.0,
      "other": 0.5
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
Analyze this Reddit post and extract all pain-related slang or colloquial expressions.

Extract - The clinical term (medical diagnosis or treatment) and the expressions that people use to describe/express the pain

Return a JSON object with this format:

{
  "clinical_term": "cervical radiculopathy",
  "colloquial_expressions": [
    "my neck is doing its best Vader force choke impression",
    "feels like my spine is trying to escape",
    "neck.exe has stopped working"
  ]
}

Please analyze the following Reddit post and comments:
{input_text}
"""