from bs4 import BeautifulSoup
import requests
import json
from config.headers import REDDIT_HEADERS


def process_comment(comment_elem, depth=0, parent_id=None):
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

    # Look directly for child comments either by a div with slot='children' or by shreddit-comment with slot='children'
    # First try: direct shreddit-comment with slot='children'
    child_comments = comment_elem.find_all('shreddit-comment', attrs={'slot': 'children'}, recursive=False)
    
    if not child_comments:
        # If none found, maybe they're inside a div with slot='children'
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
    """
    Fetches additional replies using the more_replies URL.
    
    Args:
        more_replies_url: Relative URL path to fetch more replies
    
    Returns:
        List of comment dictionaries for the additional replies
    """
    full_url = f"https://www.reddit.com{more_replies_url}?render-mode=partial&is_lit_ssr=false"
    print(f"Fetching more replies from: {full_url}")
    
    try:
        response = requests.get(full_url, headers=REDDIT_HEADERS)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        comment_trees = soup.find_all('shreddit-comment-tree')
        
        comments = []
        for tree in comment_trees:
            # Find all comments in this tree
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
    """
    Extracts comment content from a Reddit post using the comments endpoint.

    Args:
        post_id: The Reddit post ID (t3_xxxxx format)

    Returns:
        A list of dictionaries containing structured comment data including:
        - thing_id: unique comment identifier
        - depth: nesting level of the comment
        - parent_id: ID of parent comment (if any)
        - author: username of commenter
        - text: actual comment content
        - action_id: comment action identifier
        - more_replies: link to additional replies if any
        - replies: list of child comments
    """
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
            comments.append(process_comment(comment_elem))
    
    return comments

if __name__ == '__main__':
    url = "https://www.reddit.com/r/ChronicPain/comments/1hflkkb/can_the_world_end_already/"
    post_id = f"t3_{url.split('/comments/')[1].split('/')[0]}"
    
    extracted_comments = extract_comments(post_id)

    # Write to JSON file with timestamp to avoid overwrites
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_filename = f"comments_{post_id}_{timestamp}.json"
    
    try:
        with open(output_filename, 'w', encoding='utf-8') as f:
            json.dump(extracted_comments, f, indent=2, ensure_ascii=False)
        print(f"Comments saved to {output_filename}")
    except IOError as e:
        print(f"Error writing to JSON file: {e}")

    # Existing console output
    if extracted_comments:
        print("\nExtracted Comments Preview:")
        
        def print_comment_tree(comments, level=0):
            for comment in comments:
                indent = "  " * level
                print(f"{indent}└─ Author: {comment['author']}")
                print(f"{indent}   Text: {comment['text'][:100]}...")
                if comment['more_replies']:
                    print(f"{indent}   More replies available: {comment['more_replies']}")
                if comment['replies']:
                    print_comment_tree(comment['replies'], level + 1)

        print_comment_tree(extracted_comments)
    else:
        print("No comments found.")