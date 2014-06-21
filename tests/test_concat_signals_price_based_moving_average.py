import pandas as pd
import numpy as np
import unittest

from blvresearch.concat.signals.price_based.moving_average import (
    get_signals
)

PATH = 'blvresearch/tests/mock_ubs_data/ubs_alpha.csv'

MOCK_DATA = {'alpha': pd.Series.from_csv(PATH)}


class TestGetSignals(unittest.TestCase):

    def test_get1(self):
        res = get_signals(MOCK_DATA, window=10, confirmation_window=3)
        exp = pd.Series(
            {'2012-06-27': False,
             '2012-08-23': True,
             '2012-09-28': False,
             '2012-10-16': True,
             '2012-11-28': False,
             '2013-01-11': True,
             '2013-02-01': False,
             '2013-04-11': True,
             '2013-06-28': False,
             '2013-07-18': True,
             '2013-09-20': False,
             '2013-10-11': True,
             '2013-10-22': False,
             '2013-11-27': True,
             '2013-12-17': False,
             '2014-01-08': True,
             '2014-01-31': False,
             '2014-05-02': True,
             '2014-05-13': False}
        )
        np.testing.assert_array_equal(res.dropna(), exp)

    def test_get2(self):
        res = get_signals(MOCK_DATA, window=50, confirmation_window=5)
        exp = pd.Series(
           {'2012-06-29': False,
            '2012-09-11': True,
            '2013-01-04': False,
            '2013-01-15': True,
            '2013-02-07': False,
            '2013-05-07': True,
            '2013-07-04': False,
            '2013-07-24': True,
            '2013-10-29': False,
            '2014-01-14': True,
            '2014-03-07': False}
        )
        np.testing.assert_array_equal(res.dropna(), exp)
