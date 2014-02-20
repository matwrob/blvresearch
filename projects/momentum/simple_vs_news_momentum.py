"""
Concat: news from Friday evening (Saturday/Sunday) are assigned to Monday
any non-trading day news is assigned to the next trading day

This implies for TR Sentiment Data to discard 'date' column (which gives
dates of publication) and use only 'tdate' column (which gives the next
trading day)

"""

import pandas as pd

from blvresearch.core.portfolio import (
    PortfolioStrategy, SimpleMomentumStrategy, StockReturns, Portfolio
)
from blvresearch.core.SP500output import ABSRET, ALPHA, NEWS, SP500_RETURNS
from blvresearch.core.sentiment import RTRS_SENTIMENT_ENTITY
from blvresearch.core.utils import start, end

from blvworker.news.important_days import add_important_day_column





class SimpleMomentumStrategy_1W_1W_1W(SimpleMomentumStrategy):

    RANKING_PERIODS = 1
    PAUSE_PERIODS = 1
    HOLDING_PERIODS = 1
    REBALANCING_FREQUENCY = 'W'
    PORTFOLIO_SIZE = 20


class AlphaBasedMomentum_1W_1W_1W(SimpleMomentumStrategy_1W_1W_1W):

    def _get_returns(self):
        if self.REBALANCING_FREQUENCY in ['W-FRI', 'W']:
            return StockReturns(self.supplementary_data).weekly
        if self.REBALANCING_FREQUENCY in ['M']:
            return StockReturns(self.supplementary_data).monthly
        if self.REBALANCING_FREQUENCY in ['B', 'D']:
            return StockReturns(self.supplementary_data).daily
        raise AttributeError('Provide proper rebalancing frequency')
