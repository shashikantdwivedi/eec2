import pymongo

# TODO - Replace DATABASE-URL with your mongoDB database url
db_connection = pymongo.MongoClient("DATABASE-URL")
database = db_connection["eec2"]
users = database["users"]
admin = database["admin"]

