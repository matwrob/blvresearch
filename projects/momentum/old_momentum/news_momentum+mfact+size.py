import numpy as np
import matplotlib.dates as dates
import matplotlib.ticker as ticker
from newsproject import *
threshold = 2
news_cat = 1
holding_period = 20
cost = 0
o = load_object('eu03_12.p')


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

n0 = NegNews(o, holding_period, cost)


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
        mfact = self.mfact < 0
        starts = returns & viable_news & mfact
        starts = starts.shift(1).fillna(False)
        return starts

n1 = NegNews(o, holding_period, cost)


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
        mfact = self.mfact < -0.003
        starts = returns & viable_news & mfact
        starts = starts.shift(1).fillna(False)
        return starts

n2 = NegNews(o, holding_period, cost)


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
        mfact = self.mfact < - 0.005
        starts = returns & viable_news & mfact
        starts = starts.shift(1).fillna(False)
        return starts

n3 = NegNews(o, holding_period, cost)


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
        mfact = self.mfact < - 0.007
        starts = returns & viable_news & mfact
        starts = starts.shift(1).fillna(False)
        return starts

n4 = NegNews(o, holding_period, cost)

neg0 = - n0.mean_rel_ret.cumsum()
neg0 = neg0.dropna()
neg1 = - n1.mean_rel_ret.cumsum()
neg1 = neg1.dropna()
neg2 = - n2.mean_rel_ret.cumsum()
neg2 = neg2.dropna()
neg3 = - n3.mean_rel_ret.cumsum()
neg3 = neg3.dropna()
neg4 = - n4.mean_rel_ret.cumsum()
neg4 = neg4.dropna()

fig = figure(1, figsize=(15, 17))

ax1 = fig.add_subplot(511)
ax1.plot(neg0.index, neg0, color='blue', label='Negative')
ax1.legend()

ax2 = fig.add_subplot(512)
ax2.plot(neg1.index, neg1, color='blue', label='Negative + mfact<0')
ax2.legend()

ax3 = fig.add_subplot(513)
ax3.plot(neg2.index, neg2, color='blue', label='Negative + mfact<-0.003')
ax3.legend()

ax4 = fig.add_subplot(514)
ax4.plot(neg3.index, neg3, color='blue', label='Negative + mfact<-0.005')
ax4.legend()

ax5 = fig.add_subplot(515)
ax5.plot(neg4.index, neg4, color='blue', label='Negative + mfact<-0.007')
ax5.legend()
