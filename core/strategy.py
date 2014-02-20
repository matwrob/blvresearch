import pandas as pd
from datetime import timedelta

from blvresearch.core.portfolio import StockReturns, PortfolioDates


class PortfolioStrategy:
    """ Determines a strategy for portfolio formation over time
    takes on init returns data and any supplementary data that should be used
    to determine which stocks should enter portfolio at which time

    .positions: dataframe indexed by time (daily) with columns representing
                entities and values being booleans
                open on init and filled initially with False
                _compute_positions fills proper cells with True whenever a
                given entity should be held in the portfolio

    """
    NAME = 'Portfolio strategy'
    RANKING_PERIODS = 1
    PAUSE_PERIODS = 1
    HOLDING_PERIODS = 1
    REBALANCING_FREQUENCY = 'B'
    PORTFOLIO_SIZE = 1

    def __init__(self, returns, supplementary_data=None):
        self.returns = returns
        self.supplementary_data = supplementary_data
        self.positions = pd.DataFrame(data=False,
                                      index=returns.index,
                                      columns=returns.columns)

    def __repr__(self):
        return self.NAME

    def calculate(self):
        raise NotImplementedError

    def _get_returns(self):
        if self.REBALANCING_FREQUENCY in ['W-FRI', 'W']:
            return StockReturns(self.returns).weekly
        if self.REBALANCING_FREQUENCY in ['M']:
            return StockReturns(self.returns).monthly
        if self.REBALANCING_FREQUENCY in ['B', 'D']:
            return StockReturns(self.returns).daily
        raise AttributeError('Provide proper rebalancing frequency')


class StaticStrategy(PortfolioStrategy):

    def _compute_positions(self, data):
        for ix, rank_end in enumerate(self.ranking_days):
            rank_start = self._get_ranking_period_start(rank_end)
            entities = self._select_entities(data[rank_start:rank_end])
            holding_dates = self._get_holding_dates(ix)
            self._set_positions(entities, holding_dates)
        self.positions = self.positions.shift(1).fillna(False)

    def _set_positions(self, list_of_entities, holding_dates):
            if isinstance(holding_dates, tuple):
                s, e = holding_dates[0], holding_dates[1]
                self.positions[s:e][list_of_entities] = True
            else:
                self.positions[holding_dates:][list_of_entities] = True

    def _get_holding_dates(self, start_position):
        rebal_day = self.rebalancing_days[start_position]
        hold_start = get_date_position_in_index(self.positions.index,
                                                rebal_day)
        if start_position + 1 < len(self.rebalancing_days):
            next_rebal_day = self.rebalancing_days[start_position + 1]
            hold_end = get_date_position_in_index(self.positions.index,
                                                  next_rebal_day)
            return (self.positions.index[hold_start],
                    self.positions.index[hold_end - 1])
        return self.positions.index[hold_start]

    def _get_ranking_period_start(self, end_date):
        rebalanced_dates = list(self._portfolio_dates._rebalanced_index)
        position = rebalanced_dates.index(end_date)
        return rebalanced_dates[position - self.RANKING_PERIODS + 1]

    @property
    def rebalancing_days(self):
        return self._portfolio_dates.rebalancing_days

    @property
    def ranking_days(self):
        return self._portfolio_dates.ranking_days

    @property
    def _portfolio_dates(self):
        return PortfolioDates(self.returns.index,
                              self.REBALANCING_FREQUENCY,
                              self.RANKING_PERIODS,
                              self.PAUSE_PERIODS,
                              self.HOLDING_PERIODS)


class PositiveMomentumStrategy(StaticStrategy):

    NAME = 'Simple positive momentum - static strategy'
    RANKING_PERIODS = 2
    PAUSE_PERIODS = 1
    HOLDING_PERIODS = 2
    REBALANCING_FREQUENCY = 'W'
    PORTFOLIO_SIZE = 1

    def calculate(self):
        returns = self._get_returns()
        self._compute_positions(returns)

    def _select_entities(self, data):
        data = data.sum().dropna()
        data.sort(ascending=True)
        return self._get_slice(data)

    def _get_slice(self, series):
        return TOP_SLICE(series, self.PORTFOLIO_SIZE)


