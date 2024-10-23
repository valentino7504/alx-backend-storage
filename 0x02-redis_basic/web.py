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
    def data_cacher(url):
        '''wrapper for get_page'''
        res_key = f'result:{url}'
        html_content = cache.get(res_key).decode('utf-8')
        if html_content:
            return html_content
        count_key = f'count:{url}'
        cache.incr(count_key)
        res = fn(url)
        cache.set(res_key, ex=10, value=res)
        return res
    return data_cacher


@cache_responses
def get_page(url: str) -> str:
    '''expiring web cache'''
    return requests.get(url).text
