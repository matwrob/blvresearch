import pandas as pd


class Event:

    def __init__(self, entity_id, date):
        self.entity_id = entity_id
        self.date = date

    def sreturn(self, lag=0):




def find_events(data_structure, list_of_functions):
    for f in list_of_functions:
        data_structure = f(data_structure)
    return data_structure


class EventStudy:
    """
    df_of_events = dataframe of booleans indexed by time with columns being
                   certain entities (firms/industries/countries)
    df_of_effects = dataframe of values we check for event effect,
                    e.g. absolute returns

    .map_events_on_returns: returns dataframe with values given only for cells
                            of df_of_events containing True; providing lag
                            shifts those cells forward/backward to check
                            effect next/previous N periods

    """
    def __init__(self, df_of_events, df_of_effects):
        self.events = df_of_events
        self.effects = df_of_effects

    def map_events_on_returns(self, lag=0):
        result = pd.DataFrame(index=self.effects.index,
                              columns=self.effects.columns)
        for k, series in self.events.items():
            series = series.shift(lag).fillna(value=False)
            result[k] = self.effects[k][series]
        return result


class SeriesSummaryStatistics:

    def __init__(self, series, freq='M'):
        self.s = series

    @property
    def mean(self):
        return self.s.mean()

    @property
    def standard_deviation(self):
        return self.s.std()

    @property
    def skeweness(self):
        return self.s.skew()

    @property
    def kurtosis(self):
        return self.s.kurt()

    def autocorrelation(self, lag):
        return self.s.corr(self.d.shift(-lag))
