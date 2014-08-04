"""
OVERVIEW:
First identifies CMO signals.

Then it checks if over previous 20 days there was an important
news day that could support price changes that generated CMO signal.

"""
import datetime as dt
import pandas as pd

from blvresearch.concat.signals.utils import remove_consecutive_values
from blvresearch.concat.signals.news_based.news_common_funcs import (
    get_days_to_check
)
from blvresearch.concat.signals.price_based.cmo_signals import (
    get_cmo_signals
)


DAYS_AFTER = 3
FIRST_LOC = (8 +  # CMO takes 9 days to generate a signal hence first 9 days
             5)   # cannot give a signal, then we also look back 5 days to find
                  # out if a CMO strategy generated a signal
LAST_LOC = -DAYS_AFTER


def get_signals(days_to_check, data, first_loc, last_loc):
    first_day = days_to_check.index[0]
    cmo_signals = get_cmo_signals(data, periods=9)
    cmo_signals = cmo_signals[first_day:]

    days_to_check = days_to_check.reindex(data.index)
    result = pd.Series(index=data.index)
    for date, signal in cmo_signals.items():
        loc = data.index.get_loc(date)
        news_days = days_to_check[loc - 20:loc].dropna()
        if news_days.any():
            last_day = news_days.index[-1]
            if _is_negative_surprise(data, last_day) and signal == False:
                result[date] = False
            elif _is_positive_surprise(data, last_day) and signal == True:
                result[date] = True
    return remove_consecutive_values(result)


def _is_negative_surprise(data, date):
    if data['alpha'][date] < 0:
        return True
    return False


def _is_positive_surprise(data, date):
    if data['alpha'][date] > 0:
        return True
    return False