class NegativeMomentumStrategy(PositiveMomentumStrategy):

    NAME = 'Simple negative momentum - static strategy'

    def _get_slice(self, series):
        return BOTTOM_SLICE(series, self.PORTFOLIO_SIZE)


class DynamicStrategy(PortfolioStrategy):
    """Dynamic strategies should use for Rebalancing Frequency only business
    end periods, e.g. 'B', 'W-FRI', 'BM'"""

    NAME = 'Dynamic strategy'
    RANKING_PERIODS = 0
    PAUSE_PERIODS = 0
    HOLDING_PERIODS = 5
    REBALANCING_FREQUENCY = 'B'
    PORTFOLIO_SIZE = 20

    def _compute_positions(self, data):
        for ix, rank_end in enumerate(self.ranking_days):
            rank_start = self._get_ranking_period_start(rank_end)
            entities = self._select_entities(data[rank_start:rank_end])
            holding_dates = self._get_holding_dates(ix)
            self._set_positions(entities, holding_dates)
        self.positions = self.positions.shift(1).fillna(False)

    def _set_positions(self, list_of_entities, holding_dates):
            if isinstance(holding_dates, tuple):
                s, e = holding_dates[0], holding_dates[1]
                self.positions[s:e][list_of_entities] = True
            else:
                self.positions[holding_dates:][list_of_entities] = True

    def _get_holding_dates(self, start_position):
        rebal_day = self.rebalancing_days[start_position]
        hold_start = get_date_position_in_index(self.positions.index,
                                                rebal_day)
        if start_position + 1 < len(self.rebalancing_days):
            tmp = self.rebalancing_days[start_position + self.HOLDING_PERIODS]
            hold_end = get_date_position_in_index(self.positions.index, tmp)
            return (self.positions.index[hold_start],
                    self.positions.index[hold_end - 1])
        return self.positions.index[hold_start]

    def _get_ranking_period_start(self, end_date):
        end = get_date_position_in_index(self.positions.index, end_date)
        start = end - self.RANKING_PERIODS
        return self.positions.index[start]

    @property
    def ranking_days(self):
        start = max(self.RANKING_PERIODS - 1, 0)
        end = -self.PAUSE_PERIODS - 1
        return self.positions.index[start:end]

    @property
    def rebalancing_days(self):
        start = self.RANKING_PERIODS + self.PAUSE_PERIODS
        end = -1
        return self.positions.index[start:end]


import random


class RandomStockUpTo20(DynamicStrategy):

    NAME = "Random Stock holding up to 20 in total"
    RANKING_PERIODS = 0
    PAUSE_PERIODS = 0
    HOLDING_PERIODS = 10
    REBALANCING_FREQUENCY = 'B'
    PORTFOLIO_SIZE = 20

    def calculate(self):
        returns = self._get_returns()
        self._compute_positions(returns)

    def _select_entities(self, returns):
        tmp = list(returns.index)
        random.shuffle(tmp)
        return tmp[:1]



# class PositiveRolling95(DynamicStrategy):
#     """
#     Dynamic strategy that holds stocks if their return exceeds threshold based
#     on returns of last 22 days (mean + 2 * sigma)

#     """
#     NAME = "Positive rolling strategy 95% - dynamic strategy"
#     REBALANCING_FREQUENCY = "B"
#     RANKING_PERIODS = 0
#     PAUSE_PERIODS = 0
#     HOLDING_PERIODS = 20

#     def _select_entities(self, data):
#         pass


def get_date_position_in_index(index, timestamp):
    if timestamp >= index[0]:
        if timestamp in index:
            return index.get_loc(timestamp)
        else:
            tmp = timestamp - timedelta(days=1)
            return get_date_position_in_index(index, tmp)
    else:
        raise AttributeError('Given date is before index starts')


TOP_SLICE = lambda series, size: list(series[-size:].index)
BOTTOM_SLICE = lambda series, size: list(series[:size].index)
