#!/usr/bin/env python3
'''

implementing a web cache tracker

'''
import redis
import requests
from functools import wraps
from typing import Callable


cache = redis.Redis()


def cache_responses(fn: Callable) -> Callable:
    '''implements a response count'''
    @wraps(fn)
    def data_cacher(url):
        '''wrapper for get_page'''
        count_key = f'count:{url}'
        cache.incr(count_key)
        res = fn(url)
        cache.set(f'result:{url}', ex=10, value=res)
        cache.set(count_key, 0)
        return res
    return data_cacher


@cache_responses
def get_page(url: str) -> str:
    '''expiring web cache'''
    return requests.get(url).text
