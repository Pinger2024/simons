# app/scheduler.py
import os
import schedule
import time
from datetime import datetime
from data_retrieval import fetch_data
from preprocess_data import preprocess_data, compute_features
from genetic_algorithm import run_ga
from backtest_strategy import backtest_strategy

def job():
    print(f"Job started at {datetime.now()}")
    symbol = os.environ.get('SYMBOL', 'AAPL')
    df = fetch_data(symbol)
    df = preprocess_data(df)
    df = compute_features(df)
    best_params = run_ga(df)
    final_value = backtest_strategy(df, best_params)
    print(f"Optimized Parameters for {symbol}: {best_params}")
    print(f"Final Portfolio Value: {final_value}")
    # Here you can save results to a database or file
    print(f"Job completed at {datetime.now()}")

def run_scheduler():
    schedule_interval = int(os.environ.get('SCHEDULE_INTERVAL', 60))  # in minutes
    schedule.every(schedule_interval).minutes.do(job)
    job()  # Run once at startup
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    run_scheduler()
