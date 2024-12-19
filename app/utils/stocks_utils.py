import requests
import pandas as pd
from datetime import datetime, timedelta
import traceback
from .. import setup_logger

logger = setup_logger("Stock-Utils")

# Alpaca API details
ALPACA_API_KEY = 'your_alpaca_api_key'
ALPACA_API_SECRET = 'your_alpaca_api_secret'
ALPACA_BASE_URL = 'https://data.alpaca.markets/v2/stocks/bars'

# Polygon API details
POLYGON_API_KEY = 'your_polygon_api_key'
POLYGON_URL = 'https://api.polygon.io/v2/aggs/ticker'

# Alpha Vantage API details
ALPHA_VANTAGE_API_KEY = 'X4VE8829GA6AZNHI'
ALPHA_VANTAGE_URL = 'https://www.alphavantage.co/query'


# Function to fetch Alpaca data
def fetch_alpaca_data(stock_symbol, timeframe):
    try:
        logger.debug(f"Fetching Alpaca data for {stock_symbol} with timeframe {timeframe}")

        end_date = datetime.utcnow()

        # Determine the start date based on the timeframe
        if timeframe == '1D':
            start_date = end_date - timedelta(days=1)
        elif timeframe == '1h':
            start_date = end_date - timedelta(hours=1)
        elif timeframe == '8h':
            start_date = end_date - timedelta(hours=8)
        else:
            start_date = end_date - timedelta(days=365)

        start_date_str = start_date.isoformat() + "Z"

        url = f"{ALPACA_BASE_URL}?symbols={stock_symbol}&timeframe={timeframe}&start={start_date_str}&limit=100&sort=desc"
        
        headers = {
            'APCA-API-KEY-ID': ALPACA_API_KEY,
            'APCA-API-SECRET-KEY': ALPACA_API_SECRET
        }
        
        response = requests.get(url, headers=headers)
        data = response.json()

        if 'bars' in data:
            df = pd.DataFrame(data['bars'])
            df['time'] = pd.to_datetime(df['timestamp'], unit='s')
            return df[['time', 'open', 'high', 'low', 'close', 'volume']]
        else:
            logger.error("Error fetching Alpaca data: Bars not found")
            raise Exception("Error fetching Alpaca data")

    except Exception as e:
        logger.error(f"Exception in fetch_alpaca_data: {e}\n{traceback.format_exc()}")
        raise


# Function to fetch Polygon data
def fetch_polygon_data(stock_symbol, timeframe):
    try:
        logger.debug(f"Fetching Polygon data for {stock_symbol} with timeframe {timeframe}")
        
        end_date = datetime.utcnow()

        if timeframe == '1D':
            start_date = end_date - timedelta(days=1)
        elif timeframe == '1h':
            start_date = end_date - timedelta(hours=1)
        elif timeframe == '8h':
            start_date = end_date - timedelta(hours=8)
        else:
            start_date = end_date - timedelta(days=365)

        start_date_str = start_date.isoformat()

        url = f"{POLYGON_URL}/{stock_symbol}/range/1/minute/{start_date_str}/{end_date.isoformat()}"

        params = {'apiKey': POLYGON_API_KEY}
        
        response = requests.get(url, params=params)
        data = response.json()

        if 'results' in data:
            df = pd.DataFrame(data['results'])
            df['time'] = pd.to_datetime(df['t'], unit='ms')
            return df[['time', 'o', 'h', 'l', 'c', 'v']]
        else:
            logger.error("Error fetching Polygon data: Results not found")
            raise Exception("Error fetching Polygon data")

    except Exception as e:
        logger.error(f"Exception in fetch_polygon_data: {e}\n{traceback.format_exc()}")
        raise


# Function to fetch Alpha Vantage data
def fetch_alpha_vantage_data(stock_symbol, timeframe):
    try:
        if timeframe == '1D':
            function = 'TIME_SERIES_DAILY'
        elif timeframe == '1h':
            function = 'TIME_SERIES_INTRADAY'
            interval = '60min'
        elif timeframe == '8h':
            function = 'TIME_SERIES_INTRADAY'
            interval = '240min'
        else:
            function = 'TIME_SERIES_DAILY'

        params = {
            'function': function,
            'symbol': stock_symbol,
            'apikey': ALPHA_VANTAGE_API_KEY
        }

        if function == 'TIME_SERIES_INTRADAY':
            params['interval'] = interval

        response = requests.get(ALPHA_VANTAGE_URL, params=params)
        data = response.json()
       

        if function == 'TIME_SERIES_DAILY' and 'Time Series (Daily)' in data:
            df = pd.DataFrame(data["Time Series (Daily)"]).T
            df.index = pd.to_datetime(df.index)
            df = df.sort_index(ascending=False)
            recent_26_data = df.head(26)
            recent_26_data = recent_26_data.reset_index().rename(columns={'index': 'Eastern-time-zone'})
            return recent_26_data

        elif function == 'TIME_SERIES_INTRADAY' and f'Time Series ({interval})' in data:
            df = pd.DataFrame(data[f'Time Series ({interval})']).T
            df['time'] = pd.to_datetime(df.index)
            df = df.sort_values(by='time', ascending=False)
            recent_26_data = df.head(26)
            recent_26_data = recent_26_data.reset_index().rename(columns={'index': 'Eastern-time-zone'})
            return recent_26_data
        else:
            raise Exception("Error fetching Alpha Vantage data")

    except Exception as e:
        logger.error(f"Exception in fetch_alpha_vantage_data: {e}\n{traceback.format_exc()}")
        raise


# Main function to fetch stock data based on the timeframe and stock symbol
def fetch_stock_data(stock_symbol, timeframe):
    try:
        
        logger.debug(f"Fetching stock data for {stock_symbol} with timeframe {timeframe}")

        # Switch-like logic to fetch data from different APIs
        if timeframe not in ['1h', '8h', '1D']:
            logger.error("Invalid timeframe provided.")
            raise Exception("Invalid timeframe")

        # Choose which API to fetch data from based on the timeframe
        if timeframe == '1D':
            # Choose one API based on preference, Alpaca or Polygon or Alpha Vantage
            Data = fetch_alpha_vantage_data(stock_symbol, timeframe) 
            return Data
        elif timeframe == '1h':
            # Fetch data from Polygon API for intraday (1 hour data)
            Data = fetch_alpha_vantage_data(stock_symbol, timeframe)
            return Data
        elif timeframe == '8h':
            # Fetch data from Alpha Vantage for 8-hour data
            Data = fetch_alpha_vantage_data(stock_symbol, timeframe)
            return Data

    except Exception as e:
        logger.error(f"Error fetching stock data: {e}\n{traceback.format_exc()}")
        return None
