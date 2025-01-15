

lexicon_expansion_prompt =r"""
Lexicon Expansion with Colloquialisms and Contextual Synonyms
Goal: To expand the pain lexicon by extracting colloquial terms, slang, idioms, and their contextual synonyms from Reddit posts.

"I am building a comprehensive pain lexicon that captures the diverse ways people describe pain, including formal medical terms, colloquialisms, and nuanced slang expressions. I need your help to expand this lexicon using Reddit data.
Task:
Analyze Reddit Data: I will provide you with a set of Reddit posts (in JSON format) related to chronic pain or specific pain conditions.


Extract Colloquial Terms: Identify and extract colloquialisms, slang, idioms, and informal expressions used to describe pain experiences. Pay close attention to the context in which these terms are used.


Generate Contextual Synonyms: For each extracted term, generate a list of contextually relevant synonyms or alternative phrases that convey a similar meaning within the specific context of the Reddit post.


Categorize and Organize: Categorize the extracted terms and their synonyms based on:


Pain Intensity: (e.g., mild, moderate, severe, extreme)
Pain Quality: (e.g., stabbing, burning, aching, pressure, tingling)
Emotional Descriptors: (e.g., distressing, depressing, anxious)
Pain Location (if specified): (e.g., head, back, limbs)
Output Format: Structure the output in JSON format as follows:

 {
"reddit_source": "post_id or comment_id",
"colloquial_term": "e.g., My back is killing me",
"context": "Brief description of the surrounding text in the post",
"category": {
    "intensity": "severe",
    "quality": "aching",
    "emotional": "distressing",
    "location": "back"
},
"synonyms": ["My back is throbbing intensely", "I have severe back pain", "My back is aching badly"]
}



Example JSON Input:
{{'title': 'Advise needed please…also a bit of a rant because I’m hanging on by a thread ', 'author': '-MetalKitty-', 'created_timestamp': '2024-12-09T04:15:57.791000+0000', 'score': '30', 'upvote_ratio': 0, 'content': "The doctor I had been seeing for 20 years retired and now I can't find a doctor that will prescribe my pain meds and I'll run out next week and seriously don't know what to do. Have seen one gp and three pain management doctors who all have a strict no opioids policy. Was told by one doctor that I can't just stop taking them because I'll have a heart attack.... have heart issues...and one said I won't die from withdrawal. I'm absolutely terrified, don't know what to do, my anxiety is through the roof and I’m very depressed", 'post_id': 't3_1ha1foo', 'comments': [], 'image_url': '<https://www.reddit.com/r/ChronicPain/comments/1ha1foo/advise_needed_pleasealso_a_bit_of_a_rant_because/>', 'comment_count': '32'}}

"""

pain_context_classification_prompt = r"""
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

slang_generation_prompt = r"""Generation of Nuanced Slang Expressions
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

Input: \[Insert list of clinical pain descriptions here, e.g., "chronic, burning sensation in the legs," "sharp, stabbing pain in the lower back," "dull, aching pain in the joints," "intense, cramping pain in the abdomen"]
This task will help me create a more comprehensive and relatable pain lexicon that includes the informal language people use to express their pain experiences."
"""