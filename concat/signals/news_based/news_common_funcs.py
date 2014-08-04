import pandas as pd


def get_days_to_check(entity_data):
    """returns pandas Series object with index representing days where
    relevant news occurred and alpha was abnormal

    alpha is abnormal if it is greater than mean + 2 standard deviations
    or smaller than mean - 2 standard deviations

    expected value & standard deviation are calculated based on previous
    125 days (c.a. 6 months)

    """
    mean = pd.rolling_mean(entity_data['alpha'], window=125)
    std = pd.rolling_std(entity_data['alpha'], window=125)

    first_day = mean.dropna().index[0]
    first_loc = entity_data['alpha'].index.get_loc(first_day)
    last_day = entity_data.index[-2]
    last_loc = entity_data['alpha'].index.get_loc(last_day)

    result = pd.Series(index=entity_data.index)
    for date, row in entity_data[first_day:last_day].iterrows():
        if (_has_relevant_news(row['news']) and
            _has_abnormal_alpha(row['alpha'], mean[date], std[date])):
            result[date] = True
    return result.dropna(), first_loc, last_loc


def _has_relevant_news(news_list):
    if isinstance(news_list, list):
        relevant_news = [n for n in news_list if n['irrelevant'] == False]
        if len(relevant_news) > 0:
            return True
    return False


def _has_abnormal_alpha(alpha, mean, std):
    if alpha > mean + 2 * std or alpha < mean - 2 * std:
        return True
    return False
