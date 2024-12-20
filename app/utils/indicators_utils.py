import pandas as pd
from .. import setup_logger

# Logger setup for production and debug
logger = setup_logger("INDICATORS-UTILS")

def calculate_rsi(df, period=14):
    """
    Calculate the RSI (Relative Strength Index) for the given DataFrame using the first 'period' rows.
    
    :param df: A pandas DataFrame containing at least the 'Close' price column.
    :param period: The number of periods to use for RSI calculation (default is 14).
    :return: The latest RSI value as an integer.
    """
    logger.debug("Starting RSI calculation")
    try:
        # Ensure necessary columns are present and limit to the first 'period' rows
        df = df[['Close']].head(period)
        # Calculate price differences (delta), gains, and losses
        delta = df['Close'].diff()
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)

        # Calculate the average gain and loss
        avg_gain = gain.rolling(window=period, min_periods=1).mean()
        avg_loss = loss.rolling(window=period, min_periods=1).mean()

        # Calculate RSI
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))

        # Log the calculated RSI value
        rsi_value = int(rsi.iloc[-1])
        logger.info(f"RSI calculated: {rsi_value}")
        return rsi_value
    except Exception as e:
        logger.error(f"Error in RSI calculation: {e}")
        raise

def calculate_macd(df, fast_period=12, slow_period=26, signal_period=9):
    """
    Calculate the MACD (Moving Average Convergence Divergence) for the given DataFrame using the first 'period' rows.
    
    :param df: A pandas DataFrame containing at least the 'Close' price column.
    :param fast_period: The period for the fast EMA (default is 12).
    :param slow_period: The period for the slow EMA (default is 26).
    :param signal_period: The period for the signal line (default is 9).
    :return: The latest MACD value as an integer.
    """
    logger.debug("Starting MACD calculation")
    try:
        # Ensure necessary columns are present and limit to the first 'slow_period' rows
        df = df[['Close']].head(slow_period)
        print(df)

        # Calculate the fast and slow EMAs
        fast_ema = df['Close'].ewm(span=fast_period, adjust=False).mean()
        slow_ema = df['Close'].ewm(span=slow_period, adjust=False).mean()

        # Calculate the MACD line and signal line
        macd = fast_ema - slow_ema
        signal_line = macd.ewm(span=signal_period, adjust=False).mean()

        # Calculate the MACD histogram
        macd_histogram = macd - signal_line

        # Log the calculated MACD value
        macd_value = int(macd_histogram.iloc[-1])
        logger.info(f"MACD calculated: {macd_value}")
        return macd_value
    except Exception as e:
        logger.error(f"Error in MACD calculation: {e}")
        raise

def calculate_adx(df, period=14):
    """
    Calculate the ADX (Average Directional Index) for the given DataFrame using the first 'period' rows.
    
    :param df: A pandas DataFrame containing 'High', 'Low', and 'Close' price columns.
    :param period: The number of periods to use for ADX calculation (default is 14).
    :return: The latest ADX value as an integer.
    """
    logger.debug("Starting ADX calculation")
    try:
        # Ensure necessary columns are present and limit to the first 'period' rows
        df = df[['High', 'Low', 'Close']].head(period)

        # Calculate True Range (TR) and directional movement (+DM and -DM)
        df['H-L'] = df['High'] - df['Low']
        df['H-C'] = (df['High'] - df['Close'].shift()).abs()
        df['L-C'] = (df['Low'] - df['Close'].shift()).abs()
        df['TR'] = df[['H-L', 'H-C', 'L-C']].max(axis=1)

        df['+DM'] = df['High'] - df['High'].shift()
        df['-DM'] = df['Low'].shift() - df['Low']
        df['+DM'] = df['+DM'].where(df['+DM'] > 0, 0)
        df['-DM'] = df['-DM'].where(df['-DM'] > 0, 0)

        # Calculate smoothed True Range, +DM, and -DM
        df['ATR'] = df['TR'].rolling(window=period, min_periods=1).sum()
        df['+DM_smooth'] = df['+DM'].rolling(window=period, min_periods=1).sum()
        df['-DM_smooth'] = df['-DM'].rolling(window=period, min_periods=1).sum()

        # Calculate +DI and -DI
        df['+DI'] = (df['+DM_smooth'] / df['ATR']) * 100
        df['-DI'] = (df['-DM_smooth'] / df['ATR']) * 100

        # Calculate ADX
        df['DX'] = (df['+DI'] - df['-DI']).abs() / (df['+DI'] + df['-DI']) * 100
        df['ADX'] = df['DX'].rolling(window=period, min_periods=1).mean()

        # Log the calculated ADX value
        adx_value = int(df['ADX'].iloc[-1])
        logger.info(f"ADX calculated: {adx_value}")
        return adx_value
    except Exception as e:
        logger.error(f"Error in ADX calculation: {e}")
        raise
