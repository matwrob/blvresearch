from blvresearch.concat.signals.news_based.news_signals_strategy1 import (
    get_news1day_signals
)
from blvresearch.concat.signals.news_based.news_signals_strategy2 import (
    get_news3days_signals
)
from blvresearch.concat.signals.news_based.news_signals_strategy3 import (
    get_news5days_signals
)
from blvresearch.concat.signals.news_based.news_signals_strategy6 import (
    get_news_movavg_signals
)
from blvresearch.concat.signals.news_based.news_signals_strategy7 import (
    get_news_cmo_signals
)
from blvresearch.concat.signals.news_based.news_common_funcs import (
    get_days_to_check
)
from blvresearch.concat.signals.price_based.four_down_days import (
    get_4down_signals
)
from blvresearch.concat.signals.price_based.moving_average import (
    get_movavg_signals
)
from blvresearch.concat.signals.price_based.cmo_signals import (
    get_cmo_signals
)
from blvresearch.concat.signals.price_based.rsi_agita import (
    get_rsi_signals
)
from blvresearch.concat.signals.price_based.dmac import (
    get_dmac_signals
)


def get_entity_signals(entity_data):
    returns = entity_data['alpha']
    days_to_check, first_loc, last_loc = get_days_to_check(entity_data)

    result = dict()
    result['mov_avg'] = get_mov_avg_signals(
        entity_data, window=20, confirmation_window=5
    )
    result['dmac'] = get_dmac_signals(
        entity_data, long_window=20, short_window=10, confirmation_window=5
    )
    result['4down'] = get_4down_signals(
        entity_data, down_days=4, up_days=2
    )
    result['rsi_agita'] = get_rsi_agita_signals(
        entity_data, periods=14, buy_thrsh=35, sell_thrsh=55
    )
    result['cmo'] = get_cmo_signals(
        entity_data, periods=9
    )


    result['news_1day'] = get_news1_signals(days_to_check, returns,
                                            first_loc, last_loc)
    result['news_3days'] = get_news2_signals(days_to_check, returns,
                                             first_loc, last_loc)
    result['news_5days'] = get_news3_signals(days_to_check, returns,
                                             first_loc, last_loc)
    result['news_cmo'] = get_news6_signals(days_to_check, returns,
                                           first_loc, last_loc)
    result['news_mov_avg'] = get_news7_signals(days_to_check,
                                               cummulative_returns,
                                               first_loc, last_loc)
    return result
