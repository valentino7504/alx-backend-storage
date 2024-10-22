#!/usr/bin/env python3
'''

inserts a new document in a collection

'''


def insert_school(mongo_collection, **kwargs):
    '''inserts a school in a collection'''
    return mongo_collection.insert_one(kwargs).inserted_id
