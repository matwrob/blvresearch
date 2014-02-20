from itertools import chain
import pandas as pd
import numpy as np

from blvresearch.data.risk_free_rates import RISK_FREE_RATES
from concat.core.regression import fastols


class StockReturns:

    def __init__(self, df_of_returns):
        self._all_returns = df_of_returns

    @property
    def monthly(self):
        return self._all_returns.resample('M', how='sum')

    @property
    def weekly(self):
        return self._all_returns.resample('W', how='sum')

    @property
    def daily(self):
        return self._all_returns


class PortfolioDates:

    def __init__(self, date_index, main_frequency,
                 rebalancing_periods, ranking_periods, pause_periods,
                 holding_periods):
        self.index = date_index
        self.main_freq = main_frequency
        self.reb_per = rebalancing_periods
        self.rank_per = ranking_periods
        self.pause_per = pause_periods
        self.hold_per = holding_periods

    @property
    def ranking_days(self):
        start = self.rank_per - 1 if self.rank_per else -1
        end = -self.pause_per - 1
        if start == -1:
            return list()
        return self._rebalanced_index[start:end]

    @property
    def rebalancing_days(self):
        start = self.rank_per + self.pause_per - 1
        end = -1
        if start == -1:
            ind = self._rebalanced_index
            temp = ind.insert(0, ind[0] - 1)
            return temp[:end]
        return self._rebalanced_index[start:end]

    @property
    def _rebalanced_index(self):
        temp = pd.Series(index=self.index)
        return temp.resample(self.main_freq).index


class Portfolio:
    """represents the portfolio of stocks over time; on init takes
    PortfolioStrategy:

    .members          to see time series of entities' sets on a daily basis
    .performance      to see time series of returns

    feed PortfolioCharacteristics class with Portfolio instance to obtain
    a set of portfolio return characteristics (e.g. alpha, Sharpe ratio, etc.)

    """
    def __init__(self, portfolio_strategy):
        self.strategy = portfolio_strategy

    def daily_performance(self, how='mean'):
        returns = self._members_returns.daily
        result = dict()
        for k, v in self.members.items():
            if type(v) == list:
                result[k] = returns.loc[k][v].mean()
            else:
                result[k] = 0
        return pd.Series(result, name='daily_returns')

    @property
    def members(self):
        return self.strategy.positions

    @property
    def _static_members(self):
        positions = self.strategy.positions.dropna()
        return list(set(chain.from_iterable(positions)))

    @property
    def _members_returns(self):
        returns = self.strategy.returns[self._static_members]
        return StockReturns(returns)

    @property
    def _output_data(self):
        return self.strategy.output

    @property
    def ranking_periods(self):
        return self.strategy.RANKING_PERIODS

    @property
    def holding_periods(self):
        return self.strategy.HOLDING_PERIODS

    @property
    def pause_periods(self):
        return self.strategy.PAUSE_PERIODS

    @property
    def size(self):
        return self.strategy.PORTFOLIO_SIZE

    @property
    def rebalancing_frequency(self):
        return self.strategy.REBALANCING_FREQUENCY


class PortfolioCharacteristics:

    def __init__(self, benchmark_portfolio):
        self.benchmark = benchmark_portfolio

    def get(self, portfolio):
        self._load_returns(portfolio)
        self.excess_over_risk_free = self._get_excess_over_risk_free()
        self.excess_over_market = self._get_excess_over_market()
        self.mean_yearly_excess_over_rf = self._get_mean_yearly_excess_rf()
        self.mean_yearly_excess_over_mkt = self._get_mean_yearly_excess_mkt()
        self.mean_yearly_std = self._get_mean_yearly_standard_deviation()
        self.alpha, self.beta, self.r2 = self._run_regression()

    def _load_returns(self, portfolio):
        self.portfolio_returns = portfolio.daily_performance()
        self.benchmark_returns = self.benchmark.daily_performance()
        self.risk_free = RISK_FREE_RATES['B']
        self.bench_exc_ret = (self.benchmark_returns - self.risk_free).dropna()

    def _get_excess_over_risk_free(self):
        result = self.portfolio_returns - self.risk_free
        return result.dropna()

    def _get_excess_over_market(self):
        result = self.portfolio_returns - self.benchmark_returns
        return result.dropna()

    def _get_mean_yearly_excess_rf(self):
        "values in percentage and annualized"
        result = self.excess_over_risk_free.resample('A', how='sum')
        return result.mean() * 100

    def _get_mean_yearly_excess_mkt(self):
        "values in percentage and annualized"
        result = self.excess_over_market.resample('A', how='sum')
        return result.mean() * 100

    def _get_mean_yearly_standard_deviation(self):
        "values in percentage and annualized"
        result = self.excess_over_risk_free.std()
        return result * np.sqrt(12) * 100

    def _run_regression(self):
        y = self.excess_over_risk_free
        x = self.bench_exc_ret
        result = fastols.regress(y, x[y.index])
        return result['a'], result['b1'], result['r2']
