import pandas as pd
import numpy as np
import unittest

from blvresearch.concat.signals.price_based.four_down_days import (
    get_4down_signals
)

PATH = 'blvresearch/tests/mock_ubs_data/ubs_alpha.csv'

MOCK_DATA = {'alpha': pd.Series.from_csv(PATH)}


class TestGetSignals(unittest.TestCase):

    def test_get1(self):
        res = get_4down_signals(MOCK_DATA, down_days=4, up_days=2)
        exp = pd.Series(
            {'2012-06-22': False,
             '2012-07-06': True,
             '2012-07-12': False,
             '2012-07-18': True,
             '2012-07-24': False,
             '2012-09-20': True,
             '2012-10-03': False,
             '2012-11-28': True,
             '2012-12-05': False,
             '2012-12-27': True,
             '2013-01-08': False,
             '2013-02-04': True,
             '2013-03-06': False,
             '2013-03-28': True,
             '2013-04-05': False,
             '2013-06-28': True,
             '2013-07-17': False,
             '2013-09-23': True,
             '2013-10-02': False,
             '2013-10-22': True,
             '2013-10-28': False,
             '2013-11-20': True,
             '2013-11-26': False,
             '2013-12-17': True,
             '2013-12-20': False,
             '2014-01-23': True,
             '2014-01-27': False,
             '2014-02-03': True,
             '2014-02-27': False,
             '2014-03-11': True,
             '2014-04-01': False,
             '2014-04-07': True,
             '2014-04-22': False,
             '2014-06-16': True,
             '2014-06-18': False
            }
        )
        np.testing.assert_array_equal(res.dropna(), exp)

    def test_get2(self):
        res = get_4down_signals(MOCK_DATA, down_days=6, up_days=3)
        exp = pd.Series(
           {'2012-07-10': True,
            '2012-07-25': False,
            '2012-11-30': True,
            '2013-01-09': False,
            '2013-04-03': True,
            '2013-04-11': False,
            '2013-10-24': True,
            '2013-11-12': False,
            '2014-03-28': True,
            '2014-04-30': False}
        )
        np.testing.assert_array_equal(res.dropna(), exp)
