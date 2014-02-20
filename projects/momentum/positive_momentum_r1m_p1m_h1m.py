import pandas as pd

from blvresearch.core.portfolio import (
    StaticStrategy, Portfolio, PositiveMomentumStrategy, StockReturns,
    PortfolioCharacteristics, TOP_DECILE
)
from blvresearch.core.SP500output import ABSRET, ALPHA, NEWS, SP500_RETURNS
from blvresearch.core.sentiment import RTRS_SENTIMENT_ENTITY

from blvworker.news.important_days import add_important_day_column


class PositiveSentiment_1M_1M_1M(StaticStrategy):
    "1M_1M_1M stands for rankPeriods_pausePeriods_holdingPeriods"

    NAME = 'Positive sentiment score based momentum'
    RANKING_PERIODS = 1
    PAUSE_PERIODS = 1
    HOLDING_PERIODS = 1
    REBALANCING_FREQUENCY = 'M'
    PORTFOLIO_SIZE = 20

    def _get_positions(self):
        sent = self.supplementary_data.resample(self.REBALANCING_FREQUENCY,
                                                how=sum)
        result = self._positions_per_rebalancing_day(sent)
        return result.reindex(self.returns.index, method='ffill')

    def _positions_per_rebalancing_day(self, sentiment_scores):
        result = dict()
        for day in self.rebalancing_days:
            temp = sentiment_scores.loc[day].dropna()
            temp.sort()
            result[day] = self._get_decile(temp)
        return pd.Series(result)

    def _get_decile(self, series):
        return TOP_DECILE(series, self.PORTFOLIO_SIZE)


pos_sent_strat = PositiveSentiment_1M_1M_1M(
    ABSRET, supplementary_data=RTRS_SENTIMENT_ENTITY
)
pos_sent_port = Portfolio(pos_sent_strat)
pos_sent_perf = pos_sent_port.daily_performance()
pos_sent_perf.name = 'Positive sentiment score momentum'
pos_sent_char = PortfolioCharacteristics(pos_sent_port)


class PositiveMomentum_1M_1M_1M(PositiveMomentumStrategy):

    RANKING_PERIODS = 1
    PAUSE_PERIODS = 1
    HOLDING_PERIODS = 1
    REBALANCING_FREQUENCY = 'M'
    PORTFOLIO_SIZE = 20


pos_mom_strat = PositiveMomentum_1M_1M_1M(ABSRET)
pos_mom_port = Portfolio(pos_mom_strat)
pos_mom_perf = pos_mom_port.daily_performance()
pos_mom_perf.name = 'Positive momentum'
pos_mom_char = PortfolioCharacteristics(pos_mom_port)


class PositiveAlphaMomentum_1M_1M_1M(PositiveMomentum_1M_1M_1M):

    def _get_returns(self):
        if self.REBALANCING_FREQUENCY in ['W-FRI', 'W']:
            return StockReturns(self.supplementary_data).weekly
        if self.REBALANCING_FREQUENCY in ['M']:
            return StockReturns(self.supplementary_data).monthly
        if self.REBALANCING_FREQUENCY in ['B', 'D']:
            return StockReturns(self.supplementary_data).daily
        raise AttributeError('Provide proper rebalancing frequency')

pos_alpha_strat = PositiveAlphaMomentum_1M_1M_1M(
    ABSRET, supplementary_data=ALPHA
)
pos_alpha_port = Portfolio(pos_alpha_strat)
pos_alpha_perf = pos_alpha_port.daily_performance()
pos_alpha_perf.name = 'Positive alpha momentum'
pos_alpha_char = PortfolioCharacteristics(pos_alpha_port)


"""
Important days momentum strategy:
- important days are calculated based on alphas and news amount for a given
  calendar year; this is important because we decide on whether a day is
  important using standard deviation and mean of daily alphas / daily news
  amounts
- in concat we do this based on 2 years of data
- important_days is a dict with keys = [2003, 2004, 2005, ..., 2012] and values
  being dataframes indexed with daily timestamps and columns being entity_ids
- resampling important_days to e.g. monthly periods is done by summing
  booleans (zeros and ones), and therefore any month that has value > 0 had
  at least one important day; it's possible to sort on amount of important days
  or simply consider all values > 0 being equal
"""


class PositiveImpDays_1M_1M_1M(PositiveMomentum_1M_1M_1M):

    NAME = """Considers only stocks that experienced important day within
              the ranking period and ranking period return was positive"""

    def _get_positions(self):
        important_days = self._get_input_data()
        positions = self._positions_per_rebalancing_day(important_days)
        return self._reindex_positions(positions)

    def _positions_per_rebalancing_day(self, important_days):
        returns = self.returns.resample(self.REBALANCING_FREQUENCY, how=sum)
        important_days = important_days.resample(self.REBALANCING_FREQUENCY,
                                                 how=sum)
        result = dict()
        for ix, end_day in enumerate(self.ranking_days):
            start_day = self._get_ranking_period_start(end_day)
            importance_scores = important_days[start_day:end_day].sum()
            relevant_scores = importance_scores[importance_scores > 0]
            relevant_entities = list(relevant_scores.index)
            temp = returns[start_day:end_day].sum()[relevant_entities]
            temp.sort(ascending=True)
            rebal_day = self.rebalancing_days[ix]
            result[rebal_day] = self._get_decile(temp)
        return pd.Series(result)

    def _get_input_data(self):
        news_by_year, alpha_by_year = self._get_news_and_alpha_yearly()
        result = list()
        for year, v in news_by_year.items():
            res = pd.concat([v.T.stack(), alpha_by_year[year].T.stack()],
                            axis=1)
            res = res.rename(columns={0: 'news', 1: 'alpha'})
            res = add_important_day_column(res)
            result.append(res['important_day'].unstack().T)
        return pd.concat(result)

    def _get_news_and_alpha_yearly(self):
        news_by_year = self._get_dict_of_yearly_batches(
            self.supplementary_data['news']
        )
        alpha_by_year = self._get_dict_of_yearly_batches(
            self.supplementary_data['alpha']
        )
        return news_by_year, alpha_by_year

    def _get_dict_of_yearly_batches(self, df):
        result = dict()
        for group in df.groupby(df.index.year):
            result[group[0]] = group[1]
        return result

    def _get_decile(self, series):
        return TOP_DECILE(series, self.PORTFOLIO_SIZE)


pos_import_strat = PositiveImpDays_1M_1M_1M(
    ABSRET, supplementary_data={'news': NEWS, 'alpha': ALPHA}
)
pos_import_port = Portfolio(pos_import_strat)
pos_import_perf = pos_import_port.daily_performance()
pos_import_perf.name = 'Important day based momentum'


sp500_perf = SP500_RETURNS
sp500_perf.name = 'SP500'


data = pd.concat([pos_sent_perf, pos_mom_perf, pos_alpha_perf,
                  pos_import_perf, sp500_perf], axis=1)
