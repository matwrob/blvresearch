import pandas as pd
import math

from blvresearch.core.event_study import Event
from memnews import NewsList


class NewsEvent(Event):
    DISTANCE_THRESH = 20  # business days

    def alpha_is_greater_than(self, pct):
        return self._event_day_alpha > pct

    def alpha_is_smaller_than(self, pct):
        return self._event_day_alpha < pct

    def absolute_alpha_is_greater_than(self, pct):
        return abs(self._event_day_alpha) > pct

    def absolute_alpha_is_smaller_than(self, pct):
        return abs(self._event_day_alpha) < pct

    @property
    def alpha_is_greater_than_miu_plus_2_sigmas(self):
        mean = self.additional_data['alpha_miu']
        sigma = self.additional_data['alpha_sigma']
        return self._event_day_alpha > mean + 2 * sigma

    @property
    def alpha_is_smaller_than_miu_minus_2_sigmas(self):
        mean = self.additional_data['alpha_miu']
        sigma = self.additional_data['alpha_sigma']
        return self._event_day_alpha < mean - 2 * sigma

    @property
    def alpha_is_smaller_than_miu_minus_sigma(self):
        mean = self.additional_data['alpha_miu']
        sigma = self.additional_data['alpha_sigma']
        return self._event_day_alpha < mean - sigma

    @property
    def alpha_is_greater_than_miu_minus_2_sigmas(self):
        mean, sigma = self._get_alpha_moments()
        return self._event_day_alpha > mean - 2 * sigma

    @property
    def has_relevant_news(self):
        nl = self.concat_data.series_after('news', lag=0, length=1)[0]
        result = [n for n in nl if n.relevance[self.entity_id]['score'] > 0.3]
        return bool(result)

    @property
    def has_many_news(self):
        mean = self.additional_data['news_count_miu']
        sigma = self.additional_data['news_count_sigma']
        return self._event_day_news_amount > mean + 2 * sigma

    @property
    def has_more_news(self):
        mean = self.additional_data['news_count_miu']
        sigma = self.additional_data['news_count_sigma']
        return self._event_day_news_amount > mean + sigma

    @property
    def has_some_news(self):
        mean = self.additional_data['news_count_miu']
        sigma = self.additional_data['news_count_sigma']
        return self._event_day_news_amount > mean

    @property
    def has_few_news(self):
        mean = self.additional_data['news_count_miu']
        sigma = self.additional_data['news_count_sigma']
        return self._event_day_news_amount < mean

    @property
    def has_no_news(self):
        return self._event_day_news_amount == 0

    @classmethod
    def _calculate_additional_data(cls, data):
        res = dict()
        res['alpha_miu'], res['alpha_sigma'] = cls._get_alpha_moments(data)
        res['news_count_miu'], res['news_count_sigma'] = (
            cls._get_news_count_moments(data)
        )
        return res

    @classmethod
    def _get_alpha_moments(cls, data):
        # year = self.date.year
        # start, end = pd.datetime(year, 1, 1), pd.datetime(year, 12, 31)
        # val = self.concat_data._data['alpha'][start:end]
        val = data['alpha']
        mean = val.mean()
        sigma = 0 if math.isnan(val.std()) else val.std()
        return mean, sigma

    @classmethod
    def _get_news_count_moments(cls, data):
        # year = self.date.year
        # start, end = pd.datetime(year, 1, 1), pd.datetime(year, 12, 31)
        # news = self.concat_data._data['news'][start:end]
        news = data['news']
        val = news.map(cls._get_news_list_len)
        val = val[val > 0]
        mean = val.mean()
        sigma = 0 if math.isnan(val.std()) else val.std()
        return mean, sigma

    @classmethod
    def _get_news_list_len(cls, news_list):
        if not isinstance(news_list, NewsList):
            return 0
        return len(news_list)

    @property
    def _event_day_alpha(self):
        return self.concat_data.series_after('alpha', lag=0, length=1)[0]

    @property
    def _event_day_news_amount(self):
        news_list = self.concat_data.series_after('news', lag=0, length=1)[0]
        return self._get_news_list_len(news_list)
