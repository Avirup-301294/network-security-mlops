import os
import sys
import json
import certifi
import pandas as pd
import numpy as np
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

import urllib.parse
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

from dotenv import load_dotenv

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

ca=certifi.where()

class NetworkDataExtract():
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def csv_to_json_convertor(self,file_path):
        try:
            data=pd.read_csv(file_path)
            data.reset_index(drop=True,inplace=True)
            records=list(json.loads(data.T.to_json()).values())
            return records
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def insert_data_mongodb(self,records,database,collection):
        try:
            self.database=database
            self.collection=collection
            self.records=records

            self.mongo_client=MongoClient(uri, server_api=ServerApi('1'))
            self.database = self.mongo_client[self.database]
            
            self.collection=self.database[self.collection]
            self.collection.insert_many(self.records)
            return(len(self.records))
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
if __name__=='__main__':
    FILE_PATH="Network_Data/phisingData.csv"
    DATABASE="network-security-db"
    Collection="NetworkData"
    networkobj=NetworkDataExtract()
    records=networkobj.csv_to_json_convertor(file_path=FILE_PATH)
    print(records)
    no_of_records=networkobj.insert_data_mongodb(records,DATABASE,Collection)
    print(no_of_records)
        