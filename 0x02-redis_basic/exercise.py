#!/usr/bin/env python3
"""
Module contains a class to cache redis
Author: Khalfan Athman
"""
import redis
import uuid
from typing import Union, Callable, Optional
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """
    Prototype: def count_calls(method: Caallable) -> Callable:
    Returns a Callable
    """
    @wraps(method)
    def wrapper(self, *args, **kwds):
        """
        Prototype: def wrapper(self, *args, **kwds):
        Returns wrapper
        """
        key_m = method.__qualname__
        self._redis.incr(key_m)
        return method(self, *args, **kwds)
    return wrapper

class Cache:
    """
    Class containing a method to generate and set keys
    """
    def __init__(self):
        """
        Initialize the Cache class.

        This initializes a connection to a Redis database.
        Author: Khalfan Athman
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store data in the Redis cache and return the key.

        Parameters:
        data (Union[str, bytes, int, float]): The data to store in the cache.
            It can be of type str, bytes, int, or float.

        Returns:
        str: The key under which the data is stored.
        Author: Khalfan Athman
        """
        key = str(uuid.uuid4())  # Ensure key is a string
        self._redis.set(key, data)
        return key


    def get(self, key: str,
            fn: Optional[Callable] = None) -> Union[str, bytes, int, float]:
        """
        Convert data back to desired format
        """
        value = self._redis.get(key)
        return value if not fn else fn(value)

    def get_int(self, key):
        """
        automatically parametrize Cache.get
        """
        return self.get(key, int)

    def get_str(self, key):
        """
        automatically parametrize Cache.get
        """
        value = self._redis.get(key)
        return value.decode("utf-8")
