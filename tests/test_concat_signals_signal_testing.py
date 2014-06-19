from unittest.mock import patch, Mock
import pandas as pd
import unittest

from blvresearch.concat.signals.signal_testing import (
    get_total_return_on_signals,
    split_signals_into_good_and_bad,
    SignalReport, StrategyCharacteristics
)

PATH = 'blvresearch/tests/mock_signals/'
MOCK_SIGNALS = pd.Series.from_csv(PATH + 'mock_signals.csv')
MOCK_RETURNS = pd.Series.from_csv(PATH + 'mock_returns.csv')

MOCK_DICT_OF_SIGNALS = {
    '05J4MH-E': pd.Series({'2013-06-04': True,
                           '2014-01-15': True,
                           '2013-08-22': True,
                           '2013-09-06': True,
                           '2012-11-27': True,
                           '2013-10-18': True,
                           '2014-05-21': True,
                           '2013-01-14': False,
                           '2013-07-01': False,
                           '2013-01-03': False,
                           '2013-12-16': False,
                           '2012-12-13': False,
                           '2013-03-05': False,
                           '2012-08-09': False,
                           '2013-07-16': False,
                           '2013-07-29': False,
                           '2013-01-31': False}),
    '065V4R-E': pd.Series({'2014-02-05': True,
                           '2013-11-26': True,
                           '2013-01-25': True,
                           '2012-11-23': True,
                           '2013-09-27': True,
                           '2012-06-27': True,
                           '2013-09-10': True,
                           '2013-02-22': True,
                           '2014-03-04': False,
                           '2014-04-09': False,
                           '2013-08-16': False,
                           '2013-07-18': False}),
    '07MTLN-E': pd.Series({'2014-03-24': True,
                           '2012-08-09': True,
                           '2014-01-09': True,
                           '2014-01-23': True,
                           '2014-05-26': True,
                           '2013-02-25': True,
                           '2014-02-18': True,
                           '2013-06-14': True,
                           '2013-08-16': False,
                           '2013-12-05': False,
                           '2013-06-04': False,
                           '2013-11-13': False,
                           '2012-12-12': False,
                           '2012-12-21': False,
                           '2013-10-28': False,
                           '2013-05-15': False,
                           '2012-11-23': False,
                           '2013-02-14': False}),
    '05HWWL-E': pd.Series({'2014-06-12': True,
                           '2012-07-16': True,
                           '2014-02-28': True,
                           '2012-12-11': True,
                           '2013-05-14': True,
                           '2013-03-27': True,
                           '2013-12-09': True,
                           '2013-10-23': True,
                           '2012-10-08': True,
                           '2012-12-03': False,
                           '2013-03-11': False,
                           '2013-04-23': False,
                           '2013-08-21': False,
                           '2013-03-19': False,
                           '2012-07-26': False,
                           '2013-05-03': False,
                           '2012-11-08': False,
                           '2014-03-28': False,
                           '2013-01-30': False})
}

