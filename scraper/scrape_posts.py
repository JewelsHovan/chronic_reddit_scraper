import asyncio
import aiohttp
from bs4 import BeautifulSoup
from tqdm import tqdm
import json
from datetime import datetime
import random
import os
from pathlib import Path
import sys

# Add project root to Python path to enable absolute imports
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.append(str(PROJECT_ROOT))

from config.constants import MAX_WORKERS, RATE_LIMIT_REQUESTS, TOKEN_REFRESH_RATE, CHECKPOINT_INTERVAL
from config.headers import REDDIT_HEADERS
from config.paths import RAW_DATA_DIR, PARTIAL_DATA_DIR
from scraper.src.session import RateLimiter
from scraper.src.utils import extract_post_id, print_comment_tree

# Create directories if they don't exist
RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
PARTIAL_DATA_DIR.mkdir(parents=True, exist_ok=True)


async def scrape_post(session, url, semaphore, rate_limiter):
    """Updated scrape_post function with rate limiting"""
    async with semaphore:
        await rate_limiter.acquire()  # Wait for rate limiter
        try:
            async with session.get(url, headers=REDDIT_HEADERS, timeout=60) as response:
                response.raise_for_status()
                html = await response.text()

            soup = BeautifulSoup(html, 'html.parser')

            # Find the main post content
            post_container = soup.find('shreddit-post')
            if not post_container:
                return None

            post_id = extract_post_id(url)

            # Extract post data
            post_data = {
                'title': post_container.get('post-title', ''),
                'author': post_container.get('author', ''),
                'created_timestamp': post_container.get('created-timestamp', ''),
                'score': post_container.get('score', 0),
                'upvote_ratio': post_container.get('upvote-ratio', 0),
                'content': '',
                'post_id': post_id,
                'comments': [],
                'image_url': post_container.get('content-href', ''),
                'comment_count': post_container.get('comment-count', 0)
            }

            # Get post content
            content_elem = post_container.find('div', {'slot': 'text-body'})
            if content_elem:
                post_data['content'] = content_elem.get_text(strip=True)

            # Extract comments if we have a valid post_id
            if post_id:
                post_data['comments'] = await extract_comments(session, post_id, rate_limiter)

            return post_data

        except (aiohttp.ClientError, asyncio.TimeoutError) as e:
            if isinstance(e, aiohttp.ClientResponseError) and e.status == 429:
                print(f"Rate limited while scraping {url}. Retrying with exponential backoff...")
                await asyncio.sleep(random.uniform(2, 10))  # Wait for a random time before retrying
                return await scrape_post(session, url, semaphore, rate_limiter)  # Retry the request
            else:
                print(f"An error occurred while scraping {url}: {e}")
                return None

async def process_comment(comment_elem, session, depth=0, parent_id=None, rate_limiter=None):
    """Process individual comment elements."""
    if comment_elem is None:
        return None

    thing_id = comment_elem.get('thingid')
    author = comment_elem.get('author')
    text_elem = comment_elem.find('div', id=lambda x: x and x.endswith('-post-rtjson-content'))
    text = text_elem.get_text(strip=True) if text_elem else "Comment Text Missing"

    action_row = comment_elem.find('shreddit-comment-action-row')
    comment_action_id = action_row.get('comment-id') if action_row else None

    more_replies = comment_elem.find('a', {'slot': "more-comments-permalink"})
    more_replies_link = more_replies.get('href') if more_replies else None

    comment = {
        'thing_id': thing_id,
        'depth': int(comment_elem.get('depth', 0)),
        'parent_id': parent_id,
        'author': author,
        'text': text,
        'action_id': comment_action_id,
        'more_replies': more_replies_link,
        'replies': []
    }

    # Process child comments - Updated to handle nested comments better
    child_comments = []
    
    # First check direct children with slot='children'
    children_slot = comment_elem.find('div', {'slot': 'children'})
    if children_slot:
        # Use recursive=True to get all nested comments
        child_comments.extend(children_slot.find_all('shreddit-comment', recursive=True))
    
    # Also check for comments that are direct descendants
    child_comments.extend(comment_elem.find_all('shreddit-comment', recursive=True))
    
    # Remove duplicates while preserving order
    seen = set()
    child_comments = [x for x in child_comments if not (x.get('thingid') in seen or seen.add(x.get('thingid')))]

    # Process child comments
    child_tasks = []
    for child_elem in child_comments:
        # Only process comments that are one level deeper than current
        if int(child_elem.get('depth', 0)) == depth + 1:
            child_tasks.append(process_comment(
                child_elem, 
                session, 
                depth + 1, 
                thing_id, 
                rate_limiter
            ))
    
    if child_tasks:
        child_comments = await asyncio.gather(*child_tasks)
        comment['replies'].extend(c for c in child_comments if c is not None)

    # Fetch additional replies if they exist
    if more_replies_link:
        additional_replies = await fetch_more_replies(session, more_replies_link, rate_limiter)
        for reply in additional_replies:
            reply['parent_id'] = thing_id
            reply['depth'] = depth + 1
            comment['replies'].append(reply)

    return comment

