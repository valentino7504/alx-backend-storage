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
        res_key = f'cached:{url}'
        count_key = f'count:{url}'
        html_content = cache.get(res_key)
        cache.incr(count_key)
        if html_content:
            return html_content.decode('utf-8')
        res = fn(url)
        cache.setex(res_key, 10, res)
        return res
    return data_cacher


@cache_responses
def get_page(url: str) -> str:
    '''expiring web cache'''
    return requests.get(url).text
