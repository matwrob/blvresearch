import unittest
import pandas as pd
import numpy as np

from blvresearch.core.es import (
    Event, EventPriceData, EventList, EventStatistics
)


class TestEvent(unittest.TestCase):

    EV = Event('000C7F-E', pd.datetime(2011, 1, 3))

    def test_access_to_attributes(self):
        self.assertEqual(self.EV.year, 2011)
        self.assertEqual(self.EV._position_in_index, 0)
        self.assertEqual(self.EV.security.blvindustry, '1300.1')
        self.assertEqual(self.EV.security.country, 'US')
        self.assertEqual(self.EV.security.exchange, 'NAS')
        self.assertEqual(self.EV.security.fs_perm_sec_id, 'R85KLC-S-US')
        self.assertEqual(self.EV.security.geounit, 'US')
        self.assertEqual(self.EV.security.industry, '1340')
        self.assertEqual(self.EV.security.sector, '1300')
        self.assertEqual(self.EV.security.zone, 'am')


class TestEventPriceData(unittest.TestCase):

    _ev = Event('000C7F-E', pd.datetime(2011, 1, 4))
    ED = EventPriceData(_ev)

    def test_position_correctness(self):
        lag = -1
        expected = 0.021499609032373197
        result = self.ED.abs_ret(lag=lag)
        self.assertEqual(result, expected)

        lag = 0
        expected = 0.0052053502518267852
        result = self.ED.abs_ret(lag=lag)
        self.assertEqual(result, expected)

        lag = 1
        expected = 0.0081468682495512961
        result = self.ED.abs_ret(lag=lag)
        self.assertEqual(result, expected)

        lag = -2
        self.assertRaises(ValueError, self.ED.abs_ret, -2)

    def test_series_correctness(self):
        lag = 0
        expected = pd.Series()
        result = self.ED.series('abs_ret', lag=lag)
        pd.np.testing.assert_array_equal(result, expected)

        lag = -1
        expected = pd.Series(data=0.021499609032373197,
                             index=pd.DatetimeIndex([pd.datetime(2011, 1, 3)]),
                             name='abs_ret')
        result = self.ED.series('abs_ret', lag=lag)
        pd.np.testing.assert_array_equal(result, expected)

        lag = 2
        expected = pd.Series(data=[0.0081468682495512961,
                                   -0.00080871015145414092],
                             index=pd.DatetimeIndex([pd.datetime(2011, 1, 5),
                                                     pd.datetime(2011, 1, 6)]),
                             name='abs_ret')
        result = self.ED.series('abs_ret', lag=lag)
        pd.np.testing.assert_array_equal(result, expected)

        lag = -2
        self.assertRaises(ValueError, self.ED.series, 'abs_ret', lag)


