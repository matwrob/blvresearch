import datetime as dt
import pandas as pd


TODAY = dt.datetime.today()


def get_signals(df):
    result = pd.Series(index=df.index)
    for i, day in enumerate(df.index):
        if _matches_criteria(df, day):
            two_days = df[i:i + 2]
            if all(two_days['alpha'] > 0):
                result.loc[df.index[i + 3]] = True
            elif all(two_days['alpha'] < 0):
                result.loc[df.index[i + 3]] = False
    result = _remove_consecutive_values(result)
    return result





def _matches_criteria(df, date):
    row = df.loc[date]
    c1 = df['important_day'][date] == True
    c2 = (TODAY - dt.datetime.fromtimestamp(date.timestamp())).days > 3
    if c1 and c2:
        return True


def _remove_consecutive_values(series):
    result = series.dropna()
    result[result.shift(1) == result] = None
    result = result.dropna()
    return result
