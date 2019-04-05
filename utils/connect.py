import os
from elasticsearch import Elasticsearch
import pymongo
import json

def main():
    # print(os.getcwd())
    filepath = os.getcwd() + '/config.json'
    with open(filepath) as f :
        data = json.load(f)

    ES_HOST = data["ES_HOST"]

    config_data = [] 

    es = Elasticsearch(hosts = [ES_HOST])

    url = data["MONGO_HOST"]["url"]
    myclient = pymongo.MongoClient(url)
    dbname = data["Database"]
    db = myclient[dbname]
    INDEX_NAME = dbname

    feilds = data["Collections"]

    source = {

    }

    def filter(x,var,params):
        if not var in params:
            return 
        for i in x.copy():
            # print(i)
            if not i in params[var]:
                x.pop(i)
                # print(i)
        return x

    for change in db.watch():
        print(change)
        cur_id=change['documentKey']['_id']
        var = change['ns']['coll']
        # print(var)
        if(change["operationType"]=="delete"):
            if change['ns']['coll'] in feilds: 
                res = es.delete(index=INDEX_NAME,doc_type=var,id=cur_id)
                print(INDEX_NAME)
                # print(res['result'])
            continue
        source = change['fullDocument']
        y = filter(source,var,feilds)
        print(y)
        if(change["operationType"]=="insert"):
            if change['ns']['coll'] in feilds:
                res = es.index(index=INDEX_NAME,doc_type=var,body=y,id=cur_id) 
                # print(res['result'])   

        if(change["operationType"]=="replace"):
            if change['ns']['coll'] in feilds: 
                res = es.update(index=INDEX_NAME,doc_type=var,id=cur_id,body=y) 
                # print(res['result'])


if __name__ == "__main__":
    main()