import pandas as pd
import numpy as np
import unittest
import math

from blvresearch.core.es import (
    Event, EventConcatData, EventList, EventStatistics
)


class TestEvent(unittest.TestCase):

    entity_id = '000C7F-E'
    date = pd.datetime(2011, 1, 3)
    EV = Event(entity_id, date, EventList())

    def test_triggers(self):
        with self.assertRaises(NotImplementedError):
            self.EV.triggers

    def test_access_to_meta_data(self):
        self.assertEqual(self.EV.meta_data.blvindustry, '1300.1')
        self.assertEqual(self.EV.meta_data.country, 'US')
        self.assertEqual(self.EV.meta_data.exchange, 'NAS')
        self.assertEqual(self.EV.meta_data.fs_perm_sec_id, 'R85KLC-S-US')
        self.assertEqual(self.EV.meta_data.geounit, 'US')
        self.assertEqual(self.EV.meta_data.industry, '1340')
        self.assertEqual(self.EV.meta_data.sector, '1300')
        self.assertEqual(self.EV.meta_data.zone, 'am')

    def test_access_to_concat_data(self):
        self.assertEqual(self.EV.concat_data._position, 0)

        # Example: access to absolute return on event day
        expected = pd.Series(
            data=0.021499609032373197,
            index=pd.DatetimeIndex([pd.datetime(2011, 1, 3)])
        )
        result = self.EV.concat_data.series_after('abs_ret', lag=0, length=1)
        pd.np.testing.assert_array_equal(result, expected)

    def test_distance_to_last(self):
        # distance_to_last of single event is nan
        self.assertTrue(math.isnan(self.EV.distance_to_last))

        tmp = EventList()
        tmp.append_event(self.EV)
        tmp.append_event(Event('000C7F-E', pd.datetime(2011, 1, 4), tmp))
        # only if we have 2 events distance_to_last of the second event is int
        self.assertEqual(tmp[1].distance_to_last, 1)
        self.assertTrue(math.isnan(tmp[0].distance_to_last))


