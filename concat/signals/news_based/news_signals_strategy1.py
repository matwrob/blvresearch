"""
OVERVIEW:
First identifies important events, i.e.
(1) relevant news need to exist
(2) alpha needs to exceed expected alpha by 1 standard deviation

    Remark: alpha moments are calculated based on previous 6 months

Next for each of these days:
(3) checks what was the return on that day & invests accordingly,
    i.e. if alpha was positive => buy,
         if alpha was negative => sell

"""
import pandas as pd

from blvresearch.concat.signals.news_based.news_common_funcs import (
    get_days_to_check
)
from blvresearch.concat.signals.utils import remove_consecutive_values


FIRST_LOC = 0
LAST_LOC = -1


def get_news1day_signals(days_to_check, data, first_loc, last_loc):
    first_day = data.index[first_loc + FIRST_LOC]
    last_day = data.index[last_loc + LAST_LOC]
    result = pd.Series(index=data.index)
    for date in days_to_check[first_day:last_day].index:
        if _is_negative_suprise(data, date):
            result[date] = False
        elif _is_positive_suprise(data, date):
            result[date] = True
    return remove_consecutive_values(result)


def _is_negative_suprise(data, date):
    if data['alpha'][date] < 0:
        return True
    return False


def _is_positive_suprise(data, date):
    if data['alpha'][date] > 0:
        return True
    return False


def get_signals(data):
    days_to_check = get_days_to_check(data, FIRST_LOC, LAST_LOC)
    result = pd.Series(index=data.index)
    for date in days_to_check.index:
        if _is_negative_suprise(data, date):
            result[date] = False
        elif _is_positive_suprise(data, date):
            result[date] = True
    return remove_consecutive_values(result)


DESCRIPTION_BUY = """
This is a BUY signal generated using company news and its stock return.\n
On that day company relevant news were published and its stock experienced
an abnormal positive alpha.
"""

DESCRIPTION_SELL = """
This is a SELL signal generated using company news and its stock return.\n
On that day company relevant news were published and its stock experienced
an abnormal negative alpha.
"""


def get_news1day_descr(signal):
    if signal == True:
        return DESCRIPTION_BUY
    elif signal == False:
        return DESCRIPTION_SELL
