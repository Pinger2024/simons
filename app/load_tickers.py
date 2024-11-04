# load_tickers.py
import os
import pandas as pd
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env

def load_tickers_to_mongo(csv_file):
    # Read the CSV file
    df = pd.read_csv(csv_file)

    # Connect to MongoDB
    mongo_uri = os.environ['MONGODB_CONNECTION_STRING']
    database_name = os.environ['DATABASE_NAME']
    client = MongoClient(mongo_uri)
    db = client[database_name]
    tickers_collection = db['tickers']

    # Insert records into MongoDB
    records = df.to_dict(orient='records')
    tickers_collection.insert_many(records)

    print(f"Inserted {len(records)} tickers into MongoDB collection 'tickers'.")

    client.close()

if __name__ == "__main__":
    csv_file = 'tickers.csv'
    load_tickers_to_mongo(csv_file)
