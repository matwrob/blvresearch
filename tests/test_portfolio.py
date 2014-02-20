import pandas as pd
import unittest
import datetime

from blvresearch.core.portfolio import (
    Portfolio, SimpleMomentumStrategy
)


def get_mock_returns():
    result = pd.read_csv('blvresearch/tests/mock_returns.csv')
    result.index = result['Date'].apply(
        lambda x: datetime.datetime.strptime(x, '%Y-%m-%d')
    )
    return result.drop('Date', axis=1)


MOCK_RETURNS = get_mock_returns()


class TestPortfolio(unittest.TestCase):

    SMS = SimpleMomentumStrategy(MOCK_RETURNS)
    PORTFOLIO = Portfolio(SMS)

    def test_daily_performance(self):
        exp = pd.Series(data=[0] * 32 + [pd.np.log(0.5)] + [0] * 30,
                        index=pd.date_range('2003-01-02', '2003-03-31',
                                            freq='B'))
        pd.np.testing.assert_array_equal(self.PORTFOLIO.daily_performance(),
                                         exp)

    def test_members(self):
        exp_index = pd.DatetimeIndex(pd.date_range('2003-01-02', '2003-03-31',
                                                   freq='B'))
        exp_data = ([pd.np.nan] * 12 + [['Stock1']] * 10 + [['Stock3']] * 10 +
                    [['Stock1']] * 10 + [['Stock2']] * 10 + [['Stock4']] * 10 +
                    [['Stock1']])
        exp = pd.Series(exp_data, exp_index)
        pd.np.testing.assert_array_equal(self.PORTFOLIO.members.dropna(),
                                         exp.dropna())

    def test_static_members(self):
        expected = set(['Stock1', 'Stock2', 'Stock3', 'Stock4'])
        self.assertEqual(set(self.PORTFOLIO._static_members), expected)

    def test_ranking_periods(self):
        self.assertEqual(self.PORTFOLIO.holding_periods, 2)

    def test_pause_periods(self):
        self.assertEqual(self.PORTFOLIO.pause_periods, 1)

    def test_holding_periods(self):
        self.assertEqual(self.PORTFOLIO.holding_periods, 2)

    def test_size(self):
        self.assertEqual(self.PORTFOLIO.size, 1)

    def test_rebalancing_frequency(self):
        self.assertEqual(self.PORTFOLIO.rebalancing_frequency, 'W')
