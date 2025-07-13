#!/usr/bin/env python3
"""
Module containing a get_page function
"""
import functools
import requests
import redis

# Assuming you have Redis client already configured
redis_conn = redis.Redis()


def track_url_access(func):
    @functools.wraps(func)
    def wrapper(url: str) -> str:
        count_key = f"count:{url}"
        redis_conn.incr(count_key)
        return func(url)
    return wrapper


@track_url_access
def get_page(url: str) -> str:
    """
    Fetch the content of the page at the given URL.
    Caches it in Redis for 10 seconds and tracks
    how many times the URL was accessed.
    """
    cache_key = f"cached:{url}"
    count_key = f"count:{url}"

    # Try to get cached content
    cached_content = redis_conn.get(cache_key)

    if cached_content:
        content = cached_content.decode("utf-8")
    else:
        # If not cached, fetch it from the internet
        try:
            response = requests.get(url)
            if response.status_code != 200:
                print(f"Failed to fetch {url}: {response.status_code}")
                return None
            content = response.text
            redis_conn.set(cache_key, content, ex=10)  # cache for 10 seconds
        except Exception as e:
            print(f"Error fetching URL {url}: {e}")
            return None

    # Get access count
    count = int(redis_conn.get(count_key) or 0)
    ts = "time" if count == 1 else "times"
    print(f"{url} was called {count} {ts}:")

    return content
