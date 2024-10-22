#!/usr/bin/env python3
'''

updates the list of topics in a school

'''


def update_topics(mongo_collection, name, topics):
    '''updates topics in a school'''
    mongo_collection.update_many(
        filter={"name": name},
        update={"$set": {"topics": topics}}
    )
