# You could expose important items at the package level
from .headers import REDDIT_HEADERS
from .constants import MAX_WORKERS, RATE_LIMIT_REQUESTS, TOKEN_REFRESH_RATE, CHECKPOINT_INTERVAL

__all__ = ['REDDIT_HEADERS', 'MAX_WORKERS', 'RATE_LIMIT_REQUESTS', 'TOKEN_REFRESH_RATE', 'CHECKPOINT_INTERVAL']