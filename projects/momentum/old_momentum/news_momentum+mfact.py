import pandas as pd
import numpy as np
import matplotlib.dates as dates
import matplotlib.ticker as ticker
from newsproject import *
threshold = 2
news_cat = 1
holding_period = 20
cost = 0
o = load_object('eu03_12.p')

class PosNews(DynamicBacktest):

    def get_starting_points(self):
        def viable_news(x):
            if type(x) == pd.core.frame.DataFrame:
                viable = any(x.category == news_cat)
            else:
                viable = False
            return viable
        std = pd.rolling_std(p.rel, 200, 150)
        returns = self.rel / std > threshold
        volume = self.volume / self.volume.std() > 1
        viable_news = self.news.applymap(viable_news)
        mfact = self.mfact > 0.015
        starts = returns & viable_news & mfact
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

        std = pd.rolling_std(p.rel, 200, 150)
        returns = self.rel / std < -threshold
        volume = self.volume / self.volume.std() > 1
        viable_news = self.news.applymap(viable_news)
        mfact = self.mfact < - 0.015
        starts = returns & viable_news & mfact
        starts = starts.shift(1).fillna(False)
        return starts

p1 = PosNews(o, holding_period, cost)
n1 = NegNews(o, holding_period, cost)

class PosNews(DynamicBacktest):

    def get_starting_points(self):
        def viable_news(x):
            if type(x) == pd.core.frame.DataFrame:
                viable = any(x.category == news_cat)
            else:
                viable = False
            return viable
        std = pd.rolling_std(p.rel, 200, 150)
        returns = self.rel / std > threshold
        volume = self.volume / self.volume.std() > 1
        viable_news = self.news.applymap(viable_news)
        mfact = self.mfact < - 0.015
        starts = returns & viable_news & mfact
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

        std = pd.rolling_std(p.rel, 200, 150)
        returns = self.rel / std < -threshold
        volume = self.volume / self.volume.std() > 1
        viable_news = self.news.applymap(viable_news)
        mfact = self.mfact > 0.015
        starts = returns & viable_news & mfact
        starts = starts.shift(1).fillna(False)
        return starts

p2 = PosNews(o, holding_period, cost)
n2 = NegNews(o, holding_period, cost)

neg1 = - n1.mean_rel_ret.cumsum()
neg1 = neg1.dropna()
pos1 = p1.mean_rel_ret.cumsum()
pos1 = pos1.dropna()
neg2 = - n2.mean_rel_ret.cumsum()
neg2 = neg2.dropna()
pos2 = p2.mean_rel_ret.cumsum()
pos2 = pos2.dropna()

fig = figure(1, figsize=(15, 17))

ax1 = fig.add_subplot(411)
ax1.plot(pos1.index, pos1, color='blue', label='Positive + mfact > 0.015')
ax1.legend()

ax2 = fig.add_subplot(412)
ax2.plot(pos2.index, pos2, color='blue', label='Positive + mfact < -0.015')
ax2.legend()

ax3 = fig.add_subplot(413)
ax3.plot(neg1.index, neg1, color='red', label='Negative + mfact < -0.015')
ax3.legend()

ax4 = fig.add_subplot(414)
ax4.plot(neg2.index, neg2, color='red', label='Negative + mfact > 0.015')
ax4.legend()

ax1.xaxis.set_major_locator(dates.MonthLocator())
ax1.xaxis.set_minor_locator(dates.MonthLocator(bymonthday=15))
ax1.xaxis.set_major_formatter(ticker.NullFormatter())
ax1.xaxis.set_minor_formatter(dates.DateFormatter('%b'))

ax2.xaxis.set_major_locator(dates.MonthLocator())
ax2.xaxis.set_minor_locator(dates.MonthLocator(bymonthday=15))
ax2.xaxis.set_major_formatter(ticker.NullFormatter())
ax2.xaxis.set_minor_formatter(dates.DateFormatter('%b'))

ax3.xaxis.set_major_locator(dates.MonthLocator())
ax3.xaxis.set_minor_locator(dates.MonthLocator(bymonthday=15))
ax3.xaxis.set_major_formatter(ticker.NullFormatter())
ax3.xaxis.set_minor_formatter(dates.DateFormatter('%b'))

ax4.xaxis.set_major_locator(dates.MonthLocator())
ax4.xaxis.set_minor_locator(dates.MonthLocator(bymonthday=15))
ax4.xaxis.set_major_formatter(ticker.NullFormatter())
ax4.xaxis.set_minor_formatter(dates.DateFormatter('%b'))

ax4.set_xlabel('2012')
