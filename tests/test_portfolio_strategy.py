import pandas as pd
import unittest
import datetime

from blvresearch.core.strategy import PositiveMomentumStrategy, DynamicStrategy


def get_mock_returns():
    result = pd.read_csv('blvresearch/tests/mock_returns.csv')
    result.index = result['Date'].apply(
        lambda x: datetime.datetime.strptime(x, '%Y-%m-%d')
    )
    return result.drop('Date', axis=1)


MOCK_RETURNS = get_mock_returns()


class TestPositiveMomentumStrategy1(unittest.TestCase):

    SMS1 = PositiveMomentumStrategy(MOCK_RETURNS)

    def test_ranking_days(self):
        exp = pd.DatetimeIndex([pd.datetime(2003, 1, 12),
                                pd.datetime(2003, 1, 26),
                                pd.datetime(2003, 2, 9),
                                pd.datetime(2003, 2, 23),
                                pd.datetime(2003, 3, 9),
                                pd.datetime(2003, 3, 23)])
        pd.np.testing.assert_array_equal(self.SMS1.ranking_days, exp)

    def test_rebalancing_days(self):
        exp = pd.DatetimeIndex([pd.datetime(2003, 1, 19),
                                pd.datetime(2003, 2, 2),
                                pd.datetime(2003, 2, 16),
                                pd.datetime(2003, 3, 2),
                                pd.datetime(2003, 3, 16),
                                pd.datetime(2003, 3, 30)])
        pd.np.testing.assert_array_equal(self.SMS1.rebalancing_days, exp)

    def test_positions(self):
        exp_index = pd.DatetimeIndex(pd.date_range('2003-01-02',
                                                   '2003-03-31',
                                                   freq='B'))
        exp_data = ([pd.np.nan] * 12 + [['Stock1']] * 10 + [['Stock3']] * 10 +
                    [['Stock1']] * 10 + [['Stock2']] * 10 + [['Stock4']] * 10 +
                    [['Stock1']] * 1)
        exp = pd.Series(exp_data, exp_index)
        pd.np.testing.assert_array_equal(self.SMS1.positions.dropna(),
                                         exp.dropna())


class TestPositiveMomentumStrategy2(unittest.TestCase):

    class PositiveMomentumStrategy2(PositiveMomentumStrategy):
        RANKING_PERIODS = 1
        PAUSE_PERIODS = 1
        HOLDING_PERIODS = 1

    SMS2 = PositiveMomentumStrategy2(MOCK_RETURNS)

    def test_ranking_days(self):
        exp = pd.DatetimeIndex([pd.datetime(2003, 1, 5),
                                pd.datetime(2003, 1, 12),
                                pd.datetime(2003, 1, 19),
                                pd.datetime(2003, 1, 26),
                                pd.datetime(2003, 2, 2),
                                pd.datetime(2003, 2, 9),
                                pd.datetime(2003, 2, 16),
                                pd.datetime(2003, 2, 23),
                                pd.datetime(2003, 3, 2),
                                pd.datetime(2003, 3, 9),
                                pd.datetime(2003, 3, 16),
                                pd.datetime(2003, 3, 23)])
        pd.np.testing.assert_array_equal(self.SMS2.ranking_days, exp)

    def test_rebalancing_days(self):
        exp = pd.DatetimeIndex([pd.datetime(2003, 1, 12),
                                pd.datetime(2003, 1, 19),
                                pd.datetime(2003, 1, 26),
                                pd.datetime(2003, 2, 2),
                                pd.datetime(2003, 2, 9),
                                pd.datetime(2003, 2, 16),
                                pd.datetime(2003, 2, 23),
                                pd.datetime(2003, 3, 2),
                                pd.datetime(2003, 3, 9),
                                pd.datetime(2003, 3, 16),
                                pd.datetime(2003, 3, 23),
                                pd.datetime(2003, 3, 30)])
        pd.np.testing.assert_array_equal(self.SMS2.rebalancing_days, exp)

    def test_positions(self):
        exp_index = pd.DatetimeIndex(pd.date_range('2003-01-02',
                                                   '2003-03-31',
                                                   freq='B'))
        exp_data = ([pd.np.nan] * 7 + [['Stock1']] * 5 + [['Stock2']] * 5 +
                    [['Stock3']] * 5 + [['Stock4']] * 5 + [['Stock5']] * 5 +
                    [['Stock1']] * 5 + [['Stock2']] * 5 + [['Stock3']] * 5 +
                    [['Stock4']] * 5 + [['Stock5']] * 5 + [['Stock1']] * 5 +
                    [['Stock2']] * 1)
        exp = pd.Series(exp_data, exp_index)
        pd.np.testing.assert_array_equal(self.SMS2.positions.dropna(),
                                         exp.dropna())


class TestPositiveMomentumStrategy3(unittest.TestCase):

    class PositiveMomentumStrategy3(PositiveMomentumStrategy):
        RANKING_PERIODS = 0
        PAUSE_PERIODS = 0
        HOLDING_PERIODS = 4

        def _positions_per_rebalancing_day(self, returns):
            result = dict()
            for ix, day in enumerate(self.rebalancing_days):
                result[day] = list(returns.columns)[:ix + 1]
            return pd.Series(result)

    SMS3 = PositiveMomentumStrategy3(MOCK_RETURNS)

    def test_ranking_days(self):
        self.assertEqual(self.SMS3.ranking_days, [])

    def test_rebalancing_days(self):
        exp = pd.DatetimeIndex([pd.datetime(2002, 12, 29),
                                pd.datetime(2003, 1, 26),
                                pd.datetime(2003, 2, 23),
                                pd.datetime(2003, 3, 23)])
        pd.np.testing.assert_array_equal(self.SMS3.rebalancing_days, exp)

    def test_positions(self):
        exp_index = pd.DatetimeIndex(pd.date_range('2003-01-02',
                                                   '2003-03-31',
                                                   freq='B'))
        exp_data = ([['Stock1']] * 17 + [['Stock1', 'Stock2']] * 20 +
                    [['Stock1', 'Stock2', 'Stock3']] * 20 +
                    [['Stock1', 'Stock2', 'Stock3', 'Stock4']] * 6)
        exp = pd.Series(exp_data, exp_index)
        pd.np.testing.assert_array_equal(self.SMS3.positions.dropna(),
                                         exp.dropna())


