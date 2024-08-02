# Advanced Momentum Stock Model

This project analyzes the momentum of stocks using various technical indicators such as RSI, MACD, ADX, Stochastic Oscillator and so on. The model identifies stocks that satisfy specific conditions indicating upward trends and momentum.

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
python advanced_momentum_stock_model.py
```

The script will output a DataFrame containing the analyzed data for each stock.

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

## Files
advanced_momentum_stock_model.py: The main script that performs the stock analysis.
requirements.txt: List of required Python packages.
README.md: This readme file.
NSE Stocks.xlsx: Excel file containing the list of stock tickers to analyze (not included, must be provided).

## Contributing
Contributions are welcome! Please follow these steps to contribute:

Fork the repository.
Create a new branch (git checkout -b feature-branch).
Make your changes.
Commit your changes (git commit -am 'Add new feature').
Push to the branch (git push origin feature-branch).
Create a new Pull Request.
