from itertools import product
import pandas as pd
import unittest

from blvresearch.core.portfolio import (
    StockReturns, PortfolioStrategy, Portfolio, PortfolioDates
)


INDEX = pd.MultiIndex.from_tuples(
    [v for v in product(['012ABC-D', '123BCD-E', '234CDE-F'],
                        pd.date_range('2003-01-02', '2003-03-31', freq='B'))]
)
DATA = ([[1, 2, 3]] * 21 + [[2, 3, 4]] * 21 + [[3, 4, 5]] * 21 +
        [[5, 4, 3]] * 21 + [[4, 3, 2]] * 21 + [[3, 2, 1]] * 21 +
        [[0, 3, 1]] * 21 + [[6, 4, 2]] * 21 + [[3, 6, 9]] * 21)
COLUMNS = ['abs_ret', 'rel_ret', 'alpha']
MOCK_OUTPUT = pd.DataFrame(data=DATA, index=INDEX, columns=COLUMNS)


class TestReturns(unittest.TestCase):

    result = StockReturns(MOCK_OUTPUT)

    def test_monthly(self):
        exp = pd.DataFrame(data=[[23, 109, 6], [40, 80, 120], [63, 63, 63]],
                           index=pd.date_range('2003-01-02', '2003-03-31',
                                               freq='BM'),
                           columns=['012ABC-D', '123BCD-E', '234CDE-F'])
        pd.np.testing.assert_array_equal(self.result.monthly, exp)

    def test_weekly(self):
        exp = pd.DataFrame(data=[[2, 10, 0], [5, 25, 0], [5, 25, 0],
                                 [5, 25, 0], [6, 24, 6], [10, 20, 30],
                                 [10, 20, 30], [10, 20, 30], [10, 20, 30],
                                 [15, 15, 15], [15, 15, 15], [15, 15, 15],
                                 [15, 15, 15], [3, 3, 3]],
                           index=pd.date_range('2003-01-02', '2003-04-06',
                                               freq='W'),
                           columns=['012ABC-D', '123BCD-E', '234CDE-F'])
        pd.np.testing.assert_array_equal(self.result.weekly, exp)

    def test_daily(self):
        expected = MOCK_OUTPUT['abs_ret'].unstack(level=0)
        pd.np.testing.assert_array_equal(self.result.daily, expected)


