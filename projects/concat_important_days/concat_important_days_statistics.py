import pandas as pd

from blvworker.news.important_days import add_important_day_column
from blvresearch.core.SP500output import ABSRET, ALPHA, NEWS
from blvresearch.core.es import EventStudy, find_events


def find_important_days(news, alpha):
    news_by_year = {g[0]: g[1] for g in news.groupby(news.index.year)}
    alpha_by_year = {g[0]: g[1] for g in alpha.groupby(alpha.index.year)}
    result = list()
    for year, news in news_by_year.items():
        df = get_news_alpha_dataframe(news, alpha_by_year[year])
        df = find_events(df, [add_important_day_column])
        result.append(df['important_day'].unstack().T)
    return merge_years(result)


def get_news_alpha_dataframe(news, alpha):
    news, alpha = news.T.stack(), alpha.T.stack()
    df = pd.concat([news, alpha], axis=1)
    df = df.rename(columns={0: 'news', 1: 'alpha'})
    return df


def merge_years(list_of_dataframes):
    result = pd.concat(list_of_dataframes).unstack().T
    result = result.fillna(value=False)
    return result


important_days = find_important_days(NEWS, ALPHA)
es = EventStudy(ABSRET, important_days)
important_days_returns = es.map_events_on_returns()


positive_returns = lambda df: df.applymap(lambda x: x >= 0)
negative_returns = lambda df: df.applymap(lambda x: x < 0)

important_days_positive = find_events(important_days_returns,
                                      [positive_returns])
important_days_negative = find_events(important_days_returns,
                                      [negative_returns])


def get_dataframe_of_mean_effects():
    lags = list(range(-10, 11))
    pos_es = EventStudy(important_days_positive, ABSRET)
    neg_es = EventStudy(important_days_negative, ABSRET)
    result = pd.DataFrame(index=lags, columns=['Positive', 'Negative'])
    for l in lags:
        pos_mean = pos_es.map_events_on_returns(lag=l).mean().mean()
        neg_mean = neg_es.map_events_on_returns(lag=l).mean().mean()
        result['Positive'][l] = pos_mean
        result['Negative'][l] = neg_mean
    return result
