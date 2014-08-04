from blvresearch.concat.signals.news_based.news_common_funcs import (
    get_days_to_check
)


from blvresearch.concat.signals.news_based.news_movavg import (
    get_news_movavg_signals, get_news_movavg_descr
)
from blvresearch.concat.signals.news_based.news5days import (
    get_news5days_signals, get_news5days_descr
)
from blvresearch.concat.signals.news_based.news3days import (
    get_news3days_signals, get_news3days_descr
)
from blvresearch.concat.signals.news_based.news1day import (
    get_news1day_signals, get_news1day_descr
)
from blvresearch.concat.signals.news_based.news_cmo import (
    get_news_cmo_signals, get_news_cmo_descr
)


from blvresearch.concat.signals.price_based.four_down_days import (
    get_4down_signals, get_4down_descr
)
from blvresearch.concat.signals.price_based.moving_average import (
    get_movavg_signals, get_movavg_descr
)
from blvresearch.concat.signals.price_based.cmo_signals import (
    get_cmo_signals, get_cmo_descr
)
from blvresearch.concat.signals.price_based.rsi_agita import (
    get_rsi_signals, get_rsi_descr
)
from blvresearch.concat.signals.price_based.dmac import (
    get_dmac_signals, get_dmac_descr
)


PRICE_BASED = {'movavg': get_movavg_signals,
               'dmac': get_dmac_signals,
               '4down': get_4down_signals,
               'rsi_agita': get_rsi_signals,
               'cmo': get_cmo_signals}

NEWS_BASED = {'news1day': get_news1day_signals,
              'news3days': get_news3days_signals,
              'news5days': get_news5days_signals,
              'news_cmo': get_news_cmo_signals,
              'news_movavg': get_news_movavg_signals}


def get_entity_signals(entity_data):
    days_to_check, first_loc, last_loc = get_days_to_check(entity_data)
    result = dict()
    for name, func in PRICE_BASED.items():
        result[name] = func(entity_data)
    for name, func in NEWS_BASED.items():
        result[name] = func(days_to_check, entity_data, first_loc, last_loc)
    return result
