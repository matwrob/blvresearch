"""
OVERVIEW:
First identifies important events, i.e.
(1) relevant news need to exist
(2) alpha needs to exceed expected alpha by 1 standard deviation

    Remark: alpha moments are calculated based on previous 6 months

Next for each of these days, it checks:
(1) what was the return on that day
(2) what was the return over the next 3 days
(3) if over the previous 5 or the next 3 days a buy/sell signal - generated by
    a MODIFIED-CMO strategy - occurred and if is in line with news based signal

"""
import datetime as dt
import pandas as pd

from blvresearch.concat.signals.utils import remove_consecutive_values
from blvresearch.concat.signals.news_based.news_common_funcs import (
    get_days_to_check
)
from blvresearch.concat.signals.price_based.cmo_signals import (
    _calculate_cmo_values, _adjust_series_of_signals
)


DAYS_AFTER = 3
FIRST_LOC = (8 +  # CMO takes 9 days to generate a signal hence first 9 days
             5)   # cannot give a signal, then we also look back 5 days to find
                  # out if a CMO strategy generated a signal
LAST_LOC = -DAYS_AFTER


def get_signals(days_to_check, returns, first_loc, last_loc):
    first_day = returns.index[first_loc + FIRST_LOC]
    last_day = returns.index[last_loc + LAST_LOC]

    cmo_signals = get_cmo_signals(returns, periods=9)
    cmo_signals = cmo_signals.reindex(returns.index)

    result = pd.Series(index=returns.index)
    for date in days_to_check[first_day:last_day].index:
        loc = returns.index.get_loc(date)
        signal_day = returns.index[loc + DAYS_AFTER]
        if ((cmo_signals[loc - 5:loc + 1 + DAYS_AFTER] == False).any() and
            _is_negative_suprise(returns, date)):
            result[signal_day] = False
        elif ((cmo_signals[loc - 5:loc + 1 + DAYS_AFTER] == True).any() and
              _is_positive_suprise(returns, date)):
            result[signal_day] = True
    return remove_consecutive_values(result)


def _is_negative_suprise(returns, date):
    loc = returns.index.get_loc(date)
    if (returns[date] < 0 and
        returns[loc + 1:loc + 1 + DAYS_AFTER].sum() < 0):
        return True
    return False


def _is_positive_suprise(returns, date):
    loc = returns.index.get_loc(date)
    if (returns[date] > 0 and
        returns[loc + 1:loc + 1 + DAYS_AFTER].sum() > 0):
        return True
    return False


def func(x):
    if x < 0:
        return -1
    else:
        return 1


def get_cmo_signals(returns, periods):
    cmos = _calculate_cmo_values(returns, periods)
    result = cmos.dropna().map(_cmo_logic)
    result = _adjust_series_of_signals(result)
    return result


def _cmo_logic(x):
    if x <= -0.3:
        return True
    elif x >= 0.3:
        return False