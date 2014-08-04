"""
OVERVIEW:
First identifies important events, i.e days where:
(1) relevant news was published
(2) alpha on that day exceeds expected alpha by 2 standard deviations

    Remarks:
    alpha moments are calculated based on previous 6 months of data

Next, for each of these days, checks:
(3) alpha on that day
(4) cumulative alpha over 5 days (that day + 4 next days)
(5) ratio of the number of days with positive and negative alpha

    alpha > 0 AND cum_alpha > 0 AND at least 4 pos. alpha days => buy signal
    alpha < 0 AND cum_alpha < 0 AND at least 4 neg. alpha days => sell signal

"""
import datetime as dt
import pandas as pd

from blvresearch.concat.signals.news_based.news_common_funcs import (
    get_days_to_check
)


DESCRIPTION_BUY = """
This is a BUY signal generated using company news and its stock return.
Two days ago company-relevant news was published and its stock experienced
abnormal positive alpha.
In addition the cumulative alpha over 5 days (news day and two following days)
was also positive and out of these 5 days at least 4 had positive alpha.
"""


DESCRIPTION_SELL = """
This is a SELL signal generated using company news and its stock return.
Two days ago company-relevant news was published and its stock experienced
abnoraml negative alpha.
In addition the cumulative alpha over 5 days (news day and two following days)
was also negative and out of these 5 days at least 4 had negative alpha.
"""


DESCRIPTION_COMMON = """
For all trading strategies, tha past performance does
not guarantee future results.
"""


DAYS_AFTER = 4
FIRST_LOC = 0
LAST_LOC = -DAYS_AFTER


def get_news5days_signals(days_to_check, data, first_loc, last_loc):
    first_day = data.index[first_loc + FIRST_LOC]
    last_day = data.index[last_loc + LAST_LOC]
    result = pd.Series(index=data.index)
    for date in days_to_check[first_day:last_day].index:
        loc = data.index.get_loc(date)
        signal_day = data.index[loc + DAYS_AFTER]
        if _is_negative_surprise(data, date):
            result[signal_day] = False
        elif _is_positive_surprise(data, date):
            result[signal_day] = True
    return result.dropna()


def _is_negative_surprise(data, date):
    loc = data.index.get_loc(date)
    if (data['alpha'][date] < 0 and
        data['alpha'][loc:loc + 1 + DAYS_AFTER].sum() < 0 and
        data['alpha'][loc:loc + 1 + DAYS_AFTER].map(_func).sum() < -1):
        return True
    return False


def _is_positive_surprise(data, date):
    loc = data.index.get_loc(date)
    if (data['alpha'][date] > 0 and
        data['alpha'][loc:loc + 1 + DAYS_AFTER].sum() > 0 and
        data['alpha'][loc:loc + 1 + DAYS_AFTER].map(_func).sum() > 1):
        return True
    return False


def _func(x):
    if x < 0:
        return -1
    else:
        return 1


def get_news5days_descr(signal):
    if signal == True:
        result = DESCRIPTION_BUY
    elif signal == False:
        result = DESCRIPTION_SELL
    result += DESCRIPTION_COMMON
    return result
