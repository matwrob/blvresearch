import unittest
import pandas as pd

from blvresearch.core.portfolio import StockReturns


INDEX = pd.DatetimeIndex(pd.date_range('2003-01-02', '2003-03-31', freq='B'))
DATA = ([[1, 2, 3]] * 21 + [[2, 3, 4]] * 21 + [[3, 4, 5]] * 21)
COLUMNS = ['Stock1', 'Stock2', 'Stock3']
MOCK_RETURNS = pd.DataFrame(data=DATA, index=INDEX, columns=COLUMNS)


class TestReturns(unittest.TestCase):

    result = StockReturns(MOCK_RETURNS)

    def test_monthly(self):
        exp = pd.DataFrame(data=[[23, 45, 67], [40, 60, 80], [63, 84, 105]],
                           index=pd.date_range('2003-01-02', '2003-03-31',
                                               freq='BM'),
                           columns=['012ABC-D', '123BCD-E', '234CDE-F'])
        pd.np.testing.assert_array_equal(self.result.monthly, exp)

    def test_weekly(self):
        exp = pd.DataFrame(data=[[2, 4, 6], [5, 10, 15], [5, 10, 15],
                                 [5, 10, 15], [6, 11, 16], [10, 15, 20],
                                 [10, 15, 20], [10, 15, 20], [10, 15, 20],
                                 [15, 20, 25], [15, 20, 25], [15, 20, 25],
                                 [15, 20, 25], [3, 4, 5]],
                           index=pd.date_range('2003-01-02', '2003-04-06',
                                               freq='W'),
                           columns=['012ABC-D', '123BCD-E', '234CDE-F'])
        pd.np.testing.assert_array_equal(self.result.weekly, exp)

    def test_daily(self):
        pd.np.testing.assert_array_equal(self.result.daily, MOCK_RETURNS)