class TestPositiveMomentumStrategy4(unittest.TestCase):

    class PositiveMomentumStrategy4(PositiveMomentumStrategy):
        RANKING_PERIODS = 1
        PAUSE_PERIODS = 1
        HOLDING_PERIODS = 1
        REBALANCING_FREQUENCY = 'M'

        def _positions_per_rebalancing_day(self, returns):
            result = dict()
            for ix, day in enumerate(self.rebalancing_days):
                result[day] = list(returns.columns)[:ix + 1]
            return pd.Series(result)

    SMS4 = PositiveMomentumStrategy4(MOCK_RETURNS)

    def test_ranking_days(self):
        exp = pd.DatetimeIndex([pd.datetime(2003, 1, 31)])
        pd.np.testing.assert_array_equal(self.SMS4.ranking_days, exp)

    def test_rebalancing_days(self):
        exp = pd.DatetimeIndex([pd.datetime(2003, 2, 28)])
        pd.np.testing.assert_array_equal(self.SMS4.rebalancing_days, exp)

    def test_positions(self):
        exp_index = pd.DatetimeIndex(pd.date_range('2003-01-02',
                                                   '2003-03-31',
                                                   freq='B'))
        exp_data = [pd.np.nan] * 42 + [['Stock1']] * 21
        exp = pd.Series(exp_data, exp_index)
        pd.np.testing.assert_array_equal(self.SMS4.positions.dropna(),
                                         exp.dropna())


class TestDynamicStrategy1(unittest.TestCase):

    ds = DynamicStrategy(MOCK_RETURNS)

    def test_ranking_days(self):
        exp = pd.date_range('2003-01-02', '2003-03-28', freq='B')
        pd.np.testing.assert_array_equal(self.ds.ranking_days, exp)

    def test_rebalancing_days(self):
        exp = pd.date_range('2003-01-02', '2003-03-28', freq='B')
        pd.np.testing.assert_array_equal(self.ds.ranking_days, exp)


class TestDynamicStrategy2(unittest.TestCase):

    class DynamicStrategy2(DynamicStrategy):
        RANKING_PERIODS = 1

    ds = DynamicStrategy3(MOCK_RETURNS)

    def test_ranking_days(self):
        exp = pd.date_range('2003-01-03', '2003-03-26', freq='B')
        pd.np.testing.assert_array_equal(self.ds.ranking_days, exp)

    def test_rebalancing_days(self):
        exp = pd.date_range('2003-01-07', '2003-03-28', freq='B')
        pd.np.testing.assert_array_equal(self.ds.ranking_days, exp)



class TestDynamicStrategy2(unittest.TestCase):

    class DynamicStrategy2(DynamicStrategy):
        RANKING_PERIODS = 2

    ds = DynamicStrategy2(MOCK_RETURNS)

    def test_ranking_days(self):
        exp = pd.date_range('2003-01-03', '2003-03-28', freq='B')
        pd.np.testing.assert_array_equal(self.ds.ranking_days, exp)

    def test_rebalancing_days(self):
        exp = pd.date_range('2003-01-03', '2003-03-28', freq='B')
        pd.np.testing.assert_array_equal(self.ds.ranking_days, exp)


class TestDynamicStrategy3(unittest.TestCase):

    class DynamicStrategy3(DynamicStrategy):
        RANKING_PERIODS = 2
        PAUSE_PERIODS = 2

    ds = DynamicStrategy3(MOCK_RETURNS)

    def test_ranking_days(self):
        exp = pd.date_range('2003-01-03', '2003-03-26', freq='B')
        pd.np.testing.assert_array_equal(self.ds.ranking_days, exp)

    def test_rebalancing_days(self):
        exp = pd.date_range('2003-01-07', '2003-03-28', freq='B')
        pd.np.testing.assert_array_equal(self.ds.ranking_days, exp)


class TestDynamicStrategy4(unittest.TestCase):

    class DynamicStrategy4(DynamicStrategy):
        RANKING_PERIODS = 5
        PAUSE_PERIODS = 5

    ds = DynamicStrategy4(MOCK_RETURNS)

    def test_ranking_days(self):
        exp = pd.date_range('2003-01-08', '2003-03-21', freq='B')
        pd.np.testing.assert_array_equal(self.ds.ranking_days, exp)

    def test_rebalancing_days(self):
        exp = pd.date_range('2003-01-15', '2003-03-28', freq='B')
        pd.np.testing.assert_array_equal(self.ds.ranking_days, exp)


class TestDynamicStrategy5(unittest.TestCase):

    class DynamicStrategy5(DynamicStrategy):
        REBALANCING_FREQUENCY = 'W'

    ds = DynamicStrategy5(MOCK_RETURNS)

    def test_ranking_days(self):
        self.assertTrue(False)

    def test_rebalancing_days(self):
        self.assertTrue(False)
