from pymongo.mongo_client import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()
# the uri is the connection string to the database, get it from the environment variables
uri = os.getenv("DATABASE_URL")

# Create a new client and connect to the server
client = MongoClient(uri)

db = client.blog_db

blog_collection = db["blogs"]
users_collection = db["users"]
