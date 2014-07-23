import pandas as pd
import numpy as np
import unittest
import pickle

from blvresearch.concat.signals.news_based.news_common_funcs import (
    get_days_to_check, _get_rows, _has_relevant_news, _has_abnormal_alpha,
    _value_is_abnormal
)

PATH = 'blvresearch/tests/mock_signals/mock_pickle.p'
with open(PATH, 'rb') as _input:
    MOCK_DATA = pickle.load(_input)


class TestGetDaysToCheck(unittest.TestCase):

    def test_get(self):
        res, first_loc, last_loc = get_days_to_check(MOCK_DATA)
        self.assertEqual(len(res), 170)
        self.assertEqual(first_loc, 124)
        self.assertEqual(last_loc, 494)
        self.assertEqual(res.index[0].strftime('%Y-%m-%d'), '2013-01-16')
        self.assertEqual(res.index[1].strftime('%Y-%m-%d'), '2013-01-17')
        self.assertEqual(res.index[2].strftime('%Y-%m-%d'), '2013-01-18')
        self.assertEqual(res.index[3].strftime('%Y-%m-%d'), '2013-01-23')
        self.assertEqual(res.index[4].strftime('%Y-%m-%d'), '2013-01-24')
        self.assertEqual(res.index[5].strftime('%Y-%m-%d'), '2013-01-25')
        self.assertEqual(res.index[6].strftime('%Y-%m-%d'), '2013-01-28')
        self.assertEqual(res.index[7].strftime('%Y-%m-%d'), '2013-01-29')
        self.assertEqual(res.index[8].strftime('%Y-%m-%d'), '2013-01-30')
        self.assertEqual(res.index[9].strftime('%Y-%m-%d'), '2013-01-31')
        self.assertEqual(res.index[10].strftime('%Y-%m-%d'), '2013-02-04')
        self.assertEqual(res.index[11].strftime('%Y-%m-%d'), '2013-02-05')
        self.assertEqual(res.index[12].strftime('%Y-%m-%d'), '2013-02-06')
        self.assertEqual(res.index[13].strftime('%Y-%m-%d'), '2013-02-11')
        self.assertEqual(res.index[14].strftime('%Y-%m-%d'), '2013-02-12')


class TestGetRows(unittest.TestCase):

    def test_get1(self):
        date = MOCK_DATA.index[1]
        self.assertEqual(date.strftime('%Y-%m-%d'), '2012-07-17')

        row0, row1, row2 = _get_rows(date, MOCK_DATA)
        self.assertEqual(row0.name.strftime('%Y-%m-%d'),
                         '2012-07-16')
        self.assertEqual(row1.name.strftime('%Y-%m-%d'),
                         '2012-07-17')
        self.assertEqual(row2.name.strftime('%Y-%m-%d'),
                         '2012-07-18')

    def test_get2(self):
        date = MOCK_DATA.index[2]
        self.assertEqual(date.strftime('%Y-%m-%d'), '2012-07-18')

        row0, row1, row2 = _get_rows(date, MOCK_DATA)
        self.assertIsInstance(row0, pd.core.series.Series)
        self.assertEqual(row0.name.strftime('%Y-%m-%d'),
                         '2012-07-17')
        self.assertEqual(row1.name.strftime('%Y-%m-%d'),
                         '2012-07-18')
        self.assertEqual(row2.name.strftime('%Y-%m-%d'),
                         '2012-07-19')


class TestHasRelevantNews(unittest.TestCase):

    def test_relevant_news(self):
        date = MOCK_DATA.index[1]
        self.assertEqual(date.strftime('%Y-%m-%d'), '2012-07-17')
        row0, row1, row2 = _get_rows(date, MOCK_DATA)

        self.assertTrue(_has_relevant_news(row0['news']))
        self.assertFalse(_has_relevant_news(row1['news']))
        self.assertTrue(_has_relevant_news(row2['news']))



class TestHasAbnormalAlpha(unittest.TestCase):

    def test_case_has_abnormal_alpha(self):
        date = MOCK_DATA.index[105]
        self.assertEqual(date.strftime('%Y-%m-%d'), '2012-12-11')
        row0, row1, row2 = _get_rows(date, MOCK_DATA)
        self.assertTrue(_has_abnormal_alpha(row0, row1, row2,
                                            0.000465, 0.014029))

    def test_case_does_not_have_abnormal_alpha(self):
        date = MOCK_DATA.index[0]
        self.assertEqual(date.strftime('%Y-%m-%d'), '2012-07-16')
        row0, row1, row2 = _get_rows(date, MOCK_DATA)
        self.assertFalse(_has_abnormal_alpha(row0, row1, row2,
                                             0.000465, 0.014029))


class TestValueIsAbnormal(unittest.TestCase):

    def test_case_is_not_abnormal(self):
        res = _value_is_abnormal(alpha=10, mean=5, std=5)
        self.assertFalse(res)

        res = _value_is_abnormal(alpha=0, mean=5, std=5)
        self.assertFalse(res)

    def test_case_is_abnormal(self):
        res = _value_is_abnormal(alpha=10, mean=5, std=4.99)
        self.assertTrue(res)

        res = _value_is_abnormal(alpha=0, mean=5, std=4.99)
        self.assertTrue(res)
