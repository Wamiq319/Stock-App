import requests
import pandas as pd
from .. import setup_logger 

# Set up logging

logger = setup_logger("Stock-Utils")

# Function to fetch and process data based on the time frame
def fetch_stock_data(symbol, time_frame, api_key="X4VE8829GA6AZNHI"):
    base_url = "https://www.alphavantage.co/query"
    logger.info(f"Fetching stock data for symbol: {symbol}, time frame: {time_frame}")

    if time_frame == 'daily':
        function = "TIME_SERIES_DAILY"
        interval = None
    elif time_frame == '1hour':
        function = "TIME_SERIES_INTRADAY"
        interval = "60min"
    elif time_frame == '8hours':
        function = "TIME_SERIES_INTRADAY"
        interval = "60min"
    else:
        logger.error(f"Invalid time frame: {time_frame}")
        raise ValueError("Invalid time frame. Choose from '1hour', '8hours', or 'daily'.")

    url = f"{base_url}?function={function}&symbol={symbol}&apikey={api_key}"
    if interval:
        url += f"&interval={interval}"

    logger.debug(f"API URL constructed: {url}")
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        logger.debug("API response received successfully")
    except requests.exceptions.RequestException as e:
        logger.error(f"API request failed: {e}")
        raise

    # Check for errors or information messages in the API response
    if 'Error Message' in data:
        logger.error(f"API Error: {data['Error Message']}")
        raise ValueError(f"API Error: {data['Error Message']}")
    elif 'Information' in data:
        logger.warning(f"API Information: {data['Information']}")
        raise ValueError(f"API Information: {data['Information']}")
    elif 'Note' in data:
        logger.warning(f"API Note: {data['Note']}")
        raise ValueError(f"API Note: {data['Note']}")

    # Extract time series data
    if 'Time Series (60min)' in data:
        time_series = data['Time Series (60min)']
    elif 'Time Series (Daily)' in data:
        time_series = data['Time Series (Daily)']
    else:
        logger.error("Unexpected data structure in API response")
        raise ValueError("Error fetching data from API")

    # Convert to DataFrame
    df = pd.DataFrame.from_dict(time_series, orient='index')
    df = df.astype({'1. open': 'float', '2. high': 'float', '3. low': 'float', '4. close': 'float', '5. volume': 'int'})
    df.index = pd.to_datetime(df.index)

    # Resample data if required
    if time_frame == '8hours':
        logger.info("Resampling data for 8-hour intervals")
        df = df.resample('8H').agg({
            '1. open': 'first',
            '2. high': 'max',
            '3. low': 'min',
            '4. close': 'last',
            '5. volume': 'sum'
        })

    logger.info(f"Data fetched and processed for symbol: {symbol}, time frame: {time_frame}")
    return df
