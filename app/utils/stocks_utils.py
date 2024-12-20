import requests
import pandas as pd
from datetime import datetime, timedelta
import traceback
from .. import setup_logger

# Logger setup
logger = setup_logger("Stock-Utils")

# Alpaca API details
ALPACA_API_KEY = 'PKB57FN6PC18Q3MUF2PE'
ALPACA_API_SECRET = 'zmX3oNYBrA4AqbOtfSxxXnvNdGccDeVHfQl5uzha'
ALPACA_BASE_URL = 'https://data.alpaca.markets/v2/stocks/bars'

# Alpha Vantage API details
ALPHA_VANTAGE_API_KEY = 'X4VE8829GA6AZNHI'
ALPHA_VANTAGE_URL = 'https://www.alphavantage.co/query'


def fetch_alpaca_data(stock_symbol, timeframe_hours, interval_hours):
    """
    Fetches stock data from Alpaca API.

    :param stock_symbol: Symbol of the stock.
    :param timeframe_hours: The timeframe for which to fetch data in hours.
    :param interval_hours: Interval for the data in hours.
    :return: JSON response with stock data.
    """
    try:
        logger.debug(f"Fetching Alpaca data for {stock_symbol} with timeframe {timeframe_hours} hours")

        # Calculate the start time for fetching historical data
        current_time = datetime.utcnow()
        total_time_range = timedelta(hours=interval_hours * 100)
        start_date = current_time - total_time_range
        start_date_str = start_date.isoformat() + "Z"  # Convert to ISO format with 'Z' for UTC

        # Construct the API URL
        url = f"{ALPACA_BASE_URL}?symbols={stock_symbol}&timeframe={timeframe_hours}H&start={start_date_str}&limit=100&sort=desc"
        logger.debug(f"API URL: {url}")

        # Set headers for API request
        headers = {
            'APCA-API-KEY-ID': ALPACA_API_KEY,
            'APCA-API-SECRET-KEY': ALPACA_API_SECRET
        }

        # Make the API request
        response = requests.get(url, headers=headers)
        response.raise_for_status() 
        response = response.json()
        next_page_token = response.get('next_page_token')
        Data = response['bars'][stock_symbol]
        while next_page_token:
            url = f"{ALPACA_BASE_URL}?symbols={stock_symbol}&timeframe={timeframe_hours}H&start={start_date_str}&limit=100&sort=desc&page_token={next_page_token}"
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            response = response.json()
            next_page_token = response.get('next_page_token')
            data = response['bars'][stock_symbol]
            Data.extend(data)
        
        return Data
    except Exception as e:
        logger.error(f"An error occurred while fetching Alpaca data: {str(e)}")
        raise


def fetch_alpha_vantage_data(stock_symbol, timeframe):
    """
    Fetches stock data from Alpha Vantage API.

    :param stock_symbol: Symbol of the stock.
    :param timeframe: Timeframe for which to fetch data (1D, 1h, or 8h).
    :return: DataFrame with the latest stock data.
    """
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
        response.raise_for_status()  # Raise error for bad response
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


def fetch_stock_data(stock_symbol, timeframe):
    """
    Main function to fetch stock data based on the given timeframe.

    :param stock_symbol: Symbol of the stock.
    :param timeframe: Timeframe for which to fetch data (1h, 8h, or 1D).
    :return: Data from the selected API (Alpaca or Alpha Vantage).
    """
    try:
       
        # Validate timeframe
        if timeframe not in ['1H', '8H', '1D','23H']:
            logger.error("Invalid timeframe provided.")
            raise ValueError("Invalid timeframe")

        # Fetch data based on the timeframe
        if timeframe == '1D':
            data = fetch_alpha_vantage_data(stock_symbol,timeframe)
            return data
        elif timeframe == '23H':
            data = fetch_alpaca_data(stock_symbol, 23,23)
            return data
        elif timeframe == '1h':
            data = fetch_alpaca_data(stock_symbol, 1,1)
            return data
        elif timeframe == '8h':
            data = fetch_alpaca_data(stock_symbol, 8,8)
            return data

    except Exception as e:
        logger.error(f"Error fetching stock data: {e}\n{traceback.format_exc()}")
        return None
