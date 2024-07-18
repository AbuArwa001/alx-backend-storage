#!/usr/bin/env python3
"""
Module contains a class to cache redis
Author: Khalfan Athman
"""

import redis
import uuid
from typing import Union, Callable, Optional, Any
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """
    Decorator that counts the number of calls to a method.

    Args:
        method (Callable): The method to decorate.

    Returns:
        Callable: The decorated method.
    """

    @wraps(method)
    def wrapper(self: Any, *args: Any, **kwargs: Any) -> Any:
        """
        Wrapper function to increment call count.

        Args:
            self (Any): The instance the method is called on.
            *args (Any): The positional arguments to the method.
            **kwargs (Any): The keyword arguments to the method.

        Returns:
            Any: The output of the original method.
        """
        key_m = method.__qualname__
        self._redis.incr(key_m)
        return method(self, *args, **kwargs)

    return wrapper


def call_history(method: Callable) -> Callable:
    """
    Decorator to store the history of inputs and outputs for a method.

    Args:
        method (Callable): The method to decorate.

    Returns:
        Callable: The decorated method.
    """

    @wraps(method)
    def wrapper(self: Any, *args: Any, **kwargs: Any) -> Any:
        """
        Wrapper function to add input and output history.

        Args:
            self (Any): The instance the method is called on.
            *args (Any): The positional arguments to the method.
            **kwargs (Any): The keyword arguments to the method.

        Returns:
            Any: The output of the original method.
        """
        input_key = method.__qualname__ + ":inputs"
        output_key = method.__qualname__ + ":outputs"
        self._redis.rpush(input_key, str(args))

        output = method(self, *args, **kwargs)

        self._redis.rpush(output_key, str(output))

        return output

    return wrapper


class Cache:
    """
    Class for caching data using Redis.
    """

    def __init__(self) -> None:
        """
        Initialize the Cache class.

        This initializes a connection to a Redis database.
        Author: Khalfan Athman
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
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

    def get(
        self, key: str, fn: Optional[Callable[[bytes], Any]] = None
    ) -> Union[str, bytes, int, float]:
        """
        Retrieve data from the Redis cache and optionally apply a
        conversion function.
        Parameters:
        key (str): The key under which the data is stored.
        fn (Optional[Callable[[bytes], Any]]):
            An optional function to apply to the data.

        Returns:
        Union[str, bytes, int, float]:
            The retrieved data, optionally converted.
        """
        value = self._redis.get(key)
        return value if not fn else fn(value)

    def get_int(self, key: str) -> Optional[int]:
        """
        Retrieve data from the Redis cache and convert it to an integer.

        Parameters:
        key (str): The key under which the data is stored.

        Returns:
        Optional[int]:
        The retrieved data as an integer, or None if conversion fails.
        """
        return self.get(key, int)

    def get_str(self, key: str) -> Optional[str]:
        """
        Retrieve data from the Redis cache and convert it to a string.

        Parameters:
        key (str): The key under which the data is stored.

        Returns:
        Optional[str]:
        The retrieved data as a string, or None if conversion fails.
        """
        value = self._redis.get(key)
        return value.decode("utf-8") if value else None


cache = Cache()


def replay(method: Callable) -> None:
    """
    Display the history of calls of a particular function.

    Parameters:
    method (Callable): The method to replay.
    """
    fun = method.__qualname__
    inputs = cache._redis.lrange(f"{fun}:inputs", 0, -1)
    outputs = cache._redis.lrange(f"{fun}:outputs", 0, -1)
    count = cache.get(fun)
    ts = "times"
    if count == 1:
        ts = "time"
    print(f"{fun} was called {count.decode('utf-8')} {ts}:")

    for input_key, output_key in zip(inputs, outputs):
        input_str = input_key.decode("utf-8")
        output_str = output_key.decode("utf-8")
        print(f"{fun}(*{input_str}) -> {output_str}")
