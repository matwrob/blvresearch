from dateutil.relativedelta import relativedelta
import datetime as dt

from concat_overlord.universes.standard import new_universe
from fsprices.universe import get_research_universe, Universe, Security
from fsprices.raw_prices import exec_and_group


TODAY = dt.datetime.today()
START =  TODAY - relativedelta(years=1)


def get():
    """returns dict with keys being factset_entity_ids and values being lists
    of factset_entity_ids representing closest peers"""
    funi = new_universe()
    runi = get_research_universe(TODAY.year)
    countries = list(set([s.country for s in funi]))
    country_bench = _get_country_benchmarks(runi, countries)
    returns = _get_return_data(country_bench, funi)
    res = {}
    for sec in funi:
        res[sec] = _find_closest_peers(sec, country_bench[sec.country])
    return res



def _get_country_benchmarks(runi, list_of_countries):
    by_country = dict(iter(runi.groupby('country')))
    res = {country: list() for country in list_of_countries}
    for country in list_of_countries:
        secs = by_country[country]
        secs = secs.sort(columns='market_cap', ascending=False)[:30]
        res[country] = [Security(row) for i, row in secs.iterrows()]
    return res


def _find_closest_peers(security, list_of_securities, returns):



def _get_return_data(dict_of_secs, funi):
    s = START.strftime("%Y-%m-%d")
    e = TODAY.strftime("%Y-%m-%d")
    secs = list(chain.from_iterable(dict_of_secs.values()))
    secs.extend([s for s in funi if s not in secs])
    entities = [s.factset_entity_id for s in secs]
    return _get_alphas(entities, s, e)


def _get_alphas(entity_ids, start, end):
    query = """SELECT risk_relative_return
               FROM return_data
               WHERE DATE > %s
               AND DATE <= %s
               AND factset_entity_id = ANY(%s)"""
    values = "('" + "', '".join(entity_ids) + "')"
    data = NEWSDB.execute(query, (start, end, values))
    result = data.fetchall()
    return pd.DataFrame(result, columns=data.keys())
