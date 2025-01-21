import json
from tqdm import tqdm
from llm_extractor import LLMExtractor

def main():
    """
    Loads Reddit post data, processes each post using LLMExtractor,
    and saves the processed data.
    """
    data_path = '/Users/julienh/Desktop/McGillWork/PainLexicon/chronic_reddit_scraper/posts_data_20250110_152846.json'  # Update with the actual path
    output_path = 'processed_posts.json'  
    num_posts_to_process = 500

    try:
        with open(data_path, 'r', encoding='utf-8') as f:
            posts_data = json.load(f)
    except FileNotFoundError:
        print(f"Error: Data file not found at {data_path}")
        return
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in {data_path}")
        return

    model_name = "openai/gpt-4o-mini" 
    extractor = LLMExtractor(model_name)

    processed_posts = []
    for post in tqdm(posts_data[:num_posts_to_process], desc="Processing posts"):
        try:
            processed_post = extractor.process_post(post)
            processed_posts.append(processed_post)
        except Exception as e:
            print(f"Error processing post {post.get('post_id', 'UNKNOWN')}: {e}")

    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(processed_posts, f, indent=2)
        print(f"Processed data saved to {output_path}")
    except Exception as e:
        print(f"Error saving processed data: {e}")

if __name__ == "__main__":
    main()
