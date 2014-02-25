from blvworker.news.important_days import _values_to_scores
from concat.core.universe import Universe
from concat.core.benchmark_model import BenchmarkModelData
from concat.core.news import NewsList
from blvresearch.core.es import EventGenerator


u = Universe(['R85KLC-S-US'])
start = '2013-01-01'
end = '2013-12-31'
DATA = BenchmarkModelData(u, start, end, in_currency='USD', news=True)


class BusyNewsDaysEvents(EventGenerator):

    def _find_dates(self, data):
        news = data['news']
        news_len = news.map(lambda x: len(x) if isinstance(x, NewsList) else 0)
        scores = _values_to_scores(news_len)
        return list(scores[scores == 2].index)
