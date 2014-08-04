import pandas as pd
import numpy as np
import unittest
import pickle

from blvresearch.concat.signals.news_based.news_common_funcs import (
    get_days_to_check, _has_relevant_news, _has_abnormal_alpha
)

PATH = 'blvresearch/tests/mock_signals/mock_pickle.p'
with open(PATH, 'rb') as _input:
    MOCK_DATA = pickle.load(_input)


class TestGetDaysToCheck(unittest.TestCase):

    def test_get(self):
        res, first_loc, last_loc = get_days_to_check(MOCK_DATA)
        self.assertEqual(len(res), 8)
        self.assertEqual(first_loc, 124)
        self.assertEqual(last_loc, 494)
        self.assertEqual(res.index[0].strftime('%Y-%m-%d'), '2013-04-30')
        self.assertEqual(res.index[1].strftime('%Y-%m-%d'), '2013-07-22')
        self.assertEqual(res.index[2].strftime('%Y-%m-%d'), '2013-09-06')
        self.assertEqual(res.index[3].strftime('%Y-%m-%d'), '2013-10-29')
        self.assertEqual(res.index[4].strftime('%Y-%m-%d'), '2013-11-04')
        self.assertEqual(res.index[5].strftime('%Y-%m-%d'), '2014-01-08')
        self.assertEqual(res.index[6].strftime('%Y-%m-%d'), '2014-02-04')
        self.assertEqual(res.index[7].strftime('%Y-%m-%d'), '2014-05-15')


class TestHasRelevantNews(unittest.TestCase):

    def test_relevant_news(self):
        news1 = MOCK_DATA['news']['2012-08-15'][0]
        self.assertFalse(_has_relevant_news(news1))

        news2 = MOCK_DATA['news']['2012-08-17'][0]
        self.assertTrue(_has_relevant_news(news2))


class TestHasAbnormalAlpha(unittest.TestCase):

    def test_abnormal_alpha(self):
        alpha1 = MOCK_DATA['alpha']['2013-04-30'][0]
        self.assertTrue(_has_abnormal_alpha(alpha1,
                                            mean=0.000172, std=0.013728))

        alpha2 = MOCK_DATA['alpha']['2013-04-29'][0]
        self.assertFalse(_has_abnormal_alpha(alpha2,
                                             mean=-0.000237, std=0.01293))
