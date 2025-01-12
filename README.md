# Advanced Momentum Stock Model

This project analyzes the momentum of stocks using various technical indicators such as RSI, MACD, ADX, Stochastic Oscillator and so on. The model identifies stocks that satisfy specific conditions indicating upward trends and momentum. Proven to perform better than the Indian Stock Index for the past 3 years via Backtesting.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Technical Indicators](#technical-indicators)
- [Conditions Satisfied](#conditions-satisfied)
- [Files](#files)
- [Contributing](#contributing)
- [License](#license)

## Installation

To install the required packages, run:

```sh
pip install -r requirements.txt
```

## Usage

Ensure you have the list of stocks in an Excel file named NSE Stocks.xlsx with a column Ticker containing the stock symbols. Save this file in the same directory as the script.

Run the script with the desired input date:
```sh
python Advanced_Momentum_Stock_Model.py
```

The script will output a DataFrame containing the analyzed data for each stock.


Run the script with the desired stock ticker input:
```sh
python Get_Stock_Info.py
```

The script will output all the important information pertaining to a stock including time-series graphs.


Run the script with the desired number of stocks and their ticker as input:
```sh
python Multi_Stock_Comparison.py
```

he script will compare all the important information pertaining to stocks including time-series graphs.


## Technical Indicators
The script calculates the following technical indicators for each stock:

- RSI (Relative Strength Index): Measures the magnitude of recent price changes to evaluate overbought or oversold conditions.
- MACD (Moving Average Convergence Divergence): Indicates momentum by comparing short-term and long-term moving averages.
- ADX (Average Directional Index): Measures the strength of a trend.
- Stochastic Oscillator: Compares a particular closing price of a security to a range of its prices over a certain period of time.

## Conditions Satisfied
The script evaluates whether each stock satisfies certain conditions, including:

- RSI is trending upwards.
- ADX is trending upwards.
- Relative volume is increasing.
- 3-month change percentage is greater than 1-month change percentage and both are greater than zero.
- MACD is greater than zero.
- Histogram (difference between MACD and Signal Line) is greater than zero.
- Slope of the last week's closing prices is positive.
- %K (Stochastic Oscillator) is trending upwards.
- %D (Stochastic Oscillator) is trending upwards.
Each condition is counted, and the total number of satisfied conditions is recorded for each stock.

## Stock Information
The script to view and compare multiple stocks covers these important stock details

- General Stock Information
- Valuation Metrics
- Profitability Metrics
- Growth Metrics
- Dividend Metrics
- Financial Health Metrics
- Performance Metrics
- Yahoo Analyst Recommendations
- Shareholder Data
- Historical Data
- Technical Metrics
- Stock Performance Graphs over 5 days, 1 month, 3 months, 6 months, 1 year and 5 years 

## Files
- Advanced_Momentum_Stock_Model.py: The main script that performs the stock analysis.
- Get_Stock_Info.py : The script that allows user to view important stock details.
- Multi_Stock_Comparison.py : The script that allows user to view and compare across multiple stocks.
- requirements.txt: List of required Python packages.
- README.md: This readme file.
- NSE Stocks.xlsx: Excel file containing the list of stock tickers to analyze (not included, must be provided).

## Contributing
Contributions are welcome! Please follow these steps to contribute:

Fork the repository.
Create a new branch (git checkout -b feature-branch).
Make your changes.
Commit your changes (git commit -am 'Add new feature').
Push to the branch (git push origin feature-branch).
Create a new Pull Request.

## License
This project is licensed under the MIT License - see the LICENSE file for details.
