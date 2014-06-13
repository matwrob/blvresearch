import datetime as dt
import pandas as pd

from concat_overlord.standard import MeanSigma
from memnews.core import NewsList

TODAY = dt.datetime.today()


def get_suprises(data, entity_id):
    result = pd.Series(index=data.index)
    enough_days_before_event = lambda x: x - 22 > 0
    days_to_check = _get_days_to_check(data, entity_id)
    for i, day in enumerate(days_to_check.index):
        if enough_days_before_event(i):
            if _is_positive_suprise(data, day):
                result[day] = True
            elif _is_negative_suprise(data, day):
                result[day] = False
    return _remove_consecutive_values(result)


def _remove_consecutive_values(series):
    result = series.dropna()
    result[result.shift(1) == result] = None
    result = result.dropna()
    return result


def _get_days_to_check(df, entity_id):
    result = pd.Series(index=df.index)
    ms = MeanSigma(df['alpha'])
    news = df['news'].map(lambda x: True if isinstance(x, NewsList) else False)
    for date, row in df[news].iterrows():
        if (_has_relevant_news(row['news'], entity_id) and
            abs(row['alpha']) > ms.mean + 2 * ms.sigma):
            result[date] = True
    return result


def _has_relevant_news(news_list, entity_id):
    for n in news_list:
        if n['relevance'][entity_id]['score'] > 0.3:
            return True
    return False


def _is_negative_suprise(df, date):
    loc = df.index.get_loc(date)
    d = df['alpha'][date]
    w = df['alpha'][loc - 5:loc].sum()
    m = df['alpha'][loc - 22:loc].sum()
    q = df['alpha'][loc - 63:loc].sum()
    if d < 0:
        return True
    return False


def _is_positive_suprise(df, date):
    loc = df.index.get_loc(date)
    d = df['alpha'][date]
    w = df['alpha'][loc - 5:loc].sum()
    m = df['alpha'][loc - 22:loc].sum()
    q = df['alpha'][loc - 63:loc].sum()
    if d > 0:
        return True
    return False
