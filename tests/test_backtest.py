from itertools import product
import pandas as pd
import unittest

from blvresearch.core.portfolio import (
    StockReturns, PortfolioStrategy, Portfolio
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


class TestPortfolioStrategy(unittest.TestCase):

    class MockStrategy(PortfolioStrategy):
        HOLDING_PERIODS = 2
        PAUSE_PERIODS = 1
        REBALANCING_FREQUENCY = 'W-FRI'

    STRATEGY = MockStrategy(MOCK_OUTPUT)

    def test_positions(self):
        self.assertIsInstance(self.STRATEGY.positions, pd.Series)

    def test_rebalancing_days(self):
        expected = ['2003-01-17', '2003-01-24', '2003-01-31', '2003-02-07',
                    '2003-02-14', '2003-02-21', '2003-02-28', '2003-03-07',
                    '2003-03-14']
        for i, d in enumerate(self.STRATEGY.rebalancing_days):
            self.assertEqual(d.strftime('%Y-%m-%d'), expected[i])

    def test_date_index(self):
        expected = pd.date_range('2003-01-02', '2003-03-31', freq='B')
        pd.np.testing.assert_array_equal(self.STRATEGY._date_index.values,
                                         expected.values)


class TestPortfolio(unittest.TestCase):

    class MockStrategy(PortfolioStrategy):
        HOLDING_PERIODS = 2
        PAUSE_PERIODS = 1
        REBALANCING_FREQUENCY = 'W-FRI'

    _STRATEGY = MockStrategy(MOCK_OUTPUT)
    PORTFOLIO = Portfolio(_STRATEGY)

    def test_daily_performance(self):
        result = self.PORTFOLIO.daily_performance()
        expected = pd.Series(data=[2] * 21 + [4] * 21 + [3] * 21,
                             index=pd.date_range('2003-01-02', '2003-03-31',
                                                 freq='B'))
        pd.np.testing.assert_array_equal(result, expected)

    def test_members(self):
        no_investment_period = self.PORTFOLIO.members['2003-01-02':'2003-01-16']
        pd.np.testing.assert_array_equal(no_investment_period.dropna(),
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
