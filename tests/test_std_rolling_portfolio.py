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
        self.assertEqual(set(winners[ts(2011, 1, 31)]),
                         set(['000Y8N-E', '000KYG-E', '002Q0G-E']))
        self.assertEqual(set(winners[ts(2011, 2, 28)]),
                         set(['000CS1-E', '000DP6-E', '000Y8N-E']))
        self.assertEqual(set(winners[ts(2011, 3, 31)]),
                         set(['000DP6-E', '000Y8N-E', '069J8N-E']))
        self.assertEqual(set(winners[ts(2011, 4, 30)]),
                         set(['000KN2-E', '000YMS-E', '002Q0G-E']))
        self.assertEqual(set(winners[ts(2011, 5, 31)]),
                         set(['000C7F-E', '000YMS-E', '069J8N-E']))
        self.assertEqual(set(winners[ts(2011, 6, 30)]),
                         set(['000CS1-E', '000DP6-E', '069J8N-E']))

        losers = get_losers(resampled, test_per=1, no_of_quantiles=3)
        self.assertEqual(set(losers[ts(2011, 7, 31)]),
                         set(['000KN2-E', '000KYG-E', '069J8N-E']))
        self.assertEqual(set(losers[ts(2011, 8, 31)]),
                         set(['000LNN-E', '000KYG-E', '000Y8N-E']))
        self.assertEqual(set(losers[ts(2011, 9, 30)]),
                         set(['000KN2-E', '000LNN-E', '000Y8N-E']))
        self.assertEqual(set(losers[ts(2011, 10, 31)]),
                         set(['000C7F-E', '002Q0G-E', '069J8N-E']))
        self.assertEqual(set(losers[ts(2011, 11, 30)]),
                         set(['000C7F-E', '000KN2-E', '000Y8N-E']))
        self.assertEqual(set(losers[ts(2011, 12, 31)]),
                         set(['000CS1-E', '000LNN-E', '000Y8N-E']))

    def test_2M_quintiles(self):
        df = get_dataframe_of_returns(PRICE_DATA)
        resampled = df.resample('M', how=sum)

        winners = get_winners(resampled, test_per=2, no_of_quantiles=5)
        self.assertEqual(set(winners[ts(2011, 2, 28)]),
                         set(['002Q0G-E', '000Y8N-E']))
        self.assertEqual(set(winners[ts(2011, 3, 31)]),
                         set(['000Y8N-E', '000DP6-E']))

        losers = get_losers(resampled, test_per=2, no_of_quantiles=5)
        self.assertEqual(set(losers[ts(2011, 4, 30)]),
                         set(['000CS1-E', '000LNN-E']))
        self.assertEqual(set(losers[ts(2011, 5, 31)]),
                         set(['000LNN-E', '000Y8N-E']))

    def test_1Q_quintiles(self):
        df = get_dataframe_of_returns(PRICE_DATA)
        resampled = df.resample('Q', how=sum)

        winners = get_winners(resampled, test_per=1, no_of_quantiles=5)
        self.assertEqual(set(winners[ts(2011, 3, 31)]),
                         set(['000DP6-E', '000Y8N-E'])),
        self.assertEqual(set(winners[ts(2011, 6, 30)]),
                         set(['000YMS-E', '069J8N-E']))
        self.assertEqual(set(winners[ts(2011, 9, 30)]),
                         set(['000C7F-E', '000YMS-E']))

        losers = get_losers(resampled, test_per=1, no_of_quantiles=5)
        self.assertEqual(set(losers[ts(2011, 12, 31)]),
                         set(['000C7F-E', '000CS1-E']))
        self.assertEqual(set(losers[ts(2012, 3, 31)]),
                         set(['000DP6-E', '000LNN-E']))
        self.assertEqual(set(losers[ts(2012, 6, 30)]),
                         set(['000KN2-E', '000LNN-E']))