class TestEventList(unittest.TestCase):

    e1 = Event('000C7F-E', pd.datetime(2012, 10, 31))
    e2 = Event('000BG2-E', pd.datetime(2011, 10, 31))
    e3 = Event('000KYG-E', pd.datetime(2012, 10, 31))
    EL = EventList([e1, e2, e3])

    def test_attributes(self):
        self.assertEqual(len(self.EL), 3)
        for e in self.EL:
            self.assertIsInstance(e, Event)

    def test_getitem(self):
        with self.assertRaises(TypeError):
            self.EL['bla']
        with self.assertRaises(IndexError):
            self.EL[3]
        self.assertEqual(self.EL[0], self.e1)
        self.assertEqual(self.EL[1], self.e2)
        self.assertEqual(self.EL[2], self.e3)

    def test_filter(self):
        by_zone = self.EL.filter('zone', 'am')
        self.assertIsInstance(by_zone, EventList)
        self.assertEqual(len(by_zone), 3)

        by_sector = self.EL.filter('sector', '1300')
        self.assertIsInstance(by_sector, EventList)
        self.assertEqual(len(by_sector), 1)

        by_exchange = self.EL.filter('exchange', 'NYS')
        self.assertIsInstance(by_exchange, EventList)
        self.assertEqual(len(by_exchange), 2)

        self.assertRaises(AttributeError, self.EL.filter, 'xchange', 'NYS')

        wrong_value = self.EL.filter('exchange', 'SMI')
        self.assertIsInstance(wrong_value, EventList)
        self.assertEqual(len(wrong_value), 0)

    def test_split_by_date(self):
        result = self.EL.split_by_date()

        self.assertIsInstance(result, dict)
        self.assertEqual(set(result.keys()), set([pd.datetime(2011, 10, 31),
                                                  pd.datetime(2012, 10, 31)]))

        date = pd.datetime(2011, 10, 31)
        self.assertIsInstance(result[date], EventList)
        self.assertEqual(len(result[date]), 1)
        self.assertEqual(result[date][0], self.e2)

        date = pd.datetime(2012, 10, 31)
        self.assertIsInstance(result[date], EventList)
        self.assertEqual(len(result[date]), 2)
        self.assertEqual(result[date][0], self.e1)
        self.assertEqual(result[date][1], self.e3)

    def test_split_by_entity(self):
        result = self.EL.split_by_entity()

        self.assertIsInstance(result, dict)
        self.assertEqual(set(result.keys()),
                         set(['000C7F-E', '000BG2-E', '000KYG-E']))

        entity_id = '000C7F-E'
        self.assertIsInstance(result[entity_id], EventList)
        self.assertEqual(len(result[entity_id]), 1)
        self.assertEqual(result[entity_id][0], self.e1)

    def test_date_index(self):
        expected = pd.date_range('2011-10-31', '2012-10-31', freq='B')
        result = self.EL._date_index
        pd.np.testing.assert_array_equal(result, expected)

    def test_to_series(self):
        result = self.EL._to_series_of_event_lists()

        expected = pd.date_range('2011-10-31', '2012-10-31', freq='B')
        pd.np.testing.assert_array_equal(result.index, expected)

        date = pd.datetime(2011, 10, 31)
        self.assertIsInstance(result[date], EventList)
        self.assertEqual(result[date][0].entity_id, '000BG2-E')

        date = pd.datetime(2012, 10, 31)
        self.assertIsInstance(result[date], EventList)
        self.assertEqual(result[date][0].entity_id, '000C7F-E')
        self.assertEqual(result[date][1].entity_id, '000KYG-E')

    def test_to_dataframe(self):
        result = self.EL._to_dataframe_of_events()
        expected = pd.DataFrame(
            data={'000C7F-E': pd.Series({pd.datetime(2012, 10, 31): self.e1}),
                  '000BG2-E': pd.Series({pd.datetime(2011, 10, 31): self.e2}),
                  '000KYG-E': pd.Series({pd.datetime(2012, 10, 31): self.e3})},
            index=pd.date_range('2011-10-31', '2012-10-31', freq='B')
        )
        pd.np.testing.assert_array_equal(result, expected)

    def test_from_list_of_lists(self):
        inp = [[self.e1, self.e2], [self.e3]]
        expected = EventList._from_list_of_lists(inp)
        self.assertIsInstance(expected, EventList)
        self.assertEqual(len(expected), 3)

    def test_from_dict(self):
        inp = {'000C7F-E': [self.e1],
               '000BG2-E': [self.e2],
               '000KYG-E': [self.e3]}
        expected = EventList._from_dict(inp)
        self.assertIsInstance(expected, EventList)
        self.assertEqual(len(expected), 3)


