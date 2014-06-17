import pandas as pd

from blvresearch.concat.signals.utils import remove_consecutive_values
from concat_overlord.standard import MeanSigma
from memnews.core import NewsList


def get(data, entity_id):
    result = pd.Series(index=data.index)
    days_to_check = _get_days_to_check(data, entity_id)
    for i, day in enumerate(days_to_check.index):
        if _is_positive_suprise(data, day):
            result[day] = True
        elif _is_negative_suprise(data, day):
            result[day] = False
    return remove_consecutive_values(result)


def _get_days_to_check(entity_id, df):
    result = pd.Series(index=df.index)
    ms = MeanSigma(df['alpha'])
    for date, row in df.iterrows():
        if (_has_relevant_news(row['news'], entity_id) and
            abs(row['alpha']) > ms.mean):
            result[date] = True
    return result.dropna()


def _has_relevant_news(news_list, entity_id):
    if isinstance(news_list, list):
        return [n for n in news_list if n['irrelevant'] == False]


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
