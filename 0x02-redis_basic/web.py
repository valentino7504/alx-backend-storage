#!/usr/bin/env python3
'''

implementing a web cache tracker

'''
import redis
import requests
from functools import wraps
from typing import Callable


cache = redis.Redis()
cache.flushdb()


def cache_responses(fn: Callable) -> Callable:
    '''implements a response count'''
    @wraps(fn)
    def data_cacher(url: str) -> str:
        '''wrapper for get_page'''
        html_content = cache.get(url)
        if html_content:
            return html_content.decode('utf-8')
        return fn(url)
    return data_cacher


@cache_responses
def get_page(url: str) -> str:
    '''expiring web cache'''
    response = requests.get(url).text
    cache.incr(f'count:{url}')
    cache.setex(url, 10, response)
    return response