class TestEventStatistics(unittest.TestCase):

    e1 = Event('000C7F-E', pd.datetime(2012, 10, 31))
    e2 = Event('000BG2-E', pd.datetime(2011, 10, 31))
    e3 = Event('000KYG-E', pd.datetime(2012, 10, 31))
    EL = EventList([e1, e2, e3])
    ES = EventStatistics(EL)

    def test_mean(self):
        lag = 0
        expected = (-0.014475121833857024 +
                    -0.0064761073780771304 +
                    -0.002371355154399863) / 3
        result = self.ES.mean('abs_ret', lag=lag)
        self.assertEqual(result, expected)

        lag = 1
        expected = (0.0020470533927549762 +
                    -0.02082040884332851 +
                    0.01320773916777794) / 3
        result = self.ES.mean('abs_ret', lag=lag)
        self.assertEqual(result, expected)

        lag = -1
        expected = (-0.0091270952284665044 +
                    0.0016612832616329327 +
                    -0.0070805110535726353) / 3
        result = self.ES.mean('abs_ret', lag=lag)
        self.assertEqual(result, expected)

    def test_standard_deviation(self):
        lag = 0
        expected = np.std([-0.014475121833857024,
                           -0.0064761073780771304,
                           -0.002371355154399863])
        result = self.ES.standard_deviation('abs_ret', lag=lag)
        self.assertEqual(result, expected)

        lag = 1
        expected = np.std([0.0020470533927549762,
                           -0.02082040884332851,
                           0.01320773916777794])
        result = self.ES.standard_deviation('abs_ret', lag=lag)
        self.assertEqual(result, expected)

        lag = -1
        expected = np.std([-0.0091270952284665044,
                           0.0016612832616329327,
                           -0.0070805110535726353])
        result = self.ES.standard_deviation('abs_ret', lag=lag)
        self.assertEqual(result, expected)

    def test_median(self):
        lag = 0
        expected = -0.0064761073780771304
        result = self.ES.median('abs_ret', lag=lag)
        self.assertEqual(result, expected)

        lag = 1
        expected = 0.0020470533927549762
        result = self.ES.median('abs_ret', lag=lag)
        self.assertEqual(result, expected)

        lag = -1
        expected = -0.0070805110535726353
        result = self.ES.median('abs_ret', lag=lag)
        self.assertEqual(result, expected)

    def test_series(self):
        lag = 2
        result = self.ES._series('abs_ret', lag=lag)

        key = ('000C7F-E', pd.datetime(2012, 10, 31))
        expected = pd.Series(
            data=[0.0020470533927549762, -0.033650543522973628],
            index=pd.DatetimeIndex([pd.datetime(2012, 11, 1),
                                    pd.datetime(2012, 11, 2)])
        )
        pd.np.testing.assert_array_equal(result[key], expected)

        key = ('000BG2-E', pd.datetime(2011, 10, 31))
        expected = pd.Series(
            data=[-0.02082040884332851, 0.002271867694317023],
            index=pd.DatetimeIndex([pd.datetime(2011, 11, 1),
                                    pd.datetime(2011, 11, 2)])
        )
        pd.np.testing.assert_array_equal(result[key], expected)

        key = ('000KYG-E', pd.datetime(2012, 10, 31))
        expected = pd.Series(
            data=[0.01320773916777794, -0.0014067997630816834],
            index=pd.DatetimeIndex([pd.datetime(2012, 11, 1),
                                    pd.datetime(2012, 11, 2)])
        )
        pd.np.testing.assert_array_equal(result[key], expected)

        lag = -2
        result = self.ES._series('abs_ret', lag=lag)

        key = ('000C7F-E', pd.datetime(2012, 10, 31))
        expected = pd.Series(
            data=[-0.011892166035338377, -0.0091270952284665044],
            index=pd.DatetimeIndex([pd.datetime(2012, 10, 25),
                                    pd.datetime(2012, 10, 26)])
        )
        pd.np.testing.assert_array_equal(result[key], expected)

        key = ('000BG2-E', pd.datetime(2011, 10, 31))
        expected = pd.Series(
            data=[0.0089070917321790177, 0.0016612832616329327],
            index=pd.DatetimeIndex([pd.datetime(2011, 10, 27),
                                    pd.datetime(2011, 10, 28)])
        )
        pd.np.testing.assert_array_equal(result[key], expected)

        key = ('000KYG-E', pd.datetime(2012, 10, 31))
        expected = pd.Series(
            data=[0.0, -0.0070805110535726353],
            index=pd.DatetimeIndex([pd.datetime(2012, 10, 25),
                                    pd.datetime(2012, 10, 26)])
        )
        pd.np.testing.assert_array_equal(result[key], expected)

    def test_cumulative_values(self):
        lag = 2
        result = self.ES._cumulative_values('abs_ret', lag=lag)

        key = ('000C7F-E', pd.datetime(2012, 10, 31))
        expected = np.sum([0.0020470533927549762, -0.033650543522973628])
        self.assertEqual(result[key], expected)

        key = ('000BG2-E', pd.datetime(2011, 10, 31))
        expected = np.sum([-0.02082040884332851, 0.002271867694317023])
        self.assertEqual(result[key], expected)

        key = ('000KYG-E', pd.datetime(2012, 10, 31))
        expected = np.sum([0.01320773916777794, -0.0014067997630816834])
        self.assertEqual(result[key], expected)

        lag = 0
        result = self.ES._cumulative_values('abs_ret', lag=lag)

        key = ('000C7F-E', pd.datetime(2012, 10, 31))
        expected = 0
        self.assertEqual(result[key], expected)

        key = ('000BG2-E', pd.datetime(2011, 10, 31))
        expected = 0
        self.assertEqual(result[key], expected)

        key = ('000KYG-E', pd.datetime(2012, 10, 31))
        expected = 0
        self.assertEqual(result[key], expected)

        lag = -2
        result = self.ES._cumulative_values('abs_ret', lag=lag)

        key = ('000C7F-E', pd.datetime(2012, 10, 31))
        expected = np.sum([-0.011892166035338377, -0.0091270952284665044])
        self.assertEqual(result[key], expected)

        key = ('000BG2-E', pd.datetime(2011, 10, 31))
        expected = np.sum([0.0089070917321790177, 0.0016612832616329327])
        self.assertEqual(result[key], expected)

        key = ('000KYG-E', pd.datetime(2012, 10, 31))
        expected = np.sum([0.0, -0.0070805110535726353])
        self.assertEqual(result[key], expected)

    def test_mean_over_cumulative_values(self):
        lag = 2
        result = self.ES.mean_over_cumulative_values('abs_ret', lag=lag)
        expected = np.mean(
            [np.sum([0.0020470533927549762, -0.033650543522973628]),
             np.sum([-0.02082040884332851, 0.002271867694317023]),
             np.sum([0.01320773916777794, -0.0014067997630816834])]
        )
        self.assertEqual(result, expected)

        lag = 0
        result = self.ES.mean_over_cumulative_values('abs_ret', lag=lag)
        expected = 0
        self.assertEqual(result, expected)

        lag = -2
        result = self.ES.mean_over_cumulative_values('abs_ret', lag=lag)
        expected = np.mean(
            [np.sum([-0.011892166035338377, -0.0091270952284665044]),
             np.sum([0.0089070917321790177, 0.0016612832616329327]),
             np.sum([0.0, -0.0070805110535726353])]
        )
        self.assertEqual(result, expected)

    def test_standard_deviation_over_cumulative_values(self):
        lag = 2
        result = self.ES.standard_deviation_over_cumulative_values('abs_ret',
                                                                   lag=lag)
        expected = np.std(
            [np.sum([0.0020470533927549762, -0.033650543522973628]),
             np.sum([-0.02082040884332851, 0.002271867694317023]),
             np.sum([0.01320773916777794, -0.0014067997630816834])]
        )
        self.assertEqual(result, expected)

        lag = 0
        result = self.ES.standard_deviation_over_cumulative_values('abs_ret',
                                                                   lag=lag)
        expected = 0
        self.assertEqual(result, expected)

        lag = -2
        result = self.ES.standard_deviation_over_cumulative_values('abs_ret',
                                                                   lag=lag)
        expected = np.std(
            [np.sum([-0.011892166035338377, -0.0091270952284665044]),
             np.sum([0.0089070917321790177, 0.0016612832616329327]),
             np.sum([0.0, -0.0070805110535726353])]
        )
        self.assertEqual(result, expected)

    def test_median_over_cumulative_values(self):
        lag = 2
        result = self.ES.median_over_cumulative_values('abs_ret', lag=lag)
        expected = np.median(
            [np.sum([0.0020470533927549762, -0.033650543522973628]),
             np.sum([-0.02082040884332851, 0.002271867694317023]),
             np.sum([0.01320773916777794, -0.0014067997630816834])]
        )
        self.assertEqual(result, expected)

        lag = 0
        result = self.ES.median_over_cumulative_values('abs_ret', lag=lag)
        expected = 0
        self.assertEqual(result, expected)

        lag = -2
        result = self.ES.median_over_cumulative_values('abs_ret', lag=lag)
        expected = np.median(
            [np.sum([-0.011892166035338377, -0.0091270952284665044]),
             np.sum([0.0089070917321790177, 0.0016612832616329327]),
             np.sum([0.0, -0.0070805110535726353])]
        )
        self.assertEqual(result, expected)
