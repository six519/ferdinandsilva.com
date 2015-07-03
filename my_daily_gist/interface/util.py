from django.conf import settings
import pymongo

def insert_gists(data_dict):

    mongo_client = pymongo.MongoClient(settings.MONGODB_HOST, settings.MONGODB_PORT)
    mongo_db = mongo_client[settings.MONGODB_NAME]
    mongo_collection = mongo_db[settings.MONGODB_COLLECTION_NAME]
    mongo_collection.delete_many({})

    dt = []

    for d_d in data_dict:

        tmp = {}
        tmp.update(d_d["files"])

        d_d["files"] = {}

        for k,v in tmp.items():
            d_d["files"][k.replace(".", "_")] = v

        dt.append(d_d)

    if len(dt) > 0:
        mongo_collection.insert_many(dt)

    mongo_client.close()

def load_gists():

    ret = []
    mongo_client = pymongo.MongoClient(settings.MONGODB_HOST, settings.MONGODB_PORT)
    mongo_db = mongo_client[settings.MONGODB_NAME]
    mongo_collection = mongo_db[settings.MONGODB_COLLECTION_NAME]
    ret = [gist for gist in mongo_collection.find({})]
    mongo_client.close()

    return ret