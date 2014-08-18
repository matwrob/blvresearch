from memnews.nlp.numbernorm import (
    Normalizer, Currency, MutableString, Prefix, Suffix
)


def normalize_line(string):
    norm = ResearchStringNormalizer(string, 'en')
    result = norm.run()
    return result.strip()


class ResearchStringNormalizer(Normalizer):

    def _activate_number_case(self, number_index):
        self.number_index = number_index
        self.this_prefix = Prefix(self.this_prefixstr)
        self.this_suffix = Suffix(self.this_suffixstr)
        self.this_number = Number(self.this_numberstr)


class Number(MutableString):
    "the number string. Gets normalized"
    def __init__(self, string):
        super().__init__(string)
