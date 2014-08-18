from collections import namedtuple
import re

from blvresearch.concat.analysts.reuters.normalizer import (
    normalize_line
)
from memnews.entity_security_transl import (
    ric_entity_transl
)


TRANSL = ric_entity_transl()

ACTIONS = [r"cuts?", r"raises?", r"starts?", r"\bups?", r"rates?",
           r"(down|up)grades?", r"resumes?", r"(re)?-?initiates?",
           r"reinstates?", r"lowers?", r"adjusts?", r"revises?",
           r"establish(es)?", r"assumes?", r"maintains?"]
ACTIONS = "(%s)" % r"|".join(ACTIONS)
RATINGS = [r"buy", r"hold", r"sell", r"neutral", r"positive", r"negative",
           r"reduce", r"add", r"accumulate",
           r"over(-*|\s)weight",
           r"under(-*|\s)weight",
           r"equal(-*|\s)weight",
           r"out(-*|\s)perform(er)?",
           r"over(-*|\s)perform(er)?",
           r"under(-*|\s)perform(er)?",
           r"sector(-*|\s)(out|under)?perform(er)?",
           r"market(-*|\s)(out|under)?perform(er)?",
           r"in(-*|\s)line",
           r"top(-*|\s)pick",
           r"conviction(-*|\s)buy(-*|\s)list",
           r"fair(-*|\s)value"]
RATINGS = "(%s)" % r"|".join(RATINGS)
PTARGET = r"((target|price|objective) )+"
TO_FROM = r"(to|from|previous|with|at)"
NUMBER = r"[0-9]+(\.|\,)?[0-9\,\'\.]*"
CURRENCY = ['AUD', 'BAM', 'BRL', 'CAD', 'CHF', 'CNY', 'CZK', 'DKK',
            'EUR', 'GBP', 'HKD', 'IDR', 'ILS', 'INR', 'JPY', 'KRW',
            'MYR', 'MXN', 'NGN', 'NOK', 'NZD', 'PLN', 'RUB', 'SEK',
            'SGD', 'THB', 'TRY', 'TWD', 'USD', 'ZAR']
CURRENCY = "(%s)" % r"|".join(CURRENCY)
TICKER = r"\<[^\>]*\>|\[[^\]]*\]"


def is_research_line(string):
    crit0 = string.strip().startswith("*")
    crit1 = _has_actions(string) and _has_ratings(string)
    crit2 = _has_actions(string) and _has_prices(string)
    crit3 = _has_price_target(string) and _has_prices(string)
    if crit0 and (crit1 or crit2 or crit3):
        return True
    return False


def _has_actions(string):
    regex = re.compile(ACTIONS + " " + TO_FROM, re.I)
    if regex.search(string):
        return True
    return False


def _has_ratings(string):
    regex = re.compile(RATINGS, re.I)
    if regex.search(string):
        return True
    return False


def _has_prices(string):
    regex = re.compile(CURRENCY + " " + NUMBER, re.I)
    if regex.search(string):
        return True
    return False


def _has_price_target(string):
    regex = re.compile(PTARGET, re.I)
    if regex.search(string):
        return True
    return False


class Price:

    def __init__(self, currency, nominal):
        self.currency = currency
        self.nominal = nominal

    def __repr__(self):
        if self.currency and self.nominal:
            return self.currency + " " + str(self.nominal)
        else:
            return "N/A"

    def __bool__(self):
        if self.currency and self.nominal:
            return True
        return False

    def __str__(self):
        return repr(self)

    def __eq__(self, other_price):
        c1 = self.currency == other_price.currency
        c2 = self.nominal == other_price.nominal
        if c1 and c2:
            return True
        return False


class ResearchLine:

    def __init__(self, string):
        self.s = normalize_line(string)
        self.analyzed_entity = None
        self.analysts_house = None
        self.new_price_target = Price(None, None)
        self.old_price_target = Price(None, None)

    def __repr__(self):
        ah = self.analysts_house
        ae = self.analyzed_entity
        npt = self.new_price_target
        opt = self.old_price_target
        return "%s: %s recommends %s ---> %s" % (ah, ae, opt, npt)

    def __str__(self):
        return repr(self)

    def __eq__(self, other_line):
        attri = ['analyzed_entity', 'analysts_house',
                 'new_price_target', 'old_price_target']
        for a in attri:
            if getattr(self, a) != getattr(other_line, a):
                return False
        return True

    def find_info(self):
        self._find_analyzed_entity()
        self._find_analysts_house()
        self._find_prices()

    def _find_analyzed_entity(self):
        if ":" in self.s:
            parts = self.s.split(":")
            ticker = re.compile(TICKER)
            candidate = parts[0].split()[-1].strip()
            match = ticker.match(candidate)
            if match:
                ric = match.group()[1:-1]
                entity = TRANSL.flipget(ric)
                if entity:
                    self.analyzed_entity = entity
                self.s = parts[1].strip()

    def _find_analysts_house(self):
        regex = re.compile(ACTIONS, re.I)
        parts = regex.split(self.s)
        result = parts[0].strip().lstrip('*').strip()
        if result:
            self.analysts_house = result

    def _find_prices(self):
        result = get_price_actions(self.s)
        if result:
            self._determine_time(result)

    def _determine_time(self, list_of_strings):
        for s in list_of_strings:
            if "to" in s.lower() or re.search(PTARGET, s, re.I):
                self.new_price_target = get_price(s)
            elif "from" in s.lower() or "previous" in s:
                self.old_price_target = get_price(s)

    @property
    def has_price_target(self):
        if self.new_price_target:
            return True
        return False


def get_price(string):
    nominal = re.search(NUMBER, string).group()
    nominal = translate_string_to_float(nominal)
    currency = re.search(CURRENCY, string).group()
    return Price(currency, nominal)


def translate_string_to_float(string):
    if "," in string and not "." in string:
        if len(string.split(",")[1]) <= 2:
            string = string.replace(",", ".")
        else:
            string = string.replace(",", "")
    if "," in string and "." in string:
        string = string.replace(",", "")
    string = string.strip("'")
    return float(string)


def get_price_actions(string):
    RE1 = TO_FROM + " " + CURRENCY + " " + NUMBER
    RE2 = PTARGET + r"(of )?" + CURRENCY + " " + NUMBER
    RE3 = CURRENCY + " " + NUMBER + " " + PTARGET
    regex = RE1 + r"|" + RE2 + r"|" + RE3
    regex = re.compile(regex, re.I)
    result = list()
    for match in regex.finditer(string):
        result.append(match.group().strip())
    return result
