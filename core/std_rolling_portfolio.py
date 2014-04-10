import pandas as pd


class JegadeeshReturns:
    """Jegadeesh & Titman (1993) and Fama (1998) use portfolios with
    overlapping holding periods.

    Example: strategy that selects stocks on the basis of returns over the past
    2 months and holds them for 2 months (2-month/2-month strategy) is
    constructed as follows:

    Step 0) we need to get a dataframe of returns with index being days and
            columns being entity ids
    Step 1) depending on the frequency of data we want to use (e.g. J&T use
            quarterly returns), we need to resample our daily returns

            get_resampled_returns

    Step 2) after resampling returns, we need to create another frame that
            contains cumulative returns for sorting entities;
            only resampling returns is not enough, because we may want to
            analyse returns of momentum strategy that uses, say, cumulative
            returns over past 2 months

            get_testing_returns

    Step 3) we need to select the top and the bottom quantiles of entities from
            the dataframe of testing returns for each date

            after determining Winners and Losers of each period we can generate
            a series of returns of these portfolios

    Step 1) having resampled returns, at the beginning of each period t
            the entities are then ranked in ascending order on the basis of
            their returns in the past 2 months

    """

    def __init__(research_data, type_of_return='abs_ret', no_of_quantiles=3):
        self.rd = research_data
        self.type = type_of_return
        self.quant = no_of_quantiles

    def get_winners_returns(self, data_freq, test_per, hold_per):
        returns = get_resampled_returns(self.rd,
                                        type_of_return=self.type,
                                        freq=data_freq)
        portfolios = get_losers(returns, test_per)
        return self._get_returns(returns, portfolios, hold_per)

    def get_losers_returns(self, data_freq, test_per, hold_per):
        returns = get_resampled_returns(self.rd,
                                        type_of_return=self.type,
                                        freq=data_freq)
        portfolios = get_losers(returns, test_per)
        return _get_returns(returns, portfolios, hold_per)

    def get_wml_returns(self, data_freq, test_per, hold_per):
        win_ret = self.get_winners_returns(data_freq, test_per, hold_per)
        los_ret = self.get_losers_returns(data_freq, test_per, hold_per)
        return win_ret - los_ret

    def _get_returns(df_of_returns, series_of_portfolios, holding_periods):
        df, sp, hp = df_of_returns, series_of_portfolios, holding_periods
        result = pd.DataFrame(data=False, index=df.index, columns=df.columns)
        for i in range(0, holding_periods):
            tmp = sp.shift(i + 1)
            result[tmp] = True



def get_dataframe_of_returns(research_data, type_of_return='abs_ret'):
    result = dict()
    for entity_id, df in research_data.items():
        result[entity_id] = df[type_of_return]
    result = pd.DataFrame.from_dict(result)
    return result


def get_resampled_returns(research_data, type_of_return='abs_ret', freq='M'):
    result = get_dataframe_of_returns(research_data, type_of_return)
    return result.resample(freq, how=sum)


def get_testing_returns(df, test_periods=1):
    result = dict()
    for i in range(len(df) - test_periods + 1):
        frame = df[i:i + test_periods]
        series = frame.dropna().sum()
        series.sort(ascending=False)
        date = df.index[i + test_periods - 1]
        result[date] = series
    return pd.DataFrame.from_dict(result, orient='index')


def get_winners(df_of_returns, test_periods=1, no_of_quantiles=3):
    df = get_testing_returns(df_of_returns, test_periods)
    result = pd.DataFrame(data=False,
                          index=df_of_returns.index,
                          columns=df_of_returns.columns)
    for date, series in df.iterrows():
        size = int(len(series) / no_of_quantiles)
        entities = list(series[:size].index)
        result.loc[date][entities] = True
    return result


def get_losers(df_of_returns, test_periods=1, no_of_quantiles=3):
    df = get_testing_returns(df_of_returns, test_periods)
    result = dict()
    for date, series in df.iterrows():
        size = int(len(series) / no_of_quantiles)
        entities = list(series[:size].index)
        result.loc[date][entities] = True
    return result
