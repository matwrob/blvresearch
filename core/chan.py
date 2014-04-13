import pandas as pd

from memnews.core import NewsList
from blvresearch.core.std_rolling_portfolio import (
    JegadeeshTitman, get_winners, get_losers
)


class ChanNews(JegadeeshTitman):

    def _get_winners(self, df_of_returns, test_per, no_of_quantiles):
        test_per = 1
        df_of_returns = self._nan_returns_without_news(df_of_returns)
        return get_winners(df_of_returns, test_per, no_of_quantiles)

    def _get_losers(self, df_of_returns, test_per, no_of_quantiles):
        test_per = 1
        df_of_returns = self._nan_returns_without_news(df_of_returns)
        return get_losers(df_of_returns, test_per, no_of_quantiles)

    def _nan_returns_without_news(self, df_of_returns):
        for entity_id, series_of_returns in df_of_returns.items():
            news = self.rd[entity_id]['news']
            news_count = news.apply(get_news_count)
            ncount_resampled = news_count.resample('M', how=sum)
            for date, count in ncount_resampled.items():
                if count == 0:
                    df_of_returns[entity_id][date] = pd.np.nan
        return df_of_returns


class ChanNoNews(JegadeeshTitman):

    def _get_winners(self, df_of_returns, test_per, no_of_quantiles):
        test_per = 1
        df_of_returns = self._nan_returns_with_news(df_of_returns)
        return get_winners(df_of_returns, test_per, no_of_quantiles)

    def _get_losers(self, df_of_returns, test_per, no_of_quantiles):
        test_per = 1
        df_of_returns = self._nan_returns_with_news(df_of_returns)
        return get_losers(df_of_returns, test_per, no_of_quantiles)

    def _nan_returns_with_news(self, df_of_returns):
        for entity_id, series_of_returns in df_of_returns.items():
            news = self.rd[entity_id]['news']
            news_count = news.apply(get_news_count)
            ncount_resampled = news_count.resample('M', how=sum)
            for date, count in ncount_resampled.items():
                if count != 0:
                    df_of_returns[entity_id][date] = pd.np.nan
        return df_of_returns


def get_news_count(news_list):
    if not isinstance(news_list, NewsList):
        return 0
    return len(news_list)
