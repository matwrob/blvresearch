import pandas as pd
import numpy as np
import unittest

from blvresearch.concat.signals.price_based.dmac import (
    get_dmac_signals
)

PATH = 'blvresearch/tests/mock_ubs_data/ubs_alpha.csv'

MOCK_DATA = {'abs_ret': pd.Series.from_csv(PATH)}


class TestGetSignals(unittest.TestCase):

    def test_get1(self):
        res = get_dmac_signals(MOCK_DATA, long_window=30, short_window=10,
                               confirmation_window=5)
        exp = pd.Series(
            {'2012-07-02': False,
             '2012-09-11': True,
             '2013-01-07': False,
             '2013-01-22': True,
             '2013-02-07': False,
             '2013-04-25': True,
             '2013-07-08': False,
             '2013-07-26': True,
             '2013-10-02': False,
             '2013-10-21': True,
             '2013-10-29': False,
             '2014-01-14': True,
             '2014-03-03': False}
        )
        np.testing.assert_array_equal(res.dropna(), exp)

    def test_get2(self):
        res = get_dmac_signals(MOCK_DATA, long_window=100, short_window=50,
                               confirmation_window=20)
        exp = pd.Series(
           {'2012-07-23': False,
            '2012-10-15': True,
            '2013-03-27': False,
            '2013-07-02': True,
            '2013-12-02': False}
        )
        np.testing.assert_array_equal(res.dropna(), exp)
