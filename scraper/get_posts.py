import requests
from config.headers import REDDIT_HEADERS
from config.urls import get_reddit_feed_url, valid_sort_options
from scraper.src.posts import get_reddit_posts

if __name__ == "__main__":
    session = requests.Session()
    session.headers.update(REDDIT_HEADERS)
    NUM_POSTS = 3000
    posts_per_sort = NUM_POSTS // len(valid_sort_options)

    new_posts = []
    for sort_option in valid_sort_options:
        feed_url = get_reddit_feed_url(
            subreddit="ChronicPain",
            sort_by=sort_option,
            time_filter="ALL",
            feed_length=25
        )
        print(f"Fetching {sort_option} posts from: {feed_url}")
        
        posts = get_reddit_posts(feed_url, num_posts=posts_per_sort, session=session)
        new_posts.extend(posts)
        print(f"Found {len(posts)} posts using {sort_option} sort")

    print(f"\nTotal unique posts collected: {len(new_posts)}")