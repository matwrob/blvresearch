import pandas as pd

from fsprices.topcountry_model import get_many
from fsprices.universe import get_research_universe, Security
from memnews.core import NewsList

from blvutils.gentypes import FlipDict
from blvutils.redishelpers import StringNamespace
from concat_overlord.dbpools import NEWSDB
from collections import Counter

from memnews.entity_security_transl import (
    ric_entity_transl, isin_entity_transl
)

def get_research_data_by_entity(entity_ids, criteria_func,
                                start_date, end_date):
    year = int(start_date[:4])
    universe = get_research_universe(year)
    daycount = entity_daycounts()
    secs = [Security(v) for k, v in universe.iterrows()
            if v['factset_entity_id'] in entity_ids
            and criteria_func(v)
            and daycount[k] > 12]
    return _get_prices_and_news(secs, start_date, end_date)


def get_research_data_by_country(list_of_countries, criteria_func,
                                 start_date, end_date):
    year = int(start_date[:4])
    universe = get_research_universe(year)
    daycount = entity_daycounts()
    secs = [Security(v) for k, v in universe.iterrows()
            if v['country'] in list_of_countries
            and criteria_func(v)
            and daycount[v['factset_entity_id']] > 12]
    return _get_prices_and_news(secs, start_date, end_date)


def _get_prices_and_news(securities, start_date, end_date):
    prices = get_many(securities, start_date, end_date)
    news = NewsList.get_by_entity([s.factset_entity_id for s in securities],
                                  start_date, end_date)
    news = news.split_by_entity()
    return _join_prices_and_news(prices, news)


def _join_prices_and_news(prices, news):
    result = dict()
    for sec, price_data in prices.items():
        if sec.factset_entity_id in news.keys():
            date_index = sec.exchangeobj.add_exact_time(price_data.index)
            price_data.index = date_index
            n = news[sec.factset_entity_id]
            n = n.align_to_date_index(date_index)
            if len(n) > 0:
                result[sec.factset_entity_id] = price_data.join(n)
    return result


def entity_daycounts():
    res = Counter()
    add_reuters_counts(res)
    add_awp_counts(res)
    return res


def add_reuters_counts(res):
    transl = ric_entity_transl()
    for ric, count in get_ric_daycounts().items():
        entity = transl.flipget(ric)
        if entity and res.get(entity, 0) < count:
            res[entity] += count


def add_awp_counts(res):
    transl = isin_entity_transl()
    for isin, count in get_awp_daycounts().items():
        entity = transl.flipget(isin)
        if entity:
            res[entity] += count


def get_ric_daycounts():
    query = """
            SELECT ric, count(ric) as count FROM (
                SELECT
                    DISTINCT story_time::DATE as date, unnest(rics) as ric
                FROM reuters_story
                WHERE story_time > %s
            ) as r
            GROUP BY ric
            HAVING count(ric) > 10
            """
    return {r['ric']: r['count']
            for r in NEWSDB.execute(query, ('2011-01-01',))
            if '.' in r['ric'] and r['ric'][0] != '.'}


def get_awp_daycounts():
    query = """
            SELECT isin, count(isin) as count FROM (
                SELECT
                    DISTINCT story_time::DATE as date, unnest(isins) as isin
                FROM awp_story
                WHERE story_time > %s
            ) as r
            GROUP BY isin
            HAVING count(isin) > 4
            """
    return {r['isin']: r['count']
            for r in NEWSDB.execute(query, (pd.datetime(2011, 1, 1),))}


def redis():
    return StringNamespace('memnews:entity_security_transl')
