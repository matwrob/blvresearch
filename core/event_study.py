import pandas as pd
import re


class EventDetector:

    def __init__(self, event_class):
        self.event = event_class

    def run(self, entity_id, entity_data, entity_meta):
        el = self._create_initial_list(entity_id, entity_data, entity_meta)
        result = EventList()
        for event in el:
            if event.triggers():
                result.append_event(event)
        return result

    def _create_initial_list(self, entity_id, entity_data, entity_meta):
        el = EventList()
        for d in entity_data.index:
            e = self.event(entity_id, entity_data, entity_meta, d, el)
            el.append_event(e)
        return el


class Event:

    def __init__(self, entity_id, entity_price_data, entity_meta_data, date,
                 event_list):
        self.entity_id = entity_id
        self._data = entity_price_data
        self.meta_data = entity_meta_data
        self.date = date
        self._list = event_list

    def __str__(self):
        return 'Event for "%s" on %s' % (self.entity_id,
                                         self.date.strftime("%Y-%m-%d"))

    def __repr__(self):
        return str(self)

    def triggers(self):
        raise NotImplementedError

    @property
    def concat_data(self):
        return EventConcatData(self)


class CloseEvents:

    def __init__(self, event):
        self.ev = event

    def find_after(self, neighbour_class, days):
        last_day = self.ev.date + pd.tseries.offsets.BDay(days)
        tmp = [e for e in self.ev._list if self.ev.date < e.date <= last_day]
        result = self._matching_events(tmp, neighbour_class)
        return result

    def find_before(self, neighbour_class, days):
        first_day = self.ev.date - pd.tseries.offsets.BDay(days)
        tmp = [e for e in self.ev._list if first_day <= e.date < self.ev.date]
        result = self._matching_events(tmp, neighbour_class)
        return result

    def _matching_events(self, list_of_events, ncls):
        result = [ncls(e.entity_id, e._data, e.meta_data, e.date, e._list)
                  for e in list_of_events]
        return [e for e in result if e.triggers()]


class EventConcatData:

    def __init__(self, event):
        self._data = event._data
        self._date = event.date

    def series_after(self, attribute, lag=1, length=5):
        start = self._position + lag
        end = start + length
        if end > len(self._data[attribute]):
            return self._data[attribute][start:]
        return self._data[attribute][start:end]

    def series_before(self, attribute, lag=1, length=5):
        end = self._position - lag + 1
        start = end - length
        if start < 0:
            return self._data[attribute][:end]
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
        if len(event_list) > 0:
            self._events.extend(event_list._events)

    def remove_consecutive_events(self, business_days):
        dates = [e.date for e in self]
        result = [dates[0]]
        for d in dates[1:]:
            if d > result[-1] + pd.tseries.offsets.BDay(business_days):
                result.append(d)
        return self.from_list([e for e in self if e.date in result])

    @property
    def last(self):
        return self._events[len(self._events) - 1]

    @property
    def all_dates(self):
        result = list(set([e.date for e in self]))
        result.sort()
        return result

    @property
    def all_entities(self):
        return list(set([e.entity_id for e in self]))

    def to_series(self):
        result = pd.Series({e.date: e for e in self})
        result.reindex(self._date_index)
        return result

    def to_dataframe(self):
        by_entity = self.split_by_entity()
        tmp = {k: v.to_series() for k, v in by_entity.items()}
        result = pd.DataFrame(tmp)
        full_index = pd.date_range(start=self.all_dates[0],
                                   end=self.all_dates[-1],
                                   freq='B')
        return result.reindex(full_index)

    @classmethod
    def from_dict(cls, dict_of_event_lists):
        result = EventList()
        for k, v in dict_of_event_lists.items():
            result.extend(v)
        return result

    @classmethod
    def from_list(cls, list_of_events):
        result = EventList()
        for e in list_of_events:
            result.append_event(e)
        return result

    def split_by_date(self):
        result = dict()
        for e in self:
            tmp = result.get(e.date, EventList())
            tmp.append_event(e)
            result[e.date] = tmp
        return result

    def split_by_entity(self):
        result = dict()
        for e in self:
            tmp = result.get(e.entity_id, EventList())
            tmp.append_event(e)
            result[e.entity_id] = tmp
        return result

    @property
    def _date_index(self):
        all_dates = [e.date for e in self]
        start, end = min(all_dates), max(all_dates)
        return pd.date_range(start, end, freq='B')

    def remove_event(self, index):
        del self._events[index]


def get_common_events(event_list1, event_list2):
    by_entity1 = event_list1.split_by_entity()
    by_entity2 = event_list2.split_by_entity()
    result = EventList()
    for entity_id, events1 in by_entity1.items():
        if entity_id in by_entity2.keys():
            dates2 = [e.date for e in by_entity2[entity_id]]
            for e in events1:
                if e.date in dates2:
                    result.append_event(e)
    return result


def get_different_events(minuend_list, subtrahend_list):
    by_entity1 = minuend_list.split_by_entity()
    by_entity2 = subtrahend_list.split_by_entity()
    result = EventList()
    for entity_id, events1 in by_entity1.items():
        if entity_id in by_entity2.keys():
            dates2 = [e.date for e in by_entity2[entity_id]]
            for e in events1:
                if e.date not in dates2:
                    result.append_event(e)
        else:
            for e in events1:
                result.append_event(e)
    return result


def check_event_news_headlines(event, regex):
    news = event.concat_data.series_after('news', lag=0, length=1)[0]
    for n in news:
        if re.search(regex, n['clean_headline']):
            return True
    return False
