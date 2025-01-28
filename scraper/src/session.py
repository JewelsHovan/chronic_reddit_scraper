import time
import asyncio
from config.constants import REQUEST_DELAY

class RateLimiter:
    """
    A rate limiter class that controls the frequency of requests.

    This class uses a token bucket algorithm to limit the number of requests
    made within a certain time frame. It ensures that the scraper does not
    exceed the allowed request rate, preventing potential issues with the
    target website.
    """
    def __init__(self, max_tokens, refresh_rate):
        """
        Initializes the RateLimiter with a maximum number of tokens and a refresh rate.

        Args:
            max_tokens (int): The maximum number of tokens the bucket can hold.
            refresh_rate (float): The time in seconds it takes to refill the bucket to max_tokens.
        """
        self.max_tokens = max_tokens
        self.tokens = max_tokens
        self.refresh_rate = refresh_rate
        self.last_refresh = time.time()
        self.lock = asyncio.Lock()

    async def acquire(self):
        """
        Acquires a token from the bucket, waiting if necessary.

        This method will block until a token is available, ensuring that the
        request rate is within the defined limits. It also adds a delay after
        acquiring a token to further control the request rate.
        """
        async with self.lock:
            current_time = time.time()
            time_passed = current_time - self.last_refresh
            
            # Refresh tokens if enough time has passed
            if time_passed >= self.refresh_rate:
                self.tokens = self.max_tokens
                self.last_refresh = current_time
            
            # Wait if no tokens available
            while self.tokens <= 0:
                await asyncio.sleep(0.1)
                current_time = time.time()
                time_passed = current_time - self.last_refresh
                if time_passed >= self.refresh_rate:
                    self.tokens = self.max_tokens
                    self.last_refresh = current_time
            
            self.tokens -= 1
            await asyncio.sleep(REQUEST_DELAY)  # Add delay between requests
