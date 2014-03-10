import pandas as pd


class EventDetector:

    def __init__(self, event_class):
        self.event = event_class

    def run(self, entity_id, entity_data, entity_meta):
        eel = EventList()
        for d in entity_data.index:
            e = self.event(entity_id, entity_data, entity_meta, d, eel)
            if e.triggers():
                eel.append_event(e)
        return eel


class Event:

    DISTANCE_THRESH = 4

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


def find_events_after(event, neighbour_class, distance_thrsh):
    all_after = [e for e in event._list if e.date > event.date
                 and (e.date - event.date).days < distance_thrsh]
    new = [neighbour_class(e.entity_id, e._data, e.meta_data, e.date, e._list)
           for e in all_after]
    matching = [e for e in new if e.triggers()]
    return matching


def find_events_before(event, neighbour_class, distance_thrsh):
    """distance_thrsh is checked using calendar days"""
    all_before = [e for e in event._list if e.date < event.date
                  and (event.date - e.date).days < distance_thrsh]
    new = [neighbour_class(e.entity_id, e._data, e.meta_data, e.date, e._list)
           for e in all_before]
    matching = [e for e in new if e.triggers()]
    return matching


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
