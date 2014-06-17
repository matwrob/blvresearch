import pandas as pd
import unittest

from blvresearch.concat.signals.utils import (
    get_total_return_on_signals,
    split_signals_into_good_and_bad
)

PATH = 'blvresearch/tests/mock_signals/'
MOCK_SIGNALS = pd.Series.from_csv(PATH + 'mock_signals.csv')
MOCK_RETURNS = pd.Series.from_csv(PATH + 'mock_returns.csv')


class TestGetTotalReturn(unittest.TestCase):

    def test_get(self):
        res = get_total_return_on_signals(MOCK_SIGNALS,
                                          MOCK_RETURNS)
        self.assertAlmostEqual(res, -0.0018956296, places=6)



class TestSplitSignalsIntoGoodAndBad(unittest.TestCase):

    def test_split_window_is_20(self):
        res = split_signals_into_good_and_bad(MOCK_SIGNALS,
                                              MOCK_RETURNS,
                                              window=20)
        exp = {'good': {'2012-07-17': 0.044577617070725085,
                        '2012-09-06': 0.098848649941241457,
                        '2013-11-04': 0.17902242246555852,
                        '2013-12-17': 0.10768392532273337,
                        '2014-01-28': 0.010159551551402527,
                        '2014-04-24': 0.056526867177459555,
                        '2014-06-02': 0.082600755323012948},
               'bad': {'2012-07-06': -0.023296553169004156,
                       '2012-10-19': -0.043479735039943845,
                       '2013-04-15': -0.0079380873373229716,
                       '2013-07-25': -0.021571318499339843,
                       '2013-10-08': -0.054422223480813062,
                       '2013-10-24': -0.037309062873418376,
                       '2013-11-22': -0.090729277572089928,
                       '2014-05-08': -0.16407993200224449}}
        for date, ret in res['good'].items():
            self.assertIn(date, exp['good'].keys())
            self.assertAlmostEqual(ret, exp['good'][date],
                                   places=6)

        for date, ret in res['bad'].items():
            self.assertIn(date, exp['bad'].keys())
            self.assertAlmostEqual(ret, exp['bad'][date],
                                   places=6)
