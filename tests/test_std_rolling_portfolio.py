import pandas as pd
import unittest

from blvresearch.core.std_rolling_portfolio import (
    get_dataframe_of_returns, get_sorted_returns,
    get_winners, get_losers, get_portfolio_positions,
    get_mean_returns
)

from concat.core.utils import load_object


PRICE_DATA = load_object('/vagrant/blvresearch/tests/mock_jegadeesh.pickle')

def ts(year, month, day):
    dt = pd.datetime(year, month, day, 0, 0, 0)
    return pd.Timestamp(dt, tz='UTC')

class TestGetDataFrameOfReturns(unittest.TestCase):

    def test_get_abs_ret(self):
        result = get_dataframe_of_returns(PRICE_DATA)
        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(set(result.columns), set(PRICE_DATA.keys()))
        self.assertEqual(result.shape, (754, 10))
        self.assertEqual(result['000C7F-E']['2013-12-31'][0],
                         0.014190946109989659)

    def test_get_alpha(self):
        result = get_dataframe_of_returns(PRICE_DATA, 'alpha')
        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(set(result.columns), set(PRICE_DATA.keys()))
        self.assertEqual(result.shape, (754, 10))
        self.assertEqual(result['000C7F-E']['2013-12-31'][0],
                         0.011690812716191207)


class TestGetSortedReturns(unittest.TestCase):

    def test_get_1_month(self):
        df = get_dataframe_of_returns(PRICE_DATA)
        resampled = df.resample('M', how=sum)
        result = get_sorted_returns(resampled, test_per=1)

        for k, v in result.items():
            self.assertIsInstance(k, pd.tslib.Timestamp)
            self.assertIsInstance(v, pd.Series)
        self.assertEqual(len(result), 36)
        self.assertEqual(len(result[ts(2011, 1, 31)]), 10)
        self.assertEqual(result[ts(2011, 1, 31)]['000C7F-E'],
                         0.028940836516168474)

    def test_get_2_months(self):
        df = get_dataframe_of_returns(PRICE_DATA)
        resampled = df.resample('M', how=sum)
        result = get_sorted_returns(resampled, test_per=2)

        for k, v in result.items():
            self.assertIsInstance(k, pd.tslib.Timestamp)
            self.assertIsInstance(v, pd.Series)
        self.assertEqual(len(result), 35)
        self.assertEqual(len(result[ts(2011, 2, 28)]), 10)
        self.assertEqual(result[ts(2011, 2, 28)]['000C7F-E'],
                         0.061647021123041996)

    def test_get_3_months(self):
        df = get_dataframe_of_returns(PRICE_DATA)
        resampled = df.resample('M', how=sum)
        result = get_sorted_returns(resampled, test_per=3)

        for k, v in result.items():
            self.assertIsInstance(k, pd.tslib.Timestamp)
            self.assertIsInstance(v, pd.Series)
        self.assertEqual(len(result), 34)
        self.assertEqual(len(result[ts(2011, 3, 31)]), 10)
        self.assertEqual(result[ts(2011, 3, 31)]['000C7F-E'],
                         0.021173995271057768)


class TestWinnersLosers(unittest.TestCase):

    def test_1M_terciles(self):
        df = get_dataframe_of_returns(PRICE_DATA)
        resampled = df.resample('M', how=sum)

        winners = get_winners(resampled, test_per=1, no_of_quantiles=3)
        self.assertEqual(winners[ts(2011, 1, 31)],
                         ['000Y8N-E', '000KYG-E', '002Q0G-E'])

        losers = get_losers(resampled, test_per=1, no_of_quantiles=3)
        self.assertEqual(losers[ts(2011, 1, 31)],
                         ['000KN2-E', '069J8N-E', '000CS1-E'])

    def test_2M_quintiles(self):
        df = get_dataframe_of_returns(PRICE_DATA)
        resampled = df.resample('M', how=sum)

        winners = get_winners(resampled, test_per=2, no_of_quantiles=5)
        self.assertEqual(winners[ts(2011, 2, 28)],
                         ['002Q0G-E', '000Y8N-E'])

        losers = get_losers(resampled, test_per=2, no_of_quantiles=5)
        self.assertEqual(losers[ts(2011, 2, 28)],
                         ['000KN2-E', '000YMS-E'])


class TestGetPorfolioPositions(unittest.TestCase):

    def test_1M_testing_1M_holding_terciles(self):
        df = get_dataframe_of_returns(PRICE_DATA)
        resampled = df.resample('M', how=sum)

        winners = get_winners(resampled, test_per=1, no_of_quantiles=3)
        result = get_portfolio_positions(resampled, winners, hold_per=1)

        self.assertIsInstance(result, pd.DataFrame)

        self.assertEqual(result.index[0], ts(2011, 1, 31))

        first_row = result.loc[ts(2011, 1, 31)]
        self.assertEqual(len(first_row[first_row == True]), 0)

        second_row = result.loc[ts(2011, 2, 28)]
        self.assertEqual(set(second_row[second_row == True].index),
                         set(['000Y8N-E', '000KYG-E', '002Q0G-E']))

    def test_2M_testing_2M_holding_quintiles(self):
        df = get_dataframe_of_returns(PRICE_DATA)
        resampled = df.resample('M', how=sum)

        losers = get_losers(resampled, test_per=2, no_of_quantiles=5)
        result = get_portfolio_positions(resampled, losers, hold_per=2)

        self.assertIsInstance(result, pd.DataFrame)

        self.assertEqual(result.index[0], ts(2011, 2, 28))

        first_row = result.loc[ts(2011, 2, 28)]
        self.assertEqual(len(first_row[first_row == True]), 0)

        second_row = result.loc[ts(2011, 3, 31)]
        self.assertEqual(set(second_row[second_row == True].index),
                         set(['000KN2-E', '000YMS-E']))


class TestGetMeanReturns(unittest.TestCase):

    def test_1M_testing_1M_holding_terciles(self):
        df = get_dataframe_of_returns(PRICE_DATA)
        resampled = df.resample('M', how=sum)
        winners = get_winners(resampled, test_per=1, no_of_quantiles=3)
        positions = get_portfolio_positions(resampled, winners, hold_per=1)
        result = get_mean_returns(resampled, positions, hold_per=1)
        self.assertTrue(False)



    def test_2M_testing_2M_holding_quintiles(self):
        self.assertTrue(False)

class TestGetJegadeeshReturns(unittest.TestCase):

    def test_get_winners_returns(self):
        self.assertTrue(False)

    def test_get_losers_returns(self):
        self.assertTrue(False)

    def test_get_wml_returns(self):
        self.assertTrue(False)
