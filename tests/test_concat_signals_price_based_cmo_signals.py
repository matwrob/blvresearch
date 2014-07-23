import pandas as pd
import numpy as np
import unittest

from blvresearch.concat.signals.price_based.cmo_signals import (
    _calculate_cmo_values, get_cmo_signals
)

PATH = 'blvresearch/tests/mock_ubs_data/ubs_alpha.csv'

MOCK_DATA = {'alpha': pd.Series.from_csv(PATH)}


class TestGetSignals(unittest.TestCase):

    def test_get1(self):
        res = get_cmo_signals(MOCK_DATA, periods=9)
        exp = pd.Series(
            {'2012-07-12': True,
             '2012-08-06': False,
             '2012-12-11': True,
             '2013-04-18': False,
             '2013-07-01': True,
             '2013-08-06': False,
             '2013-10-01': True,
             '2013-10-14': False,
             '2013-10-25': True,
             '2013-11-18': False,
             '2013-12-20': True,
             '2014-01-20': False,
             '2014-02-12': True}
        )
        np.testing.assert_array_equal(res.dropna(), exp)


class TestCalculateCMOvalues(unittest.TestCase):

    def test_calculate1(self):
        res = _calculate_cmo_values(MOCK_DATA['alpha'][:'2012-12-31'],
                                    periods=9)
        exp = pd.Series(
            {'2012-06-29 15:30:00': -0.3333333333,
             '2012-07-02 15:30:00': -0.1111111111,
             '2012-07-03 15:30:00': -0.1111111111,
             '2012-07-04 15:30:00': -0.3333333333,
             '2012-07-05 15:30:00': -0.5555555556,
             '2012-07-06 15:30:00': -0.5555555556,
             '2012-07-09 15:30:00': -0.5555555556,
             '2012-07-10 15:30:00': -0.7777777778,
             '2012-07-11 15:30:00': -0.5555555556,
             '2012-07-12 15:30:00': -0.3333333333,
             '2012-07-13 15:30:00': -0.5555555556,
             '2012-07-16 15:30:00': -0.5555555556,
             '2012-07-17 15:30:00': -0.5555555556,
             '2012-07-18 15:30:00': -0.5555555556,
             '2012-07-19 15:30:00': -0.5555555556,
             '2012-07-20 15:30:00': -0.5555555556,
             '2012-07-23 15:30:00': -0.3333333333,
             '2012-07-24 15:30:00': -0.3333333333,
             '2012-07-25 15:30:00': -0.3333333333,
             '2012-07-26 15:30:00': -0.1111111111,
             '2012-07-27 15:30:00': 0.1111111111,
             '2012-07-30 15:30:00': 0.3333333333,
             '2012-07-31 15:30:00': 0.3333333333,
             '2012-08-02 15:30:00': 0.3333333333,
             '2012-08-03 15:30:00': 0.5555555556,
             '2012-08-06 15:30:00': 0.3333333333,
             '2012-08-07 15:30:00': 0.3333333333,
             '2012-08-08 15:30:00': 0.1111111111,
             '2012-08-09 15:30:00': -0.1111111111,
             '2012-08-10 15:30:00': -0.3333333333,
             '2012-08-13 15:30:00': -0.3333333333,
             '2012-08-14 15:30:00': -0.3333333333,
             '2012-08-15 15:30:00': -0.3333333333,
             '2012-08-16 15:30:00': -0.3333333333,
             '2012-08-17 15:30:00': -0.1111111111,
             '2012-08-20 15:30:00': -0.3333333333,
             '2012-08-21 15:30:00': -0.1111111111,
             '2012-08-22 15:30:00': 0.1111111111,
             '2012-08-23 15:30:00': 0.1111111111,
             '2012-08-24 15:30:00': -0.1111111111,
             '2012-08-27 15:30:00': 0.1111111111,
             '2012-08-28 15:30:00': 0.1111111111,
             '2012-08-29 15:30:00': 0.1111111111,
             '2012-08-30 15:30:00': -0.1111111111,
             '2012-08-31 15:30:00': 0.1111111111,
             '2012-09-03 15:30:00': -0.1111111111,
             '2012-09-04 15:30:00': -0.3333333333,
             '2012-09-05 15:30:00': -0.1111111111,
             '2012-09-06 15:30:00': 0.1111111111,
             '2012-09-07 15:30:00': 0.1111111111,
             '2012-09-10 15:30:00': 0.3333333333,
             '2012-09-11 15:30:00': 0.3333333333,
             '2012-09-12 15:30:00': 0.5555555556,
             '2012-09-13 15:30:00': 0.3333333333,
             '2012-09-14 15:30:00': 0.5555555556,
             '2012-09-17 15:30:00': 0.5555555556,
             '2012-09-18 15:30:00': 0.3333333333,
             '2012-09-19 15:30:00': 0.1111111111,
             '2012-09-20 15:30:00': -0.1111111111,
             '2012-09-21 15:30:00': -0.1111111111,
             '2012-09-24 15:30:00': -0.3333333333,
             '2012-09-25 15:30:00': -0.3333333333,
             '2012-09-26 15:30:00': -0.3333333333,
             '2012-09-27 15:30:00': -0.3333333333,
             '2012-09-28 15:30:00': -0.3333333333,
             '2012-10-01 15:30:00': -0.3333333333,
             '2012-10-02 15:30:00': -0.1111111111,
             '2012-10-03 15:30:00': 0.1111111111,
             '2012-10-04 15:30:00': 0.1111111111,
             '2012-10-05 15:30:00': 0.1111111111,
             '2012-10-08 15:30:00': -0.1111111111,
             '2012-10-09 15:30:00': -0.1111111111,
             '2012-10-10 15:30:00': -0.1111111111,
             '2012-10-11 15:30:00': -0.1111111111,
             '2012-10-12 15:30:00': 0.1111111111,
             '2012-10-15 15:30:00': 0.1111111111,
             '2012-10-16 15:30:00': 0.1111111111,
             '2012-10-17 15:30:00': 0.1111111111,
             '2012-10-18 15:30:00': 0.3333333333,
             '2012-10-19 15:30:00': 0.3333333333,
             '2012-10-22 15:30:00': 0.5555555556,
             '2012-10-23 15:30:00': 0.5555555556,
             '2012-10-24 15:30:00': 0.7777777778,
             '2012-10-25 15:30:00': 0.7777777778,
             '2012-10-26 15:30:00': 0.5555555556,
             '2012-10-29 16:30:00': 0.5555555556,
             '2012-10-30 16:30:00': 0.5555555556,
             '2012-10-31 16:30:00': 0.5555555556,
             '2012-11-01 16:30:00': 0.7777777778,
             '2012-11-02 16:30:00': 0.5555555556,
             '2012-11-05 16:30:00': 0.5555555556,
             '2012-11-06 16:30:00': 0.5555555556,
             '2012-11-07 16:30:00': 0.5555555556,
             '2012-11-08 16:30:00': 0.7777777778,
             '2012-11-09 16:30:00': 0.5555555556,
             '2012-11-12 16:30:00': 0.5555555556,
             '2012-11-13 16:30:00': 0.3333333333,
             '2012-11-14 16:30:00': 0.1111111111,
             '2012-11-15 16:30:00': 0.3333333333,
             '2012-11-16 16:30:00': 0.1111111111,
             '2012-11-19 16:30:00': 0.1111111111,
             '2012-11-20 16:30:00': -0.1111111111,
             '2012-11-21 16:30:00': -0.1111111111,
             '2012-11-22 16:30:00': 0.1111111111,
             '2012-11-23 16:30:00': -0.1111111111,
             '2012-11-26 16:30:00': -0.1111111111,
             '2012-11-27 16:30:00': -0.1111111111,
             '2012-11-28 16:30:00': -0.3333333333,
             '2012-11-29 16:30:00': -0.3333333333,
             '2012-11-30 16:30:00': -0.5555555556,
             '2012-12-03 16:30:00': -0.5555555556,
             '2012-12-04 16:30:00': -0.5555555556,
             '2012-12-05 16:30:00': -0.5555555556,
             '2012-12-06 16:30:00': -0.5555555556,
             '2012-12-07 16:30:00': -0.5555555556,
             '2012-12-10 16:30:00': -0.5555555556,
             '2012-12-11 16:30:00': -0.3333333333,
             '2012-12-12 16:30:00': -0.1111111111,
             '2012-12-13 16:30:00': -0.1111111111,
             '2012-12-14 16:30:00': -0.1111111111,
             '2012-12-17 16:30:00': -0.3333333333,
             '2012-12-18 16:30:00': -0.3333333333,
             '2012-12-19 16:30:00': -0.3333333333,
             '2012-12-20 16:30:00': -0.3333333333,
             '2012-12-21 16:30:00': -0.3333333333,
             '2012-12-27 16:30:00': -0.5555555556,
             '2012-12-28 16:30:00': -0.5555555556}
        )
        np.testing.assert_array_almost_equal(res.dropna(), exp, decimal=6)
