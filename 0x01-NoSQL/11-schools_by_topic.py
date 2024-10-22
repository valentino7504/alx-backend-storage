#!/usr/bin/env python3
'''

11-schools_by_topic

'''


def schools_by_topic(mongo_collection, topic):
    '''get all schools that offer a topic'''
    cursor = mongo_collection.find({"topics": topic})
    return list(cursor)
