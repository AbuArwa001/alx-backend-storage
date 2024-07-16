#!/usr/bin/env python3
"""
MODULE TO provides some stats about Nginx logs stored in MongoDB:
"""
from pymongo import MongoClient

if __name__ == "__main__":
    client = MongoClient("mongodb://127.0.0.1:27017")
    logs = client.logs.nginx
    status = logs.count_documents({"method": "GET", "path": "/status"})
    print("{} logs".format(logs.count_documents({})))
    print("Methods:")
    print("\tmethod GET: {}".format(logs.count_documents({"method": "GET"})))
    print("\tmethod POST: {}".format(logs.count_documents({"method": "POST"})))
    print("\tmethod PUT: {}".format(logs.count_documents({"method": "PUT"})))
    print(
        "\tmethod PATCH: {}".format(logs.count_documents({"method": "PATCH"}))
    )
    print(
        "\tmethod DELETE: {}".format(
            logs.count_documents({"method": "DELETE"})
        )
    )
    print("{} status check".format(status))
    print("IPs:")
    res = logs.aggregate([
        {
            "$group":
            {
                "_id": "$ip",
                "count": {"$sum": 1}
            }
         },
        {"$sort": {"count": -1}},
        {"$limit": 10},
        {"$project": {
            "_id": 0,
            "ip": "$_id",
            "count": 1
        }}
    ])
    for ip in res:
        print(f"\t{ip.get('ip')}: {ip.get('count')}")
