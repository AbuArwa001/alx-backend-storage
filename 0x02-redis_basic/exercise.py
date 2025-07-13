#!/usr/bin/env python3
"""
Module contains a class to cache redis
Author: Khalfan Athman
"""
import redis
import uuid
from typing import Union, Callable, Optional, Any, AnyStr
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
    Class containing a method to generate and set keys
    """

    def __init__(self, host: str = 'localhost', port: int = 6379):
        """
        Initialize the Cache class.

        This initializes a connection to a Redis database.
        Author: Khalfan Athman
        """
        try:
            self._redis = redis.Redis(host=host, port=port)
            self._redis.ping()  # Check if the connection is successful
            self._redis.flushdb()
        except redis.exceptions.ConnectionError as e:
            pass

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store data in the Redis cache and return a unique key.

        Parameters:
        ----------
        data : Union[str, bytes, int, float]
            The data to store in the Redis cache. It can be a string, bytes, integer, or float.

        Returns:
        -------
        str
            A UUID string key under which the data is stored in Redis.

        Notes:
        -----
        - The key is generated using `uuid.uuid4()` to ensure uniqueness.
        - The data is stored using Redis `SET` command.
        
        Example:
        -------
        >>> cache = Cache()
        >>> key = cache.store("Hello Redis")
        >>> print(key)  # e.g., '3f50b0f2-1df3-4cb9-8d91-0b2cf416cf6a'

        Author:
        -------
        Khalfan Athman
        """
        key: str = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    # @call_history
    # @count_calls
    # def store(self, data: Union[AnyStr, int, float]) -> str:
    #     """
    #     Store data in the Redis cache and return the key.

    #     Parameters:
    #     data (Union[str, bytes, int, float]): The data to store in the cache.
    #         It can be of type str, bytes, int, or float.

    #     Returns:
    #     str: The key under which the data is stored.
    #     Author: Khalfan Athman
    #     """
    #     key = str(uuid.uuid4())  # Ensure key is a string
    #     self._redis.set(key, data)
    #     return key

    def get(
        self, key: str, fn: Optional[Callable] = None
    ) -> Union[str, bytes, int, float]:
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


cache = Cache()


# def replay(method: Callable) -> None:
#     # inputs = cache._redis.lrange("{}:
# inputs".format(method.__qualname__), 0, -1)
#     outputs = cache._redis.lrange("{}:outputs"
# .format(method.__qualname__), 0, -1)
#     count =  cache.get(method.__qualname__)
#     print("{} was called {} times:".format(method, count))
#     for key in outputs:
#         print("{}(*{}) -> {} times:".
# format(method, cache.get_str(key), key.decode('utf-8')))

def replay(method: Callable) -> None:
    """
    Display the history of calls of a particular function.
    """
    fun = method.__qualname__
    inputs = cache._redis.lrange("{}:inputs".format(fun), 0, -1)
    outputs = cache._redis.lrange("{}:outputs".format(fun), 0, -1)
    count = cache.get(fun)
    ts = "times"
    if count == 1:
        ts = "time"
    print("{} was called {} {}:".format(fun, count.decode('utf-8'), ts))

    for input_key, output_key in zip(inputs, outputs):
        input_str = input_key.decode("utf-8")
        output_str = output_key.decode("utf-8")
        print("{}(*{}) -> {}".format(fun, input_str, output_str))

# def replay(method: Callable) -> None:
#     """
#     Display the history of calls of a particular function.
#     """
#     r = redis.Redis()
#     inputs = r.lrange(f"{method.__qualname__}:inputs", 0, -1)
#     outputs = r.lrange(f"{method.__qualname__}:outputs", 0, -1)
#     count = len(input)
#     times_str = "times"
#     if count == 1:
#         times_str = "times"
#     print(
#         f"{method.__qualname__} was called {count
#                                             .decode('utf-8')} {times_str}: "
#     )

#     for input_key, output_key in zip(inputs, outputs):
#         input_str = input_key.decode("utf-8")
#         output_str = output_key.decode("utf-8")
#         print(f"{method.__qualname__}(*({input_str},)) -> {output_str}"
