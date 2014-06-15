from itertools import chain

from memnews.core import NewsList
import pandas as pd


def get_counts_of_contemporaries(series_of_news_lists, news_filter_func):
    news = _filter_news(series_of_news_lists, news_filter_func)
    all_contemporaries = _get_all_contemporaries(series_of_news_lists)


def _get_all_contemporaries(series_of_news_lists):
    res = series_of_news_lists.map(_entities_within_news_list)



def _entities_within_news_list(news_list):
    res = list()
    for g in news_list.partiter(["relevance"]):
        res.extend(g["relevance"].keys())
    return res


def _filter_news(series_of_news_lists, filter_func):
    res = dict()
    for k, v in series_of_news_lists.items():
        res[k] = filter_func(v) if isinstance(x, NewsList) else v
    return pd.Series(res)


def _remove_duplicates(series_of_news_lists):
    def func(x):
        if isinstance(x, NewsList):
            return x.split_away_duplicates()[0]
        return x
    series_of_news_lists_without_duplicates = series_of_news_lists.map(func)
    return series_of_news_lists_without_duplicates
