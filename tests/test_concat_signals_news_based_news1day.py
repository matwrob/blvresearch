import unittest
import pickle

from blvresearch.concat.signals.news_based.news1day import (
    get_news1day_signals
)
from blvresearch.concat.signals.news_based.news_common_funcs import (
    get_days_to_check
)


PATH = '/vagrant/blvresearch/tests/mock_signals/mock_pickle.p'
with open(PATH, 'rb') as _input:
    MOCK_DATA = pickle.load(_input)


DAYS_TO_CHECK, FIRST_LOC, LAST_LOC = get_days_to_check(MOCK_DATA)


class TestGetNews1daySignals(unittest.TestCase):

    def test_get(self):
        res = get_news1day_signals(DAYS_TO_CHECK, MOCK_DATA, FIRST_LOC,
                                   LAST_LOC)

        self.assertEqual(len(res), 8)

        self.assertTrue(res['2013-04-30'][0])
        self.assertTrue(res['2013-07-22'][0])
        self.assertTrue(res['2014-01-08'][0])
        self.assertTrue(res['2014-02-04'][0])

        self.assertFalse(res['2013-09-06'][0])
        self.assertFalse(res['2013-10-29'][0])
        self.assertFalse(res['2013-11-04'][0])
        self.assertFalse(res['2014-05-15'][0])
