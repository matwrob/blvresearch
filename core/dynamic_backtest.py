import pandas as pd
import numpy as np

# from blvresearch.utils.risk_free_rates import RISK_FREE_RATES_


# Determine frequency of data points
# Available frequencies:
# 'D'       daily frequency (original data)
# 'W-SUN'   weekly frequency (sundays), the same as 'W'
# 'W-FRI'   weekly frequency (fridays)
# 'M'       monthly frequency


class Portfolio:
    pass


class DynamicBacktest:
    """
    to run dynamic backtest initiate a class that inherits from DynamicBacktest
    overwriting _get_starting_points_and_holdings method and providing:
    * total_output: original database
    * holding_periods: number of periods a given portfolio should be holdings
    * pause_periods: number of periods between the formation period and
                     a period when stocks should be held
    * entities: list of entities, if portfolios should be formed for a certain
                subset, e.g. entities from Europe only
    * data_frequency: provide frequency of returns, by default weekly returns
    * weighting: weighting applied to portfolio members, value-weighting by
                 default, possible also equal-weighting
    * transaction_cost: not implemented

    """
    def __init__(self, total_output, data_frequency=None,
                 holding_periods=1, pause_periods=1,
                 entities=None, weighting='equal', transaction_cost=0):
        self.o = total_output
        self.data_freq = data_frequency
        self.hold_per = holding_periods
        self.pause_per = pause_periods
        self.entities = entities
        self.weight = weighting
        self.trans_cost = transaction_cost

    def run(self):
        self.returns = self._get_returns_from_total_output()
        starting_points = self._get_starting_points_and_holdings()
        holdings = self._get_dataframe_of_holdings(starting_points)
        returns = self.returns[holdings.applymap(bool)]
        result = returns.mean(axis=1).dropna()
        return result, result.cumsum()

    def _get_returns_from_total_output(self):
        returns = self.o['abs_ret'].unstack(level=0)
        if self.data_freq:
            returns = returns.resample(self.data_freq, how='sum')
        if self.entities:
            return returns[self.entities]
        return returns

    def _get_dataframe_of_holdings(self, starting_points):
        result = pd.DataFrame(data=False, index=self.returns.index,
                              columns=self.returns.columns)
        ind = result.index
        for date, entities in starting_points.items():
            start_loc = result.index.get_loc(date)
            end_loc = start_loc + self.hold_per - 1
            result[ind[start_loc]:ind[end_loc]][entities] = True
        return result

    def _get_starting_points_and_holdings(self):
        raise NotImplementedError('overwrite this function')

    def _shift_and_trim_starting_points(self, series):
        result = series.shift(self.pause_per + 1)
        result = result.dropna()
        return result[:-self.hold_per]



class MarketPerformance:

    def __init__(self, dynamic_backtest):
        self.backtest = dynamic_backtest

    def get(self):
        returns = self.backtest.returns
        mkt_returns = self._calc_market_returns(returns)

    def _calculate_market_returns(self):
        if self.backtest.weight == 'equal':
            return returns.mean(axis=1)
        elif self.backtest_weight == 'value':
            raise NotImplementedError('no value-weighting yet')


class PortfolioCharacteristics:

    def __init__(self, portfolio_returns):
        self.port_ret = portfolio_returns

    def calculate(self):
        return {'mean_return': self._mean_return,
                'std_deviation': self._std_deviation}
        # 'alpha', t_stat_alpha = self._calc_alphas()
        # beta = self._calc_betas()
        # sharpe = self._calc_sharpe_ratio()
        # skew = self._calc_skeweness()

    @property
    def _mean_return(self):
        "values in percent and annualized"
        result = self.port_ret.mean()
        annualized = result * 12
        return annualized * 100

    @property
    def _std_deviation(self):
        result = self.port_ret.std()
        annualized = result * np.sqrt(12)
        return annualized * 100

    def _calc_alphas(self):
        pass
