import pandas as pd

from blvresearch.core.portfolio import (
    PositiveMomentumStrategy, NegativeMomentumStrategy, Portfolio
)
from blvresearch.core.SP500output import ABSRET, SP500_RETURNS
from blvresearch.core.plotting import FinPlotter


class PositiveMomentum_r1m_p1m_h1m(PositiveMomentumStrategy):
    RANKING_PERIODS = 1
    PAUSE_PERIODS = 1
    HOLDING_PERIODS = 1
    REBALANCING_FREQUENCY = 'M'
    PORTFOLIO_SIZE = 20


class NegativeMomentum_r1m_p1m_h1m(NegativeMomentumStrategy):
    RANKING_PERIODS = 1
    PAUSE_PERIODS = 1
    HOLDING_PERIODS = 1
    REBALANCING_FREQUENCY = 'M'
    PORTFOLIO_SIZE = 20


class PositiveMomentum_r4w_p1w_h4w(PositiveMomentumStrategy):
    RANKING_PERIODS = 4
    PAUSE_PERIODS = 1
    HOLDING_PERIODS = 4
    REBALANCING_FREQUENCY = 'W'
    PORTFOLIO_SIZE = 20


class NegativeMomentum_r4w_p1w_h4w(NegativeMomentumStrategy):
    RANKING_PERIODS = 4
    PAUSE_PERIODS = 1
    HOLDING_PERIODS = 4
    REBALANCING_FREQUENCY = 'W'
    PORTFOLIO_SIZE = 20


def plot_pos_neg_wml_sp500(PosStrat, NegStrat):
    pos, neg = PosStrat(ABSRET), NegStrat(ABSRET)
    pos_port, neg_port = Portfolio(pos), Portfolio(neg)
    pos_perf = pos_port.daily_performance()
    neg_perf = neg_port.daily_performance()
    pos_perf.name, neg_perf.name = 'Positive momentum', 'Negative momentum'
    sp500_perf = SP500_RETURNS
    sp500_perf.name = 'SP500'
    wml_perf = pos_perf - neg_perf
    wml_perf.name = 'Winners minus Losers'
    data = pd.concat([sp500_perf, pos_perf, neg_perf, wml_perf], axis=1)
    first_holding_day = pos.positions.dropna().index[0]
    data = data[first_holding_day:]
    data = data.fillna(0)
    fp = FinPlotter(data.cumsum())
    fp.plot()
    return data
