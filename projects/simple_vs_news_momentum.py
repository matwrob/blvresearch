import pandas as pd

from blvresearch.core.portfolio import PortfolioStrategy, StockReturns
from blvworker.news.important_days import _values_to_scores
from concat.core.news import NewsList


class SimpleMomentum_1W_1W_4W(PortfolioStrategy):

    RANKING_PERIODS = 1
    PAUSE_PERIODS = 1
    HOLDING_PERIODS = 4
    REBALANCING_FREQUENCY = 'W'
    PORTFOLIO_SIZE = 30

    def _get_positions(self):
        returns = StockReturns(self.output).weekly
        result = dict()
        for day in self.rebalancing_days:
            temp = returns.loc[day].dropna()
            temp.sort()
            result[day] = temp.index[-self.PORTFOLIO_SIZE:]
        return pd.Series(result)


class RelevantNewsMomentum_1W_4W(SimpleMomentum_1W_1W_4W):

    def _get_positions(self):
        returns = StockReturns(self.output).weekly
        viable_entities = self._get_dataframe_of_relevance()
        result = dict()
        for day in self.rebalancing_days:
            temp = returns.loc[day].dropna()
            temp = temp[viable_entities.loc[day]]
            temp.sort()
            result[day] = temp.index[-self.PORTFOLIO_SIZE:]
        return pd.Series(result)

    def _get_dataframe_of_relevance(self):
        news = self.output['news']
        relevant_news = self._filter_function(news)
        result = relevant_news.resample(self.REBALANCING_FREQUENCY, how=sum)
        result = result.applymap(lambda x: x > 0)
        return result

    def _filter_function(self, dataframe):
        return self._filter_away_irrelevant_days(dataframe)

    def _filter_away_irrelevant_days(self, dataframe):
        def func(x):
            if isinstance(x, NewsList):
                return any([n['relevance'][k]['score'] > 0.3 for n in x])
            return False
        result = list()
        for k, v in dataframe.groupby(level=0):
            result.append(v.apply(func))
        result = pd.concat(result)
        return result.unstack(level=0)


class HeadlineNewsMomentum_1W_4W(RelevantNewsMomentum_1W_4W):

    def _filter_function(self, dataframe):
        return self._filter_away_days_without_headline_news(dataframe)

    def _filter_away_days_without_headline_news(self, dataframe):
        def func(x):
            if isinstance(x, NewsList):
                return any([k in n.headline_entities for n in x])
            return False
        result = list()
        for k, v in dataframe.groupby(level=0):
            result.append(v.apply(func))
        result = pd.concat(result)
        return result.unstack(level=0)


class ImportantNewsMomentum_1W_4W(SimpleMomentum_1W_1W_4W):

    def _filter_function(self, dataframe):
        return self._filter_away_unimportant_days(dataframe)

    def _filter_away_unimportant_days(self, dataframe):
        result = self._get_news_week_lengths(dataframe)
        scores = result.apply(_values_to_scores)
        return scores

    def _get_news_week_lengths(self, dataframe):
        result = dataframe.dropna().apply(len)
        result = result.unstack(level=0)
        result = result.resample(self.REBALANCING_FREQUENCY, how='sum')
        return result
