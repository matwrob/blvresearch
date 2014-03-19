from fsprices.topcountry_model import get_many
from fsprices.universe import Universe
from memnews.core import NewsList


year_start = 2011
year_end = 2013
runi = Universe.research(year_end)

start_date = str(year_start) + "-01-01"
end_date = str(year_end) + "-12-31"

countries_eu = ['CH', 'DE', 'GB']
securities_eu  = [s for s in runi if s.country in countries_eu]
securities_us = [s for s in runi if s.country == 'US']
entities_eu = [s.factset_entity_id for s in securities_eu]
entities_us = [s.factset_entity_id for s in securities_us]

prices_eu = get_many(securities_eu, start_date, end_date)
prices_us = get_many(securities_us, start_date, end_date)
news_eu = NewsList.get_by_entity(entities_eu, start_date, end_date)
news_us = NewsList.get_by_entity(entities_us, start_date, end_date)
