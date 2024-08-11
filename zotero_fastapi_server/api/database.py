# MongoDB connection

import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

client = AsyncIOMotorClient(MONGO_URI)

database = client.zotero
item_collection = database.get_collection("items")

# ping database
# try:
#     # The ismaster command is cheap and does not require auth.
#     client.admin.command('ismaster')
#     print("Connected to MongoDB")
# except Exception as e:
#     print("Unable to connect to MongoDB: ", e)

