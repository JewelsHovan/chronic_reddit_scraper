from typing import List, Dict, Any
import litellm
from prompts import lexicon_expansion_prompt, pain_context_classification_prompt, slang_generation_prompt
from analysis.llm_extractor.structured_outputs import (
    get_structured_lexicon_extraction,
    get_structured_pain_context_classification,
    get_structured_slang_generation,
    LexiconExtraction,
    PainContextClassifications,
    SlangGeneration,
)


class LLMExtractor:
    """
    A class for extracting information from text data using a specified model.
    """
    def __init__(self, model_name: str):
        """
        Initialize the LLMExtractor with a model_name.
        
        :param model_name: Name or path of the model to be loaded.
        """
        self.model_name = model_name
        self.model = self.load_model(model_name)

    def load_model(self, model_name: str) -> Any:
        """
        Sets the model to be used by litellm.
        
        :param model_name: The name or path of the language model to use.
        :return: Returns the model_name for potential use in litellm calls.
        """
        # litellm doesn't require explicit model loading, 
        # but we'll keep this method to maintain the model_name
        return model_name

    def extract_lexicon(self, data: List[str]) -> LexiconExtraction:
        """
        Extracts lexicon items using litellm.completion and the lexicon_expansion_prompt.
        """
        prompt = lexicon_expansion_prompt
        messages = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": str(data)},
        ]
        return get_structured_lexicon_extraction(self.model_name, messages)

    def classify_pain_context(self, data: List[str]) -> PainContextClassifications:
        """
        Classifies pain context using litellm.completion and the pain_context_classification_prompt.
        """
        prompt = pain_context_classification_prompt
        messages = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": str(data)},
        ]
        return get_structured_pain_context_classification(self.model_name, messages)

    def generate_slang(self, data: List[str]) -> SlangGeneration:
        """
        Generates slang terms using litellm.completion and the slang_generation_prompt.
        """
        prompt = slang_generation_prompt
        messages = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": str(data)},
        ]
        return get_structured_slang_generation(self.model_name, messages)

    def process_post(self, post: Dict[str, Any]) -> Dict[str, Any]:
        """
        Applies multiple LLM-based methods on a single Reddit-like post object.
        
        :param post: A dictionary containing information about the post and comments.
        :return: A dictionary containing the original post data plus results
                 from extraction, classification, and slang generation.
        """
        # Convert relevant text fields into a list that each method can process
        # For example, combine title and content, or also include comment texts.
        combined_text = []
        if "title" in post:
            combined_text.append(post["title"])
        if "content" in post:
            combined_text.append(post["content"])
        if "comments" in post:
            for comment_info in post["comments"]:
                combined_text.append(comment_info.get("text", ""))

        # Extract lexicon, classify pain context, and generate slang
        extracted_lexicon = self.extract_lexicon(combined_text)
        classified_context = self.classify_pain_context(combined_text)
        generated_slang = self.generate_slang(combined_text)

        # Attach the LLM outputs to the post dictionary:
        output = {
            **post,  # Include the original post data
            "extracted_lexicon": extracted_lexicon.model_dump(),
            "pain_context_classification": classified_context.model_dump(),
            "slang_terms": generated_slang.model_dump()
        }
        return output

    def save_processed_post(self, processed_post: Dict[str, Any], output_path: str) -> None:
        """
        Saves the processed post (with LLM results) to a file, e.g., JSON.
        
        :param processed_post: The dictionary with updated post info and LLM outputs.
        :param output_path: Path where the file should be written.
        """
        import json
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(processed_post, f, ensure_ascii=False, indent=2)