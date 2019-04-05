import os
from elasticsearch import Elasticsearch
import pymongo
import json

print(os.getcwd())
print("sync")
filepath = os.getcwd() + '/config.json'
with open(filepath) as f :
    data = json.load(f)

ES_HOST = data["ES_HOST"]

from bson import Binary, Code
from bson.json_util import dumps
from bson.objectid import ObjectId

def main():
    print("running sync......")
    config_data = []

    es = Elasticsearch(hosts = [ES_HOST])

    url = data["MONGO_HOST"]["url"]
    myclient = pymongo.MongoClient(url)
    test = data["Database"]
    db = myclient[test]

    body=[]
    collection = data["Collections"]
    print(collection)

    def filter(x,var,params):
        for i in x.copy():
            if not i in params[var]:
                x.pop(i)
        return x

    def call(cursor):
        for x in cursor:
            body.append(x)
            cur_id = str(x["_id"])
            x.pop("_id")
            print(x)
            print("x")
            x = filter(x,col.name,collection)
            res = es.index(index=db.name,doc_type=col.name,id=cur_id,body=x)
            # print(res)

    def paging(col,pagesize,records):
        pages = records//pagesize + 1
        for i in range(1,pages):
            cursor = col.find().skip(pagesize*(i-1)).limit(pagesize)
            call(cursor)

    for i in collection: 
        col = db[i]
        print(col)
        records = col.count()
        pagesize = 1
        paging(col,pagesize,records)

    res = es.search(index=db.name,doc_type=col.name)

    for hit in res['hits']['hits']:
        y = hit['_id']
        print(hit['_id'])
        cnt = col.count_documents({"_id": ObjectId(y)})
        if cnt==0:
            res2 = es.delete(index=db.name,doc_type=col.name,id=y) 
            print(res2)

    request_body = {
            "mappings" : {
                
            }
        }

    coll = []

    for i in data.keys():
        coll.append(i)
        request_body["mappings"][i] = {
                    "_source" : {
                        "includes" : data[i]
                    }
                }

if __name__ == "__main__":
    main()