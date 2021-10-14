from pymongo import MongoClient

client = MongoClient("mongodb://root:example@practices4ml-db:27017")
db = client.my_database
