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
    function  tracking url access
    """
    @functools.wraps(func)
    def wrapper(url):
        """
        Wrapper function Track URL access count in Redis
        """
        # Track URL access count in Redis
        redis_conn.incr(count_key)
        count_key = f"count:{url}"
        url_count = redis_conn.get(count_key)
        if url_count:
            return url_count.decode('utf-8')
        else:
            html = func(url)
            redis_conn.setex(
                count_key, 1, 10, html
            )  # Cache with 10 second expiration
        return html

    return wrapper


@track_url_access
def get_page(url: str) -> str:
    """
    get_page function  tracking url access
    """
    return requests.get(url).text
