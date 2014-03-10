import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats

from blvworker.news.important_days import _get_mean_and_sigma
from blvresearch.core.es import Event
from concat.core.news import NewsList


def mean_test(event_list, attribute, length):
    series = [e.concat_data.series_after(attribute, lag=2, length=length)
              for e in event_list]
    returns = [s.sum() for s in series]
    print('Mean:', np.mean(returns))
    # t-test
    # null hypothesis: expected value = 0
    t_statistic, p_value = stats.ttest_1samp(returns, 0)
    print('p_value:', p_value)


class NewsEvent(Event):
    DISTANCE_THRESH = 30

    @property
    def _event_day_alpha(self):
        return self.concat_data.series_after('alpha', lag=0, length=1)[0]

    @property
    def _event_day_news_amount(self):
        news_list = self.concat_data.series_after('news', lag=0, length=1)[0]
        return self._get_news_list_len(news_list)

    def _is_negative(self):
        return self._event_day_alpha < 0

    def _is_positive(self):
        return self._event_day_alpha > 0

    def _alpha_greater_than_2pct(self):
        return self._event_day_alpha > 0.02

    def _alpha_smaller_than_minus_2pct(self):
        return self._event_day_alpha < -0.02

    def _alpha_smaller_than_minus_4pct(self):
        return self._event_day_alpha < -0.04

    def _absolute_alpha_greater_than_2pct(self):
        return abs(self._event_day_alpha) > 0.02

    def _has_many_news(self):
        mean, sigma = self._get_news_length_moments()
        return self._event_day_news_amount > mean + 2 * sigma

    def _has_no_news(self):
        mean, sigma = self._get_news_length_moments()
        return self._event_day_news_amount < mean

    def _get_news_length_moments(self):
        news = self.concat_data._data['news']
        news_len = news.map(self._get_news_list_len)
        return _get_mean_and_sigma(news_len)

    def _get_news_list_len(self, news_list):
        if not isinstance(news_list, NewsList):
            return 0
        return len(news_list)


def plot_histogram_of_alphas(event_list):
    attribute, length = 'alpha', 20
    series = [e.concat_data.series_after(attribute, lag=2, length=length)
              for e in event_list]
    returns = [s.sum() for s in series]
    plt.hist(returns, bins=50, normed=True, alpha=0.6, color='g')
    xmin, xmax = plt.xlim()
    x = np.linspace(xmin, xmax, 100)
    mu, std = stats.norm.fit(returns)
    p = stats.norm.pdf(x, mu, std)
    plt.plot(x, p, 'k', linewidth=2)
    title = "Fit results: mu = %.2f,  std = %.2f" % (mu, std)
    plt.title(title)


class ManyNewsAlphaGreaterThan2pct(NewsEvent):
    def triggers(self):
        if self.distance_to_last < self.DISTANCE_THRESH:
            return False
        if self._has_many_news() and self._alpha_greater_than_2pct():
            return True
        return False


class ManyNewsAlphaSmallerThanMinus2pct(NewsEvent):
    def triggers(self):
        if self.distance_to_last < self.DISTANCE_THRESH:
            return False
        if self._has_many_news() and self._alpha_smaller_than_minus_2pct():
            return True
        return False


class NoNewsAlphaGreaterThan2pct(NewsEvent):
    def triggers(self):
        if self.distance_to_last < self.DISTANCE_THRESH:
            return False
        if self._has_no_news() and self._alpha_greater_than_2pct():
            return True
        return False


class NoNewsAlphaSmallerThanMinus2pct(NewsEvent):
    def triggers(self):
        if self.distance_to_last < self.DISTANCE_THRESH:
            return False
        if self._has_no_news() and self._alpha_smaller_than_minus_2pct():
            return True
        return False


class NoNewsAlphaSmallerThanMinus4pct(NewsEvent):
    def triggers(self):
        if self.distance_to_last < self.DISTANCE_THRESH:
            return False
        if self._has_no_news() and self._alpha_smaller_than_minus_4pct():
            return True
        return False
