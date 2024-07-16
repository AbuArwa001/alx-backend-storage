#!/usr/bin/env python3
"""
Module with a Function to list schools with specific topi
"""
def schools_by_topic(mongo_collection, topic):
    """
    Function to list schools with specific topi
    """
    return mongo_collection.find({"topics": {"$in": [topic]}})
