"""
OVERVIEW:
This strategy uses two moving averages of different periods, short and long
(fast and slow), to indicate a trend's direction. When the fast moving average
(short) crosses above the slow moving average (long), the trend is deemed to
have become bullish and represents a potential buying opportunity.
The system seeks to exit (sell) an open position when the fast moving average
crosses below the slow moving average.

PARAMETER DESCRIPTION:
The Moving Average is the average price of a stock over a given period.
For example, to calculate a 50 day Simple Moving Average (SMA), add the last
50 closing price values and divide the sum by 50. There are other, more complex
ways to calculate a Moving Average, but the Simple Moving Average is still the
most commonly used. Typical trend values look out over 20 and 50 days although
50 and 200 days are also frequently used.

Source: https://eresearch.fidelity.com/

###############################################################################

Calculating Moving Averages based on daily alphas increases slightly the number
of signals generated on average across entities.
Average returns of winner entities and loser entities are greater in absolute
terms (0.3365 vs 0.2994 and -0.235 vs -0.1706)

"""
from itertools import groupby
import pandas as pd

from blvresearch.concat.signals.utils import (
    remove_consecutive_values
)


def get_signals(data, long_window, short_window, confirmation_window):
    returns = data['alpha'].cumsum()
    _short = pd.ewma(returns, span=short_window)
    _long = pd.ewma(returns, span=long_window)
    result = _short > _long
    result = _adjust_series_of_signals(result, confirmation_window)
    return remove_consecutive_values(result)


def _adjust_series_of_signals(series_of_signals, confirmation_window):
    list_of_tuples = [(k, v) for k, v in series_of_signals.items()]
    list_of_tuples.sort(key=lambda x: x[0])
    result = pd.Series(index=series_of_signals.index)
    for signal, group in groupby(list_of_tuples, key=lambda x: x[1]):
        tuples = list(group)
        if len(tuples) > confirmation_window:
            signal_day = tuples[confirmation_window - 1][0]
            result[signal_day] = True if signal == True else False
    return result
