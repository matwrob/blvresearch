import unittest
import pandas as pd

from blvresearch.core.periodic_backtest import StockReturns


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