class TestGetPorfolioPositions(unittest.TestCase):

    def test_1M_testing_1M_holding_terciles(self):
        df = get_dataframe_of_returns(PRICE_DATA)
        resampled = df.resample('M', how=sum)

        winners = get_winners(resampled, test_per=1, no_of_quantiles=3)
        result = get_portfolio_positions(resampled, winners, hold_per=1)
        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(result.index[0], ts(2011, 2, 28))
        row1 = result.loc[ts(2011, 2, 28)]
        self.assertEqual(set(row1[row1 == True].index),
                         set(['000Y8N-E', '000KYG-E', '002Q0G-E']))
        row2 = result.loc[ts(2011, 3, 31)]
        self.assertEqual(set(row2[row2 == True].index),
                         set(['000CS1-E', '000DP6-E', '000Y8N-E']))
        row3 = result.loc[ts(2011, 4, 30)]
        self.assertEqual(set(row3[row3 == True].index),
                         set(['000DP6-E', '000Y8N-E', '069J8N-E']))
        row4 = result.loc[ts(2011, 5, 31)]
        self.assertEqual(set(row4[row4 == True].index),
                         set(['000KN2-E', '000YMS-E', '002Q0G-E']))
        row5 = result.loc[ts(2011, 6, 30)]
        self.assertEqual(set(row5[row5 == True].index),
                         set(['000C7F-E', '000YMS-E', '069J8N-E']))
        row6 = result.loc[ts(2011, 7, 31)]
        self.assertEqual(set(row6[row6 == True].index),
                         set(['000CS1-E', '000DP6-E', '069J8N-E']))

        losers = get_losers(resampled, test_per=1, no_of_quantiles=3)
        result = get_portfolio_positions(resampled, losers, hold_per=1)
        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(result.index[6], ts(2011, 8, 31))
        row7 = result.loc[ts(2011, 8, 31)]
        self.assertEqual(set(row7[row7 == True].index),
                         set(['000KN2-E', '000KYG-E', '069J8N-E']))
        row8 = result.loc[ts(2011, 9, 30)]
        self.assertEqual(set(row8[row8 == True].index),
                         set(['000LNN-E', '000KYG-E', '000Y8N-E']))
        row9 = result.loc[ts(2011, 10, 31)]
        self.assertEqual(set(row9[row9 == True].index),
                         set(['000KN2-E', '000LNN-E', '000Y8N-E']))
        row10 = result.loc[ts(2011, 11, 30)]
        self.assertEqual(set(row10[row10 == True].index),
                         set(['000C7F-E', '002Q0G-E', '069J8N-E']))
        row11 = result.loc[ts(2011, 12, 31)]
        self.assertEqual(set(row11[row11 == True].index),
                         set(['000C7F-E', '000KN2-E', '000Y8N-E']))

    def test_1M_testing_2M_holding_deciles(self):
        df = get_dataframe_of_returns(PRICE_DATA)
        resampled = df.resample('M', how=sum)

        winners = get_winners(resampled, test_per=1, no_of_quantiles=10)
        result = get_portfolio_positions(resampled, winners, hold_per=2)
        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(result.index[0], ts(2011, 2, 28))
        row1 = result.loc[ts(2011, 2, 28)]
        self.assertEqual(set(row1[row1 == True].index),
                         set(['002Q0G-E']))
        row2 = result.loc[ts(2011, 3, 31)]
        self.assertEqual(set(row2[row2 == True].index),
                         set(['002Q0G-E', '000Y8N-E']))
        row3 = result.loc[ts(2011, 4, 30)]
        self.assertEqual(set(row3[row3 == True].index),
                         set(['000Y8N-E', '069J8N-E']))
        row4 = result.loc[ts(2011, 5, 31)]
        self.assertEqual(set(row4[row4 == True].index),
                         set(['069J8N-E', '000YMS-E']))
        row5 = result.loc[ts(2011, 6, 30)]
        self.assertEqual(set(row5[row5 == True].index),
                         set(['069J8N-E', '000YMS-E']))
        row6 = result.loc[ts(2011, 7, 31)]
        self.assertEqual(set(row6[row6 == True].index),
                         set(['069J8N-E']))
        row7 = result.loc[ts(2011, 8, 31)]
        self.assertEqual(set(row7[row7 == True].index),
                         set(['069J8N-E', '000C7F-E']))
        row8 = result.loc[ts(2011, 9, 30)]
        self.assertEqual(set(row8[row8 == True].index),
                         set(['000YMS-E', '000C7F-E']))
        row9 = result.loc[ts(2011, 10, 31)]
        self.assertEqual(set(row9[row9 == True].index),
                         set(['000YMS-E', '069J8N-E']))

    def test_1M_testing_3M_holding_deciles(self):
        df = get_dataframe_of_returns(PRICE_DATA)
        resampled = df.resample('M', how=sum)

        winners = get_winners(resampled, test_per=1, no_of_quantiles=10)
        result = get_portfolio_positions(resampled, winners, hold_per=3)
        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(result.index[0], ts(2011, 2, 28))
        row1 = result.loc[ts(2011, 2, 28)]
        self.assertEqual(set(row1[row1 == True].index),
                         set(['002Q0G-E']))
        row2 = result.loc[ts(2011, 3, 31)]
        self.assertEqual(set(row2[row2 == True].index),
                         set(['002Q0G-E', '000Y8N-E']))
        row3 = result.loc[ts(2011, 4, 30)]
        self.assertEqual(set(row3[row3 == True].index),
                         set(['002Q0G-E', '000Y8N-E', '069J8N-E']))
        row4 = result.loc[ts(2011, 5, 31)]
        self.assertEqual(set(row4[row4 == True].index),
                         set(['000Y8N-E', '069J8N-E', '000YMS-E']))
        row5 = result.loc[ts(2011, 6, 30)]
        self.assertEqual(set(row5[row5 == True].index),
                         set(['069J8N-E', '000YMS-E']))
        row6 = result.loc[ts(2011, 7, 31)]
        self.assertEqual(set(row6[row6 == True].index),
                         set(['069J8N-E', '000YMS-E']))
        row7 = result.loc[ts(2011, 8, 31)]
        self.assertEqual(set(row7[row7 == True].index),
                         set(['069J8N-E', '000C7F-E']))
        row8 = result.loc[ts(2011, 9, 30)]
        self.assertEqual(set(row8[row8 == True].index),
                         set(['069J8N-E', '000YMS-E', '000C7F-E']))
        row9 = result.loc[ts(2011, 10, 31)]
        self.assertEqual(set(row9[row9 == True].index),
                         set(['000C7F-E', '000YMS-E', '069J8N-E']))

    def test_2M_testing_2M_holding_deciles(self):
        df = get_dataframe_of_returns(PRICE_DATA)
        resampled = df.resample('M', how=sum)

        winners = get_winners(resampled, test_per=2, no_of_quantiles=10)
        result = get_portfolio_positions(resampled, winners, hold_per=2)
        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(result.index[0], ts(2011, 3, 31))
        row1 = result.loc[ts(2011, 3, 31)]
        self.assertEqual(set(row1[row1 == True].index),
                         set(['000Y8N-E']))
        row2 = result.loc[ts(2011, 4, 30)]
        self.assertEqual(set(row2[row2 == True].index),
                         set(['000Y8N-E']))
        row3 = result.loc[ts(2011, 5, 31)]
        self.assertEqual(set(row3[row3 == True].index),
                         set(['000Y8N-E', '069J8N-E']))
        row4 = result.loc[ts(2011, 6, 30)]
        self.assertEqual(set(row4[row4 == True].index),
                         set(['000YMS-E', '069J8N-E']))

        losers = get_losers(resampled, test_per=2, no_of_quantiles=10)
        result = get_portfolio_positions(resampled, losers, hold_per=2)
        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(result.index[0], ts(2011, 3, 31))
        row1 = result.loc[ts(2011, 3, 31)]
        self.assertEqual(set(row1[row1 == True].index),
                         set(['000KN2-E']))
        row2 = result.loc[ts(2011, 4, 30)]
        self.assertEqual(set(row2[row2 == True].index),
                         set(['000KN2-E', '000LNN-E']))
        row3 = result.loc[ts(2011, 5, 31)]
        self.assertEqual(set(row3[row3 == True].index),
                         set(['000LNN-E']))
        row4 = result.loc[ts(2011, 6, 30)]
        self.assertEqual(set(row4[row4 == True].index),
                         set(['000LNN-E']))


