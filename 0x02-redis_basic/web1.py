#!/usr/bin/env python3
"""
Module containing a get_page function
"""
import requests
import redis
import functools

# Initialize Redis connection
redis_conn = redis.Redis()


def track_url_access(func):
    """
    Decorator to track URL access count in Redis.
    """
    @functools.wraps(func)
    def wrapper(url):
        # Track URL access count in Redis
        count_key = f"count:{url}"
        url_count = redis_conn.get(count_key)

        if url_count:
            # Increment the count if key exists
            redis_conn.incr(count_key)
        else:
            # Set the count to 1 and set expiration to 10 seconds
            redis_conn.set(count_key, 1, ex=10)

        # Return the result of the decorated function
        return func(url)

    return wrapper


@track_url_access
def get_page(url: str) -> str:
    """
    Fetch the content of the page at the given URL.
    """
    key_url = f"cached:{url}"
    cached_content = redis_conn.get(key_url)
    if cached_content == 1:
        ts = "time"
    print("{} was called {} {}:".format(url, cached_content.decode('utf-8'), ts))
    if cached_content:
        return cached_content
    response = requests.get(url)
    redis_conn.set(key_url, response.text, ex=10)
    return response.text
