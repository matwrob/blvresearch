"""
OVERVIEW:
When the market experiences a sharp run-up in the number of sellers versus
buyers, this typically results in a quick downtrend in price, and the market
is considered to be oversold. When the short-term oversupply of sellers
passes, it is expected that a stock's price will rise back to a more typical
level of valuation.

This strategy seeks to take advantage of this trend by investing against the
trend. It seeks to enter a position when the stock price, as measured by
the Relative Strength Index (RSI), becomes oversold (below 30). If the stock
price continues to fall, the strategy continues to buy more stock as the RSI
crosses below the 25, 20 15, 10, and 5 levels. The strategy sells all the
positions when the RSI indicator rebounds above 55.

PARAMETER DESCRIPTION:
The Relative Strength Index (RSI), created by Welles Wilder (see "New Concepts
in Technical Trading Systems"), measures a market's internal strength by
dividing the average of the sum of the up day closing prices by the average
of the sum of the down day closing prices over a specific period of time.
It returns a value within the range of 0 to 100. This strategy uses a 20 day
period. The classic way to interpret RSI is to look for oversold levels below
30 as a signal to buy and overbought levels above 70 as a signal to sell.

ADVANTAGES/RISKS:
This strategy seeks to buy during a price decline with the expectation of
profiting when the price recovers from an oversold condition. However, during
strong trends the RSI may remain in an oversold condition for extended periods.
While this strategy can work well with large cap stocks, many traders may have
difficulty following the strategy due to the approach of continuing to add to
the position as the stock price and RSI levels continue to decline.
Typically, traders following these types of strategies expect occasional
significant losses when a major downtrend continues. Traders can limit the
impact of such occurrences by trading the strategy across multiple stocks, and
by limiting the amount of trading capital devoted to such strategies.
And like all trading strategies, tha past performance of the RSI Agita strategy
is no guarantee of future results.

Source: https://eresearch.fidelity.com/

"""
from itertools import groupby
import pandas as pd

from blvresearch.concat.signals.utils import (
    remove_consecutive_values
)


def get_signals(data, periods, buy_thrsh, sell_thrsh, mean_type='exp'):
    def _logic(x):
        if x < buy_thrsh:
            return True
        if x > sell_thrsh:
            return False
    returns = data['alpha']
    rsi = _calculate_rsi(returns, periods, mean_type)
    result = pd.Series(rsi.map(_logic))
    return remove_consecutive_values(result)


def _calculate_rsi(returns, periods, mean_type):
    "mean_type: 'exp' or 'simple'"
    only_gains = returns.map(lambda x: 0 if x < 0 else x)
    only_losses = returns.map(lambda x: 0 if x >= 0 else -x)
    if mean_type == 'exp':
        avg_gains = pd.ewma(only_gains, span=periods)
        avg_losses = pd.ewma(only_losses, span=periods)
    elif mean_type == 'simple':
        avg_gains = pd.rolling_mean(only_gains, window=periods)
        avg_losses = pd.rolling_mean(only_losses, window=periods)
    rs = avg_gains / avg_losses
    return 100 - (100 / (1 + rs))
