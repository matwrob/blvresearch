import pandas as pd
import random

from blvresearch.core.portfolio import PortfolioStrategy


class RandomStocksStrategy(PortfolioStrategy):
    """take long position in a random set of 20 stocks from the universe
    at each rebalancing day

    """
    NAME = 'Default strategy - random sample of securities'
    HOLDING_PERIODS = 1
    PAUSE_PERIODS = 0
    REBALANCING_FREQUENCY = 'M'
    PORTFOLIO_SIZE = 20

    def _get_positions(self):
        "overwrite this function to implement your own strategy"
        all_entities = list(set(self.output.index.get_level_values(0)))
        result = dict()
        for day in self.rebalancing_days:
            random.shuffle(all_entities)
            result[day] = all_entities[:self.PORTFOLIO_SIZE]
        return pd.Series(result)


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


class Cheapest10Strategy(PortfolioStrategy):
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
