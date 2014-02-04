from collections import Counter
from itertools import chain

import pandas as pd

from concat.core.universe import SecurityUniverse
from concat.core.universegen import build_universe
from concat.core.prices import PriceData
from concat.core.utils import namespace


###############################################################################
###############################################################################
######################## UNIVERSE GENERATION CRITERIA #########################
###############################################################################
###############################################################################
# 0) "Fixed universe size" vs "Fixed news coverage"

# 1) News coverage
MIN_NEWS = 50            # the least amount of news per year per entity
# 2) Size (in USD)
VOLUME = 500             # median of daily volume (in thousands)
MARKET_CAP = 700000      # median of daily market cap (in thousands)
MIN_MARKET_CAP = 300000  # minimum daily market cap (in thousands)
MIN_MOVING_VOL = 350     # minimum daily volume MovMedian (in thousands)
# 3) Data coverage
MIN_TRADING_DAYS = 210   # minimum number of days stock was traded
###############################################################################
###############################################################################
###############################################################################
###############################################################################

INITIAL_UNIVERSE = SecurityUniverse(db.potential_securities())


def get_dict_of_yearly_universes(first_year, last_year):
    result = dict()
    for year in range(first_year, last_year + 1):
        print(year)
        result[year] = uni.get(start(year), end(year))
    return result


@namespace
class uni:

    def get(start_date, end_date):
        news_uni = uni._filter_on_news_coverage(start_date, end_date)
        data = PriceData(news_uni, start_date, end_date,
                         news=False, in_currency="USD")
        viable = list()
        for _id, _sec in news_uni.items():
            rc = ResearchContext(_sec, data[_id])
            if rc.is_valid() and uni._has_enough_data(data[_id]):
                viable.append(_sec.fs_perm_sec_id)
        return build_universe(data, SecurityUniverse(viable))

    def _filter_on_news_coverage(start_date, end_date):
        news_entities = db.get_news_entities(start_date, end_date)
        counter = Counter(chain.from_iterable(news_entities))
        securities = [_id for _id, _sec in INITIAL_UNIVERSE.items()
                      if counter[_sec.factset_entity_id] >= MIN_NEWS]
        return SecurityUniverse(securities)

    def _has_enough_data(dataframe):
        vol = dataframe.volume
        if len(vol[vol > 0]) >= MIN_TRADING_DAYS:
            return True
        return False


class ResearchContext:
    """contains all infos to determine if Security is valid for a research
    Universe.
    call is_valid() to find out
    """

    def __init__(self, security, price_frame):
        self.security = security
        self.price_frame = price_frame
        self.volume = (price_frame.close * price_frame.volume).fillna(0)
        self.market_cap = price_frame.close * price_frame.outstanding

    @property
    def no_price_data(self):
        return self.price_frame.empty

    @property
    def country(self):
        return self.security.country

    def is_valid(self):
        if self.no_price_data:
            return False
        if self.volume.median() <= VOLUME:
            return False
        if self.market_cap.median() <= MARKET_CAP:
            return False
        if self.market_cap.min() <= MIN_MARKET_CAP:
            return False
        min_mv = pd.rolling_median(self.volume, 20).min()
        if min_mv <= MIN_MOVING_VOL:
            return False
        return True
