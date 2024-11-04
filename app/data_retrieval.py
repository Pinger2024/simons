# app/data_retrieval.py
import os
from pymongo import MongoClient
import pandas as pd

def fetch_data(symbol):
    client = MongoClient(os.environ['MONGODB_CONNECTION_STRING'])
    db = client[os.environ['DATABASE_NAME']]
    collection = db[os.environ['COLLECTION_NAME']]

    cursor = collection.find({'symbol': symbol})
    df = pd.DataFrame(list(cursor))

    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)
    df.sort_index(inplace=True)
    client.close()
    return df
