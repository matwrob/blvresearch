import pandas as pd
import numpy as np
import unittest

from blvresearch.concat.signals.price_based.rsi_agita import (
    get_signals
)

PATH = 'blvresearch/tests/mock_ubs_data/ubs_alpha.csv'

MOCK_DATA = {'alpha': pd.Series.from_csv(PATH)}


class TestGetSignals(unittest.TestCase):

    def test_get1(self):
        res = get_signals(MOCK_DATA, periods=14, buy_thrsh=30,
                          sell_thrsh=70, mean_type='simple')
        exp = pd.Series(
            {'2012-07-06': True,
             '2012-08-22': False,
             '2012-11-30': True,
             '2013-01-24': False,
             '2013-02-15': True,
             '2013-04-19': False,
             '2013-07-10': True,
             '2013-07-23': False,
             '2013-09-30': True,
             '2014-01-13': False,
             '2014-02-24': True}
        )
        np.testing.assert_array_equal(res.dropna(), exp)

    # def test_get2(self):
    #     res = get_signals(MOCK_DATA, long_window=100, short_window=50,
    #                       confirmation_window=20)
    #     exp = pd.Series(
    #        {'2012-07-23': False,
    #         '2012-10-15': True,
    #         '2013-03-27': False,
    #         '2013-07-02': True,
    #         '2013-12-02': False}
    #     )
    #     np.testing.assert_array_equal(res.dropna(), exp)
