import json
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

def load_and_preprocess_posts(file_path):
    """
    Loads post data from a JSON file, preprocesses the text, and returns a list of cleaned texts.

    Args:
        file_path (str): The path to the JSON file containing post data.

    Returns:
        list: A list of cleaned and lemmatized post texts.
    """
    with open(file_path, 'r') as file:
        data = json.load(file)

    posts_texts = []
    for post in data:
        post_text = post["title"] + " " + post["content"]
        for comment in post["comments"]:
            post_text += " " + comment["text"]
            for reply in comment["replies"]:
                post_text += " " + reply["text"]
        posts_texts.append(post_text)

    nltk.download("stopwords", quiet=True)
    nltk.download("wordnet", quiet=True)
    stop_words = set(stopwords.words("english"))
    lemmatizer = WordNetLemmatizer()

    def preprocess_text(text):
        text = text.lower()
        text = re.sub(r"http\S+", "", text)  # Remove URLs
        text = re.sub(r"u/\S+", "", text)  # Remove usernames
        text = re.sub(r"r/\S+", "", text)  # Remove subreddit mentions
        text = re.sub(r"[^a-zA-Z\s]", "", text)  # Remove punctuation and special characters
        words = text.split()
        words = [lemmatizer.lemmatize(word) for word in words if word not in stop_words]
        return " ".join(words)

    cleaned_posts_texts = [preprocess_text(post_text) for post_text in posts_texts]
    return cleaned_posts_texts

if __name__ == '__main__':
    file_path = '../data/posts_data_20241217_192033.json'
    cleaned_texts = load_and_preprocess_posts(file_path)
    
    # save cleaned posts texts to file
    with open('cleaned_posts_texts.txt', 'w') as file:
        for text in cleaned_texts:
            file.write(text + "\n")
    print("Cleaned texts saved to 'cleaned_posts_texts.txt'")