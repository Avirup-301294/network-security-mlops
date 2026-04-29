import os
import urllib.parse
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# 1. Load the .env file
load_dotenv()

# 2. Get the RAW password from your .env
# Make sure your .env has: MONGO_DB_PASSWORD=your_actual_password
raw_password = os.getenv("MONGO_DB_PASSWORD") 

# 3. URL-encode ONLY the password
encoded_password = urllib.parse.quote_plus(raw_password)

# 4. Manually construct the URI using the encoded password
user = "avirup_db_user"
cluster = "network-security-cluste.wsw3lul.mongodb.net"
app_name = "network-security-cluster0"

uri = f"mongodb+srv://{user}:{encoded_password}@{cluster}/?appName={app_name}"

# 5. Connect
client = MongoClient(uri, server_api=ServerApi('1'))

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(f"Error: {e}")
