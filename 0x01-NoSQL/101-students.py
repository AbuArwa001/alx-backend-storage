#!/usr/bin/env python3
""" Contains top_students function"""


def top_students(mongo_collection):
    """
    Sorts students according to avag score
    """
    return mongo_collection.aggregate(
        [
            {
                "$project": {
                    "_id": 1,
                    "name": 1,
                    "averageScore": {"$avg": "$topics.score"},
                }
            },
            {"$sort": {"averageScore": -1}},
        ]
    )