class TestPortfolioDates(unittest.TestCase):

    def test_case1(self):
        date_index = pd.date_range('2013-01-02', '2013-01-18', freq='D')
        rebal = 'B'
        rank, pause, hold = 1, 0, 1
        result = PortfolioDates(date_index, rebal, rank, pause, hold)

        exp_rank = pd.date_range('2013-01-02', '2013-01-17', freq='B')
        pd.np.testing.assert_array_equal(result.ranking_days,
                                         exp_rank)

        exp_rebal = pd.date_range('2013-01-02', '2013-01-17', freq='B')
        pd.np.testing.assert_array_equal(result.rebalancing_days,
                                         exp_rebal)

    def test_case2(self):
        date_index = pd.date_range('2013-01-02', '2013-01-18', freq='D')
        rebal = 'B'
        rank, pause, hold = 1, 1, 1
        result = PortfolioDates(date_index, rebal, rank, pause, hold)

        exp_rank = pd.date_range('2013-01-02', '2013-01-16', freq='B')
        pd.np.testing.assert_array_equal(result.ranking_days,
                                         exp_rank)

        exp_rebal = pd.date_range('2013-01-03', '2013-01-17', freq='B')
        pd.np.testing.assert_array_equal(result.rebalancing_days,
                                         exp_rebal)

    def test_case3(self):
        date_index = pd.date_range('2013-01-02', '2013-01-18', freq='D')
        rebal = 'B'
        rank, pause, hold = 5, 1, 3
        result = PortfolioDates(date_index, rebal, rank, pause, hold)

        exp_rebal = pd.DatetimeIndex([pd.datetime(2013, 1, 9),
                                      pd.datetime(2013, 1, 14),
                                      pd.datetime(2013, 1, 17)])
        pd.np.testing.assert_array_equal(result.rebalancing_days,
                                         exp_rebal)

        exp_rank = pd.DatetimeIndex([pd.datetime(2013, 1, 8),
                                     pd.datetime(2013, 1, 11),
                                     pd.datetime(2013, 1, 16)])
        pd.np.testing.assert_array_equal(result.ranking_days,
                                         exp_rank)

    def test_case4(self):
        date_index = pd.date_range('2013-01-02', '2013-01-31', freq='D')
        rebal = 'W-FRI'
        rank, pause, hold = 1, 1, 1
        result = PortfolioDates(date_index, rebal, rank, pause, hold)

        exp_rank = pd.DatetimeIndex([pd.datetime(2013, 1, 4),
                                     pd.datetime(2013, 1, 11),
                                     pd.datetime(2013, 1, 18)])
        pd.np.testing.assert_array_equal(result.ranking_days,
                                         exp_rank)

        exp_rebal = pd.DatetimeIndex([pd.datetime(2013, 1, 11),
                                      pd.datetime(2013, 1, 18),
                                      pd.datetime(2013, 1, 25)])
        pd.np.testing.assert_array_equal(result.rebalancing_days,
                                         exp_rebal)

    def test_case5(self):
        date_index = pd.date_range('2013-01-02', '2013-01-31', freq='D')
        rebal = 'W-FRI'
        rank, pause, hold = 2, 0, 1
        result = PortfolioDates(date_index, rebal, rank, pause, hold)

        exp_rank = pd.DatetimeIndex([pd.datetime(2013, 1, 11),
                                     pd.datetime(2013, 1, 18),
                                     pd.datetime(2013, 1, 25)])
        pd.np.testing.assert_array_equal(result.ranking_days,
                                         exp_rank)

        exp_rebal = pd.DatetimeIndex([pd.datetime(2013, 1, 11),
                                      pd.datetime(2013, 1, 18),
                                      pd.datetime(2013, 1, 25)])
        pd.np.testing.assert_array_equal(result.rebalancing_days,
                                         exp_rebal)

    def test_case6(self):
        date_index = pd.date_range('2013-01-02', '2013-07-03', freq='D')
        rebal = 'M'
        rank, pause, hold = 1, 1, 2
        result = PortfolioDates(date_index, rebal, rank, pause, hold)

        exp_rank = pd.DatetimeIndex([pd.datetime(2013, 1, 31),
                                     pd.datetime(2013, 3, 31),
                                     pd.datetime(2013, 5, 31)])
        pd.np.testing.assert_array_equal(result.ranking_days,
                                         exp_rank)

        exp_rebal = pd.DatetimeIndex([pd.datetime(2013, 2, 28),
                                      pd.datetime(2013, 4, 30),
                                      pd.datetime(2013, 6, 30)])
        pd.np.testing.assert_array_equal(result.rebalancing_days,
                                         exp_rebal)

    def test_case7(self):
        date_index = pd.date_range('2013-01-02', '2013-01-10', freq='D')
        rebal = 'B'
        rank, pause, hold = 0, 0, 1
        result = PortfolioDates(date_index, rebal, rank, pause, hold)

        exp_rank = list()
        pd.np.testing.assert_array_equal(result.ranking_days,
                                         exp_rank)

        exp_rebal = pd.DatetimeIndex([pd.datetime(2013, 1, 1),
                                      pd.datetime(2013, 1, 2),
                                      pd.datetime(2013, 1, 3),
                                      pd.datetime(2013, 1, 4),
                                      pd.datetime(2013, 1, 7),
                                      pd.datetime(2013, 1, 8),
                                      pd.datetime(2013, 1, 9)])
        pd.np.testing.assert_array_equal(result.rebalancing_days,
                                         exp_rebal)

    def test_case8(self):
        date_index = pd.date_range('2013-01-02', '2013-01-10', freq='D')
        rebal = 'B'
        rank, pause, hold = 0, 0, 2
        result = PortfolioDates(date_index, rebal, rank, pause, hold)

        exp_rank = list()
        pd.np.testing.assert_array_equal(result.ranking_days,
                                         exp_rank)

        exp_rebal = pd.DatetimeIndex([pd.datetime(2013, 1, 1),
                                      pd.datetime(2013, 1, 3),
                                      pd.datetime(2013, 1, 7),
                                      pd.datetime(2013, 1, 9)])
        pd.np.testing.assert_array_equal(result.rebalancing_days,
                                         exp_rebal)