class TestEventConcatData(unittest.TestCase):

    entity_id = '000C7F-E'
    date = pd.datetime(2011, 1, 14)
    event = Event(entity_id, date, EventList([]))
    ECD = EventConcatData(event)

    def test_values_after_event_day(self):
        f = lambda attr, lag, length: self.ECD.series_after(attr, lag, length)

        length = 1

        lag = 0  # value on the event day
        expected = pd.Series(
            data=0.0080673481209179217,
            index=pd.DatetimeIndex([pd.datetime(2011, 1, 14)])
        )
        result = f('abs_ret', lag=lag, length=length)
        pd.np.testing.assert_array_equal(result, expected)

        lag = 1  # value one day after the event day (the next day)
        expected = pd.Series(
            data=-0.022725282524918643,
            index=pd.DatetimeIndex([pd.datetime(2011, 1, 18)])
        )
        result = f('abs_ret', lag=lag, length=length)
        pd.np.testing.assert_array_equal(result, expected)

        lag = 2  # value two days after the event day
        expected = pd.Series(
            data=-0.0053275376563269583,
            index=pd.DatetimeIndex([pd.datetime(2011, 1, 19)])
        )
        result = f('abs_ret', lag=lag, length=length)
        pd.np.testing.assert_array_equal(result, expected)

        lag = 744  # value on the last day in the series
        expected = pd.Series(
            data=0.011653680840938537,
            index=pd.DatetimeIndex([pd.datetime(2013, 12, 31)])
        )
        result = f('abs_ret', lag=lag, length=length)
        pd.np.testing.assert_array_equal(result, expected)

        lag = 745  # position outside scope
        self.assertRaises(ValueError, f, 'abs_ret', lag, length)

    def test_values_before_event_day(self):
        f = lambda attr, lag, length: self.ECD.series_before(attr, lag, length)

        length = 1

        lag = 0  # value on the event day
        expected = pd.Series(
            data=0.0080673481209179217,
            index=pd.DatetimeIndex([pd.datetime(2011, 1, 14)])
        )
        result = f('abs_ret', lag=lag, length=length)
        pd.np.testing.assert_array_equal(result, expected)

        lag = 1  # value one day before the event day (the previous day)
        expected = pd.Series(
            data=0.0036516487469242351,
            index=pd.DatetimeIndex([pd.datetime(2011, 1, 13)])
        )
        result = f('abs_ret', lag=lag, length=length)
        pd.np.testing.assert_array_equal(result, expected)

        lag = 2  # value two days before the event day
        expected = pd.Series(
            data=0.0081042917988070617,
            index=pd.DatetimeIndex([pd.datetime(2011, 1, 12)])
        )
        result = f('abs_ret', lag=lag, length=length)
        pd.np.testing.assert_array_equal(result, expected)

        lag = 9  # value on the first day in the series
        expected = pd.Series(
            data=0.021499609032373197,
            index=pd.DatetimeIndex([pd.datetime(2011, 1, 3)])
        )
        result = f('abs_ret', lag=lag, length=length)
        pd.np.testing.assert_array_equal(result, expected)

        lag = 10  # position outside scope
        self.assertRaises(ValueError, f, 'abs_ret', lag, length)

    def test_series_after_event_day(self):
        f = lambda attr, lag, length: self.ECD.series_after(attr, lag, length)

        length = 2

        lag = 0  # value on the event day and the next day
        expected = pd.Series(
            data=[0.0080673481209179217, -0.022725282524918643],
            index=pd.DatetimeIndex([pd.datetime(2011, 1, 14),
                                    pd.datetime(2011, 1, 18)])
        )
        result = f('abs_ret', lag=lag, length=length)
        pd.np.testing.assert_array_equal(result, expected)

        lag = 1  # value on the next day and the day after
        expected = pd.Series(
            data=[-0.022725282524918643, -0.0053275376563269583],
            index=pd.DatetimeIndex([pd.datetime(2011, 1, 18),
                                    pd.datetime(2011, 1, 19)])
        )
        result = f('abs_ret', lag=lag, length=length)
        pd.np.testing.assert_array_equal(result, expected)

        lag = 2
        expected = pd.Series(
            data=[-0.0053275376563269583, -0.018346952562863336],
            index=pd.DatetimeIndex([pd.datetime(2011, 1, 19),
                                    pd.datetime(2011, 1, 20)])
        )
        result = f('abs_ret', lag=lag, length=length)
        pd.np.testing.assert_array_equal(result, expected)

        lag = 743  # value on the last two days in the series
        expected = pd.Series(
            data=[-0.0099946104315767267, 0.011653680840938537],
            index=pd.DatetimeIndex([pd.datetime(2013, 12, 30),
                                    pd.datetime(2013, 12, 31)])
        )
        result = f('abs_ret', lag=lag, length=length)
        pd.np.testing.assert_array_equal(result, expected)

        lag = 744  # position outside scope
        self.assertRaises(ValueError, f, 'abs_ret', lag, length)

    def test_series_before_event_day(self):
        f = lambda attr, lag, length: self.ECD.series_before(attr, lag, length)

        length = 2

        lag = 0  # value on the event day and the previous day
        expected = pd.Series(
            data=[0.0036516487469242351, 0.0080673481209179217],
            index=pd.DatetimeIndex([pd.datetime(2011, 1, 13),
                                    pd.datetime(2011, 1, 14)])
        )
        result = f('abs_ret', lag=lag, length=length)
        pd.np.testing.assert_array_equal(result, expected)

        lag = 1  # value one day before the event day and the day before that
        expected = pd.Series(
            data=[0.0081042917988070617, 0.0036516487469242351],
            index=pd.DatetimeIndex([pd.datetime(2011, 1, 12),
                                    pd.datetime(2011, 1, 13)])
        )
        result = f('abs_ret', lag=lag, length=length)
        pd.np.testing.assert_array_equal(result, expected)

        lag = 2
        expected = pd.Series(
            data=[-0.0023827111310098367, 0.0081042917988070617],
            index=pd.DatetimeIndex([pd.datetime(2011, 1, 11),
                                    pd.datetime(2011, 1, 12)])
        )
        result = f('abs_ret', lag=lag, length=length)
        pd.np.testing.assert_array_equal(result, expected)

        lag = 8  # value on the first two days in the series
        expected = pd.Series(
            data=[0.021499609032373197, 0.0052053502518267852],
            index=pd.DatetimeIndex([pd.datetime(2011, 1, 3),
                                    pd.datetime(2011, 1, 4)])
        )
        result = f('abs_ret', lag=lag, length=length)
        pd.np.testing.assert_array_equal(result, expected)

        lag = 9  # position outside scope
        self.assertRaises(ValueError, f, 'abs_ret', lag, length)

    def test_value_on_event_day(self):
        f1 = lambda att, lag, length: self.ECD.series_after(att, lag, length)
        f2 = lambda att, lag, length: self.ECD.series_before(att, lag, length)

        lag, length = 0, 1

        expected = 0.0080673481209179217
        result1 = f1('abs_ret', lag, length)
        result2 = f2('abs_ret', lag, length)
        self.assertEqual(result1, expected)
        self.assertEqual(result2, expected)