MOCK_DATA = {
    '05J4MH-E': (0.046127828974120419,
                 {'good': {'2013-06-04': 0.0073788990407531434,
                           '2014-01-15': 0.005128503454007052,
                           '2013-08-22': 0.009283601603383965,
                           '2013-09-06': 0.018676577731066579,
                           '2012-11-27': 0.0051954503675820558,
                           '2013-10-18': 0.018806257114713006,
                           '2014-05-21': 0.0088152669584841189},
                  'bad': {'2013-01-14': -6.528566600670551e-05,
                          '2013-07-01': -0.0247592106756463,
                          '2013-01-03': -0.031530448990694737,
                          '2013-12-16': -0.016176574430914276,
                          '2012-12-13': -0.0056972328449478695,
                          '2013-03-05': -0.017535012718628951,
                          '2012-08-09': -0.0078502319839690651,
                          '2013-07-16': -0.0091873492447004552,
                          '2013-07-29': -0.05608552005768265,
                          '2013-01-31': -0.006483390706669874}}),
    '065V4R-E': (0.48063633382428783,
                 {'good': {'2014-02-05': 0.037856433312010572,
                           '2013-11-26': 0.10839675586905638,
                           '2013-01-25': 0.19068115770428881,
                           '2012-11-23': 0.0046678574184674596,
                           '2013-09-27': 0.031481904809454522,
                           '2012-06-27': 0.0066195452037600133,
                           '2013-09-10': 0.093841344599680562,
                           '2013-02-22': 0.014357669679055206},
                  'bad': {'2014-03-04': -0.033658902658173104,
                          '2014-04-09': -0.055854195461227614,
                          '2013-08-16': -0.064770641458615497,
                          '2013-07-18': -0.037881395534195339}}),
    '07MTLN-E': (0.39891048230031978,
                 {'good': {'2014-03-24': 0.078738736111894497,
                           '2012-08-09': 0.048331971219941365,
                           '2014-01-09': 0.023826247574445607,
                           '2014-01-23': 0.097414923680460674,
                           '2014-05-26': 0.16452959622559207,
                           '2013-02-25': 0.048159465511595417,
                           '2014-02-18': 0.049411042092189078,
                           '2013-06-14': 0.028369472586117606},
                  'bad': {'2013-08-16': -0.015373512086228759,
                          '2013-12-05': -0.020387169148973261,
                          '2013-06-04': -0.020143788084581424,
                          '2013-11-13': -0.070939195527478932,
                          '2012-12-12': -0.03262136636317578,
                          '2012-12-21': -0.026517749528789158,
                          '2013-10-28': -0.0060079898986292266,
                          '2013-05-15': -0.12382820386483216,
                          '2012-11-23': -0.03867734526961733,
                          '2013-02-14': -0.017412822596867075}}),
    '05HWWL-E': (-0.048969092522405971,
                 {'good': {'2014-06-12': 0.035324780449172338,
                           '2012-07-16': 0.001497075022187367,
                           '2014-02-28': 0.017245952350821839,
                           '2012-12-11': 0.11639511839934279,
                           '2013-05-14': 0.084875439896714144,
                           '2013-03-27': 0.062467843994190975,
                           '2013-12-09': 0.06006604859198026,
                           '2013-10-23': 0.014159927515477372,
                           '2012-10-08': 0.062741535021666309},
                  'bad': {'2012-12-03': -0.011284686528494887,
                          '2013-03-11': -0.052329783824358697,
                          '2013-04-23': -0.044431202472725848,
                          '2013-08-21': -0.038347772307218198,
                          '2013-03-19': -0.084412941899751431,
                          '2012-07-26': -0.022772455372281307,
                          '2013-05-03': -0.0023138204089503027,
                          '2012-11-08': -0.16195101570564835,
                          '2014-03-28': -0.020269300466136897,
                          '2013-01-30': -0.042928286256102254}})
}

with patch('blvresearch.concat.signals.signal_testing.get_sp500_return',
           return_value=0.3):
    MOCK_CHARS = StrategyCharacteristics(MOCK_DATA)

assert MOCK_CHARS.benchmark == 0.3


