from itertools import chain
import pandas as pd
import random


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


class PortfolioStrategy:
    """determines a strategy for portfolio formation over time

    takes Bluevalor Model data output on init since any strategy one wants to
    test should utilize this data

    possible to adjust other attributes:
    * HOLDING_PERIODS
    * PAUSE_PERIODS
    * REBALANCING_FREQUENCY
    * PORTFOLIO_SIZE

    to use: overwrite _get_starting_points function with any kind of algorithm
    that returns time series of lists of entities

    _get_starting_points by default returns a random subset of (size
    PORTFOLIO_SIZE) of all stocks from the universe for each rebalancing day

    """
    NAME = 'Default strategy - random sample of securities'
    HOLDING_PERIODS = 1
    PAUSE_PERIODS = 1
    REBALANCING_FREQUENCY = 'BM'
    PORTFOLIO_SIZE = 20

    def __init__(self, bluevalor_model_output):
        self.output = bluevalor_model_output
        self.positions = self._get_positions()

    def __repr__(self):
        return self.NAME

    def _get_positions(self):
        "overwrite this function to implement your own strategy"
        all_entities = list(set(self.output.index.get_level_values(0)))
        result = dict()
        for day in self.rebalancing_days:
            random.shuffle(all_entities)
            result[day] = all_entities[:self.PORTFOLIO_SIZE]
        return pd.Series(result)

    @property
    def rebalancing_days(self):
        result = pd.date_range(self._date_index[0], self._date_index[-1],
                               freq=self.REBALANCING_FREQUENCY)
        return result[self.PAUSE_PERIODS + 1: -self.HOLDING_PERIODS]

    @property
    def _date_index(self):
        return self.output.index.get_level_values(1).unique().order()


class MarketStrategy(PortfolioStrategy):
    "create a market portfolio as a Portfolio based on MarketStrategy"

    NAME = 'Benchmark strategy - hold portfolio of all securities'
    HOLDING_PERIODS = 0
    PAUSE_PERIODS = 0
    RABALANCING_FREQUENCY = 'D'

    def _get_positions(self):
        all_entities = list(set(self.output.index.get_level_values(0)))
        result = {day: all_entities for day in self.rebalancing_daysdict()
        return pd.Series(result)


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
        result = {date: row.mean() for date, row in returns.iterrows()}
        return pd.Series(result)

    @property
    def _members_returns(self):
        return StockReturns(self._output_data.ix[self._static_members])

    @property
    def members(self):
        new_index = self.strategy._date_index
        return self.strategy.positions.reindex(new_index, method='ffill')

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
