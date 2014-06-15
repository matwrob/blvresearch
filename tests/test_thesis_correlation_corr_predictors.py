import pandas as pd
import unittest

from unittest.mock import patch

from blvresearch.thesis.correlation.corr_predictors import (
    get_coocc_with_other_entities, get_relative_coocc_with_other_entities,
    _get_news_count
)
from memnews.core import NewsList


class NewsList(NewsList):
    'mocks concat NewsList'
    def __init__(self, list_of_news):
        self.l = list_of_news

    def __iter__(self):
        for v in self.l:
            yield v

    def __len__(self):
        return len(self.l)


INDEX = pd.DatetimeIndex(start='2013-06-01',
                         end='2013-12-31',
                         freq='B')
NEWS1 = {'entities': ['entity1', 'entity2']}
NEWS2 = {'entities': ['entity1', 'entity3']}

MOCK_ENTITY_1 = pd.DataFrame(
    pd.Series(data=[NewsList([NEWS1, NEWS2])] * len(INDEX),
              index=INDEX,
              name='news')
)
MOCK_ENTITY_2 = pd.DataFrame(
    pd.Series(data=[NewsList([NEWS1])] * len(INDEX),
              index=INDEX,
              name='news')
)
MOCK_ENTITY_3 = pd.DataFrame(
    pd.Series(data=[NewsList([NEWS2])] * len(INDEX),
              index=INDEX,
              name='news')
)
MOCK_DATA = {
    'entity1': MOCK_ENTITY_1,
    'entity2': MOCK_ENTITY_2,
    'entity3': MOCK_ENTITY_3
}


class TestIfMockNewsListCorrect(unittest.TestCase):

	def test_len(self):
		self.assertEqual(len(NewsList([NEWS1])), 1)
		self.assertEqual(len(NewsList([NEWS1, NEWS2])), 2)


class TestGetCoOccWithOtherEntities(unittest.TestCase):

    def test_get_daily(self):
        res = get_coocc_with_other_entities('entity1', MOCK_DATA)
        self.assertEqual(res['entity2']['2013-06-03'], 1)
        self.assertEqual(res['entity3']['2013-06-03'], 1)

    def test_get_weekly(self):
        res = get_coocc_with_other_entities('entity1', MOCK_DATA, freq='W-FRI')
        self.assertEqual(res['entity2']['2013-06-07'], 5)
        self.assertEqual(res['entity3']['2013-06-07'], 5)

    def test_get_monthly(self):
        res = get_coocc_with_other_entities('entity1', MOCK_DATA, freq='M')
        self.assertEqual(res['entity2']['2013-06-30'], 20)
        self.assertEqual(res['entity3']['2013-06-30'], 20)


class TestGetNewsCount(unittest.TestCase):

    def test_get_daily(self):
        res = _get_news_count(MOCK_DATA, freq='D')
        self.assertEqual(res['entity1']['2013-06-03'], 2)
        self.assertEqual(res['entity2']['2013-06-03'], 1)
        self.assertEqual(res['entity3']['2013-06-03'], 1)

    def test_get_weekly(self):
        res = _get_news_count(MOCK_DATA, freq='W-FRI')
        self.assertEqual(res['entity1']['2013-06-07'], 10)
        self.assertEqual(res['entity2']['2013-06-07'], 5)
        self.assertEqual(res['entity3']['2013-06-07'], 5)

    def test_get_monthly(self):
        res = _get_news_count(MOCK_DATA, freq='M')
        self.assertEqual(res['entity1']['2013-06-30'], 40)
        self.assertEqual(res['entity2']['2013-06-30'], 20)
        self.assertEqual(res['entity3']['2013-06-30'], 20)


class TestGetRelativeCoOccWithOtherEntities(unittest.TestCase):

    def test_get_daily(self):
        res = get_relative_coocc_with_other_entities('entity1', MOCK_DATA)
        self.assertAlmostEqual(res['entity2']['2013-06-03'],
                               0.333333,
                               places=6)
        self.assertAlmostEqual(res['entity3']['2013-06-03'],
                               0.333333,
                               places=6)

    def test_get_weekly(self):
        res = get_relative_coocc_with_other_entities('entity1', MOCK_DATA,
                                                     freq='W-FRI')
        self.assertAlmostEqual(res['entity2']['2013-06-07'],
                               0.333333,
                               places=6)
        self.assertAlmostEqual(res['entity3']['2013-06-07'],
                               0.333333,
                               places=6)

    def test_get_monthly(self):
        res = get_relative_coocc_with_other_entities('entity1', MOCK_DATA,
                                                     freq='M')
        self.assertAlmostEqual(res['entity2']['2013-06-30'],
                               0.333333,
                               places=6)
        self.assertAlmostEqual(res['entity3']['2013-06-30'],
                               0.333333,
                               places=6)
