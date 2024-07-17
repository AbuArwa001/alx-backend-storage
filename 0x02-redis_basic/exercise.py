#!/usr/bin/env python3
"""
Module contains a class to cache redis
"""
import redis
import uuid
from typing import Union


class Cache:
    """
    Class containing a method to generate and set keys
    """
    def __init__(self):
        """
        Initialize the Cache class.

        This initializes a connection to a Redis database.
        """
        self._redis = redis.Redis()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store data in the Redis cache and return the key.

        Parameters:
        data (Union[str, bytes, int, float]): The data to store in the cache.
            It can be of type str, bytes, int, or float.

        Returns:
        str: The key under which the data is stored.
        """
        key = str(uuid.uuid4())  # Ensure key is a string
        self._redis.set(key, data)
        return key
