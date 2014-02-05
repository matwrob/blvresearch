from concat import *
import pandas as pd
import numpy as np
import copy


class DynamicBacktest(object):  # pragma: no cover

    """
    def get_starting_points(self):
        threshold = 0.02
        news_cat = 1

        def viable_news(x):
            if type(x) == pd.core.frame.DataFrame:
                viable = any(x.category == news_cat)
            else:
                viable = False
            return viable

        returns = self.rel > threshold
        viable_news = self.news.applymap(viable_news)
        starts = returns & viable_news
        return starts
    """

    def __init__(self, total_output,
                 holding_period, transaction_cost=0):
        self.o = total_output
        self.hold_per = holding_period
        self.transaction_cost = transaction_cost

        self._add_data()

        self.holdings = pd.DataFrame(index=self.rel.index,
                                     columns=self.rel.columns)
        #hack for all falses
        self.holdings = self.holdings == 1

        self.props = pd.DataFrame(None,
                                  index=self.holdings.index,
                                  columns=['size',
                                           'holdings',
                                           'avg_beta',
                                           'mcap',
                                           'r2'],
                                  dtype=object)
        self._mean_rel_ret = pd.Series()
        self._sum_rel_ret = pd.Series()
        self.stats = dict()

    def _add_data(self):
        rel_ret = {k: v.rel_ret for k, v in self.o.items()}
        self.rel = pd.DataFrame(rel_ret)

        abs_ret = {k: v.abs_ret for k, v in self.o.items()}
        self.abs = pd.DataFrame(abs_ret)

        news = {k: v.news for k, v in self.o.items()}
        self.news = pd.DataFrame(news)

        mcap = {k: v.mcap for k, v in self.o.items()}
        self.mcap = pd.DataFrame(mcap)

        r2 = {k: v.r2 for k, v in self.o.items()}
        self.r2 = pd.DataFrame(r2)

        beta = {k: v.beta_mkt for k, v in self.o.items()}
        self.beta_mkt = pd.DataFrame(beta)

        volume = {k: v.relative_vol for k, v in self.o.items()}
        self.volume = pd.DataFrame(volume)

        mfact = {k: v.fact_mkt for k, v in self.o.items()}
        self.mfact = pd.DataFrame(mfact)

    def add_portfolio(self):
        starts = self.get_starting_points()
        self.starts = starts
        for e in starts.columns:
            points = starts[e][starts[e]]
            for d in points.index:
                i = self.holdings.index.get_loc(d)
                self.holdings.ix[i + 1:i + 1 + self.hold_per, e] = True
        self._calculate_returns()
        self._append_portfolio_summary()

    def _calculate_returns(self):
        rel = self.rel.copy()
        abs = self.abs.copy()
        rel[self.holdings == False] = np.nan
        abs[self.holdings == False] = np.nan
        self._mean_rel_ret = rel.mean(axis=1)
        self._sum_rel_ret = rel.sum(axis=1)
        self._mean_abs_ret = abs.mean(axis=1)
        self._sum_abs_ret = abs.sum(axis=1)

    def _append_portfolio_summary(self):
        for d in self.holdings.index:
            tmp = self.holdings.ix[d]
            p = list(tmp[tmp == True].index)
            if len(p) > 0:
                self.props.ix[d, 'size'] = len(p)
                self.props.ix[d, 'holdings'] = p
                self.props.ix[d, 'avg_beta'] = self.beta_mkt.ix[d, p].mean()
                self.props.ix[d, 'mcap'] = self.mcap.ix[d, p].mean()
                self.props.ix[d, 'r2'] = self.r2.ix[d, p].mean()

    def _random_sample(self):
        trials = pd.DataFrame()
        i = 0
        while i <= 5:
            trial = pd.DataFrame(self._random_trial(), columns=[i])
            trials = pd.concat([trials, trial])
            i += 1
        self.random_trials = trials
        m = trials.sum()
        m.sort()
        self.stats = {'max_conf': m[-2:].mean(),
                      'min_conf': m[:2].mean()}

    def _random_trial(self):
        trial = pd.Series()
        # creating random_starts
        starts = self.get_starting_points()
        random_starts = copy.deepcopy(starts)
        random_starts.values[:] = False
        # getting initial date
        for i, date in enumerate(starts.index):
            dummy = starts.ix[i]
            dummy = dummy[dummy == True]
            if dummy.any() == True:
                break
        # getting the initial starts
        port_size = len(dummy)
        possible_stocks = self.rel.ix[date].dropna().index
        random = np.random.rand(len(possible_stocks))
        possible_stocks = pd.Series(random, index=possible_stocks)
        possible_stocks.sort()
        initial_list = list(possible_stocks.index[:port_size])
        random_starts.ix[date, initial_list] = True
        # getting the rest of random starts
        for i, d in enumerate(random_starts.index):
            if d > date:
                temp = random_starts.ix[i - 1]
                temp = temp[temp == True]
                # starts from previous day
                old_ones = starts.ix[i - 1]
                old_ones = old_ones[old_ones == True]
                old_ones = old_ones.index
                # starts from current day
                added_ones = starts.ix[i]
                added_ones = added_ones[added_ones == True]
                added_ones = added_ones.index
                # new stocks added
                new_ones = added_ones - old_ones
                # get new random stocks
                possible_stocks = self.rel.ix[i].dropna().index - temp.index
                random = np.random.rand(len(possible_stocks))
                possible_stocks = pd.Series(random, index=possible_stocks)
                possible_stocks.sort()
                random_temp1 = list(possible_stocks.index[:len(new_ones)])
                # get new stocks out of old ones
                the_same = old_ones & added_ones
                random = np.random.rand(len(temp.index))
                possible_stocks = pd.Series(random, index=temp.index)
                possible_stocks.sort()
                random_temp2 = list(possible_stocks.index[:len(the_same)])
                random_temp = random_temp1 + random_temp2
                random_starts.ix[i, random_temp] = True
        rel = pd.DataFrame(index=self.rel.index, columns=self.rel.columns)
        for sec in self.rel.columns:
            rel[sec] = self.rel[sec][random_starts[sec]]
        trial = rel.mean(axis=1).cumsum().dropna()
        return trial

    @property
    def portfolio(self):
        if not any(self._mean_rel_ret):
            self.add_portfolio()
        return self.props

    @property
    def mean_rel_ret(self):
        if not any(self._mean_rel_ret):
            self.add_portfolio()
        return self._mean_rel_ret

    @property
    def sum_rel_ret(self):
        if not any(self._mean_rel_ret):
            self.add_portfolio()
        return self._sum_rel_ret

    @property
    def mean_abs_ret(self):
        if not any(self._mean_rel_ret):
            self.add_portfolio()
        return self._mean_abs_ret

    @property
    def sum_abs_ret(self):
        if not any(self._mean_rel_ret):
            self.add_portfolio()
        return self._sum_abs_ret

    @property
    def statistics(self):
        if not self.stats:
            self._random_sample()
        return self.stats
