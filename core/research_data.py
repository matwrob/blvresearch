import pandas as pd

from fsprices.topcountry_model import get_many
from fsprices.universe import Universe
from memnews.core import NewsList


def get_research_data(entity_ids, start_date, end_date):
    year = int(start_date[:4])
    securities = _get_securities(entity_ids, year)
    prices = get_many(securities, start_date, end_date)
    news = NewsList.get_by_entity(entity_ids, start_date, end_date)
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


def _get_securities(entity_ids, year):
    runi = Universe.research(year)
    return [s for s in runi if s.factset_entity_id in entity_ids]
