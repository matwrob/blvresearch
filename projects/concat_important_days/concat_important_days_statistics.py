import pandas as pd

from blvworker.news.important_days import _values_to_scores
from blvresearch.core.es import EntityEventGenerator

from concat.core.news import NewsList


class BusyNewsDays(EntityEventGenerator):

    def _find_dates(self, data):
        def func(x):
            if isinstance(x, NewsList):
                return len(x)
            return 0
        news = data['news']
        news = {g[0]: g[1] for g in news.groupby(news.index.year)}
        result = list()
        for year, series in news.items():
            series = series.map(func)
            series = _values_to_scores(series)
            result.append(series)
        result = pd.concat(result)
        return result[result == 2].index
