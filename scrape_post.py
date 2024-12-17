from bs4 import BeautifulSoup
import requests
import json
from config.headers import REDDIT_HEADERS

def scrape_post(url):
    """
    Scrapes a Reddit post URL and returns the prettified HTML content.

    Args:
        url (str): The URL of the Reddit post.

    Returns:
        str: The prettified HTML content of the post, or None if an error occurs.
    """
    try:
        response = requests.get(url, headers=REDDIT_HEADERS)
        response.raise_for_status()  # Raise an exception for bad status codes

        soup = BeautifulSoup(response.text, 'html.parser')
        return soup.prettify()

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

if __name__ == "__main__":
    BASE_URL = "https://www.reddit.com"

    with open('data/reddit_posts.json', 'r') as file:
        reddit_posts = json.load(file)

    # for testing get just the first post
    reddit_post = reddit_posts[:1]

    post_url = f"{BASE_URL}{reddit_post[0]}"
    print(post_url)
    print(scrape_post(post_url))