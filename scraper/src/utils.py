def extract_post_id(url):
    """
    Extracts the post ID from a Reddit URL.

    The post ID is typically in the format 't3_xxxxxxxx', where 'xxxxxxxx' is a unique identifier.
    This function parses the URL to extract this ID.

    Args:
        url (str): The Reddit URL of the post, expected to contain '/comments/'.

    Returns:
        str: The extracted post ID (e.g., 't3_abc123') if found, otherwise None.
    """
    try:
        return f"t3_{url.split('/comments/')[1].split('/')[0]}"
    except IndexError:
        return None
    

def print_comment_tree(comments, level=0, max_comments=3, current_count=0):
    """
    Recursively prints a tree-like structure of comments, with a limit on the number of comments displayed.

    This function is used to preview comments, showing a hierarchical structure with indentation.
    It limits the number of comments displayed at each level to avoid overwhelming the output.

    Args:
        comments (list): A list of comment dictionaries, each containing 'author', 'text', and 'replies'.
        level (int, optional): The current level of indentation (0 for top-level comments). Defaults to 0.
        max_comments (int, optional): The maximum number of comments to display at each level. Defaults to 3.
        current_count (int, optional): The current count of comments displayed at the current level. Defaults to 0.

    Returns:
        int: The updated count of comments displayed at the current level.
    """
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