import pandas as pd
import numpy as np
import unittest

from blvresearch.concat.signals.price_based.moving_average import (
    get_movavg_signals
)
from blvresearch.concat.signals.signal_testing import (
    get_total_return_on_signals, split_signals_into_good_and_bad
)

PATH = 'blvresearch/tests/mock_ubs_data/ubs_alpha.csv'

MOCK_DATA = {'abs_ret': pd.Series.from_csv(PATH)}


class TestGetSignals(unittest.TestCase):

    def test_get1(self):
        res = get_movavg_signals(MOCK_DATA, window=10, confirmation_window=3)
        exp = pd.Series(
            {'2012-06-27': False,
             '2012-08-23': True,
             '2012-09-28': False,
             '2012-10-16': True,
             '2012-11-27': False,
             '2012-12-14': True,
             '2012-12-21': False,
             '2013-01-11': True,
             '2013-02-01': False,
             '2013-04-11': True,
             '2013-05-30': False,
             '2013-06-04': True,
             '2013-06-13': False,
             '2013-06-24': True,
             '2013-06-28': False,
             '2013-07-18': True,
             '2013-09-20': False,
             '2013-10-11': True,
             '2013-10-22': False,
             '2013-11-27': True,
             '2013-12-17': False,
             '2014-01-08': True,
             '2014-01-24': False,
             '2014-02-06': True,
             '2014-02-11': False,
             '2014-05-02': True,
             '2014-05-13': False}
        )
        np.testing.assert_array_equal(res.dropna(), exp)

    def test_get2(self):
        res = get_movavg_signals(MOCK_DATA, window=50, confirmation_window=5)
        exp = pd.Series(
           {'2012-07-02': False,
            '2012-09-12': True,
            '2013-01-10': False,
            '2013-01-18': True,
            '2013-02-11': False,
            '2013-05-07': True,
            '2013-07-10': False,
            '2013-07-26': True,
            '2013-10-07': False,
            '2013-10-17': True,
            '2013-10-29': False,
            '2014-01-17': True,
            '2014-03-03': False}
        )
        np.testing.assert_array_equal(res.dropna(), exp)

    def test_get3(self):
        res = get_movavg_signals(MOCK_DATA, window=50, confirmation_window=2)
        exp = pd.Series(
           {'2012-06-20': False,
            '2012-06-22': True,
            '2012-06-26': False,
            '2012-08-23': True,
            '2012-08-31': False,
            '2012-09-06': True,
            '2012-12-27': False,
            '2013-01-10': True,
            '2013-02-04': False,
            '2013-04-23': True,
            '2013-04-29': False,
            '2013-05-02': True,
            '2013-07-01': False,
            '2013-07-19': True,
            '2013-09-24': False,
            '2013-10-11': True,
            '2013-10-23': False,
            '2014-01-09': True,
            '2014-02-24': False,
            '2014-02-28': True,
            '2014-03-04': False}
        )
        np.testing.assert_array_equal(res.dropna(), exp)
