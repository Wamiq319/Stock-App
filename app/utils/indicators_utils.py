import pandas as pd
from .. import setup_logger

# Logger setup
logger = setup_logger("INDICATORS-UTILS")

def calculate_rsi(df, period=14):
    """
    Calculate the RSI and return a numeric signal and the RSI value.
    """
    logger.debug("Starting RSI calculation")
    try:
        df = df[['Close']].head(period)
        delta = df['Close'].diff()
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)
        avg_gain = gain.rolling(window=period, min_periods=1).mean()
        avg_loss = loss.rolling(window=period, min_periods=1).mean()
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        rsi_value = rsi.iloc[-1]

        # Determine numeric signal
        if rsi_value > 70:
            signal = -1  # SELL
        elif rsi_value < 30:
            signal = 1  # BUY
        else:
            signal = 0  # N/A

        logger.info(f"RSI calculated: {rsi_value:.2f}, Signal: {signal}")
        return signal
    except Exception as e:
        logger.error(f"Error in RSI calculation: {e}")
        raise

def calculate_macd(df, fast_period=12, slow_period=26, signal_period=9):
    """
    Calculate the MACD and return a numeric signal and the MACD value.
    """
    logger.debug("Starting MACD calculation")
    try:
        df = df[['Close']].head(slow_period)
        fast_ema = df['Close'].ewm(span=fast_period, adjust=False).mean()
        slow_ema = df['Close'].ewm(span=slow_period, adjust=False).mean()
        macd = fast_ema - slow_ema
        signal_line = macd.ewm(span=signal_period, adjust=False).mean()
        macd_histogram = macd - signal_line
        macd_value = macd_histogram.iloc[-1]

        # Determine numeric signal
        if macd.iloc[-1] > signal_line.iloc[-1]:
            signal = 1  # BUY
        elif macd.iloc[-1] < signal_line.iloc[-1]:
            signal = -1  # SELL
        else:
            signal = 0  # N/A

        logger.info(f"MACD calculated: {macd_value:.2f}, Signal: {signal}")
        return signal
    except Exception as e:
        logger.error(f"Error in MACD calculation: {e}")
        raise

def calculate_adx(df, period=14):
    """
    Calculate the ADX and return a numeric signal and the ADX value.
    """
    logger.debug("Starting ADX calculation")
    try:
        df = df[['High', 'Low', 'Close']].head(period)
        df['H-L'] = df['High'] - df['Low']
        df['H-C'] = (df['High'] - df['Close'].shift()).abs()
        df['L-C'] = (df['Low'] - df['Close'].shift()).abs()
        df['TR'] = df[['H-L', 'H-C', 'L-C']].max(axis=1)

        df['+DM'] = df['High'] - df['High'].shift()
        df['-DM'] = df['Low'].shift() - df['Low']
        df['+DM'] = df['+DM'].where(df['+DM'] > 0, 0)
        df['-DM'] = df['-DM'].where(df['-DM'] > 0, 0)

        df['ATR'] = df['TR'].rolling(window=period, min_periods=1).sum()
        df['+DM_smooth'] = df['+DM'].rolling(window=period, min_periods=1).sum()
        df['-DM_smooth'] = df['-DM'].rolling(window=period, min_periods=1).sum()

        df['+DI'] = (df['+DM_smooth'] / df['ATR']) * 100
        df['-DI'] = (df['-DM_smooth'] / df['ATR']) * 100

        df['DX'] = (df['+DI'] - df['-DI']).abs() / (df['+DI'] + df['-DI']) * 100
        df['ADX'] = df['DX'].rolling(window=period, min_periods=1).mean()
        adx_value = df['ADX'].iloc[-1]
        di_plus = df['+DI'].iloc[-1]
        di_minus = df['-DI'].iloc[-1]

        # Determine numeric signal
        if adx_value > 40 and di_plus > di_minus:
            signal = 1  # BUY
        elif adx_value > 40 and di_minus > di_plus:
            signal = -1  # SELL
        else:
            signal = 0  # N/A

        logger.info(f"ADX calculated: {adx_value:.2f}, Signal: {signal}")
        return signal
    except Exception as e:
        logger.error(f"Error in ADX calculation: {e}")
        raise
