#!/usr/bin/env python3
'''

log nginx stats

'''
from pymongo import MongoClient


def nginx_stats(logs):
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


def extra_stats(logs):
    '''gets top 10 stats'''
    print('IPs:')
    top_ips = logs.aggregate([
        {
            '$group': {
                '_id': '$ip',
                'count': {'$sum': 1}
            },
        },
        {
            '$sort': {'count': -1}
        },
        {
            '$limit': 10
        }
    ])
    for ip in top_ips:
        print(f'\t{ip["_id"]}: {ip["count"]}')


if __name__ == "__main__":
    client = MongoClient('mongodb://127.0.0.1:27017')
    logs = client.logs.nginx
    nginx_stats(logs=logs)
    extra_stats(logs=logs)
