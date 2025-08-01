from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("MONGODB_DB_NAME")

client = AsyncIOMotorClient(MONGO_URI)
db = client[DB_NAME]
