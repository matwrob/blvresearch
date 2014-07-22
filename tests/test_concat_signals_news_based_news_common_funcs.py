import pandas as pd
import numpy as np
import unittest
import pickle

from blvresearch.concat.signals.news_based.news_common_funcs import (
    _get_rows, _has_relevant_news, get_days_to_check
)

PATH = 'blvresearch/tests/mock_signals/mock_pickle.p'
with open(PATH, 'rb') as _input:
    MOCK_DATA = pickle.load(_input)


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


class TestGetDaysToCheck(unittest.TestCase):

    def test_get(self):
        first_loc = 0
        last_loc = -1
        res = get_days_to_check(MOCK_DATA, first_loc, last_loc)
        self.assertEqual(len(res), 169)
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