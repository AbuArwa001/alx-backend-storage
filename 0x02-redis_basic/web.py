#!/usr/bin/env python3
"""
Module containing a get_page function
"""
import redis
import requests
import time

# Initialize Redis connection
redis_conn = redis.Redis()


def get_page(url: str) -> str:
    """
    Get page for link
    """
    # Check if URL access count exists in Redis
    count_key = f"count:{url}"
    url_count = redis_conn.get(count_key)
    if url_count:
        redis_conn.incr(count_key)
    else:
        redis_conn.set(count_key, 1, ex=10)  # Cache with 10 second expiration

    # Fetch page content using requests module
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise exception for bad status codes
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL {url}: {e}")
        return ""
