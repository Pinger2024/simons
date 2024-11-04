# fetch_ohlcv_data.py
import os
import pandas as pd
import yfinance as yf
from pymongo import MongoClient
from datetime import datetime, timedelta
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def fetch_and_store_ohlcv():
    # Connect to MongoDB
    mongo_uri = os.environ['MONGODB_CONNECTION_STRING']
    database_name = os.environ['DATABASE_NAME']
    client = MongoClient(mongo_uri)
    db = client[database_name]
    tickers_collection = db['tickers']
    ohlcv_collection = db['ohlcv']

    # Get the list of unique tickers
    tickers = tickers_collection.distinct('ticker')
    print(f"Found {len(tickers)} tickers.")

    # Define the date range
    end_date = datetime.today()
    start_date = end_date - timedelta(days=730)  # Past 2 years

    # Fetch data for each ticker
    for i, ticker in enumerate(tickers):
        try:
            print(f"Fetching data for {ticker} ({i+1}/{len(tickers)})")
            data = yf.download(ticker, start=start_date.strftime('%Y-%m-%d'), end=end_date.strftime('%Y-%m-%d'), progress=False)
            data.reset_index(inplace=True)

            if data.empty:
                print(f"No data found for {ticker}")
                continue

            # Prepare data for MongoDB
            records = data.to_dict('records')
            for record in records:
                record['ticker'] = ticker  # Ensure consistency in field name
                record['Date'] = record['Date'].to_pydatetime()  # Convert Date to datetime

                # Avoid duplicate records by checking for ticker and date
                if not ohlcv_collection.find_one({'ticker': ticker, 'Date': record['Date']}):
                    ohlcv_collection.insert_one(record)

            print(f"Inserted {len(records)} records for {ticker}.")

            # Be polite to yFinance servers
            time.sleep(0.1)

        except Exception as e:
            print(f"Error fetching data for {ticker}: {e}")

    client.close()
    print("Data fetching complete.")

if __name__ == "__main__":
    fetch_and_store_ohlcv()
