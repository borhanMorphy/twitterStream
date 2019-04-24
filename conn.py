from pymongo import MongoClient

def get_client(user, pwd, host, port, db):
    uri = "mongodb://%s:%s/?authSource=%s"%(host, port, db)
    return MongoClient(uri)


def insert_to(cli, db_name, collection_name, doc):
    cli[db_name][collection_name].insert_one(doc)
