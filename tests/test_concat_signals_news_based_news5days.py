import unittest
import pickle

from blvresearch.concat.signals.news_based.news5days import (
    get_news5days_signals
)
from blvresearch.concat.signals.news_based.news_common_funcs import (
    get_days_to_check
)


PATH = '/vagrant/blvresearch/tests/mock_signals/mock_pickle.p'
with open(PATH, 'rb') as _input:
    MOCK_DATA = pickle.load(_input)


DAYS_TO_CHECK, FIRST_LOC, LAST_LOC = get_days_to_check(MOCK_DATA)


class TestGetNews5daysSignals(unittest.TestCase):

    def test_get(self):
        res = get_news5days_signals(DAYS_TO_CHECK, MOCK_DATA, FIRST_LOC,
                                    LAST_LOC)

        self.assertEqual(len(res), 2)

        self.assertTrue(res['2013-07-26'][0])

        self.assertFalse(res['2013-11-04'][0])
