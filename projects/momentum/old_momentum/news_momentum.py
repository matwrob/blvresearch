'''
Test performance of stocks after news release
'''
import pandas as pd
import numpy as np
from newsproject import *
o = load_object('eu03_12.p')

threshold = 2
news_cat = 2
holding_period = 20
cost = 0

class PosNews(DynamicBacktest):

    def get_starting_points(self):
        def viable_news(x):
            if type(x) == pd.core.frame.DataFrame:
                viable = any(x.category <= news_cat)
            else:
                viable = False
            return viable
        std = pd.rolling_std(self.rel, 200, 150)
        # identifying "large" price change (days with important news events)
        # adjust return for std. deviation (rolling)
        # 10% change for a high-vola stock may be a non-event whereas
        # 5% change for a low-vola stock may be an important event
        # as a result, the sample is less likely to be biased in favor
        # of selecting highly volatilte stocks
        returns = self.rel / std > threshold
        volume = self.volume / self.volume.std() > 1
        viable_news = self.news.applymap(viable_news)
        starts = returns & viable_news & volume
        starts = starts.shift(1).fillna(False)
        return starts

class NegNews(DynamicBacktest):

    def get_starting_points(self):
        def viable_news(x):
            if type(x) == pd.core.frame.DataFrame:
                viable = any(x.category <= news_cat)
            else:
                viable = False
            return viable
        std = pd.rolling_std(self.rel, 200, 150)
        returns = self.rel / std < -threshold
        volume = self.volume / self.volume.std() > 1
        viable_news = self.news.applymap(viable_news)
        # adding volume crit. gives even better results
        starts = returns & viable_news & volume
        starts = starts.shift(1).fillna(False)
        return starts

p = PosNews(o, holding_period, cost)
n = NegNews(o, holding_period, cost)

series = pd.concat([p.mean_rel_ret, n.mean_rel_ret], axis=1)
series.rename(columns={0: 'positive', 1: 'negative'}, inplace=True)
series.dropna().cumsum().plot()

# GET THE PERCENTAGE OF DAYS THAT STOCK IS IN THE PORTFOLIO
from __future__ import division

pos_frame = pd.Series(index=n.holdings.columns)
neg_frame = pd.Series(index=p.holdings.columns)

for sec in n.holdings.columns:
    true = n.rel[sec][n.holdings[sec] == True]
    false = n.rel[sec][n.holdings[sec] == False]
    neg_frame[sec] = len(true)/len(n.holdings[sec])

for sec in p.holdings.columns:
    true = p.rel[sec][p.holdings[sec] == True]
    false = p.rel[sec][p.holdings[sec] == False]
    pos_frame[sec] = len(true)/len(p.holdings[sec])

mean(neg_frame)
mean(pos_frame)

# PLOT OF HOLDINGS

security_list = neg_frame.sort()[-10:].index
series = pd.DataFrame(index=n.holdings.index,
                      columns=security_list)
fig = plt.figure(figsize=(25, 10))
ax = plt.subplot(111)
for i, m in enumerate(security_list):
    series[m][n.holdings[m] == True] = i + 1
    line, = ax.plot(series.index, series[m], label=m)

ax.yaxis.set_ticklabels(security_list)
# Shink current axis's height by 10% on the bottom
box = ax.get_position()
ax.set_position([box.x0, box.y0 + box.height * 0.1,
                 box.width, box.height * 0.9])

# Put a legend below current axis
ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
          fancybox=True, shadow=True, ncol=5)
plt.show()
