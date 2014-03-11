import pandas as pd
import unittest

from blvresearch.core.event_study import (
    Event, EventConcatData, EventList, CloseEvents, EventDetector
)
from concat.core.utils import load_object

PRICE_DATA, META_DATA = load_object('blvresearch/tests/mock_data.pickle')


class MockEvent1(Event):
    def triggers(self):
        if self.concat_data.series_after('alpha', lag=0, length=1) > 0:
            return True


class MockEvent2(Event):
    def triggers(self):
        if self.concat_data.series_after('alpha', lag=0, length=1) < 0:
            return True


class TestEvent(unittest.TestCase):

    entity_id = '000C7F-E'
    date = pd.datetime(2011, 1, 3)
    EV = Event(entity_id, PRICE_DATA, META_DATA, date, EventList())

    def test_triggers(self):
        with self.assertRaises(NotImplementedError):
            self.EV.triggers()

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


class TestEventConcatData(unittest.TestCase):

    entity_id = '000C7F-E'
    date = pd.datetime(2011, 1, 14)
    event = Event(entity_id, PRICE_DATA, META_DATA, date, EventList())
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

    dates = [pd.datetime(2012, 10, 26),
             pd.datetime(2012, 10, 29),
             pd.datetime(2012, 10, 30)]
    EL = EventList()

    def test_append_event(self):
        self.assertEqual(len(self.EL), 0)

        event1 = Event('000C7F-E', PRICE_DATA, META_DATA, self.dates[0],
                       self.EL)
        self.EL.append_event(event1)
        self.assertEqual(len(self.EL), 1)
        self.assertEqual(self.EL.last, self.EL[0])

        event2 = Event('000C7F-E', PRICE_DATA, META_DATA, self.dates[1],
                       self.EL)
        self.EL.append_event(event2)
        self.assertEqual(len(self.EL), 2)
        self.assertEqual(self.EL.last, self.EL[1])

        event3 = Event('000C7F-E', PRICE_DATA, META_DATA, self.dates[2],
                       self.EL)
        self.EL.append_event(event3)
        self.assertEqual(len(self.EL), 3)
        self.assertEqual(self.EL.last, self.EL[2])

        for e in self.EL:
            self.assertIsInstance(e, Event)
        self.assertEqual(str(self.EL), "EventList with 3 events")

    def test_to_series(self):
        for d in self.dates:
            self.EL.append_event(Event('000C7F-E', PRICE_DATA, META_DATA, d,
                                       self.EL))
        result = self.EL.to_series()

        self.assertIsInstance(result, pd.TimeSeries)

        expected = pd.date_range('2012-10-26', '2012-10-30', freq='B')
        pd.np.testing.assert_array_equal(result.index, expected)

        self.assertEqual(result['2012-10-26'], self.EL[0])
        self.assertEqual(result['2012-10-29'], self.EL[1])
        self.assertEqual(result['2012-10-30'], self.EL[2])

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

    def test_remove_event(self):
        self.assertEqual(len(self.EL), 3)

        # remove middle event
        self.EL.remove_event(1)
        self.assertEqual(len(self.EL), 2)

        # remove first event
        self.EL.remove_event(0)
        self.assertEqual(len(self.EL), 1)

        # remove the last event
        self.EL.remove_event(0)
        self.assertEqual(len(self.EL), 0)
        self.assertIsInstance(self.EL, EventList)

    def test_extend(self):
        EL1 = EventList()
        EL1.append_event(Event('000C7F-E', PRICE_DATA, META_DATA,
                         pd.datetime(2012, 10, 26), EL1))
        EL1.append_event(Event('000C7F-E', PRICE_DATA, META_DATA,
                         pd.datetime(2012, 10, 29), EL1))
        EL1.append_event(Event('000C7F-E', PRICE_DATA, META_DATA,
                         pd.datetime(2012, 10, 30), EL1))

        EL2 = EventList()
        EL2.append_event(Event('000C7F-E', PRICE_DATA, META_DATA,
                         pd.datetime(2012, 11, 6), EL2))
        EL2.append_event(Event('000C7F-E', PRICE_DATA, META_DATA,
                         pd.datetime(2012, 11, 7), EL2))

        self.assertEqual(len(EL1), 3)
        self.assertEqual(len(EL2), 2)

        EL1.extend(EL2)
        self.assertEqual(len(EL1), 5)

        self.assertEqual(EL2[0], EL1[3])

        EL3 = EventList()
        EL1.extend(EL3)
        self.assertEqual(len(EL1), 5)

    def test_from_dict(self):
        EL1, EL2 = EventList(), EventList()

        EL1.append_event(Event('000C7F-E', PRICE_DATA, META_DATA,
                               pd.datetime(2012, 10, 26), EL1))
        EL1.append_event(Event('000C7F-E', PRICE_DATA, META_DATA,
                               pd.datetime(2012, 10, 29), EL1))
        EL1.append_event(Event('000C7F-E', PRICE_DATA, META_DATA,
                               pd.datetime(2012, 10, 30), EL1))

        EL2.append_event(Event('000BG2-E', PRICE_DATA, META_DATA,
                               pd.datetime(2012, 11, 6), EL2))
        EL2.append_event(Event('000BG2-E', PRICE_DATA, META_DATA,
                               pd.datetime(2012, 11, 7), EL2))

        result = EventList.from_dict({'000C7F-E': EL1, '000BG2-E': EL2})
        self.assertIsInstance(result, EventList)
        self.assertEqual(len(result), 5)

    def test_split_by_entity(self):
        EL1, EL2 = EventList(), EventList()

        EL1.append_event(Event('000C7F-E', PRICE_DATA, META_DATA,
                               pd.datetime(2012, 10, 26), EL1))
        EL1.append_event(Event('000C7F-E', PRICE_DATA, META_DATA,
                               pd.datetime(2012, 10, 29), EL1))
        EL1.append_event(Event('000C7F-E', PRICE_DATA, META_DATA,
                               pd.datetime(2012, 10, 30), EL1))

        EL2.append_event(Event('000BG2-E', PRICE_DATA, META_DATA,
                               pd.datetime(2012, 11, 6), EL2))
        EL2.append_event(Event('000BG2-E', PRICE_DATA, META_DATA,
                               pd.datetime(2012, 11, 7), EL2))

        EL = EventList.from_dict({'000C7F-E': EL1, '000BG2-E': EL2})
        result = EL.split_by_entity()
        self.assertIsInstance(result, dict)
        self.assertEqual(len(result), 2)
        self.assertEqual(set(result.keys()), set(['000C7F-E', '000BG2-E']))
        self.assertEqual(len(result['000C7F-E']), 3)
        self.assertIsInstance(result['000C7F-E'], EventList)
        self.assertEqual(len(result['000BG2-E']), 2)
        self.assertIsInstance(result['000BG2-E'], EventList)

    def to_dataframe(self):
        EL1, EL2 = EventList(), EventList()

        EL1.append_event(Event('000C7F-E', pd.datetime(2012, 10, 26), EL1))
        EL1.append_event(Event('000C7F-E', pd.datetime(2012, 10, 29), EL1))
        EL1.append_event(Event('000C7F-E', pd.datetime(2012, 11, 30), EL1))

        EL2.append_event(Event('000BG2-E', pd.datetime(2012, 11, 6), EL2))
        EL2.append_event(Event('000BG2-E', pd.datetime(2012, 11, 7), EL2))

        EL = EventList.from_dict({'000C7F-E': EL1, '000BG2-E': EL2})
        result = EL.to_dataframe()
        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(set(result.columns), set(['000C7F-E', '000BG2-E']))

        expected = pd.date_range('2012-10-26', '2012-11-30', freq='B')
        pd.np.testing.assert_array_equal(result.index, expected)


