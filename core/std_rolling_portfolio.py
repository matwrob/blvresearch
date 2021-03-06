"""Jegadeesh & Titman (1993) and Fama (1998) use portfolios with overlapping
holding periods.

Example: strategy that selects stocks on the basis of returns over the past
         two months and holds them for two months (2M/2M strategy) is
         constructed as follows:

Step 0) we need to get a dataframe of returns with index being days and
        columns being entity ids
Step 1) depending on the frequency of data we want to use (e.g. J&T use
        quarterly returns), we need to resample our daily returns
Step 2) for each date we need to sort entities based on their returns over
        the previous 2 months
Step 3) list of winners is generated by taking the bottom quantile of sorted
        entities' returns
        list of losers is generated by taking the top quantile of sorted
        entities' returns
Step 4) having lists of winners/losers for each date we generate a map of
        booleans;
        here we need to take care of:
        i. shifting positions to the following periods (shift by 1 forward)
        ii. filling up as many next periods as specified by hold_per variable
Step 5) apply this map onto dataframe of returns, mean over all returns

"""

import pandas as pd


class JegadeeshTitman:  # pragma: no cover

    def __init__(self, research_data, type_of_return, no_of_quantiles):
        self.rd = research_data
        self.type = type_of_return
        self.quant = no_of_quantiles

    def get_winners_returns(self, data_freq, test_per, hold_per):
        returns = self._get_initial_returns(data_freq)
        winners = self._get_winners(returns, test_per)
        positions = get_portfolio_positions(returns, winners, hold_per)
        return get_mean_returns(returns, positions, hold_per)

    def get_losers_returns(self, data_freq, test_per, hold_per):
        returns = self._get_initial_returns(data_freq)
        losers = self._get_losers(returns, test_per)
        positions = get_portfolio_positions(returns, losers, hold_per)
        return get_mean_returns(returns, positions, hold_per)

    def get_wml_returns(self, data_freq, test_per, hold_per):
        win_ret = self.get_winners_returns(data_freq, test_per, hold_per)
        los_ret = self.get_losers_returns(data_freq, test_per, hold_per)
        return win_ret - los_ret

    def _get_winners(self, df_of_returns, test_per):  # pragma: no cover
        return get_winners(df_of_returns, test_per, self.quant)

    def _get_losers(self, df_of_returns, test_per):  # pragma: no cover
        return get_losers(df_of_returns, test_per, self.quant)

    def _get_initial_returns(self, freq):  # pragma: no cover
        result = get_dataframe_of_returns(self.rd, self.type)
        return result.resample(freq, how=sum)


def get_dataframe_of_returns(research_data, type_of_return='abs_ret'):
    """returns dataframe of a given type of returns
    research_data: output of get_research_data_by_country function or
                   get_research_data_by_entity function from research_data
                   module of blvresearch.core library

    type_of_return: 'abs_ret' for total return
                    'rel_ret' for relative return against benchmark
                              (abs_ret - benchmark)
                    'alpha' for risk adjusted relative return (concat model)

    """
    result = dict()
    for entity_id, df in research_data.items():
        result[entity_id] = df[type_of_return]
    return pd.DataFrame.from_dict(result)


def get_sorted_returns(df_of_returns, test_per):
    result = dict()
    for i in range(len(df_of_returns) - test_per + 1):
        frame = df_of_returns[i:i + test_per]
        series = frame.sum(skipna=False).dropna()
        series.sort()  # ascending sort, losers on top
        date = df_of_returns.index[i + test_per - 1]
        result[date] = series
    return result


def get_winners(df_of_returns, test_per, no_of_quantiles):
    """returns time series of best performing stocks over the test_per number
    of periods

    """
    result = dict()
    sorted_returns = get_sorted_returns(df_of_returns, test_per)
    for day, series in sorted_returns.items():
        size = int(len(series) / no_of_quantiles)
        result[day] = list(series[-size:].index)
    return pd.Series(result)


def get_losers(df_of_returns, test_per, no_of_quantiles):
    """returns time series of worst performing stocks over the test_per number
    of periods

    """
    result = dict()
    sorted_returns = get_sorted_returns(df_of_returns, test_per)
    for day, series in sorted_returns.items():
        size = int(len(series) / no_of_quantiles)
        result[day] = list(series[:size].index)
    return pd.Series(result)


def get_portfolio_positions(df_of_returns, entities, hold_per):
    result = pd.DataFrame(data=False, index=entities.index,
                          columns=df_of_returns.columns)
    for i, date in enumerate(result.index):
        result[i + 1: i + hold_per + 1][entities[date]] = True
    return result[1:]  # removes day without holdings


def get_mean_returns(df_of_returns, mapping, hold_per):
    df_of_returns = df_of_returns.loc[mapping.index]
    result = df_of_returns[mapping]
    result = result.mean(axis=1)
    return result[hold_per - 1:]
