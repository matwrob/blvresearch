import pandas as pd
import unittest

from blvresearch.core.std_rolling_portfolio import (
    get_dataframe_of_returns, get_resampled_returns,
    get_testing_returns, get_winners, get_losers
)

from concat.core.utils import load_object


PRICE_DATA, META_DATA = load_object('blvresearch/tests/mock_data.pickle')
PRICE_DATA['abs_ret'] = PRICE_DATA['rel_ret'] + PRICE_DATA['bench']
PRICE_DATA = {'000C7F-E': PRICE_DATA, '001C7F-E': PRICE_DATA,
              '002C7F-E': PRICE_DATA, '003C7F-E': PRICE_DATA,
              '004C7F-E': PRICE_DATA, '005C7F-E': PRICE_DATA,
              '006C7F-E': PRICE_DATA, '007C7F-E': PRICE_DATA,
              '008C7F-E': PRICE_DATA, '009C7F-E': PRICE_DATA,
              '010C7F-E': PRICE_DATA, '011C7F-E': PRICE_DATA,
              '012C7F-E': PRICE_DATA, '013C7F-E': PRICE_DATA,
              '014C7F-E': PRICE_DATA, '015C7F-E': PRICE_DATA}


class TestGetDataFrameOfReturns(unittest.TestCase):

    def test_get_abs_ret(self):
        result = get_dataframe_of_returns(PRICE_DATA)
        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(set(result.columns), set(PRICE_DATA.keys()))
        self.assertEqual(result.shape, (754, 16))

    def test_get_alpha(self):
        result = get_dataframe_of_returns(PRICE_DATA, 'alpha')
        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(set(result.columns), set(PRICE_DATA.keys()))
        self.assertEqual(result.shape, (754, 16))


class TestGetResampledReturns(unittest.TestCase):

    def test_get_monthly(self):
        result = get_resampled_returns(PRICE_DATA)
        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(set(result.columns), set(PRICE_DATA.keys()))
        self.assertEqual(result.shape, (36, 16))
        self.assertEqual(result['000C7F-E'][0], 0.050654449496584694)

    def test_get_quarterly(self):
        result = get_resampled_returns(PRICE_DATA, freq='Q')
        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(set(result.columns), set(PRICE_DATA.keys()))
        self.assertEqual(result.shape, (12, 16))
        self.assertEqual(result['000C7F-E'][0], 0.077370585329502986)


class TestGetTestingReturns(unittest.TestCase):

    def test_get_1_month(self):
        df = get_resampled_returns(PRICE_DATA)
        result = get_testing_returns(df)
        self.assertEqual(result.shape, (36, 16))
        self.assertEqual(str(result.index[0])[:10], '2011-01-31')
        self.assertEqual(result.loc['2011-01-31'][0], 0.050654449496584694)

    def test_get_2_months(self):
        df = get_resampled_returns(PRICE_DATA)
        result = get_testing_returns(df, test_periods=2)
        self.assertEqual(result.shape, (35, 16))
        self.assertEqual(str(result.index[0])[:10], '2011-02-28')
        self.assertEqual(result.loc['2011-02-28'][0], 0.09077361545684362)

    def test_get_3_months(self):
        df = get_resampled_returns(PRICE_DATA)
        result = get_testing_returns(df, test_periods=3)
        self.assertEqual(result.shape, (34, 16))
        self.assertEqual(str(result.index[0])[:10], '2011-03-31')
        self.assertEqual(result.loc['2011-03-31'][0], 0.077370585329503014)


class TestGetWinners(unittest.TestCase):

    def test_get_winners(self):
        abs_ret = get_resampled_returns(PRICE_DATA)
        test_ret = get_testing_returns(abs_ret)
        result = get_winners(test_ret)

        for date, portf in result.items():
            self.assertEqual(len(portf), 5)


class TestGetLosers(unittest.TestCase):

    def test_get_losers(self):
        abs_ret = get_resampled_returns(PRICE_DATA)
        test_ret = get_testing_returns(abs_ret, test_periods=2)
        result = get_losers(test_ret, test_periods=2, no_of_quantiles=8)

        for date, portf in result.items():
            self.assertEqual(len(portf), 2)


class TestGetJegadeeshReturns(unittest.TestCase):

    def test_get(self):
        pass
