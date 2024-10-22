#!/usr/bin/env python3
'''

log nginx stats

'''
from pymongo import MongoClient
from pymongo.collection import Collection


def nginx_stats(logs: Collection):
    '''prints stats of nginx logs in mongo db'''
    print(f'{logs.count_documents({})} logs')
    print('Methods:')
    for method in ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']:
        method_count = logs.count_documents({"method": method})
        print(f'\tmethod {method}: {method_count}')
    status_checks = logs.count_documents({
        "method": "GET",
        "path": "/status"
    })
    print(f'{status_checks} status check')


if __name__ == "__main__":
    client = MongoClient('mongodb://127.0.0.1:27017')
    logs = client.logs.nginx
    nginx_stats(logs=logs)