class TestEventList(unittest.TestCase):

    EL = EventList()
    EL.append_event(Event('000C7F-E', pd.datetime(2012, 10, 26), EL))
    EL.append_event(Event('000C7F-E', pd.datetime(2012, 10, 29), EL))
    EL.append_event(Event('000C7F-E', pd.datetime(2012, 10, 30), EL))

    def test_append_event(self):
        EL = EventList()
        self.assertEqual(len(EL), 0)

        event1 = Event('000C7F-E', pd.datetime(2012, 10, 26), EL)
        EL.append_event(event1)
        self.assertEqual(len(EL), 1)
        self.assertTrue(math.isnan(EL[0].distance_to_last))
        self.assertEqual(EL.last, EL[0])

        event2 = Event('000C7F-E', pd.datetime(2012, 10, 29), EL)
        EL.append_event(event2)
        self.assertEqual(len(EL), 2)
        self.assertTrue(math.isnan(EL[0].distance_to_last))
        self.assertEqual(EL[1].distance_to_last, 3)
        self.assertEqual(EL.last, EL[1])

        event3 = Event('000C7F-E', pd.datetime(2012, 10, 30), EL)
        EL.append_event(event3)
        self.assertEqual(len(EL), 3)
        self.assertTrue(math.isnan(EL[0].distance_to_last))
        self.assertEqual(EL[1].distance_to_last, 3)
        self.assertEqual(EL[2].distance_to_last, 1)
        self.assertEqual(EL.last, EL[2])

        for e in EL:
            self.assertIsInstance(e, Event)
        self.assertEqual(str(EL), "EventList with 3 events")

    def test_getitem(self):
        with self.assertRaises(TypeError):
            self.EL['bla']
        with self.assertRaises(IndexError):
            self.EL[3]
        self.assertIsInstance(self.EL[0], Event)

    def test_date_index(self):
        expected = pd.date_range('2012-10-26', '2012-10-30', freq='B')
        result = self.EL._date_index
        pd.np.testing.assert_array_equal(result, expected)

    def test_to_series(self):
        result = self.EL.to_series()

        self.assertIsInstance(result, pd.TimeSeries)

        expected = pd.date_range('2012-10-26', '2012-10-30', freq='B')
        pd.np.testing.assert_array_equal(result.index, expected)

        self.assertEqual(result['2012-10-26'], self.EL[0])
        self.assertEqual(result['2012-10-29'], self.EL[1])
        self.assertEqual(result['2012-10-30'], self.EL[2])

    def test_remove_event(self):
        self.assertEqual(len(self.EL), 3)
        self.assertTrue(math.isnan(self.EL[0].distance_to_last))
        self.assertEqual(self.EL[1].distance_to_last, 3)
        self.assertEqual(self.EL[2].distance_to_last, 1)

        # remove middle event
        self.EL.remove_event(1)
        self.assertEqual(len(self.EL), 2)
        self.assertTrue(math.isnan(self.EL[0].distance_to_last))
        self.assertEqual(self.EL[1].distance_to_last, 4)

        # remove first event
        self.EL.remove_event(0)
        self.assertEqual(len(self.EL), 1)
        self.assertTrue(math.isnan(self.EL[0].distance_to_last))

        # remove the last event
        self.EL.remove_event(0)
        self.assertEqual(len(self.EL), 0)
        self.assertIsInstance(self.EL, EventList)

    def test_extend(self):
        EL = EventList()
        EL.append_event(Event('000C7F-E', pd.datetime(2012, 10, 26), EL))
        EL.append_event(Event('000C7F-E', pd.datetime(2012, 10, 29), EL))
        EL.append_event(Event('000C7F-E', pd.datetime(2012, 10, 30), EL))

        new = EventList()
        new.append_event(Event('000C7F-E', pd.datetime(2012, 11, 6), new))
        new.append_event(Event('000C7F-E', pd.datetime(2012, 11, 7), new))

        self.assertEqual(len(EL), 3)
        self.assertEqual(len(new), 2)

        self.assertTrue(math.isnan(new[0].distance_to_last))

        EL.extend(new)
        self.assertEqual(len(EL), 5)

        self.assertEqual(new[0], EL[3])
        self.assertEqual(EL[3].distance_to_last, 7)


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
