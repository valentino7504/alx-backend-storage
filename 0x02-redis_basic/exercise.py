#!/usr/bin/env python3
'''

0 - Writing strings to Redis

'''
import redis
from typing import Union, Callable, Any
from uuid import uuid4
from functools import wraps


def count_calls(method: Callable) -> Callable:
    '''implements a function call counter'''
    @wraps(method)
    def counter(self, *args, **kwargs) -> Any:
        '''invokes the method'''
        key = method.__qualname__
        if isinstance(self._redis, redis.Redis):
            self._redis.incr(key)
        return method(self, *args, **kwargs)
    return counter


class Cache:
    '''Cache class'''
    def __init__(self) -> None:
        '''dunder init for Cache class'''
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        '''stores a value in the Redis db using a random uuid4 as key'''
        data_key = str(uuid4())
        self._redis.set(name=data_key, value=data)
        return data_key

    def get(self, key: str,
            fn: Callable = None) -> Union[str, bytes, int, float]:
        '''gets information from redis database and formats it'''
        if not key:
            return None
        data = self._redis.get(key)
        if fn and data:
            return fn(data)
        else:
            return data

    def get_str(self, key: str) -> str:
        '''parameterizes get with str method'''
        if not key:
            return None
        return self.get(key, lambda v: v.decode('utf-8'))

    def get_int(self, key: str) -> int:
        '''parameterizes get with int method'''
        if not key:
            return None
        return self.get(key, int)
