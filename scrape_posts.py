from bs4 import BeautifulSoup
import requests
import json
from config.headers import REDDIT_HEADERS
from datetime import datetime

def extract_post_id(url):
    """Extract post ID from Reddit URL."""
    try:
        return f"t3_{url.split('/comments/')[1].split('/')[0]}"
    except IndexError:
        return None

def scrape_post(url):
    """
    Scrapes a Reddit post URL and returns structured post data with comments.
    """
    try:
        response = requests.get(url, headers=REDDIT_HEADERS)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        
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
            'comments': []  # Will store all comments
        }
        
        # Get post content
        content_elem = post_container.find('div', {'slot': 'text-body'})
        if content_elem:
            post_data['content'] = content_elem.get_text(strip=True)
        
        # Extract comments if we have a valid post_id
        if post_id:
            post_data['comments'] = extract_comments(post_id)
            
        return post_data

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

def process_comment(comment_elem, depth=0, parent_id=None):
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

    # Process child comments
    child_comments = comment_elem.find_all('shreddit-comment', attrs={'slot': 'children'}, recursive=False)
    
    if not child_comments:
        children_slot = comment_elem.find('div', {'slot': 'children'})
        if children_slot:
            child_comments = children_slot.find_all('shreddit-comment', recursive=False)

    for child_elem in child_comments:
        child_comment = process_comment(child_elem, depth + 1, thing_id)
        if child_comment:
            comment['replies'].append(child_comment)

    # Fetch additional replies if they exist
    if more_replies_link:
        additional_replies = fetch_more_replies(more_replies_link)
        for reply in additional_replies:
            reply['parent_id'] = thing_id
            reply['depth'] = depth + 1
            comment['replies'].append(reply)

    return comment

def fetch_more_replies(more_replies_url):
    """Fetch additional comment replies."""
    full_url = f"https://www.reddit.com{more_replies_url}?render-mode=partial&is_lit_ssr=false"
    print(f"Fetching more replies from: {full_url}")
    
    try:
        response = requests.get(full_url, headers=REDDIT_HEADERS)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        comment_trees = soup.find_all('shreddit-comment-tree')
        
        comments = []
        for tree in comment_trees:
            comment_elements = tree.find_all('shreddit-comment', recursive=False)
            for comment_elem in comment_elements:
                comment = process_comment(comment_elem)
                if comment:
                    comments.append(comment)
        
        return comments
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching more replies: {e}")
    return []

def extract_comments(post_id):
    """Extract all comments for a post."""
    comments_url = f"https://www.reddit.com/svc/shreddit/comments/r/chronicpain/{post_id}?render-mode=partial&is_lit_ssr=false"
    
    try:
        response = requests.get(comments_url, headers=REDDIT_HEADERS)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching comments: {e}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    comment_tree = soup.find('shreddit-comment-tree')
    comments = []

    if comment_tree:
        top_level_comments = comment_tree.find_all('shreddit-comment', attrs={'depth': '0'}, recursive=False)
        for comment_elem in top_level_comments:
            comment = process_comment(comment_elem)
            if comment:
                comments.append(comment)
    
    return comments

if __name__ == "__main__":
    BASE_URL = "https://www.reddit.com"

    with open('data/reddit_posts.json', 'r') as file:
        reddit_posts = json.load(file)

    # Process up to 10 posts and store results
    processed_posts = []
    for post_url in reddit_posts[:10]:  # Limit to first 10 posts
        full_url = f"{BASE_URL}{post_url}"
        print(f"Scraping: {full_url}")
        post_data = scrape_post(full_url)
        if post_data:
            processed_posts.append(post_data)

    # Save results with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_filename = f"posts_data_{timestamp}.json"
    
    try:
        with open(output_filename, 'w', encoding='utf-8') as f:
            json.dump(processed_posts, f, indent=2, ensure_ascii=False)
        print(f"\nPosts saved to {output_filename}")
        
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
                def print_comment_tree(comments, level=0, max_comments=3, current_count=0):
                    for comment in comments:
                        if current_count >= max_comments:
                            return current_count
                        indent = "  " * level
                        print(f"{indent}└─ Author: {comment['author']}")
                        print(f"{indent}   Text: {comment['text'][:100]}...")
                        current_count += 1
                        if comment['replies']:
                            current_count = print_comment_tree(
                                comment['replies'], 
                                level + 1, 
                                max_comments, 
                                current_count
                            )
                        if current_count >= max_comments:
                            return current_count
                    return current_count
                
                print_comment_tree(post['comments'])
            print("-" * 50)
    except IOError as e:
        print(f"Error writing to JSON file: {e}")