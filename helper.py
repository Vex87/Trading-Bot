from pymongo import MongoClient
from constants import DEFAULT_SESSION_DATA
import os

MONGO_TOKEN = os.getenv("TRADING_BOT_DB_TOKEN")
cluster = MongoClient(MONGO_TOKEN)
datastore = cluster["database0"]["sessions"]

# data

def attach_default_session_data(session_data):
    new_session_data = DEFAULT_SESSION_DATA.copy()
    for key in new_session_data.keys():
        if session_data.get(key):
            new_session_data[key] = session_data[key]
    return new_session_data

def get_session_data(start_time: int):
    session_data = datastore.find_one({"start_time": start_time})
    if session_data:
        session_data = attach_default_session_data(session_data)
    else:
        session_data = DEFAULT_SESSION_DATA.copy()
        session_data["start_time"] = start_time
        session_data = attach_default_session_data(session_data)
        datastore.insert_one(session_data)
    return session_data 

def save_session_data(session_data):
    datastore.update_one({"start_time": session_data["start_time"]}, {"$set": session_data})

# misc

def get_last_n_values(dic, n: int):
    new_dic = {}
    for i in list(dic)[len(dic) - n:]:
        new_dic[i] = dic.get(i)
    return new_dic

