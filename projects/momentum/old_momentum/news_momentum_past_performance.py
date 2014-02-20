import pandas as pd
import numpy as np
from newsproject import *
o = load_object('eu03_12.p')

threshold = 2
news_cat = 1
holding_period = 10
cost = 0


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
        past_perf = self.rel[]
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

series = pd.concat([p.mean_rel_ret, -n.mean_rel_ret],axis=1)
series.rename(columns={0: 'positive', 1: 'negative'}, inplace=True)
series.dropna().cumsum().plot()
#series.dropna()['2012-01-01':].cumsum().sum(axis=1).plot()