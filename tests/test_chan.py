import pandas as pd
import unittest

from blvresearch.core.chan import (
    ChanNews, ChanNoNews
)

from concat.core.utils import load_object


RESEARCH_DATA = load_object('/vagrant/blvresearch/tests/mock_jegadeesh.pickle')


def empty_some_news_fields(research_data):
    research_data['000C7F-E']['news']['2011-01-01':'2011-01-31'] = {}
    research_data['000C7F-E']['news']['2011-02-01':'2011-02-28'] = {}
    research_data['000C7F-E']['news']['2011-03-01':'2011-03-31'] = {}

    research_data['000DP6-E']['news']['2011-01-01':'2011-01-31'] = {}
    research_data['000DP6-E']['news']['2011-02-01':'2011-02-28'] = {}
    research_data['000DP6-E']['news']['2011-03-01':'2011-03-31'] = {}

    research_data['000KYG-E']['news']['2011-01-01':'2011-01-31'] = {}
    research_data['000KYG-E']['news']['2011-02-01':'2011-02-28'] = {}
    research_data['000KYG-E']['news']['2011-03-01':'2011-03-31'] = {}

    research_data['000Y8N-E']['news']['2011-01-01':'2011-01-31'] = {}
    research_data['000Y8N-E']['news']['2011-02-01':'2011-02-28'] = {}
    research_data['000Y8N-E']['news']['2011-03-01':'2011-03-31'] = {}

    return research_data

RESEARCH_DATA = empty_some_news_fields(RESEARCH_DATA)


def ts(year, month, day):
    dt = pd.datetime(year, month, day, 0, 0, 0)
    return pd.Timestamp(dt, tz='UTC')


class TestChanNews(unittest.TestCase):

    CN = ChanNews(RESEARCH_DATA,
                  type_of_return='abs_ret',
                  no_of_quantiles=3)

    def test_nan_returns_without_news(self):
        returns = self.CN._get_initial_returns(freq='M')
        result = self.CN._nan_returns_without_news(returns)
        self.assertEqual(len(result.loc[ts(2011, 1, 31)]), 10)
        self.assertEqual(len(result.loc[ts(2011, 1, 31)].dropna()), 6)

    def test_1M_terciles(self):
        returns = self.CN._get_initial_returns(freq='M')

        winners = self.CN._get_winners(returns, test_per=1, no_of_quantiles=3)
        self.assertEqual(set(winners[ts(2011, 1, 31)]),
                         set(['002Q0G-E', '000LNN-E', '000YMS-E']))
                         # using all entities we have:
                         # ['002Q0G-E', '000KYG-E', '000Y8N-E']
        self.assertEqual(set(winners[ts(2011, 2, 28)]),
                         set(['000CS1-E', '002Q0G-E', '069J8N-E']))
                         # using all entities we have:
                         # ['000Y8N-E', '000DP6-E', '000CS1-E']
        self.assertEqual(set(winners[ts(2011, 3, 31)]),
                         set(['069J8N-E', '000YMS-E', '000KN2-E']))
                         # using all entities we have:
                         # ['000DP6-E', 000Y8N-E', '069J8N-E']

        losers = self.CN._get_losers(returns, test_per=1, no_of_quantiles=3)
        self.assertEqual(set(losers[ts(2011, 1, 31)]),
                         set(['069J8N-E', '000KN2-E', '000CS1-E']))
                         # using all entities we have:
                         # ['000KN2-E', '069J8N-E', '000CS1-E']
        self.assertEqual(set(losers[ts(2011, 2, 28)]),
                         set(['000YMS-E', '000LNN-E', '000KN2-E']))
                         # using all entities we have:
                         # ['000YMS-E', '000KN2-E', '000LNN-E']
        self.assertEqual(set(losers[ts(2011, 3, 31)]),
                         set(['000LNN-E', '000CS1-E', '002Q0G-E']))
                         # using all entities we have:
                         # ['000LNN-E', '000CS1-E', '000KYG-E']


class TestChanNoNews(unittest.TestCase):

    CNN = ChanNoNews(RESEARCH_DATA,
                     type_of_return='abs_ret',
                     no_of_quantiles=3)

    def test_nan_returns_with_news(self):
        returns = self.CNN._get_initial_returns(freq='M')
        result = self.CNN._nan_returns_with_news(returns)
        self.assertEqual(len(result.loc[ts(2011, 1, 31)]), 10)
        self.assertEqual(len(result.loc[ts(2011, 1, 31)].dropna()), 4)

    def test_1M_terciles(self):
        returns = self.CNN._get_initial_returns(freq='M')
        winners = self.CNN._get_winners(returns, test_per=1, no_of_quantiles=3)
        self.assertEqual(set(winners[ts(2011, 1, 31)]),
                         set(['000KYG-E', '000Y8N-E', '000C7F-E']))
                         # using all entities we have:
                         # ['002Q0G-E', '000KYG-E', '000Y8N-E']
        self.assertEqual(set(winners[ts(2011, 2, 28)]),
                         set(['000Y8N-E', '000DP6-E', '000KYG-E']))
                         # using all entities we have:
                         # ['000Y8N-E', '000DP6-E', '000CS1-E']
        self.assertEqual(set(winners[ts(2011, 3, 31)]),
                         set(['000Y8N-E', '000DP6-E', '000C7F-E']))
                         # using all entities we have:
                         # ['000DP6-E', 000Y8N-E', '069J8N-E']

        losers = self.CNN._get_losers(returns, test_per=1, no_of_quantiles=3)
        self.assertEqual(set(losers[ts(2011, 1, 31)]),
                         set(['000DP6-E', '000C7F-E', '000Y8N-E']))
                         # using all entities we have:
                         # ['000KN2-E', '069J8N-E', '000CS1-E']
        self.assertEqual(set(losers[ts(2011, 2, 28)]),
                         set(['000C7F-E', '000KYG-E', '000DP6-E']))
                         # using all entities we have:
                         # ['000YMS-E', '000KN2-E', '000LNN-E']
        self.assertEqual(set(losers[ts(2011, 3, 31)]),
                         set(['000KYG-E', '000C7F-E', '000DP6-E']))
                         # using all entities we have:
                         # ['000LNN-E', '000CS1-E', '000KYG-E']
