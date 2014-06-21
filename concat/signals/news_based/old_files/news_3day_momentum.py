"""
OVERVIEW:
Simple strategy based on news.

First identifies important events by considering number of news published on
a given day, as well as this day's return.

Next it checks the market reaction to those events short after the event
(e.g. 3 trading days) and goes long if this return was significantly positive
or short if it was significantly negative

"""
import datetime as dt
import pandas as pd

from blvresearch.concat.signals.utils import remove_consecutive_values
from concat_overlord.standard import MeanSigma


YESTERDAY = dt.datetime.today() - pd.DateOffset(days=1)
YESTERDAY = pd.Timestamp(YESTERDAY, tz='UTC')

MOMENTUM_DAYS = 3

def get_signals(data):
    imp = data['important_day']
    ms = MeanSigma(data['alpha'])
    result = pd.Series(index=data.index)
    for this_date in imp[imp == True].index:
        loc = imp.index.get_loc(this_date)
        if (YESTERDAY - imp.index[loc]).days > MOMENTUM_DAYS:
            next_date = imp.index[imp.index.get_loc(this_date) + 1]
            this_row = data.loc[this_date]
            next_row = data.loc[next_date]
            if (abs(this_row['alpha']) > ms.mean + ms.sigma or
                abs(next_row['alpha']) > ms.mean + ms.sigma):
                result[this_date] = _find_out_type_of_signal(this_date, data)
    return remove_consecutive_values(result)


def _find_out_type_of_signal(date, data):
    if _is_negative_suprise(data, date):
        return False
    elif _is_positive_suprise(data, date):
        return True


def _is_negative_suprise(df, date):
    ret = df['alpha']
    loc = df.index.get_loc(date)
    if (ret[date] < 0 and
        ret[loc:loc + MOMENTUM_DAYS].sum() < 0 and
        ret[loc:loc + MOMENTUM_DAYS].map(func).sum() < 0):
        return True
    return False


def _is_positive_suprise(df, date):
    ret = df['alpha']
    loc = df.index.get_loc(date)
    if (ret[date] > 0 and
        ret[loc:loc + MOMENTUM_DAYS].sum() > 0 and
        ret[loc:loc + MOMENTUM_DAYS].map(func).sum() > 0):
        return True
    return False


def func(x):
    if x < 0:
        return -1
    else:
        return 1
