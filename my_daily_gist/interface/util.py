from django.conf import settings
import pymongo

def insert_gists(data_dict):

    mongo_client = pymongo.MongoClient(settings.MONGODB_HOST, settings.MONGODB_PORT)
    mongo_db = mongo_client[settings.MONGODB_NAME]
    mongo_collection = mongo_db[settings.MONGODB_COLLECTION_NAME]
    mongo_collection.delete_many({})

    mongo_collection.insert_many([d_d for d_d in data_dict ])

def load_gists():

    mongo_client = pymongo.MongoClient(settings.MONGODB_HOST, settings.MONGODB_PORT)
    mongo_db = mongo_client[settings.MONGODB_NAME]
    mongo_collection = mongo_db[settings.MONGODB_COLLECTION_NAME]

    return [gist for gist in mongo_collection.find({})]