class TestPortfolioStrategy(unittest.TestCase):

    class MockStrategy(PortfolioStrategy):
        HOLDING_PERIODS = 2
        PAUSE_PERIODS = 1
        REBALANCING_FREQUENCY = 'W-FRI'
        PORTFOLIO_SIZE = 20

        def _get_positions(self):
            all_entities = list(set(self.output.index.get_level_values(0)))
            result = dict()
            for day in self.rebalancing_days:
                result[day] = all_entities[:self.PORTFOLIO_SIZE]
            return pd.Series(result)

    STRATEGY = MockStrategy(MOCK_OUTPUT)

    def test_positions(self):
        self.assertIsInstance(self.STRATEGY.positions, pd.TimeSeries)

        exp = self.STRATEGY.rebalancing_days
        pd.np.testing.assert_array_equal(self.STRATEGY.positions.index, exp)

        for k, v in self.STRATEGY.positions.items():
            self.assertIsInstance(k, pd.tslib.Timestamp)
            self.assertIsInstance(v, list)

    def test_ranking_days(self):
        expected = ['2003-01-03', '2003-01-17', '2003-01-31', '2003-02-14',
                    '2003-02-28', '2003-03-14']
        for i, d in enumerate(expected):
            result = self.STRATEGY.ranking_days[i]
            self.assertEqual(d, result.strftime('%Y-%m-%d'))

    def test_rebalancing_days(self):
        expected = ['2003-01-10', '2003-01-24', '2003-02-07', '2003-02-21',
                    '2003-03-07', '2003-03-21']
        for i, d in enumerate(expected):
            result = self.STRATEGY.rebalancing_days[i]
            self.assertEqual(d, result.strftime('%Y-%m-%d'))


class TestPortfolio(unittest.TestCase):

    class MockStrategy(PortfolioStrategy):
        HOLDING_PERIODS = 2
        PAUSE_PERIODS = 1
        REBALANCING_FREQUENCY = 'W-FRI'
        PORTFOLIO_SIZE = 20

        def _get_positions(self):
            all_entities = list(set(self.output.index.get_level_values(0)))
            result = dict()
            for day in self.rebalancing_days:
                result[day] = all_entities[:self.PORTFOLIO_SIZE]
            return pd.Series(result)

    _STRATEGY = MockStrategy(MOCK_OUTPUT)
    PORTFOLIO = Portfolio(_STRATEGY)

    def test_daily_performance(self):
        result = self.PORTFOLIO.daily_performance()
        expected = pd.Series(data=[2] * 14 + [4] * 21 + [3] * 21,
                             index=pd.date_range('2003-01-13', '2003-03-31',
                                                 freq='B'))
        pd.np.testing.assert_array_equal(result, expected)

    def test_members(self):
        no_invest_period = self.PORTFOLIO.members['2003-01-02':'2003-01-12']
        pd.np.testing.assert_array_equal(no_invest_period.dropna(),
                                         pd.Series())

    def test_static_members(self):
        expected = set(['012ABC-D', '123BCD-E', '234CDE-F'])
        self.assertEqual(set(self.PORTFOLIO._static_members), expected)

    def test_holding_periods(self):
        self.assertEqual(self.PORTFOLIO.holding_periods, 2)

    def test_pause_periods(self):
        self.assertEqual(self.PORTFOLIO.pause_periods, 1)

    def test_size(self):
        self.assertEqual(self.PORTFOLIO.size, 20)

    def test_rebalancing_frequency(self):
        self.assertEqual(self.PORTFOLIO.rebalancing_frequency, 'W-FRI')


INDEX2 = pd.MultiIndex.from_tuples(
    [v for v in product(['012ABC-D', '123BCD-E', '234CDE-F'],
                        pd.date_range('2003-01-02', '2003-03-31', freq='B'))]
)
DATA2 = ([[1, 2, 3]] * 21 + [[2, 3, 4]] * 21 + [[3, 4, 5]] * 21 +
         [[5, 4, 3]] * 21 + [[4, 3, 2]] * 21 + [[3, 2, 1]] * 21 +
         [[0, 3, 1]] * 21 + [[6, 4, 2]] * 21 + [[3, 6, 9]] * 21)
COLUMNS2 = ['abs_ret', 'rel_ret', 'alpha']
MOCK_OUTPUT2 = pd.DataFrame(data=DATA2, index=INDEX2, columns=COLUMNS2)


class TestPortfolioStrategyWithRebalancingDays(unittest.TestCase):
    class MockStrategy(PortfolioStrategy):
        HOLDING_PERIODS = 2
        PAUSE_PERIODS = 1
        RANKING_PERIODS = 2
        REBALANCING_FREQUENCY = 'W'
        PORTFOLIO_SIZE = 2

        def _get_positions(self):
            returns = StockReturns(self.output).weekly
            result = dict()
            for day in self.rebalancing_days:
                temp = returns.loc[day].dropna()
                temp.sort()
                result[day] = temp.index[-self.PORTFOLIO_SIZE:]
            return pd.Series(result)

    STRATEGY = MockStrategy(MOCK_OUTPUT2)
