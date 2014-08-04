"""
OVERVIEW:
First identifies important events, i.e days where:
(1) relevant news was published
(2) alpha on that day exceeds expected alpha by 2 standard deviations

    Remarks:
    alpha moments are calculated based on previous 6 months of data

Next, for each of these days, checks:
(3) alpha on that day

    alpha > 0 => buy signal
    alpha < 0 => sell signal

"""
import pandas as pd

from blvresearch.concat.signals.news_based.news_common_funcs import (
    get_days_to_check
)


DESCRIPTION_BUY = """
This is a BUY signal generated using company news and its stock return.
On that day company-relevant news was published and its stock experienced
abnormal positive alpha.
"""


DESCRIPTION_SELL = """
This is a SELL signal generated using company news and its stock return.
On that day company-relevant news was published and its stock experienced
abnormal negative alpha.
"""


DESCRIPTION_COMMON = """
For all trading strategies, tha past performance does
not guarantee future results.
"""


DAYS_AFTER = 0
FIRST_LOC = 0
LAST_LOC = -DAYS_AFTER


def get_news1day_signals(days_to_check, data, first_loc, last_loc):
    first_day = data.index[first_loc + FIRST_LOC]
    last_day = data.index[last_loc + LAST_LOC]
    result = pd.Series(index=data.index)
    for date in days_to_check[first_day:last_day].index:
        loc = data.index.get_loc(date)
        signal_day = data.index[loc + DAYS_AFTER]
        if _is_negative_suprise(data, date):
            result[signal_day] = False
        elif _is_positive_suprise(data, date):
            result[signal_day] = True
    return result.dropna()


def _is_negative_suprise(data, date):
    if data['alpha'][date] < 0:
        return True
    return False


def _is_positive_suprise(data, date):
    if data['alpha'][date] > 0:
        return True
    return False


def get_news1day_descr(signal):  # pragma: no cover
    if signal == True:
        result = DESCRIPTION_BUY
    elif signal == False:
        result = DESCRIPTION_SELL
    result += DESCRIPTION_COMMON
    return result
