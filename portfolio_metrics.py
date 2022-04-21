import pandas as pd
import os
import math
import numpy as np


def fill_missing_values(df):  # FIXME: first and last day of the year need to be filled
    df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d')
    df = df.set_index('Date', inplace=False)
    df = df.sort_values(by='Date', ascending=[True])
    df = df.resample('D').fillna(method="bfill").reset_index()
    return df


def calculate_return(portfolios, start_values, end_values):
    """
    The return of profit obtained by a portfolio.
    Portfolio return is computed for a 12 months period.
    """
    portfolio_returns = []

    for i in range(0, len(portfolios)):
        buy_amount_total = []
        current_value_total = []
        for j in range(0, portfolios.shape[1]):
            # sum of (number of shares of the j-th asset acquired * share price paid for the j-th asset)
            buy_amount = (portfolios.iloc[i][j] / start_values[j]) * start_values[j]
            buy_amount_total.append(buy_amount)
            # sum of (number of shares of the j-th asset acquired * current share price for the j-th asset)
            # Note: Since return is computed for 12 months period,
            # "current share price for the j-th asset" is the price of each asset at 12/31/2020.
            current_value = (portfolios.iloc[i][j] / start_values[j]) * end_values[j]
            current_value_total.append(current_value)
        buy_amount_total = sum(buy_amount_total)
        current_value_total = sum(current_value_total)

        portfolio_return = (current_value_total - buy_amount_total) / buy_amount_total * 100
        portfolio_returns.append(portfolio_return)

    portfolios['RETURN'] = portfolio_returns

    return portfolios


def calculate_shares(portfolio_row, start_prices):
    shares = []
    for j in range(0, len(portfolio_row) - 1):
        share = (portfolio_row[j] / start_prices[j])
        shares.append(share)
    return shares


def calculate_volatility(assets, portfolios, start_prices):
    """
    The amount of uncertainty or risk related to the size of changes in an asset value.
    """
    volatilities = []

    for row in range(0, len(portfolios)):
        shares = calculate_shares(portfolios.iloc[row], start_prices)

        values = []
        # FIXME: all assets should have the same length after proper filling of missing values -> change assets index
        for day in range(0, len(assets[2])):
            value_sum = 0
            for i, asset in enumerate(assets):
                value_sum += shares[i] * asset.loc[day].Price

            values.append(value_sum)

        sample_average = sum(values) / len(values)
        standard_deviation = math.sqrt(np.square(np.subtract(values, sample_average)).mean())
        volatility = (standard_deviation / sample_average) * 100

        volatilities.append(volatility)

    portfolios['VOLAT'] = volatilities

    return portfolios


def portfolio_metrics():
    # Asset information
    ST = pd.read_csv('data/amundi-msci-wrld-ae-c.csv')
    CB = pd.read_csv('data/ishares-global-corporate-bond-$.csv')
    PB = pd.read_csv('data/db-x-trackers-ii-global-sovereign-5.csv')
    GO = pd.read_csv('data/spdr-gold-trust.csv')
    CA = pd.read_csv('data/usdollar.csv')
    assets = [ST, CB, PB, GO, CA]
    assets_filled = []

    portfolios = pd.read_csv('portfolios/portfolio_allocations.csv')

    start_price = []
    end_price = []
    for i in range(0, len(assets)):
        asset = assets[i]
        asset = fill_missing_values(asset)
        assets_filled.append(asset)

        if i == len(assets)-1:  # Cash being the last asset in the list
            # determine if dollar has gained or loss value from start to end of year,
            # necessary to calculate the return on the cash asset investment
            start = 1
            end = asset['Price'].iloc[-1] / asset['Price'].iloc[0] # FIXME BUG????!
        else:
            start = asset['Price'].iloc[0]
            end = asset['Price'].iloc[-1]

        start_price.append(start)
        end_price.append(end)

    portfolios = calculate_return(portfolios, start_price, end_price)
    portfolios = calculate_volatility(assets_filled, portfolios, start_price)

    if not os.path.exists("portfolios"):
        os.mkdir("portfolios")

    portfolios.to_csv(f'portfolios/portfolio_metrics.csv', header=True, index=False)


if __name__ == "__main__":
    portfolio_metrics()