class TestStrategyCharacteristics(unittest.TestCase):

    def test_entities_with_positive_total_returns(self):
        res = MOCK_CHARS.entities_with_positive_total_returns
        exp = {k: v for k, v in MOCK_DATA.items()
               if k in ['05J4MH-E', '065V4R-E', '07MTLN-E']}
        self.assertDictEqual(res, exp)

    def test_entities_with_negative_total_returns(self):
        res = MOCK_CHARS.entities_with_negative_total_returns
        exp = {k: v for k, v in MOCK_DATA.items()
               if k in ['05HWWL-E']}
        self.assertDictEqual(res, exp)

    def test_entities_that_beat_benchmark(self):
        res = MOCK_CHARS.entities_that_beat_benchmark
        exp = {k: v for k, v in MOCK_DATA.items()
               if k in ['065V4R-E', '07MTLN-E']}
        self.assertDictEqual(res, exp)

    def test_get_average_return_without_signal_specified(self):
        entities = MOCK_CHARS.all_entities
        res = MOCK_CHARS.get_average_return(entities)
        exp = (0.046127828974120419 +
               0.48063633382428783 +
               0.39891048230031978 -
               0.048969092522405971) / 4
        self.assertAlmostEqual(res, exp, places=6)

        entities = MOCK_CHARS.entities_with_positive_total_returns
        res = MOCK_CHARS.get_average_return(entities)
        exp = (0.046127828974120419 +
               0.48063633382428783 +
               0.39891048230031978) / 3
        self.assertAlmostEqual(res, exp, places=6)

        entities = MOCK_CHARS.entities_with_negative_total_returns
        res = MOCK_CHARS.get_average_return(entities)
        exp = -0.048969092522405971
        self.assertAlmostEqual(res, exp, places=6)

        entities = MOCK_CHARS.entities_that_beat_benchmark
        res = MOCK_CHARS.get_average_return(entities)
        exp = (0.48063633382428783 +
               0.39891048230031978) / 2
        self.assertAlmostEqual(res, exp, places=6)

    def test_get_average_return_for_good_signals(self):
        entities = MOCK_CHARS.all_entities
        res = MOCK_CHARS.get_average_return(entities, signal='good')
        exp = 0.3886856002773883
        self.assertAlmostEqual(res, exp, places=6)

        entities = MOCK_CHARS.entities_with_positive_total_returns
        res = MOCK_CHARS.get_average_return(entities, signal='good')
        exp = 0.36665622662266656
        self.assertAlmostEqual(res, exp, places=6)

        entities = MOCK_CHARS.entities_with_negative_total_returns
        res = MOCK_CHARS.get_average_return(entities, signal='good')
        exp = 0.4547737212415534
        self.assertAlmostEqual(res, exp, places=6)

        entities = MOCK_CHARS.entities_that_beat_benchmark
        res = MOCK_CHARS.get_average_return(entities, signal='good')
        exp = 0.5133420617990049
        self.assertAlmostEqual(res, exp, places=6)

    def test_get_numbers_of_good_and_bad_signals(self):
        res = MOCK_CHARS.get_numbers_of_good_and_bad_signals(MOCK_DATA)
        res = {'good': res['good'].sum(), 'bad': res['bad'].sum()}
        exp = {'good': 32, 'bad': 34}
        self.assertDictEqual(res, exp)

        res = MOCK_CHARS.get_numbers_of_good_and_bad_signals(
            MOCK_CHARS.entities_with_positive_total_returns
        )
        res = {'good': res['good'].sum(), 'bad': res['bad'].sum()}
        exp = {'good': 23, 'bad': 24}
        self.assertDictEqual(res, exp)

        res = MOCK_CHARS.get_numbers_of_good_and_bad_signals(
            MOCK_CHARS.entities_with_negative_total_returns
        )
        res = {'good': res['good'].sum(), 'bad': res['bad'].sum()}
        exp = {'good': 9, 'bad': 10}
        self.assertDictEqual(res, exp)

        res = MOCK_CHARS.get_numbers_of_good_and_bad_signals(
            MOCK_CHARS.entities_that_beat_benchmark
        )
        res = {'good': res['good'].sum(), 'bad': res['bad'].sum()}
        exp = {'good': 16, 'bad': 14}
        self.assertDictEqual(res, exp)


class TestSignalReport(unittest.TestCase):

    def test_get(self):
        with patch('blvresearch.concat.signals.utils.get_sp500_return',
                   return_value=0.3):
            with patch.object(SignalReport, '_get_data',
                              return_value=MOCK_DATA):
                sr = SignalReport(MOCK_DICT_OF_SIGNALS, 'MOCK_OUTPUT')
                res = sr.get()
        exp = ("Strategy generated profit for 3 companies (0.75)\n" +
               "Strategy generated loss for 1 companies (0.25)\n" +
               "Strategy outperformed SP500 for 2 companies (0.5)\n" +
               "Average number of signals per entity: 16.5\n" +
               "Average return of winners was 0.3086\n" +
               "Average return of losers was -0.049\n" +
               "Over the next 20 trading days after signals:\n" +
               "* 0.4894 of signals were correct among winners\n" +
               "* 0.5263 of signals were incorrect among losers\n")
        self.assertEqual(res, exp)


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
