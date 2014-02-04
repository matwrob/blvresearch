from itertools import chain
import pandas as pd

from concat.core.utils import load_object


start = lambda x: str(x) + "-01-01"
end = lambda x: str(x) + "-12-31"


def split_entities_on_zone(dict_of_universes):
    ZONES = ['am', 'eu', 'ap']
    result = {z: list() for z in ZONES}
    for k, v in dict_of_universes.items():
        for z in ZONES:
            result[z].extend(list(v.filter("zone", z).keys()))
    return {k: list(set(v)) for k, v in result.items()}


UNI = load_object('dict_of_uni.pickle')
ENTITIES_BY_ZONE = split_entities_on_zone(UNI)

SECTORS = ['1100',  # Non-Energy Minerals
           '1200',  # Producer Manufacturing
           '1300',  # Electronic Technology
           '1400',  # Consumer Durables
           '2100',  # Energy Minerals
           '2200',  # Process Industries
           '2300',  # Health Technology
           '2400',  # Consumer Non-Durables
           '3100',  # Industrial Services
           '3200',  # Commercial Services
           '3250',  # Distribution Services
           '3300',  # Technology Services
           '3350',  # Health Services
           '3400',  # Consumer Services
           '3500',  # Retail Trade
           '4600',  # Transportation
           '4700',  # Utilities
           '4800',  # Finance
           '4900',  # Communications
           '6000',  # Miscellaneous
           '7000',  # Government
           '9999']  # Not Classified
