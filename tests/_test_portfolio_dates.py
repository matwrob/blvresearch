import pandas as pd
import unittest

from blvresearch.core.portfolio import PortfolioDates


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

        exp_rank = pd.DatetimeIndex([pd.datetime(2013, 1, 8),
                                     pd.datetime(2013, 1, 9),
                                     pd.datetime(2013, 1, 10),
                                     pd.datetime(2013, 1, 11),
                                     pd.datetime(2013, 1, 14)])
        pd.np.testing.assert_array_equal(result.ranking_days,
                                         exp_rank)

        exp_rebal = pd.DatetimeIndex([pd.datetime(2013, 1, 9),
                                      pd.datetime(2013, 1, 10),
                                      pd.datetime(2013, 1, 11),
                                      pd.datetime(2013, 1, 14),
                                      pd.datetime(2013, 1, 15)])
        pd.np.testing.assert_array_equal(result.rebalancing_days,
                                         exp_rebal)

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
                                      pd.datetime(2013, 1, 2),
                                      pd.datetime(2013, 1, 3),
                                      pd.datetime(2013, 1, 4),
                                      pd.datetime(2013, 1, 7),
                                      pd.datetime(2013, 1, 8)])
        pd.np.testing.assert_array_equal(result.rebalancing_days,
                                         exp_rebal)
