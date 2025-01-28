from urllib.parse import urlencode
import uuid

valid_sort_options = {'hot', 'new', 'top', 'rising'}

def generate_navigation_session_id():
    """Generate a new navigation session ID."""
    return str(uuid.uuid4())

def get_reddit_feed_url(
    subreddit: str,
    sort_by: str = "hot",
    feed_length: int = 10,
    after: str = "",
    time_filter: str = "DAY",
    view_type: str = "compactView"
) -> str:
    """
    Generate a Reddit feed URL with the specified parameters.
    
    Args:
        subreddit (str): Name of the subreddit
        sort_by (str): Sorting method ('hot', 'new', 'top', 'rising')
        feed_length (int): Number of posts to fetch
        after (str): Pagination token
        time_filter (str): Time filter ('HOUR', 'DAY', 'WEEK', 'MONTH', 'YEAR', 'ALL')
        view_type (str): View type ('compactView', 'cardView', 'classicView')
    
    Returns:
        str: Generated Reddit feed URL
    """
    # Validate sort_by parameter
    if sort_by not in valid_sort_options:
        raise ValueError(f"sort_by must be one of {valid_sort_options}")

    # Base URL components
    base_url = "https://www.reddit.com/svc/shreddit/community-more-posts"
    
    # Query parameters
    params = {
        'feedViewType': view_type,
        'after': after,
        't': time_filter,
        'name': subreddit,
        'navigationSessionId': generate_navigation_session_id(),
        'feedLength': feed_length
    }
    
    # Construct the full URL
    url = f"{base_url}/{sort_by}/?{urlencode(params)}"
    return url

def get_hot_posts_url(subreddit: str, **kwargs) -> str:
    """Get URL for hot posts in a subreddit."""
    return get_reddit_feed_url(subreddit, sort_by='hot', **kwargs)

def get_new_posts_url(subreddit: str, **kwargs) -> str:
    """Get URL for new posts in a subreddit."""
    return get_reddit_feed_url(subreddit, sort_by='new', **kwargs)

def get_top_posts_url(subreddit: str, **kwargs) -> str:
    """Get URL for top posts in a subreddit."""
    return get_reddit_feed_url(subreddit, sort_by='top', **kwargs)

def get_rising_posts_url(subreddit: str, **kwargs) -> str:
    """Get URL for rising posts in a subreddit."""
    return get_reddit_feed_url(subreddit, sort_by='rising', **kwargs)
