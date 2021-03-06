"""
OVERVIEW:
4 Down Days is a Counter-Trend Strategy that attempts to buy a stock when the
price has declined for four days in a row. Positions are then sold at market
when the stock price rises on two consecutive days.

PARAMETER DESCRIPTION:
down_days: number of consecutive days the stock price declines to generate a
           trade signal to buy the stock
up_days: number of consecutive days the stock price rises before the stock is
         sold

Source: https://eresearch.fidelity.com/

"""
from itertools import groupby
import pandas as pd

from blvresearch.concat.signals.utils import (
    remove_consecutive_values
)


def get_signals(data, down_days, up_days):
    ups_and_downs = data['alpha'].map(lambda x: 'UP' if x >= 0 else 'DOWN')
    result = _find_consecutive_ups_and_downs(ups_and_downs, down_days, up_days)
    return remove_consecutive_values(result)


def _find_consecutive_ups_and_downs(series_of_signals, down_days, up_days):
    list_of_tuples = [(k, v) for k, v in series_of_signals.items()]
    list_of_tuples.sort(key=lambda x: x[0])

    result = pd.Series(index=series_of_signals.index)
    for signal, group in groupby(list_of_tuples, key=lambda x: x[1]):
        tuples = list(group)
        if signal == 'UP' and len(tuples) > up_days - 1:
            signal_day = tuples[up_days - 1][0]
            result[signal_day] = False
        elif signal == 'DOWN' and len(tuples) > down_days - 1:
            signal_day = tuples[down_days - 1][0]
            result[signal_day] = True
    return result
