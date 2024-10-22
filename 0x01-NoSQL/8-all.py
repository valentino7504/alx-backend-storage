#!/usr/bin/env python3
'''

gets all documents in a collection

'''


def list_all(mongo_collection):
    return mongo_collection.find()
