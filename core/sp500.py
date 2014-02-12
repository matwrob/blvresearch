import pandas as pd

from blvworker.news.news_data import (
    _create_entity_lookup_dict, _invert_entity_transl
)


PATH_TO_CSV = 'blvresearch/extras/ticker_rics_sp500_2012.csv'
sp500 = pd.read_csv(PATH_TO_CSV)


entity_lookup = _create_entity_lookup_dict()
ric_to_entity = _invert_entity_transl(entity_lookup)


def get_SP500_ric_to_ent():
    result = dict()
    for ric in sp500.ric.dropna():
        result[ric] = ric_to_entity.get(ric)
    return pd.Series(result).dropna()


def get_SP500_tick_to_ric():
    result = sp500[['TICKER', 'ric']].dropna()
    result.index = result['TICKER']
    return result.drop('TICKER', axis=1)


def get_SP500_tick_to_ent():
    ric_to_ent = get_SP500_ric_to_ent()
    tick_to_ric = get_SP500_tick_to_ric()
    tick_to_ric['factset_entity_id'] = ""
    for ticker, row in tick_to_ric.iterrows():
        tick_to_ric['factset_entity_id'][ticker] = ric_to_ent.get(row['ric'])
    return tick_to_ric['factset_entity_id'].dropna()


tick_to_ent = get_SP500_tick_to_ent()

dupli_tickers = ['AGL', 'GAS', 'VIA', 'VIAB', 'PHA', 'PHM', 'EA', 'ERTS',
                 'JOY', 'JOYG', 'CMCSA', 'CMCSK', 'FPL', 'NEE', 'WFM', 'WFMI',
                 'NWS', 'NWSA']

tick_to_ent_no_dupli = tick_to_ent.drop(dupli_tickers).drop_duplicates()

"""
Ticker to Factset_Entity_Id is "N to 1" relation for the following entities:

TICKER
AGL       0012LR-E
GAS       0012LR-E
GAS       0012LR-E

TICKER
VIA       06BZ3S-E
VIA       06BZ3S-E
VIAB      06BZ3S-E

TICKER
PHA       000V2H-E
PHM       000V2H-E

TICKER
EA        000HZ5-E
ERTS      000HZ5-E

TICKER
JOY       000LH0-E
JOYG      000LH0-E

TICKER
CMCSA     05LL2F-E
CMCSK     05LL2F-E

TICKER
FPL       000KQ5-E
NEE       000KQ5-E

TICKER
WFM       000YWC-E
WFMI      000YWC-E

TICKER
NWS       001KWY-E
NWSA      001KWY-E
"""

ent_to_tick = {
    '0012LR-E': ['AGL', 'GAS'],
    '06BZ3S-E': ['VIA', 'VIAB'],
    '000V2H-E': ['PHA', 'PHM'],
    '000HZ5-E': ['EA', 'ERTS'],
    '000LH0-E': ['JOY', 'JOYG'],
    '05LL2F-E': ['CMCSA', 'CMCSK'],
    '000KQ5-E': ['FPL', 'NEE'],
    '000YWC-E': ['WFM', 'WFMI'],
    '001KWY-E': ['NWS', 'NWSA']
}