class TestCloseEvents(unittest.TestCase):

    EL = EventList()
    for d in PRICE_DATA.index:
        EL.append_event(Event('000C7F-E', PRICE_DATA, META_DATA, d, EL))
    by_date = EL.split_by_date()
    event = by_date[pd.datetime(2012, 10, 31)][0]
    CE = CloseEvents(event)

    def test_events_before(self):
        expected = ['2012-10-22', '2012-10-24']
        result = [e.date.strftime('%Y-%m-%d')
                  for e in self.CE.find_before(MockEvent1, days=10)]
        self.assertEqual(set(result), set(expected))

        expected = ['2012-10-17', '2012-10-18', '2012-10-19', '2012-10-23',
                    '2012-10-25', '2012-10-26']
        result = [e.date.strftime('%Y-%m-%d')
                  for e in self.CE.find_before(MockEvent2, days=10)]
        self.assertEqual(set(result), set(expected))

    def test_events_after(self):
        expected = ['2012-11-05', '2012-11-09', '2012-11-13']
        result = [e.date.strftime('%Y-%m-%d')
                  for e in self.CE.find_after(MockEvent1, days=10)]
        self.assertEqual(set(result), set(expected))

        expected = ['2012-11-01', '2012-11-02', '2012-11-06', '2012-11-07',
                    '2012-11-08', '2012-11-12', '2012-11-14']
        result = [e.date.strftime('%Y-%m-%d')
                  for e in self.CE.find_after(MockEvent2, days=10)]
        self.assertEqual(set(result), set(expected))


class TestEventDetector(unittest.TestCase):

    D = EventDetector(MockEvent1)

    def test_create_initial_list(self):
        result = self.D._create_initial_list('000C7F-E', PRICE_DATA, META_DATA)
        self.assertIsInstance(result, EventList)
        self.assertEqual(len(result), 754)

    def test_run(self):
        result = self.D.run('000C7F-E', PRICE_DATA, META_DATA)
        self.assertIsInstance(result, EventList)
        self.assertEqual(len(result), 378)
