import pandas as pd


def get_days_to_check(entity_data):
    """returns pandas Series object with index representing days where
    relevant news occurred and alpha was abnormal (on that day, or 2 days
    around that day)

    alpha is abnormal if it is greater than mean alpha + 1 standard deviation
    or smaller than mean alpha - 1 standard deviation

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
    for date in entity_data[first_day:last_day].index:
        yesterday, today, tomorrow = _get_rows(date, entity_data)
        if (_has_relevant_news(today['news']) and
            _has_abnormal_alpha(yesterday, today, tomorrow,
                                mean[date], std[date])):
            result[date] = True
    return result.dropna(), first_loc, last_loc


def _get_rows(date, data):
    loc = data.index.get_loc(date)
    row1 = data.loc[data.index[loc - 1]]
    row2 = data.loc[data.index[loc]]
    row3 = data.loc[data.index[loc + 1]]
    return row1, row2, row3


def _has_relevant_news(news_list):
    if isinstance(news_list, list):
        relevant_news = [n for n in news_list if n['irrelevant'] == False]
        if len(relevant_news) > 0:
            return True
    return False


def _has_abnormal_alpha(yesterday, today, tomorrow, mean, std):
    if _value_is_abnormal(yesterday['alpha'], mean, std):
        return True
    elif _value_is_abnormal(today['alpha'], mean, std):
        return True
    elif _value_is_abnormal(tomorrow['alpha'], mean, std):
        return True
    return False


def _value_is_abnormal(alpha, mean, std):
    if alpha > mean + std or alpha < mean - std:
        return True
    return False
