"""
OVERVIEW:
The X-Day Exponential Moving Average (EMA) Crossover Strategy uses the
exponential moving average to determine the trend's direction.
When the stock price crosses the X-day EMA, it's considered bullish and
represents a potential buying opportunity.
The system seeks to exit or sell an open position when the stock price has
appreciated by a specific percentage, or after holding the stock for a specific
period of time.

PARAMETER DESCRIPTION:
The Exponential Moving Average is similar to the Simple Moving Average in that
it calculates the average price of a stock over a given period. EMA gives more
weight to recent data, and the most weight is placed on the most recent price.
As a result, the EMA follows the stock price closer than an SMA. Typical
short-term trend values look at 12 and 26 day periods, whereas 50 and 200 day
periods are used for longer term trends.
The EMA Period is the number of days used by the strategy in the EMA
calculation.

Source: https://eresearch.fidelity.com/
"""
from itertools import groupby
import pandas as pd

from blvresearch.concat.signals.utils import (
    remove_consecutive_values
)


def get_signals(data, window, confirmation_window):
    returns = data['alpha'].cumsum()
    avg = pd.ewma(returns, span=window)
    result = returns > avg
    result = adjust_series_of_signals(result, confirmation_window)
    return remove_consecutive_values(result)


def adjust_series_of_signals(series_of_signals, confirmation_window):
    """adjusts raw signals by checking if there are X consecutive signals of
    the same type; if yes, the Xth day is the signal day, otherwise there is no
    signal

    """
    list_of_tuples = [(k, v) for k, v in series_of_signals.items()]
    list_of_tuples.sort(key=lambda x: x[0])
    result = pd.Series(index=series_of_signals.index)
    for signal, group in groupby(list_of_tuples, key=lambda x: x[1]):
        tuples = list(group)
        if len(tuples) > confirmation_window:
            signal_day = tuples[confirmation_window - 1][0]
            result[signal_day] = True if signal == True else False
    return result
