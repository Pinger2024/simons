# load_tickers.py
import os
import pandas as pd
from pymongo import MongoClient, errors
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def load_tickers_to_mongo(csv_file):
    # Connect to MongoDB
    mongo_uri = os.environ['MONGODB_CONNECTION_STRING']
    database_name = os.environ['DATABASE_NAME']
    client = MongoClient(mongo_uri)
    db = client[database_name]
    tickers_collection = db['tickers']

    # Read the CSV file
    df = pd.read_csv(csv_file)

    # Ensure ticker field is consistent
    if 'Ticker' in df.columns:
        df.rename(columns={'Ticker': 'ticker'}, inplace=True)

    # Insert records, avoiding duplicates
    inserted_count = 0
    for record in df.to_dict(orient='records'):
        # Check if the ticker already exists
        if not tickers_collection.find_one({'ticker': record['ticker']}):
            tickers_collection.insert_one(record)
            inserted_count += 1

    print(f"Inserted {inserted_count} new tickers into MongoDB collection 'tickers'.")
    client.close()

if __name__ == "__main__":
    csv_file = 'tickers.csv'
    load_tickers_to_mongo(csv_file)
