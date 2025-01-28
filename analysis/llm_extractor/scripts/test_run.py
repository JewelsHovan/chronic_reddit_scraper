import json
from analysis.llm_extractor.core.processor import LLMExtractor

def main():
    """
    Loads a small subset of Reddit post data, processes it using LLMExtractor,
    and prints the processed data for testing and demonstration purposes.
    """
    data_path = '/Users/julienh/Desktop/McGillWork/PainLexicon/chronic_reddit_scraper/posts_data_20250110_152846.json'  # Update with the actual path

    try:
        with open(data_path, 'r', encoding='utf-8') as f:
            posts_data = json.load(f)
    except FileNotFoundError:
        print(f"Error: Data file not found at {data_path}")
        return
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in {data_path}")
        return

    # Select a small subset of posts for testing (e.g., first 3 posts)
    test_posts = posts_data[:3]

    model_name = "openai/gpt-4o"  # Update with your desired model
    extractor = LLMExtractor(model_name)

    processed_posts = []
    for post in test_posts:
        try:
            processed_post = extractor.process_post(post)
            processed_posts.append(processed_post)
            print("-" * 20)  # Separator for clarity
            print(f"Processed Post (ID: {post.get('post_id', 'UNKNOWN')})\n")
            print(json.dumps(processed_post, indent=2))  # Print the processed post
            print("-" * 20)
        except Exception as e:
            print(f"Error processing post {post.get('post_id', 'UNKNOWN')}: {e}")

if __name__ == "__main__":
    main() 