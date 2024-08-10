from pymongo.mongo_client import MongoClient

import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

MONGO_DETAILS = os.getenv("MONGO_DETAILS")

client = AsyncIOMotorClient(MONGO_DETAILS)
database = client.zotero
item_collection = database.get_collection("items")


# connect to mongodb

# connect to mongodb
client = MongoClient("mongodb://localhost:27017/", username="admin", password="yxcv4321")

# ping database
# try:
#     # The ismaster command is cheap and does not require auth.
#     client.admin.command('ismaster')
#     print("Connected to MongoDB")
# except Exception as e:
#     print("Unable to connect to MongoDB: ", e)

# create database

db = client.library

# create collection

collection_name = db["library_collection"]

