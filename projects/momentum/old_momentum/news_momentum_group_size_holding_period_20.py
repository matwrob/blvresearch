'''
Viable_news:
days when a group of news appears of the size greater than
or equal to the average size of biggest group on news day,
i.e. I check group sizes for each company every day and take
the mean over the biggest groups

Returns:
days with returns adjusted by std. deviation greater/smaller
than a certain threshold
'''

import newsproject as n
import pandas as pd
import numpy as np
from newsproject.backtest.backtest import *

o = n.load_object('output_eu_08_12_research.pickle')

threshold = 2
holding_period = 20  # c.a. 1 month
cost = 0


class PosNews(DynamicBacktest):
    def get_starting_points(self):
        def return_viable_news(x):
            result = {}
            for k, v in x.items():
                v = v.dropna()
                avg = mean([max(i) for i in v if type(i) != float])
                avg = max(0, ceil(avg))
                d = {p: any([i >= avg for i in q]) for p, q in v.items() if type(q) != float}
                d = pd.Series(d)
                d.fillna(False)
                result[k] = d
            return pd.DataFrame(result)

        # identifying "large" price change (days with important news events)
        # adjust return for std. deviation (rolling)
        # 10% change for a high-vola stock may be a non-event whereas
        # 5% change for a low-vola stock may be an important event
        # as a result, the sample is less likely to be biased in favor
        # of selecting highly volatilte stocks

        std = pd.rolling_std(self.rel, 200, 150)
        returns = self.rel / std > threshold

        # volume = self.volume / self.volume.std() > 1
        news_groups = {k: v.news_groups for k, v in o.items()}
        viable_news = return_viable_news(news_groups)
        #
        # define criteria for starts
        #
        starts = {}
        for k, v in returns.items():
            a = returns[k].fillna(False)
            b = viable_news[k].fillna(False)
            if a.any() and b.any():
                starts[k] = a & b
        starts = pd.DataFrame(starts)
        #
        # pay attention to the shift in starts
        #
        starts = starts.shift(1).fillna(False)
        return starts


class NegNews(DynamicBacktest):
    def get_starting_points(self):
        def return_viable_news(x):
            result = {}
            for k, v in x.items():
                v = v.dropna()
                avg = mean([max(i) for i in v if type(i) != float])
                avg = max(0, ceil(avg))
                d = {p: any([i >= avg for i in q]) for p, q in v.items() if type(q) != float}
                d = pd.Series(d)
                d.fillna(False)
                result[k] = d
            return pd.DataFrame(result)

        # identifying "large" price change (days with important news events)
        # adjust return for std. deviation (rolling)
        # 10% change for a high-vola stock may be a non-event whereas
        # 5% change for a low-vola stock may be an important event
        # as a result, the sample is less likely to be biased in favor
        # of selecting highly volatilte stocks

        std = pd.rolling_std(self.rel, 200, 150)
        returns = self.rel / std < -threshold

        # volume = self.volume / self.volume.std() > 1
        news = {k: v.news for k, v in o.items()}
        viable_news = return_viable_news(news)
        #
        # define criteria for starts
        #
        starts = {}
        for k, v in returns.items():
            a = returns[k].fillna(False)
            b = viable_news[k].fillna(False)
            if a.any() and b.any():
                starts[k] = a & b
        starts = pd.DataFrame(starts)
        #
        # pay attention to the shift in starts
        #
        starts = starts.shift(1).fillna(False)
        return starts


pos = PosNews(o, holding_period, cost)
neg = NegNews(o, holding_period, cost)

font = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 8}

matplotlib.rc('font', **font)

########### relative returns plot
fig = figure(1, figsize=(25, 17))
ax1 = fig.add_subplot(111)
series1 = pd.concat([pos.mean_rel_ret, neg.mean_rel_ret], axis=1)
series1 = series1.dropna().cumsum()
ax1.plot(series1.index, series1)
ax1.legend(['positive news eu rel_ret, thresh %s, hold_per %s days, costs %s' % (threshold, holding_period, cost),
            'negative news eu rel_ret, thresh %s, hold_per %s days, costs %s' % (threshold, holding_period, cost)])
ax1.xaxis.set_major_locator(MaxNLocator(10))
