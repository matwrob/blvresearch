"""
OVERVIEW:
First identifies important events, i.e.
(1) relevant news need to exist
(2) alpha needs to exceed expected alpha by 1 standard deviation

    Remark: alpha moments are calculated based on previous 6 months

Next for each of these days, it checks:
(1) what was the return on that day
(2) what was the return over the next 3 days
(3) if the last signal generated by MA strategy is in line with news
    based signal

"""
import datetime as dt
import pandas as pd

from blvresearch.concat.signals.utils import remove_consecutive_values
from blvresearch.concat.signals.news_based.news_common_funcs import (
    get_days_to_check
)
from blvresearch.concat.signals.price_based.moving_average import (
    get_movavg_signals
)


DAYS_AFTER = 3
FIRST_LOC = (20 +  # MA window
             3)    # MA confirmation window
LAST_LOC = -DAYS_AFTER


def get_news_movavg_signals(days_to_check, data, first_loc, last_loc):
    first_day = data.index[first_loc + FIRST_LOC]
    last_day = data.index[last_loc + LAST_LOC]

    ma_signals = get_movavg_signals(data, window=20, confirmation_window=3)
    ma_signals = ma_signals.reindex(data.index)

    result = pd.Series(index=data.index)
    for date in days_to_check[first_day:last_day].index:
        loc = data.index.get_loc(date)
        signal_day = data.index[loc + DAYS_AFTER]
        previous_ma_signals = ma_signals[:signal_day].dropna()
        if len(previous_ma_signals) > 0:
            if (previous_ma_signals[-1] == False and
                _is_negative_suprise(data, date)):
                result[signal_day] = False
            elif (previous_ma_signals[-1] == True and
                  _is_positive_suprise(data, date)):
                result[signal_day] = True
    return remove_consecutive_values(result)


def _is_negative_suprise(data, date):
    loc = data.index.get_loc(date)
    if (data['alpha'][date] < 0 and
        data['alpha'][loc + 1:loc + 1 + DAYS_AFTER].sum() < 0):
        return True
    return False


def _is_positive_suprise(data, date):
    loc = data.index.get_loc(date)
    if (data['alpha'][date] > 0 and
        data['alpha'][loc + 1:loc + 1 + DAYS_AFTER].sum() > 0):
        return True
    return False


def func(x):
    if x < 0:
        return -1
    else:
        return 1


DESCRIPTION_BUY = """
This is a BUY signal generated using company news and its stock return.\n
It combines a news-based signal and a Moving Average signal.\n\n
3 days before the signal day relevant news about this company was published
and its stock experienced an abnormal positive alpha.\n
In addition the cumulative alpha over the following 3 days was also positive
and at least 2 out of these 3 days had positive alpha.\n\n
This signal is additionally reaffirmed by checking if the last signal
generated by 20-day Moving Average was also a buy signal.
"""

DESCRIPTION_SELL = """
This is a SELL signal generated using company news and its stock return.\n
It combines a news-based signal and a Moving Average signal.\n\n
3 days before the signal day relevant news about this company was published
and its stock experienced an abnormal negative alpha.\n
In addition the cumulative alpha over the following 3 days was also negative
and at least 2 out of these 3 days had negative alpha.\n\n
This signal is additionally reaffirmed by checking if the last signal
generated by 20-day Moving Average was also a sell signal.
"""


def get_news_movavg_descr(signal):
    if signal == True:
        return DESCRIPTION_BUY
    elif signal == False:
        return DESCRIPTION_SELL
