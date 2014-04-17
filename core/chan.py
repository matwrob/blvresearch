"""Wesley Chan paper 'Stock price reaction to News and No News' 2003

Chan uses JegadeeshTitman standard rolling portfolio method, but for
News and No News portfolios he uses only 1-month TESTING PERIOD, i.e.
he checks which entities had/didn't have news in the previous month
and selects winners/losers from the entities that had/didn't have news

"""
from copy import deepcopy
import pandas as pd
import math

from memnews.core import NewsList
from blvresearch.core.std_rolling_portfolio import (
    JegadeeshTitman, get_winners, get_losers,
    get_sorted_returns
)


class ChanNews(JegadeeshTitman):

    def _get_winners(self, df_of_returns, test_per):
        naned_returns = self._nan_returns_without_news(df_of_returns)
        return get_winners(naned_returns, 1, self.quant)

    def _get_losers(self, df_of_returns, test_per):
        naned_returns = self._nan_returns_without_news(df_of_returns)
        return get_losers(naned_returns, 1, self.quant)

    def _nan_returns_without_news(self, df_of_returns):
        "inserts NaN in place of return, if a given month had no news"
        nan_ret = deepcopy(df_of_returns)  # need to dcopy to save orig. dframe
        for entity_id, series_of_returns in df_of_returns.items():
            news = self.rd[entity_id]['news']
            news_count = news.apply(get_news_count)
            ncount_resampled = news_count.resample('M', how=sum)
            for date, count in ncount_resampled.items():
                if count == 0:
                    nan_ret[entity_id][date] = pd.np.nan
        return nan_ret

    def get_breakpoints(self, df_of_returns):
        naned_ret = self._nan_returns_without_news(df_of_returns)
        sort_ret = get_sorted_returns(naned_ret, test_per=1)
        result = dict()
        for day, series in sort_ret.items():
            size = int(len(series) / self.quant)
            winners = series[-size:]  # series[-size] and
            losers = series[:size]    # series[size - 1] would also work
            result[day] = {'w': winners[0], 'l': losers[-1]}
        return result



class ChanNoNews(JegadeeshTitman):

    def _get_winners(self, df_of_returns, test_per):
        naned_returns = self._nan_returns_with_news(df_of_returns)
        brkpts = self._get_breakpoints()
        return self._get_winners_using_breakpoints(naned_returns, brkpts)

    def _get_losers(self, df_of_returns, test_per):
        naned_returns = self._nan_returns_with_news(df_of_returns)
        brkpts = self._get_breakpoints()
        return self._get_losers_using_breakpoints(naned_returns, brkpts)

    def _nan_returns_with_news(self, df_of_returns):
        nan_ret = deepcopy(df_of_returns)
        for entity_id, series_of_returns in df_of_returns.items():
            news = self.rd[entity_id]['news']
            news_count = news.apply(get_news_count)
            ncount_resampled = news_count.resample('M', how=sum)
            for date, count in ncount_resampled.items():
                if count > 0:
                    nan_ret[entity_id][date] = pd.np.nan
        return nan_ret

    def _get_winners_using_breakpoints(self, df_of_returns, dict_of_brkpts):
        result = dict()
        for day, series in df_of_returns.iterrows():
            win_brkpt = dict_of_brkpts[day]['w']
            series = series.dropna()
            result[day] = list(series[series > win_brkpt].index)
        return pd.Series(result)

    def _get_losers_using_breakpoints(self, df_of_returns, dict_of_brkpts):
        result = dict()
        for day, series in df_of_returns.iterrows():
            los_brkpt = dict_of_brkpts[day]['l']
            series = series.dropna()
            result[day] = list(series[series < los_brkpt].index)
        return pd.Series(result)

    def _get_breakpoints(self):
        cn = ChanNews(self.rd, type_of_return=self.type,
                      no_of_quantiles=self.quant)
        df_of_returns = cn._get_initial_returns(freq='M')
        return cn.get_breakpoints(df_of_returns)



def get_news_count(news_list):
    if not isinstance(news_list, NewsList):
        return 0
    return len(news_list)


def get_news_count_moments(news):
    # year = self.date.year
    # start, end = pd.datetime(year, 1, 1), pd.datetime(year, 12, 31)
    # news = self.concat_data._data['news'][start:end]
    val = news.map(get_news_count)
    val = val[val > 0]
    mean = val.mean()
    sigma = 0 if math.isnan(val.std()) else val.std()
    return mean, sigma


class ChanNews1Sigma(ChanNews):

    def _nan_returns_without_news(self, df_of_returns):
        proper_index = df_of_returns.resample('M', how=sum).index
        for entity_id, series_of_returns in df_of_returns.items():
            news = self.rd[entity_id]['news']
            m, s = get_news_count_moments(news)
            news_count = news.apply(get_news_count)
            news_count = news_count[news_count > m + s]
            ncount_resampled = news_count.resample('M', how=sum)
            ncount_resampled.reindex(proper_index)
            ncount_resampled.fillna(0, inplace=True)
            for date, count in ncount_resampled.items():
                if count == 0:
                    df_of_returns[entity_id][date] = pd.np.nan
        return df_of_returns


class ChanNoNews1Sigma(ChanNoNews):

    def _nan_returns_without_news(self, df_of_returns):
        proper_index = df_of_returns.resample('M', how=sum).index
        for entity_id, series_of_returns in df_of_returns.items():
            news = self.rd[entity_id]['news']
            m, s = get_news_count_moments(news)
            news_count = news.apply(get_news_count)
            news_count = news_count[news_count > m + s]
            ncount_resampled = news_count.resample('M', how=sum)
            ncount_resampled.reindex(proper_index)
            ncount_resampled.fillna(0, inplace=True)
            for date, count in ncount_resampled.items():
                if count > 0:
                    df_of_returns[entity_id][date] = pd.np.nan
        return df_of_returns


class ChanNews2Sigma(ChanNews):

    def _nan_returns_without_news(self, df_of_returns):
        proper_index = df_of_returns.resample('M', how=sum).index
        for entity_id, series_of_returns in df_of_returns.items():
            news = self.rd[entity_id]['news']
            m, s = get_news_count_moments(news)
            news_count = news.apply(get_news_count)
            news_count = news_count[news_count > m + 2 * s]
            ncount_resampled = news_count.resample('M', how=sum)
            ncount_resampled.reindex(proper_index)
            ncount_resampled.fillna(0, inplace=True)
            for date, count in ncount_resampled.items():
                if count == 0:  # if month without news, return is nan
                    df_of_returns[entity_id][date] = pd.np.nan
        return df_of_returns


class ChanNoNews2Sigma(ChanNoNews):

    def _nan_returns_without_news(self, df_of_returns):
        proper_index = df_of_returns.resample('M', how=sum).index
        for entity_id, series_of_returns in df_of_returns.items():
            news = self.rd[entity_id]['news']
            m, s = get_news_count_moments(news)
            news_count = news.apply(get_news_count)
            news_count = news_count[news_count > m + 2 * s]
            ncount_resampled = news_count.resample('M', how=sum)
            ncount_resampled.reindex(proper_index)
            ncount_resampled.fillna(0, inplace=True)
            for date, count in ncount_resampled.items():
                if count > 0:  # if month with news, return is nan
                    df_of_returns[entity_id][date] = pd.np.nan
        return df_of_returns
