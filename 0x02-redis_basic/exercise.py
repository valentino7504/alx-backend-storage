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


def call_history(method: Callable) -> Callable:
    '''implements a function call history'''
    @wraps(method)
    def history(self, *args, **kwargs) -> Any:
        '''invokes the history'''
        method_name = method.__qualname__
        in_key = f'{method_name}:inputs'
        out_key = f'{method_name}:outputs'
        inputs = str(args)
        outputs = method(self, *args, **kwargs)
        self._redis.rpush(in_key, inputs)
        self._redis.rpush(out_key, outputs)
        return outputs
    return history


def replay(method: Callable) -> None:
    '''displays the history of a function call'''
    method_name = method.__qualname__
    cache: Cache = method.__self__
    inputs = cache._redis.lrange(f'{method_name}:inputs', 0, -1)
    output = cache._redis.lrange(f'{method_name}:outputs', 0, -1)
    print(f'{method_name} was called {cache.get_int(method_name)} times:')
    for i, o in zip(inputs, output):
        ins = i.decode('utf-8')
        out = o.decode('utf-8')
        print(f'Cache.store(*{ins}) -> {out}')


class Cache:
    '''Cache class'''
    def __init__(self) -> None:
        '''dunder init for Cache class'''
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
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
