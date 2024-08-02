import pandas as pd
import yfinance as yf
import datetime
import numpy as np
from scipy.stats import percentileofscore
from sklearn.linear_model import LinearRegression

# Function to calculate change percentage
def get_change_percent(stock_data, num_months, end_date):
    start_date = (end_date - datetime.timedelta(days=30 * num_months)).strftime('%Y-%m-%d')
    relevant_data = stock_data.loc[start_date:end_date]
    if relevant_data.empty:
        return None
    start_close = relevant_data['Close'].iloc[0]
    end_close = relevant_data['Close'].iloc[-1]
    change_percent = ((end_close - start_close) / start_close) * 100
    return change_percent

# Function to calculate RSI
def calculate_rsi(data, window=14):
    delta = data.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

# Function to calculate ADX
def calculate_adx(data, window=14):
    data['High-Low'] = data['High'] - data['Low']
    data['High-PrevClose'] = abs(data['High'] - data['Close'].shift(1))
    data['Low-PrevClose'] = abs(data['Low'] - data['Close'].shift(1))
    data['TrueRange'] = data[['High-Low', 'High-PrevClose', 'Low-PrevClose']].max(axis=1)
    data['UpMove'] = data['High'] - data['High'].shift(1)
    data['DownMove'] = data['Low'].shift(1) - data['Low']
    data['PlusDM'] = np.where((data['UpMove'] > data['DownMove']) & (data['UpMove'] > 0), data['UpMove'], 0)
    data['MinusDM'] = np.where((data['DownMove'] > data['UpMove']) & (data['DownMove'] > 0), data['DownMove'], 0)
    data['TR_EMA'] = data['TrueRange'].ewm(span=window, adjust=False).mean()
    data['PlusDM_EMA'] = data['PlusDM'].ewm(span=window, adjust=False).mean()
    data['MinusDM_EMA'] = data['MinusDM'].ewm(span=window, adjust=False).mean()
    data['PlusDI'] = (data['PlusDM_EMA'] / data['TR_EMA']) * 100
    data['MinusDI'] = (data['MinusDM_EMA'] / data['TR_EMA']) * 100
    data['DX'] = abs(data['PlusDI'] - data['MinusDI']) / (data['PlusDI'] + data['MinusDI']) * 100
    data['ADX'] = data['DX'].ewm(span=window, adjust=False).mean()
    data.drop(['High-Low', 'High-PrevClose', 'Low-PrevClose', 'TrueRange', 'UpMove', 'DownMove', 'PlusDM', 'MinusDM',
               'TR_EMA', 'PlusDM_EMA', 'MinusDM_EMA', 'PlusDI', 'MinusDI', 'DX'], axis=1, inplace=True)
    return data['ADX']

# Function to calculate MACD
def calculate_macd(data):
    ema_12 = data['Close'].ewm(span=12, min_periods=0, adjust=False).mean()
    ema_26 = data['Close'].ewm(span=26, min_periods=0, adjust=False).mean()
    macd = ema_12 - ema_26
    signal_line = macd.ewm(span=9, min_periods=0, adjust=False).mean()
    histogram = macd - signal_line
    return macd, signal_line, histogram

# Function to calculate linear regression slope for the past week
def calculate_slope(data):
    y = data['Close'].values[-5:]  # Take last 5 closing prices
    x = np.arange(len(y)).reshape(-1, 1)  # Create an array of shape (5, 1) for regression
    model = LinearRegression().fit(x, y)
    slope = model.coef_[0]
    return slope

# Function to calculate Stochastic Oscillator (%K and %D)
def calculate_stochastic(data, window=14):
    low_min = data['Low'].rolling(window=window).min()
    high_max = data['High'].rolling(window=window).max()
    data['%K'] = 100 * ((data['Close'] - low_min) / (high_max - low_min))
    data['%D'] = data['%K'].rolling(window=3).mean()
    return data['%K'], data['%D']

# Function to check trend direction
def is_trend_upwards(data, column):
    return data[column].iloc[-1] > data[column].rolling(window=5).mean().iloc[-1]

# Define columns for the DataFrame
hqm_columns = [
    'Ticker', 
    'Price', 
    '1-Month Change Percentage',
    '3-Month Change Percentage',
    'RSI',
    'Relative Volume',
    'MACD',
    'Signal Line',
    'Histogram',
    'ADX',
    'RSI Trend Upwards',
    'ADX Trend Upwards',
    'Relative Volume Trend Upwards',
    '3M Change > 1M Change and > 0',
    'MACD > 0',
    'Histogram > 0',
    'Slope',
    'Slope > 0',
    '%K',
    '%D',
    '%K Trend Upwards',
    '%D Trend Upwards',
    'Conditions Satisfied'
]

