#!/usr/bin/env python3
""" Contains top_students function"""


def top_students(mongo_collection):
    """
    Sorts students according to avag score
    """
    avg_score = 0
    for student in mongo_collection.find({}):
        avg_score = 0
        for sub in student.get("topics"):
            avg_score += sub.get("score", 0)

        if avg_score:
            mongo_collection.update_one(
                {"name": student.get("name")},
                {"$set": {"averageScore": avg_score / 3}},
            )
    return list(mongo_collection.aggregate([{"$sort": {"averageScore": -1}}]))
