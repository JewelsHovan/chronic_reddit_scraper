import requests
from bs4 import BeautifulSoup
import time
from urllib.parse import parse_qs, urlparse, urlencode
import json
from config.headers import REDDIT_HEADERS
from config.urls import get_reddit_feed_url

def load_existing_urls(filename='reddit_posts.json'):
    """
    Load existing URLs from a JSON file.
    
    Args:
        filename (str): Name of the file to load URLs from
    Returns:
        set: Set of existing URLs
    """
    try:
        with open(filename, 'r') as f:
            return set(json.load(f))
    except (FileNotFoundError, json.JSONDecodeError):
        return set()

def save_urls(urls, filename='reddit_posts.json'):
    """
    Save URLs to a JSON file.
    
    Args:
        urls (set): Set of URLs to save
        filename (str): Name of the file to save URLs to
    """
    with open(filename, 'w') as f:
        json.dump(list(urls), f, indent=2)

def get_reddit_posts(
    initial_url,
    num_posts=20,
    session=None,
    delay=2,
    filename='data/reddit_posts.json'
):
    """
    Fetches Reddit posts from a community, handling pagination
    and session cookies. Saves unique URLs to a file.

    Args:
        initial_url (str): The starting URL for the Reddit feed.
        num_posts (int): The number of posts to fetch (total).
        session (requests.Session): Session object to persist cookies.
        delay (float): Time to wait between requests in seconds.
        filename (str): Name of the file to save URLs to.
    Returns:
        List of new links added in this run
    """
    # Load existing URLs
    existing_urls = load_existing_urls(filename)
    new_urls = set()
    
    current_url = initial_url
    posts_fetched = 0
    if session is None:
        session = requests.Session()

    while posts_fetched < num_posts and current_url:
        try:
            response = session.get(current_url)
            response.raise_for_status()
            html_content = response.text

            soup = BeautifulSoup(html_content, 'html.parser')
            post_links = soup.select('shreddit-post a[slot="full-post-link"]')

            # Extract post URLs
            for link in post_links:
                url = link['href']
                if url not in existing_urls:
                    new_urls.add(url)
                    existing_urls.add(url)
                    posts_fetched += 1

            # If we haven't reached the limit, check for next page URL
            if posts_fetched < num_posts:
                load_after_tag = soup.find('faceplate-partial', attrs={'slot': 'load-after'})
                if load_after_tag and 'src' in load_after_tag.attrs:
                    current_url = f'https://www.reddit.com{load_after_tag["src"]}'
                else:
                    current_url = None

            # Add delay before next request
            if current_url:  # Only delay if there's going to be another request
                time.sleep(delay)

        except requests.RequestException as e:
            print(f"Error during request: {e}")
            break

    # Save all URLs (both existing and new)
    save_urls(existing_urls, filename)
    
    return list(new_urls)

if __name__ == "__main__":
    initial_url = get_reddit_feed_url(subreddit="ChronicPain", sort_by="hot", time_filter="ALL", feed_length=25)
    session = requests.Session()
    session.headers.update(REDDIT_HEADERS)

    NUM_POSTS = 1500

    new_posts = get_reddit_posts(initial_url, num_posts=NUM_POSTS, session=session)
    print(f"Found {len(new_posts)} new post links")
    
    for url in new_posts:
        print(url)