# Initialize DataFrame
hqm_dataframe = pd.DataFrame(columns=hqm_columns)

# Input the desired date
input_date = '2024-06-25'  # Example date, format: 'YYYY-MM-DD'
end_date = datetime.datetime.strptime(input_date, '%Y-%m-%d')
end_date += datetime.timedelta(days=1)  # Adjust to include the specified date

# Read stocks from file
stocks = pd.read_excel(r"C:\Users\sanan\Downloads\NSE Stocks.xlsx")
stocks_list = stocks['Ticker'].tolist()

# Loop through stocks
for stock in stocks_list:  
    try:
        # Fetch historical data for the stock
        stock_data = yf.download(stock, start=end_date - datetime.timedelta(days=365), end=end_date)
        if stock_data.empty:
            continue
        # Calculate RSI
        stock_data['RSI'] = calculate_rsi(stock_data['Close'])
        # Calculate change percentages based on actual close values
        change_percent_1_month = get_change_percent(stock_data, 1, end_date)
        change_percent_3_months = get_change_percent(stock_data, 3, end_date)
        # Fetch historical volume data for the last 91 days
        stock_volume = yf.download(stock, start=end_date - datetime.timedelta(days=91), end=end_date)['Volume']
        # Calculate relative volume
        avg_volume_10_days = stock_volume.tail(10).mean()
        avg_volume_91_days = stock_volume.mean()
        relative_volume = avg_volume_10_days / avg_volume_91_days
        # Calculate MACD, Signal Line, and Histogram
        macd, signal_line, histogram = calculate_macd(stock_data)
        # Calculate ADX
        stock_data['ADX'] = calculate_adx(stock_data)
        # Calculate trend direction for RSI and ADX
        rsi_trend_upwards = is_trend_upwards(stock_data, 'RSI')
        adx_trend_upwards = is_trend_upwards(stock_data, 'ADX')
        # Determine if relative volume is increasing
        increasing_rel_volume = relative_volume > stock_volume.iloc[-1] / avg_volume_91_days
        # Determine if 3-month change percentage is greater than 1-month change percentage and both are greater than zero
        change_comparison = (change_percent_3_months > change_percent_1_month) and (change_percent_1_month > 0) and (change_percent_3_months > 0)
        # Determine if MACD and Histogram are greater than zero
        macd_positive = macd.iloc[-1] > 0
        histogram_positive = histogram.iloc[-1] > 0
        # Calculate the slope of the last week's closing prices
        slope = calculate_slope(stock_data)
        slope_positive = slope > 0
        # Calculate %K and %D for Stochastic Oscillator
        k_percent, d_percent = calculate_stochastic(stock_data)
        # Determine if %K and %D are trending upwards
        k_trend_upwards = is_trend_upwards(stock_data, '%K')
        d_trend_upwards = is_trend_upwards(stock_data, '%D')
        
        # Count the number of conditions satisfied
        conditions_satisfied = sum([
            rsi_trend_upwards,
            adx_trend_upwards,
            increasing_rel_volume,
            change_comparison,
            macd_positive,
            histogram_positive,
            slope_positive,
            k_trend_upwards,
            d_trend_upwards
        ])
        
        # Append data to the DataFrame
        hqm_dataframe = hqm_dataframe.append({
            'Ticker': stock, 
            'Price': stock_data['Close'].iloc[-1],  # Use the last close price
            '1-Month Change Percentage': change_percent_1_month,
            '3-Month Change Percentage': change_percent_3_months,
            'RSI': stock_data['RSI'].iloc[-1],
            'Relative Volume': relative_volume,
            'MACD': macd.iloc[-1],
            'Signal Line': signal_line.iloc[-1],
            'Histogram': histogram.iloc[-1],
            'ADX': stock_data['ADX'].iloc[-1],
            'RSI Trend Upwards': rsi_trend_upwards,
            'ADX Trend Upwards': adx_trend_upwards,
            'Relative Volume Trend Upwards': increasing_rel_volume,
            '3M Change > 1M Change and > 0': change_comparison,
            'MACD > 0': macd_positive,
            'Histogram > 0': histogram_positive,
            'Slope': slope,
            'Slope > 0': slope_positive,
            '%K': k_percent.iloc[-1],
            '%D': d_percent.iloc[-1],
            '%K Trend Upwards' : k_trend_upwards,
            '%D Trend Upwards' : d_trend_upwards,
            'Conditions Satisfied': conditions_satisfied
        }, ignore_index=True)
    except Exception as e:
        print(f"Error processing {stock}: {e}")

print(hqm_dataframe)