import pandas as pd
import numpy as np
from itertools import chain

from concat.core.utils import load_object

# from blvresearch.core.utils import get_universe_by_entity_id, start, end
# from blvresearch.core.SP500output import ENTITIES_SP560
# from concat.core.benchmark_model import BenchmarkModelData
# UNI = {y: get_universe_by_entity_id(ENTITIES_SP560, start(y), end(y))
#        for y in RESEARCH_YEARS}
# DATA = {k: BenchmarkModelData(v, start(k), end(k),
#                               in_currency='USD', news=True)
#         for k, v in UNI.items()}
RESEARCH_YEARS = [2011, 2012, 2013]
UNI = load_object('uni_sp500_2011_2013.pickle')
DATA = load_object('bmd_sp500_2011_2013.pickle')


def find_events(list_of_entities, entity_event_generator):  # pragma: no cover
    result = dict()
    for entity_id in list_of_entities:
        eeg = EntityEventGenerator(entity_id)
        result[entity_id] = eeg.generate()
    return result


class EntityEventGenerator:  # pragma: no cover

    def __init__(self, entity_id):
        self.entity_id = entity_id

    def generate(self):
        dates = self._find_dates(self.data)
        result = [Event(self.entity_id, date) for date in dates]
        return EventList(result)

    @property
    def data(self):
        return pd.concat([DATA[y][self.entity_id] for y in RESEARCH_YEARS])

    def _find_dates(self, data):
        raise NotImplementedError


class Event:

    def __init__(self, entity_id, date):
        self.entity_id = entity_id
        self.date = date

    def __str__(self):
        return 'Event for "%s" on %s' % (self.entity_id,
                                         self.date.strftime("%Y-%m-%d"))

    def __repr__(self):
        return str(self)

    @property
    def meta_data(self):
        return UNI[self.date.year][self.entity_id]

    @property
    def price_data(self):
        data = pd.concat([DATA[y][self.entity_id] for y in RESEARCH_YEARS])
        return EventPriceData(data, self.date)


class EventPriceData:

    def __init__(self, data, date):
        self._data = data
        self._date = date

    @property
    def _position(self):
        "gives event day position in data index"
        return self._data.index.get_loc(self._date)

    def abs_ret(self, lag=0):
        self._validate_date(lag)
        return self._data['abs_ret'][self._position + lag]

    def alpha(self, lag=0):
        self._validate_date(lag)
        return self._data['alpha'][self._position + lag]

    def rel_ret(self, lag=0):
        self._validate_date(lag)
        return self._data['rel_ret'][self._position + lag]

    def bench(self, lag=0):
        self._validate_date(lag)
        return self._data['bench'][self._position + lag]

    def beta(self, lag=0):
        self._validate_date(lag)
        return self._data['beta'][self._position + lag]

    def r2(self, lag=0):
        self._validate_date(lag)
        return self._data['r2'][self._position + lag]

    def series(self, attribute, lag=5):
        self._validate_date(lag)
        start, end = self._get_intervals_start_end(lag)
        return self._data[attribute][start:end]

    def _get_intervals_start_end(self, lag):
        s = self._position + 1 if lag > 0 else self._position
        return min(s, s + lag), max(s, s + lag)

    def _validate_date(self, lag):
        if self._position + lag < 0:
            raise ValueError('Date lag outside total date scope')


class EventList:

    def __init__(self, list_of_events):
        self._events = list_of_events

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

    def filter(self, attribute, value):
        if attribute in ['blvindustry', 'country', 'exchange', 'geounit',
                         'industry', 'sector', 'zone']:
            tmp = [e for e in self if getattr(e.meta_data, attribute) == value]
            return EventList(tmp)
        raise AttributeError

    def split_by_date(self):
        result = {event.date: [] for event in self._events}
        [result[event.date].append(event) for event in self._events]
        return {k: EventList(v) for k, v in result.items()}

    def split_by_entity(self):
        result = {event.entity_id: [] for event in self._events}
        [result[event.entity_id].append(event) for event in self._events]
        return {k: EventList(v) for k, v in result.items()}

    def _to_series_of_event_lists(self):
        return pd.Series(data=self.split_by_date(),
                         index=self._date_index,
                         name='event_lists')

    def _to_dataframe_of_events(self):
        by_entity = self.split_by_entity()
        data = {k: pd.Series(data={event.date: event for event in v},
                             index=self._date_index)
                for k, v in by_entity.items()}
        return pd.DataFrame(data=data,
                            index=self._date_index)

    @property
    def _date_index(self):
        all_dates = [e.date for e in self]
        start, end = min(all_dates), max(all_dates)
        return pd.date_range(start, end, freq='B')

    @classmethod
    def _from_list_of_lists(cls, list_of_lists):
        tmp = chain.from_iterable(list_of_lists)
        return cls(list(tmp))

    @classmethod
    def _from_dict(cls, dict_of_lists):
        tmp = chain.from_iterable(dict_of_lists.values())
        return cls(list(tmp))


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
