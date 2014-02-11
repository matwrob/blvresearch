from itertools import chain
import pandas as pd
import numpy as np

from blvresearch.data.risk_free_rates import RISK_FREE_RATES
from concat.core.regression import fastols


class StockReturns:
    """container for stock returns
    provide Bluevalor Model data output and type of return on init
    types: 'abs_ret'   (default, total returns, Factset methodology)
           'rel_ret'   (returns relative to Blv benchmarks)
           'alpha'     (risk adjusted returns relative to Blv benchmarks)

    """

    def __init__(self, total_output, type_of_return='abs_ret'):
        self.o = total_output
        self.type = type_of_return

    @property
    def monthly(self):
        return self._unstacked.resample('M', how='sum')

    @property
    def weekly(self):
        return self._unstacked.resample('W', how='sum')

    @property
    def daily(self):
        return self._unstacked

    @property
    def _unstacked(self):
        return self.o[self.type].unstack(level=0)


class PortfolioDates:

    def __init__(self, date_index, ranking_periods, pause_periods,
                 holding_periods, rebalancing_frequency):
        self.date_index = date_index
        self.ranking_periods = ranking_periods
        self.pause_periods = pause_periods
        self.holding_periods = holding_periods
        self.rebalancing_frequency = rebalancing_frequency

    @property
    def ranking_days(self):
        "days when we perform security comparison on certain characteristics"
        first = self.ranking_periods - 1
        jump = self.holding_periods
        last = -jump - self.pause_periods
        return self._rebalanced_index[first:last:jump]

    @property
    def rebalancing_days(self):
        "days when portfolio is reconstructed"
        temp = list(self._rebalanced_index)
        positions = [temp.index(d) + self.pause_periods + 1
                     for d in self.ranking_days]
        dates = [temp[pos] for pos in positions]
        return pd.DatetimeIndex(dates)

    @property
    def _rebalanced_index(self):
        return pd.date_range(self.date_index[0],
                             self.date_index[-1],
                             freq=self.rebalancing_frequency)


class PortfolioStrategy:
    """determines a strategy for portfolio formation over time

    takes Bluevalor Model data output on init since any strategy one wants to
    test should utilize this data

    possible to adjust other attributes:
    * HOLDING_PERIODS
    * PAUSE_PERIODS
    * REBALANCING_FREQUENCY
    * PORTFOLIO_SIZE

    create your own strategy that inherits from PortfolioStrategy, overwrite
    _get_positions function with your methodology, adjust other global
    attributes according to your needs

    _get_positions must return a time series of lists of entities where index
    is given by .rebalancing_days

    """

    NAME = 'PortfolioStrategy'
    HOLDING_PERIODS = 0
    PAUSE_PERIODS = 0
    RANKING_PERIODS = 0
    REBALANCING_FREQUENCY = 'B'
    PORTFOLIO_SIZE = 0

    def __init__(self, bluevalor_model_output):
        self.output = bluevalor_model_output
        self.positions = self._get_positions()

    def __repr__(self):
        return self.NAME

    def _get_positions(self):
        raise NotImplementedError

    @property
    def rebalancing_days(self):
        return self._portfolio_dates.rebalancing_days

    @property
    def ranking_days(self):
        return self._portfolio_dates.ranking_days

    def _portfolio_dates(self):
        date_index = self.output.index.get_level_values(1).unique().order()
        return PortfolioDates(date_index,
                              self.RANKING_PERIODS,
                              self.PAUSE_PERIODS,
                              self.HOLDING_PERIODS,
                              self.REBALANCING_FREQUENCY)


class Portfolio:
    """represents the evolution of a portfolio of stocks over time
    on init takes portfolio_strategy:

    .members          to see time series of entities sets on a daily basis
    .performance      to see time series of returns

    feed PortfolioCharacteristics class with Portfolio instance to obtain
    a set of portfolio return characteristics (e.g. alpha, Sharpe ratio, etc.)

    """
    def __init__(self, portfolio_strategy):
        self.strategy = portfolio_strategy

    def daily_performance(self, how='mean'):
        returns = self._members_returns.daily
        members = self.members
        result = {k: returns.loc[k][v].mean() for k, v in members.items()}
        result = pd.Series(result, name='daily_returns').fillna(0)
        return result

    @property
    def _members_returns(self):
        return StockReturns(self._output_data.ix[self._static_members])

    @property
    def members(self):
        new_index = self._members_returns.daily.index
        result = self.strategy.positions.reindex(new_index, method='ffill')
        return result.shift(1).dropna()

    @property
    def _static_members(self):
        return list(set(chain.from_iterable(self.strategy.positions)))

    @property
    def _output_data(self):
        return self.strategy.output

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
