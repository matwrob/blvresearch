import pandas as pd
import random

from blvresearch.core.portfolio import PortfolioStrategy, StockReturns
from concat.core.news import NewsList


class RandomPortfolioStrategy(PortfolioStrategy):
    """take long position in a random set of 20 stocks from the universe
    at each rebalancing day

    """
    NAME = 'Default strategy - random sample of securities'
    HOLDING_PERIODS = 1
    PAUSE_PERIODS = 0
    REBALANCING_FREQUENCY = 'M'
    PORTFOLIO_SIZE = 20

    def _get_positions(self):
        "randomly select N stocks from the UNIVERSE"
        all_entities = list(set(self.output.index.get_level_values(0)))
        result = dict()
        for day in self.rebalancing_days:
            random.shuffle(all_entities)
            result[day] = all_entities[:self.PORTFOLIO_SIZE]
        return pd.Series(result)


class Random2(RandomPortfolioStrategy):

    PORTFOLIO_SIZE = 2


class Random5(RandomPortfolioStrategy):

    PORTFOLIO_SIZE = 5


class Random10(RandomPortfolioStrategy):

    PORTFOLIO_SIZE = 10


class Random25(RandomPortfolioStrategy):

    PORTFOLIO_SIZE = 25


class MarketPortfolioStrategy(PortfolioStrategy):
    "use MarketStrategy to create the market portfolio"

    NAME = 'Benchmark strategy - long positions in all securities'
    HOLDING_PERIODS = 'Constant holding'
    PAUSE_PERIODS = 'Adjust depending on strategy benchmarked against market'
    REBALANCING_FREQUENCY = 'No rebalancing'
    PORTFOLIO_SIZE = 'All securities available'

    def _get_positions(self):
        all_entities = list(set(self.output.index.get_level_values(0)))
        result = {day: all_entities for day in self.rebalancing_days}
        return pd.Series(result)

    @property
    def rebalancing_days(self):
        return self._date_index


class Cheap10Strategy(PortfolioStrategy):
    "implemented only to check regression result of PortfolioCharacteristics"

    NAME = 'Long position in 10 stocks with lowest prices'
    HOLDING_PERIODS = 1
    PAUSE_PERIODS = 0
    REBALANCING_FREQUENCY = 'M'
    PORTFOLIO_SIZE = 10

    def _get_positions(self):
        close = self.output.close.unstack(level=0)
        close = close.resample(self.REBALANCING_FREQUENCY, how='mean')
        result = dict()
        for day in self.rebalancing_days:
            temp = close.loc[day].dropna()
            temp.sort()
            result[day] = temp.index[:self.PORTFOLIO_SIZE]
        return pd.Series(result)


class Pricy10Strategy(PortfolioStrategy):
    "implemented only to check regression result of PortfolioCharacteristics"

    NAME = 'Long position in 10 stocks with lowest prices'
    HOLDING_PERIODS = 1
    PAUSE_PERIODS = 0
    REBALANCING_FREQUENCY = 'M'
    PORTFOLIO_SIZE = 10

    def _get_positions(self):
        close = self.output.close.unstack(level=0)
        close = close.resample(self.REBALANCING_FREQUENCY, how='mean')
        result = dict()
        for day in self.rebalancing_days:
            temp = close.loc[day].dropna()
            temp.sort()
            result[day] = temp.index[-self.PORTFOLIO_SIZE:]
        return pd.Series(result)


