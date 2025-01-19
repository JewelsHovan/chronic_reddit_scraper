lexicon_expansion_prompt = """
You are an expert in identifying and categorizing colloquial terms and phrases related to chronic pain.
Analyze the provided text and extract a list of colloquial terms or phrases used to describe pain.
Return a JSON object with a single key "terms". The value for "terms" should be a list of JSON objects.
Each object in the list must have the following keys:

"reddit_source": "The ID of the Reddit post or comment where the term was found.",
"colloquial_term": "The colloquial term or phrase extracted.",
"context": "A brief description of the surrounding text in the post.",
"category": "Categorization of the term (a single string representing one of the following: intensity, quality, emotional, location, other).",
"synonyms": "A list of contextually relevant synonyms or alternative phrases."

Example:

Input Text:
"Post ID: t3_xyz, Comment ID: comment_abc, Text: My back is killing me today. It feels like a burning sensation."

Output JSON:
{
  "terms": [
    {
      "reddit_source": "comment_abc",
      "colloquial_term": "killing me",
      "context": "Used to describe the intensity of back pain.",
      "category": "intensity",
      "synonyms": ["very painful", "extremely sore", "hurting badly"]
    },
    {
      "reddit_source": "comment_abc",
      "colloquial_term": "burning sensation",
      "context": "Used to describe the quality of back pain.",
      "category": "quality",
      "synonyms": ["hot sensation", "searing feeling", "like it's on fire"]
    }
  ]
}

Input: {}
"""

pain_context_classification_prompt = """
Zero-Shot Classification of Pain Contexts
Goal: To classify Reddit posts into predefined pain context categories without prior training examples.

"I am working on a project to automatically categorize descriptions of pain from Reddit posts into different pain contexts. I need your help to perform zero-shot classification.
Task:
Input: I will provide you with a set of Reddit posts (in JSON format) describing pain experiences and a predefined set of pain context labels.


Zero-Shot Classification: Without any prior training examples, classify each Reddit post into one or more of the predefined pain context labels based on the language used to describe the pain.


Confidence Score: Provide a confidence score (0.0 to 1.0) for each classification, where 1.0 represents the highest confidence.


Output Format: Structure the output in JSON format as follows:

 {
"post_id": "t3_examplepost",
"classifications": [
    {
    "context": "neuropathic pain",
    "confidence": 0.85
    },
    {
    "context": "emotional pain",
    "confidence": 0.6
    }
]
}

Pain Context Labels: \[Insert list of pain context labels here, e.g., "neuropathic pain," "musculoskeletal pain," "post-surgical pain," "emotional pain," "visceral pain," "inflammatory pain"]
This task will help me develop a system for automatically understanding and categorizing different types of pain based on how people describe them on Reddit."

Input:
Reddit Posts: {}

"""

slang_generation_prompt = """Generation of Nuanced Slang Expressions
Goal: To generate creative and realistic slang expressions for clinical pain descriptions.

"I am expanding my pain lexicon to include nuanced slang expressions that people might use on social media platforms like Reddit. I need your help to generate these expressions.
Task:
Input: I will provide you with a set of formal or clinical descriptions of pain (e.g., "severe, throbbing headache," "chronic, burning sensation in the legs").


Generate Slang: Generate a list of 3-5 nuanced slang expressions or colloquialisms that a person might use on Reddit to describe the same pain experience.


Creativity and Realism: Aim for creative and realistic expressions that capture the intensity, quality, and emotional impact of the pain. Consider how different demographics or online communities might express themselves.


Output Format: Structure the output in JSON format as follows:

 {
"clinical_description": "severe, throbbing headache",
"slang_expressions": [
    "My head is pounding like a drum",
    "Brain is on fire, send help",
    "This migraine is killing me softly",
    "Got a skull-splitter of a headache",
    "Feel like my head's gonna explode"
]
}

Input: {}
"""