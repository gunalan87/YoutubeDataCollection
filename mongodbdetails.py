import pymongo
import os
from dotenv import load_dotenv
from pathlib import Path
from pprint import pprint
import pandas as pd
class mongodbdetails:
    def __init__(self):
        dotenv_path = Path('.env')
        load_dotenv(dotenv_path=dotenv_path)
        self.mongoconnurl = os.getenv("mongoconnurl")
        self.dbname = os.getenv("dbname")
        _conn_obj = pymongo.MongoClient(self.mongoconnurl)
        _dbname = _conn_obj[self.dbname] #USE DBS
        self._channel_collection = _dbname['channels'] 
    def add_data(self,channel_data):
        recid = self._channel_collection.insert_one(channel_data)
        return recid
    def get_all_channel_names(self):
        channel_names = []
        for icn in self._channel_collection.find():
            channel_names.append(icn['channel_name'])
        
        return channel_names
    def get_channel_data(self,channel_name):
        channel_result = self._channel_collection.find_one({"channel_name": channel_name})
        return channel_result
