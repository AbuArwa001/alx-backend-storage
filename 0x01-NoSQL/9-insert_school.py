#!/usr/bin/env python3
"""
    Function that changes all topics of a
    school document based on the name
"""


def insert_school(mongo_collection, **kwargs):
    """
    Function that changes all topics of a
    school document based on the name
    """
    insert = mongo_collection.insert_one(kwargs)
    return insert.inserted_id
