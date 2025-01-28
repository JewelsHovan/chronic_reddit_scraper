from typing import List, Dict, Any
import litellm
from analysis.llm_extractor.core.prompts import lexicon_expansion_prompt, content_analysis_prompt, slang_generation_prompt
from backup.structured_outputs import (
    get_structured_lexicon_extraction,
    get_structured_slang_generation,
    get_structured_content_analysis,
    LexiconExtraction,
    ContentAnalysis,
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

    def extract_lexicon(self, data: str) -> LexiconExtraction:
        """
        Extracts lexicon items using litellm.completion and the lexicon_expansion_prompt.
        """
        prompt = lexicon_expansion_prompt
        messages = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": data},
        ]
        return get_structured_lexicon_extraction(self.model_name, messages)

    def extract_content_analysis(self, data: str) -> ContentAnalysis:
        """
        Extracts content analysis using litellm.completion and the content_analysis_prompt.
        """
        prompt = content_analysis_prompt
        messages = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": data},
        ]
        return get_structured_content_analysis(self.model_name, messages)

    def generate_slang(self, data: str) -> SlangGeneration:
        """
        Generates slang terms using litellm.completion and the slang_generation_prompt.
        """
        prompt = slang_generation_prompt
        messages = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": data},
        ]
        return get_structured_slang_generation(self.model_name, messages)

    def process_post(self, post: Dict[str, Any]) -> Dict[str, Any]:
        """
        Applies multiple LLM-based methods on a single Reddit-like post object.
        
        :param post: A dictionary containing information about the post and comments.
        :return: A dictionary containing the original post data plus results
                 from extraction, classification, and slang generation.
        """
        # Pass the entire post dictionary as a string
        post_string = str(post)

        # Extract lexicon, classify pain context, and generate slang
        extracted_lexicon = self.extract_lexicon(post_string)
        extracted_content = self.extract_content_analysis(post_string)
        generated_slang = self.generate_slang(post_string)

        # Attach the LLM outputs to the post dictionary:
        output = {
            **post,  # Include the original post data
            "extracted_lexicon": extracted_lexicon.model_dump(),
            "content_analysis": extracted_content.model_dump(),
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