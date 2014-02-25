import datetime

from concat.core.prices import PriceData
from concat.core.universe import SecurityUniverse
from concat.core.universegen import build_universe, db


def get_universe_by_entity_id(list_of_entity_ids, start_date, end_date):
    potentials = SecurityUniverse(db.potential_securities())
    pot_sec = [k for k, v in potentials.items()
               if v.factset_entity_id in list_of_entity_ids]
    pot_univ = SecurityUniverse(pot_sec)
    data = PriceData(pot_univ, start_date, end_date,
                     in_currency='EUR', news=False)
    return build_universe(data, pot_univ)


def int2datetime(proper_int):
    return datetime.datetime.strptime(str(proper_int), "%Y%m%d")


start = lambda x: str(x) + "-01-01"
end = lambda x: str(x) + "-12-31"


def split_entities_by_zone(dict_of_universes):
    ZONES = ['am', 'eu', 'ap']
    result = {z: list() for z in ZONES}
    for k, v in dict_of_universes.items():
        for z in ZONES:
            result[z].extend(list(v.filter("zone", z).keys()))
    return {k: list(set(v)) for k, v in result.items()}


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
