import unittest
import pandas as pd

from blvresearch.core.portfolio import StockReturns, PortfolioStrategy


INDEX = pd.MultiIndex.from_tuples(
    [('012ABC-D', d)
     for d in pd.date_range('2003-01-02', '2003-03-31', freq='B')]
)
RETURNS = [1] * 63
DATA = [[v, v * (-1), v * (-2)] for v in RETURNS]
COLUMNS = ['abs_ret', 'rel_ret', 'alpha']
MOCK_OUTPUT = pd.DataFrame(data=DATA, index=INDEX, columns=COLUMNS)


class TestReturns(unittest.TestCase):

    result = StockReturns(MOCK_OUTPUT)

    def test_monthly(self):
        expected = pd.DataFrame([22, 20, 21],
                                index=pd.date_range('2003-01-02',
                                                    '2003-03-31',
                                                    freq='BM'),
                                columns=['012ABC-D'])
        pd.np.testing.assert_array_equal(self.result.monthly, expected)

    def test_weekly(self):
        expected = pd.DataFrame([2, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 1],
                                index=pd.date_range('2003-01-02',
                                                    '2003-04-04',
                                                    freq='W-FRI'),
                                columns=['012ABC-D'])
        pd.np.testing.assert_array_equal(self.result.weekly, expected)

    def test_daily(self):
        expected = MOCK_OUTPUT['abs_ret'].unstack(level=0)
        pd.np.testing.assert_array_equal(self.result.daily, expected)


class TestPortfolioStrategy(unittest.TestCase):

    STRATEGY = PortfolioStrategy(MOCK_OUTPUT)

    def test_get_starting_points(self):
        result = self.STRATEGY._get_starting_points()
        expected = pd.Series()
        pd.np.testing.assert_array_equal(result, expected)

    def test_shift_and_trim_starting_points(self):
        TEMP_MOCK = pd.Series(data=['A', 'B', 'C', 'D', 'E', 'F'],
                              index=pd.date_range('2003-01-02', '2003-06-30',
                                                  freq='M'))
        result = self.STRATEGY._shift_and_trim_starting_points(TEMP_MOCK)
        expected = pd.Series({'2003-03-31': 'A',
                              '2003-04-30': 'B',
                              '2003-05-31': 'C'})
        pd.np.testing.assert_array_equal(result, expected)

    def test_rebalancing_days(self):
        expected = ['2003-01-31', '2003-02-28', '2003-03-31']
        for i, d in enumerate(self.STRATEGY.rebalancing_days):
            self.assertEqual(d.strftime('%Y-%m-%d'), expected[i])

    def test_date_index(self):
        expected = pd.date_range('2003-01-02', '2003-03-31', freq='B')
        pd.np.testing.assert_array_equal(self.STRATEGY._date_index.values,
                                         expected.values)

