import unittest
import pickle

from blvresearch.concat.signals.news_based.news_signals_strategy1 import (
    get_news1day_signals
)
from blvresearch.concat.signals.news_based.news_common_funcs import (
    get_days_to_check
)


PATH = '/vagrant/blvresearch/tests/mock_signals/mock_pickle.p'
with open(PATH, 'rb') as _input:
    MOCK_DATA = pickle.load(_input)


DAYS_TO_CHECK = get_days_to_check(MOCK_DATA)


class TestGetNews1daySignals(unittest.TestCase):

    def test_get(self):
        res = get_news1day_signals(DAYS_TO_CHECK)
        self.assertTrue(False)
