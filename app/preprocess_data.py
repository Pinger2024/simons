# app/preprocess_data.py
import pandas as pd
import numpy as np

def preprocess_data(df):
    df.fillna(method='ffill', inplace=True)
    df.dropna(inplace=True)
    return df

def compute_features(df):
    # Moving Averages
    df['ma_short'] = df['close'].rolling(window=10).mean()
    df['ma_long'] = df['close'].rolling(window=50).mean()

    # RSI
    delta = df['close'].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=14).mean()
    avg_loss = loss.rolling(window=14).mean()
    rs = avg_gain / avg_loss
    df['rsi'] = 100 - (100 / (1 + rs))

    # MACD
    exp1 = df['close'].ewm(span=12, adjust=False).mean()
    exp2 = df['close'].ewm(span=26, adjust=False).mean()
    df['macd'] = exp1 - exp2
    df['signal_line'] = df['macd'].ewm(span=9, adjust=False).mean()

    # Momentum
    df['momentum'] = df['close'] - df['close'].shift(10)

    df.dropna(inplace=True)
    return df
