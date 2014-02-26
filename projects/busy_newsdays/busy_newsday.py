from blvworker.news.important_days import _get_mean_and_sigma
from concat.core.news import NewsList
from blvresearch.core.es import Event


class BusyNewsDay(Event):

    @property
    def triggers(self):
        def func(x):
            if not isinstance(x, NewsList):
                return 0
            return len(x)
        if self.distance_to_last < self.DISTANCE_THRESH:
            return False
        news = self.concat_data._data['news']
        news_len = news.map(func)
        mean, sigma = _get_mean_and_sigma(news_len)
        this_value = self.concat_data.series_after('news', lag=0, length=1)
        this_value = func(this_value)
        if this_value > mean + 2 * sigma:
            return True
        return False
