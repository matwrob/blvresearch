import unittest
import pickle

from blvresearch.concat.signals.news_based.news3days import (
    get_news3days_signals
)
from blvresearch.concat.signals.news_based.news_common_funcs import (
    get_days_to_check
)


PATH = '/vagrant/blvresearch/tests/mock_signals/mock_pickle.p'
with open(PATH, 'rb') as _input:
    MOCK_DATA = pickle.load(_input)


DAYS_TO_CHECK, FIRST_LOC, LAST_LOC = get_days_to_check(MOCK_DATA)


class TestGetNews3daysSignals(unittest.TestCase):

    def test_get(self):
        res = get_news3days_signals(DAYS_TO_CHECK, MOCK_DATA, FIRST_LOC,
                                    LAST_LOC)

        self.assertEqual(len(res), 8)

        self.assertTrue(res['2013-05-03'][0])
        self.assertTrue(res['2013-07-24'][0])
        self.assertTrue(res['2014-01-10'][0])
        self.assertTrue(res['2014-02-06'][0])

        self.assertFalse(res['2013-09-10'][0])
        self.assertFalse(res['2013-10-31'][0])
        self.assertFalse(res['2013-11-06'][0])
        self.assertFalse(res['2014-05-19'][0])