class TestGetMeanReturns(unittest.TestCase):

    def test_1M_testing_1M_holding_terciles(self):
        df = get_dataframe_of_returns(PRICE_DATA)
        resampled = df.resample('M', how=sum)
        winners = get_winners(resampled, test_per=1, no_of_quantiles=3)
        positions = get_portfolio_positions(resampled, winners, hold_per=1)
        result = get_mean_returns(resampled, positions, hold_per=1)
        self.assertEqual(result.index[0], ts(2011, 2, 28))
        self.assertEqual(result[ts(2011, 2, 28)], 0.064505575190823269)
        self.assertEqual(result[ts(2011, 3, 31)], -0.010649519188363175)
        self.assertEqual(result[ts(2011, 4, 30)], -0.045685388593123634)

        losers = get_losers(resampled, test_per=1, no_of_quantiles=3)
        positions = get_portfolio_positions(resampled, losers, hold_per=1)
        result = get_mean_returns(resampled, positions, hold_per=1)
        self.assertEqual(result.index[0], ts(2011, 2, 28))
        self.assertEqual(result[ts(2011, 2, 28)], 0.0053024694393602441)
        self.assertEqual(result[ts(2011, 3, 31)], -0.047737127144462765)
        self.assertEqual(result[ts(2011, 4, 30)], -0.044099986434406352)

    def test_1M_testing_2M_holding_terciles(self):
        df = get_dataframe_of_returns(PRICE_DATA)
        resampled = df.resample('M', how=sum)
        winners = get_winners(resampled, test_per=1, no_of_quantiles=3)
        positions = get_portfolio_positions(resampled, winners, hold_per=2)
        result = get_mean_returns(resampled, positions, hold_per=2)
        self.assertTrue(result.index[0], ts(2011, 3, 31))
        self.assertEqual(result[ts(2011, 3, 31)], -0.029013800897697867)
        self.assertEqual(result[ts(2011, 4, 30)], -0.04636471209374237)
        self.assertEqual(result[ts(2011, 5, 31)], 0.01157248440762014)

        losers = get_losers(resampled, test_per=1, no_of_quantiles=3)
        positions = get_portfolio_positions(resampled, losers, hold_per=2)
        result = get_mean_returns(resampled, positions, hold_per=2)
        self.assertTrue(result.index[0], ts(2011, 3, 31))
        self.assertEqual(result[ts(2011, 3, 31)], -0.032885665157726299)
        self.assertEqual(result[ts(2011, 4, 30)], -0.025912516913738425)
        self.assertEqual(result[ts(2011, 5, 31)], -0.017573165108614345)

    def test_2M_testing_2M_holding_quintiles(self):
        df = get_dataframe_of_returns(PRICE_DATA)
        resampled = df.resample('M', how=sum)
        winners = get_winners(resampled, test_per=2, no_of_quantiles=5)
        positions = get_portfolio_positions(resampled, winners, hold_per=2)
        result = get_mean_returns(resampled, positions, hold_per=2)
        self.assertEqual(result.index[0], ts(2011, 4, 30))
        self.assertEqual(result[ts(2011, 4, 30)], -0.040979783188388429)
        self.assertEqual(result[ts(2011, 5, 31)], 0.022401918324901751)
        self.assertEqual(result[ts(2011, 6, 30)], -0.030064390067186864)

        losers = get_losers(resampled, test_per=2, no_of_quantiles=5)
        positions = get_portfolio_positions(resampled, losers, hold_per=2)
        result = get_mean_returns(resampled, positions, hold_per=2)
        self.assertEqual(result.index[0], ts(2011, 4, 30))
        self.assertEqual(result[ts(2011, 4, 30)], -0.018821568778121554)
        self.assertEqual(result[ts(2011, 5, 31)], -0.023591727632861503)
        self.assertEqual(result[ts(2011, 6, 30)], -0.047617713321615608)