async def fetch_more_replies(session, more_replies_url, rate_limiter):
    """Asynchronously fetch additional comment replies."""
    full_url = f"https://www.reddit.com{more_replies_url}?render-mode=partial&is_lit_ssr=false"
    
    try:
        await rate_limiter.acquire()  # Add rate limiting
        async with session.get(full_url, headers=REDDIT_HEADERS, timeout=60) as response:
            response.raise_for_status()
            html = await response.text()
        
        soup = BeautifulSoup(html, 'html.parser')
        comment_trees = soup.find_all('shreddit-comment-tree')
        
        comments = []
        for tree in comment_trees:
            comment_elements = tree.find_all('shreddit-comment', recursive=False)
            for comment_elem in comment_elements:
                comment = await process_comment(comment_elem, session, rate_limiter=rate_limiter)
                if comment:
                    comments.append(comment)
        
        return comments
        
    except (aiohttp.ClientError, asyncio.TimeoutError) as e:
        print(f"Error fetching more replies: {e}")
    return []

async def extract_comments(session, post_id, rate_limiter):
    """Asynchronously extract all comments for a post."""
    comments_url = f"https://www.reddit.com/svc/shreddit/comments/r/chronicpain/{post_id}?render-mode=partial&is_lit_ssr=false"
    
    try:
        await rate_limiter.acquire()  # Add rate limiting
        async with session.get(comments_url, headers=REDDIT_HEADERS, timeout=60) as response:
            response.raise_for_status()
            html = await response.text()
    except (aiohttp.ClientError, asyncio.TimeoutError) as e:
        print(f"Error fetching comments: {e}")
        return []

    soup = BeautifulSoup(html, 'html.parser')
    comment_tree = soup.find('shreddit-comment-tree')
    comments = []

    if comment_tree:
        top_level_comments = comment_tree.find_all('shreddit-comment', attrs={'depth': '0'}, recursive=False)
        tasks = [asyncio.create_task(process_comment(
            comment_elem, 
            session=session, 
            rate_limiter=rate_limiter
        )) for comment_elem in top_level_comments]
        comments = await asyncio.gather(*tasks)
        comments = [c for c in comments if c is not None]  # Filter out None values
    
    return comments

async def main():
    """Updated main function with rate limiter"""
    BASE_URL = "https://www.reddit.com"
    
    with open('data/reddit_posts.json', 'r') as file:
        reddit_posts = json.load(file)

    rate_limiter = RateLimiter(RATE_LIMIT_REQUESTS, TOKEN_REFRESH_RATE)
    
    async with aiohttp.ClientSession() as session:
        semaphore = asyncio.Semaphore(MAX_WORKERS)
        tasks = []
        for post_url in reddit_posts:
            full_url = f"{BASE_URL}{post_url}"
            tasks.append(scrape_post(session, full_url, semaphore, rate_limiter))
        
        print(f"Total tasks: {len(tasks)}")

        processed_posts = []
        checkpoint_counter = 0
        
        # Initialize tqdm progress bar for fetching more replies
        more_replies_progress = tqdm(total=0, desc="Fetching more replies", unit="reply")
        
        for task in tqdm(asyncio.as_completed(tasks), total=len(tasks), desc="Scraping Posts"):
            post_data = await task
            if post_data:
                # Update the count of fetched replies
                for comment in post_data['comments']:
                    more_replies_progress.total += len(comment.get('replies', []))
                    more_replies_progress.update(len(comment.get('replies', [])))
                
                processed_posts.append(post_data)
                checkpoint_counter += 1

                if checkpoint_counter >= CHECKPOINT_INTERVAL:
                    date_str = datetime.now().strftime("%Y%m%d")
                    checkpoint_filename = f"data/partial/checkpoint_{date_str}.json"
                    try:
                        # Load existing checkpoint if it exists
                        existing_posts = []
                        if os.path.exists(checkpoint_filename):
                            with open(checkpoint_filename, 'r', encoding='utf-8') as f:
                                existing_posts = json.load(f)
                        
                        # Combine existing and new posts
                        all_posts = existing_posts + processed_posts
                        
                        with open(checkpoint_filename, 'w', encoding='utf-8') as f:
                            json.dump(all_posts, f, indent=2, ensure_ascii=False)
                        print(f"\nCheckpoint saved to {checkpoint_filename}")
                    except IOError as e:
                        print(f"Error writing to checkpoint file: {e}")

                    checkpoint_counter = 0  # Reset counter only
        
        # Close the progress bar for fetching more replies
        more_replies_progress.close()

    # Save remaining results after processing all tasks
    if processed_posts:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_filename = f"posts_data_{timestamp}.json"
        try:
            with open(output_filename, 'w', encoding='utf-8') as f:
                json.dump(processed_posts, f, indent=2, ensure_ascii=False)
            print(f"\nPosts saved to {output_filename}")
        except IOError as e:
            print(f"Error writing to JSON file: {e}")

    # Updated preview section
    print("\nScraped Posts Preview:")
    for post in processed_posts:
        print(f"\nTitle: {post['title']}")
        print(f"Author: {post['author']}")
        print(f"Content preview: {post['content'][:100]}...")
        print(f"Number of comments: {len(post['comments'])}")
        
        # Preview first few comments
        if post['comments']:
            print("\nFirst few comments:")
            print_comment_tree(post['comments'])
        print("-" * 50)

if __name__ == "__main__":
    asyncio.run(main())
