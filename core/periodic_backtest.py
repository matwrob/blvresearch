import pandas as pd
import numpy as np

import random

# from blvresearch.utils.risk_free_rates import RISK_FREE_RATES_


class PeriodicBacktest:
    """
    to run periodic backtest initiate a class that inherits from it overwriting
    overwriting _get_starting_points_and_holdings method and optionally
    any global attributes; at init provide:
    * total_output: original database
    * entities: list of entities, if portfolios should be formed for a certain
                subset, e.g. entities from Europe only

    """
    DATA_FREQUENCY = None
    REBALANCING = 'BM'     # frequency of portfolio rebalancing
    RANKING_PERIODS = 5    # number of periods used to rank entities
    HOLDING_PERIODS = 20
    PAUSE_PERIODS = 3
    WEIGHTING = 'equal'
    TRANSACTION_COSTS = 0
    TYPE_OF_RETURNS = 'abs_ret'

    def __init__(self, list_of_portfolios):
        self.o = total_output
        self.entities = entities

    def run(self):
        self.returns = self._get_returns_from_total_output()
        starting_points = self._get_starting_points_and_holdings()
        holdings = self._get_dataframe_of_holdings(starting_points)
        returns = self.returns[holdings.applymap(bool)]
        result = returns.mean(axis=1).dropna()
        return result, result.cumsum()

    def _get_returns_from_total_output(self):
        stock_returns = StockReturns(self.o, self.TYPE_OF_RETURNS)
        if self.DATA_FREQUENCY == 'M':
            returns = stock_returns.monthly
        elif self.DATA_FREQUENCY == 'W':
            returns = stock_returns.weekly
        else:
            returns = stock_returns.daily
        if self.entities:
            return returns[self.entities]
        return returns

    def _get_dataframe_of_holdings(self, starting_points):
        result = pd.DataFrame(data=False,
                              index=self.returns.index,
                              columns=self.returns.columns)
        ind = result.index
        for date, entities in starting_points.items():
            start_loc = result.index.get_loc(date)
            end_loc = start_loc + self.HOLDING_PERIODS - 1
            result[ind[start_loc]:ind[end_loc]][entities] = True
        return result

    def _get_starting_points_and_holdings(self):
        raise NotImplementedError('overwrite this function')

    def _shift_and_trim_starting_points(self, series):
        result = series.shift(self.PAUSE_PERIODS + 1)
        result = result.dropna()[:-self.HOLDING_PERIODS]
        return self._apply_rebalancing_frequency(result)

    def _apply_rebalancing_frequency(self, series):
        index = series.resample(self.REBALANCING, how=len)
        return series[index]

    @property
    def _ranking_period_returns(self):
        def func(column):
            return pd.rolling_sum(column, self.RANKING_PERIODS)
        result = self.returns.apply(func)
        return result.dropna()
