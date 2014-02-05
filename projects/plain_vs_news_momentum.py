import pandas as pd

from blvresearch.core.dynamic_backtest import DynamicBacktest


class OneMonthMomentumPortfolioWINNERS(DynamicBacktest):

    HOLDING_PERIODS = 30

    def _get_starting_points_and_holdings(self):
        SIZE = lambda x: int(len(x) / 10)
        result = dict()
        for k, v in self._ranking_period_returns.iterrows():
            v = v.dropna()
            v.sort(ascending=False)
            result[k] = list(v[:SIZE(v)].index)
        result = pd.Series(result)
        return self._shift_and_trim_starting_points(result)


class OneMonthMomentumPortfolioLOSERS(DynamicBacktest):

    def _get_starting_points_and_holdings(self):
        SIZE = lambda x: int(len(x) / 10)
        result = dict()
        for k, v in self._ranking_period_returns.iterrows():
            v = v.dropna()
            v.sort(ascending=False)
            result[k] = list(v[-SIZE(v):].index)
        result = pd.Series(result)
        return self._shift_and_trim_starting_points(result)


class OneMonthMomentumPortfolioWINNERSwithNews(DynamicBacktest):

    def _get_starting_points_and_holdings(self):
        SIZE = lambda x: int(len(x) / 10)
        result = dict()
        for k, v in self.returns.iterrows():
            v = v.dropna()
            v.sort(ascending=False)
            result[k] = list(v[:SIZE(v)].index)
        result = pd.Series(result)
        return self._shift_and_trim_starting_points(result)
