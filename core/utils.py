import pandas as pd
import datetime

from concat.core.benchmark_model import BenchmarkModelData
from concat.core.prices import PriceData
from concat.core.universe import SecurityUniverse
from concat.core.universegen import build_universe, db


class UniverseByEntityIdGenerator:

    def __init__(self, start_date, end_date):
        self.start = start_date
        self.end = end_date

    def get(self, list_of_entities):
        pot_univ = self._potential_universe(list_of_entities)
        data = PriceData(pot_univ, self.start, self.end,
                         in_currency='USD', news=False)
        return build_universe(data, pot_univ)

    def _potential_universe(self, list_of_entities):
        potentials = SecurityUniverse(db.potential_securities())
        pot_sec = [k for k, v in potentials.items()
                   if v.factset_entity_id in list_of_entities]
        return SecurityUniverse(pot_sec)


class DataGetter:

    def __init__(self, start_date, end_date, entities):
        self.start = start_date
        self.end = end_date
        self.entities = entities

    def get(self):
        uni = self._get_potential_universe()
        data = BenchmarkModelData(uni, self.start, self.end,
                                  in_currency='USD', news=True)
        return self._create_df_from_collection(data)

    def _get_potential_universe(self):
        gen = UniverseByEntityIdGenerator(self.start, self.end)
        return gen.get(self.entities)

    def _create_df_from_collection(self, concat_collection):
        result = dict()
        for col in concat_collection.columns:
            df = concat_collection.matrix(col)
            df.name = col
            result[col] = self._to_multi_index(df)
        return pd.DataFrame(result)

    def _to_multi_index(self, output):
        output = output.stack()
        output = output.reorder_levels(order=[1, 0])
        return output


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
