import pandas as pd
import numpy as np
from newsproject import *
o = load_object('eu03_12.p')

news_cat = 1
holding_period = 20
cost = 0
threshold = 2


class PosNewsCounter(DynamicBacktest):

    def get_starting_points(self):
        def viable_news(x):
            if type(x) == pd.core.frame.DataFrame:
                viable = True
            else:
                viable = False
            return viable
        returns = self.rel > 0
        viable_news = self.news.applymap(viable_news)
        starts = returns & viable_news
        starts = starts.shift(1).fillna(False)
        return starts


class NegNewsCounter(DynamicBacktest):

    def get_starting_points(self):
        def viable_news(x):
            if type(x) == pd.core.frame.DataFrame:
                viable = True
            else:
                viable = False
            return viable
        returns = self.rel < 0
        viable_news = self.news.applymap(viable_news)
        starts = returns & viable_news
        starts = starts.shift(1).fillna(False)
        return starts

p = PosNewsCounter(o, 1, cost)
n = NegNewsCounter(o, 1, cost)

psize = p.portfolio.size['2012-01-01':].dropna()
nsize = n.portfolio.size['2012-01-01':].dropna()
ratio = psize/nsize
psize = pd.rolling_mean(psize, 10)
nsize = pd.rolling_mean(nsize, 10)
ratio = pd.rolling_mean(ratio, 10)
series = pd.concat([psize, nsize], axis=1)
series.rename(columns={0: 'positive', 1: 'negative'}, inplace=True)

class PosNews(DynamicBacktest):

    def get_starting_points(self):
        def viable_news(x):
            if type(x) == pd.core.frame.DataFrame:
                viable = any(x.category == news_cat)
            else:
                viable = False
            return viable
        std = pd.rolling_std(self.rel, 200, 150)
        returns = self.rel / std > threshold
        volume = self.volume / self.volume.std() > 1
        viable_news = self.news.applymap(viable_news)
        starts = returns & viable_news 
        starts = starts.shift(1).fillna(False)
        return starts

class NegNews(DynamicBacktest):

    def get_starting_points(self):
        def viable_news(x):
            if type(x) == pd.core.frame.DataFrame:
                viable = any(x.category == news_cat)
            else:
                viable = False
            return viable

        std = pd.rolling_std(self.rel, 200, 150)
        returns = self.rel / std < -threshold
        volume = self.volume / self.volume.std() > 1
        viable_news = self.news.applymap(viable_news)
        starts = returns & viable_news
        starts = starts.shift(1).fillna(False)
        return starts

p = PosNews(o, holding_period, cost)
n = NegNews(o, holding_period, cost)

neg = - n.mean_rel_ret.cumsum()
neg = neg.dropna()
pos = p.mean_rel_ret.cumsum()
pos = pos.dropna()

fig = figure(1, figsize=(15, 17))

ax1 = fig.add_subplot(511)
ax1.plot(pos.index, pos, color='blue', label='Positive')
ax1.legend()

ax2 = fig.add_subplot(512)
ax2.plot(psize.index, psize, color='blue', label='Positive News Counter')
ax2.legend()

ax3 = fig.add_subplot(513)
ax3.plot(neg.index, neg, color='red', label='Negative')
ax3.legend()

ax4 = fig.add_subplot(514)
ax4.plot(nsize.index, nsize, color='red', label='Negative News Counter')
ax4.legend()

ax5 = fig.add_subplot(515)
ax5.plot(ratio.index, ratio, color='green', label='Positive Count/Negative Count')
ax5.legend()
