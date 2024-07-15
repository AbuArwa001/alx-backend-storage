#!/usr/bin/env python3
""" lists all documents in a collection"""

def list_all(mongo_collection):
    """
    Lists all documents in a collection.
    
    Parameters:
    mongo_collection (pymongo.collection.Collection): The collection to list documents from.

    Returns:
    list: A list of all documents in the collection, or an empty list if the collection is empty.
    """
    return list(mongo_collection.find())
