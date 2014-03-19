import pandas as pd
import math

from blvresearch.core.event_study import Event
from concat.core.news import NewsList


class NewsEvent(Event):
    DISTANCE_THRESH = 20  # business days

    @property
    def alpha_is_negative(self):
        return self._event_day_alpha < 0

    @property
    def alpha_is_positive(self):
        return self._event_day_alpha > 0

    @property
    def alpha_is_greater_than_2pct(self):
        return self._event_day_alpha > 0.02

    @property
    def absolute_alpha_is_greater_than_2pct(self):
        return abs(self._event_day_alpha) > 0.02

    @property
    def alpha_is_smaller_than_minus_2pct(self):
        return self._event_day_alpha < -0.02

    @property
    def alpha_is_smaller_than_miu_minus_2_sigmas(self):
        mean, sigma = self._get_alpha_moments()
        return self._event_day_alpha < mean - 2 * sigma

    @property
    def alpha_is_smaller_than_miu_minus_sigma(self):
        mean, sigma = self._get_alpha_moments()
        return self._event_day_alpha < mean - sigma

    def has_relevant_news(self):
        nl = self.concat_data.series_after('news', lag=0, length=1)[0]
        result = [n for n in nl if n.relevance[self.entity_id]['score'] > 0.3]
        return bool(result)

    @property
    def has_many_news(self):
        mean, sigma = self._get_news_length_moments()
        return self._event_day_news_amount > mean + 2 * sigma

    @property
    def has_more_news(self):
        mean, sigma = self._get_news_length_moments()
        return self._event_day_news_amount > mean + sigma

    @property
    def has_some_news(self):
        mean, sigma = self._get_news_length_moments()
        return self._event_day_news_amount > mean

    @property
    def has_few_news(self):
        mean, sigma = self._get_news_length_moments()
        return self._event_day_news_amount < mean

    def _get_alpha_moments(self):
        year = self.date.year
        start, end = pd.datetime(year, 1, 1), pd.datetime(year, 12, 31)
        val = self.concat_data._data['alpha'][start:end]
        mean = val.mean()
        sigma = 0 if math.isnan(val.std()) else val.std()
        return mean, sigma

    def _get_news_length_moments(self):
        year = self.date.year
        start, end = pd.datetime(year, 1, 1), pd.datetime(year, 12, 31)
        news = self.concat_data._data['news'][start:end]
        val = news.map(self._get_news_list_len)
        val = val[val > 0]
        mean = val.mean()
        sigma = 0 if math.isnan(val.std()) else val.std()
        return mean, sigma

    def _get_news_list_len(self, news_list):
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
