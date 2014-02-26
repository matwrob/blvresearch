from itertools import chain
import pandas as pd
import numpy as np

from concat.core.utils import load_object
# from blvresearch.core.utils import get_universe_by_entity_id, start, end
# from blvresearch.core.SP500output import ENTITIES_SP560
# from concat.core.benchmark_model import BenchmarkModelData
# UNI = {y: get_universe_by_entity_id(ENTITIES_SP560, start(y), end(y))
#        for y in RESEARCH_YEARS}
# DATA = {k: BenchmarkModelData(v, start(k), end(k),
#                               in_currency='USD', news=True)
#         for k, v in UNI.items()}
UNI = load_object('uni_sp500_2011_2013.pickle')
DATA = load_object('bmd_sp500_2011_2013.pickle')


class EventDetector:

    def __init__(self, event_class):
        self.event = event_class

    def run(self, entity_id, entity_data):
        eel = EventList()
        for d in entity_data.index:
            e = self.event(entity_id, d, eel)
            if e.triggers():
                eel.append_event(e)
        return eel


class Event:

    DISTANCE_THRESH = 4

    def __init__(self, entity_id, date, event_list):
        self.entity_id = entity_id
        self.date = date
        self.distance_to_last = self._find_distance(event_list)

    def __str__(self):
        return 'Event for "%s" on %s' % (self.entity_id,
                                         self.date.strftime("%Y-%m-%d"))

    def __repr__(self):
        return str(self)

    def triggers(self):
        raise NotImplementedError

    @property
    def meta_data(self):
        return UNI[self.date.year][self.entity_id]

    @property
    def concat_data(self):
        return EventConcatData(self)

    def _find_distance(self, event_list):
        if len(event_list) > 0:
            prev = len(event_list) - 1
            return (self.date - event_list[prev].date).days
        return np.nan


class EventConcatData:

    def __init__(self, event):
        self._data = DATA[event.date.year][event.entity_id]
        self._date = event.date

    def series_after(self, attribute, lag=1, length=5):
        start = self._position + lag
        end = start + length
        if end > len(self._data[attribute]):
            raise ValueError('Date outside total date scope')
        return self._data[attribute][start:end]

    def series_before(self, attribute, lag=1, length=5):
        end = self._position - lag + 1
        start = end - length
        if start < 0:
            raise ValueError('Date outside total date scope')
        return self._data[attribute][start:end]

    @property
    def _position(self):
        "gives event day position in data index"
        return self._data.index.get_loc(self._date)


class EventList:

    def __init__(self):
        self._events = list()

    def __str__(self):
        return 'EventList with %s events' % len(self)

    def __repr__(self):
        return str(self)

    def __iter__(self):
        for e in self._events:
            yield e

    def __getitem__(self, value):
        if not isinstance(value, int):
            raise TypeError('Event list indices must be integers')
        if 0 <= value < len(self):
            return self._events[value]
        raise IndexError('Index out of range')

    def __len__(self):
        return len(self._events)

    def append_event(self, event):
        self._events.append(event)

    def extend(self, event_list):
        e = event_list[0]
        e.distance_to_last = (e.date - self.last.date).days
        self._events.extend(event_list._events)

    @property
    def last(self):
        return self._events[len(self._events) - 1]

    def to_series(self):
        result = pd.Series({e.date: e for e in self})
        result.reindex(self._date_index)
        return result

    @classmethod
    def from_dict(cls, dict_of_event_lists):
        iterable = [d.values._events for d in dict_of_event_lists]
        events = chain.from_iterable(iterable)
        return EventList(list(events))

    @property
    def _date_index(self):
        all_dates = [e.date for e in self]
        start, end = min(all_dates), max(all_dates)
        return pd.date_range(start, end, freq='B')

    def remove_event(self, index):
        del self._events[index]
        # reset distances
        if len(self._events) > 1:
            self._reset_close_distances(index)
        if len(self._events) == 1:
            self._events[0].distance_to_last = np.nan

    def _reset_close_distances(self, index):
        if index == 0:
            self._events[index].distance_to_last = np.nan
        else:
            prev, this = self._events[index - 1], self._events[index]
            this.distance_to_last = (this.date - prev.date).days


class EventStatistics:

    def __init__(self, event_list):
        self._list = event_list

    def mean(self, attribute, lag=0):
        return np.mean([getattr(e.price_data, attribute)(lag)
                        for e in self._list])

    def standard_deviation(self, attribute, lag=0):
        return np.std([getattr(e.price_data, attribute)(lag)
                       for e in self._list])

    def median(self, attribute, lag=0):
        return np.median([getattr(e.price_data, attribute)(lag)
                          for e in self._list])

    def mean_over_cumulative_values(self, attribute, lag=5):
        values = list(self._cumulative_values(attribute, lag).values())
        return np.mean(values)

    def standard_deviation_over_cumulative_values(self, attribute, lag=5):
        values = list(self._cumulative_values(attribute, lag).values())
        return np.std(values)

    def median_over_cumulative_values(self, attribute, lag=5):
        values = list(self._cumulative_values(attribute, lag).values())
        return np.median(values)

    def _cumulative_values(self, attribute, lag=5):
        return {k: np.sum(v) for k, v in self._series(attribute, lag).items()}

    def _series(self, attribute, lag=5):
        return {(e.entity_id, e.date): e.price_data.series(attribute, lag)
                for e in self._list}
