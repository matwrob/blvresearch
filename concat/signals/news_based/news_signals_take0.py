"""
OVERVIEW:
Simple strategy based on news.

First identifies important events by considering alpha and existence of
relevant news on a given day.
Alpha needs to exceed mean by 1 sigma in absolute terms.

Next for each of these days:
(1) checks what was the return on that day & invests accordingly

"""
import pandas as pd

from blvresearch.concat.signals.news_based.news_common_funcs import (
    get_days_to_check
)
from blvresearch.concat.signals.utils import remove_consecutive_values


FIRST_LOC = 0
LAST_LOC = -1


def get_signals(data):
    days_to_check = get_days_to_check(data, FIRST_LOC, LAST_LOC)
    result = pd.Series(index=data.index)
    for date in days_to_check.index:
        if _is_negative_suprise(data, date):
            result[date] = False
        elif _is_positive_suprise(data, date):
            result[date] = True
    return remove_consecutive_values(result)


def _is_negative_suprise(df, date):
    if df['alpha'][date] < 0:
        return True
    return False


def _is_positive_suprise(df, date):
    if df['alpha'][date] > 0:
        return True
    return False
