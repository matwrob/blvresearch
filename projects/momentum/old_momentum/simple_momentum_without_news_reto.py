import pandas as pd
import numpy as np
from copy import *
from newsproject import *

o = load_object('eu03_12.p')

threshold = 1
holding_period = 3
cost = 0

### DYNAMIC

class News(DynamicBacktest):

    def get_starting_points(self):
        def viable_news(x):
            if type(x) == pd.core.frame.DataFrame:
                viable = any(x.category <= 2)
            else:
                viable = False
            return viable
        std = pd.rolling_std(self.rel, 200, 150)
        returns = np.abs(self.rel / std) > threshold
        volume = self.volume / self.volume.std() > 1
        viable_news = self.news.applymap(viable_news)
        starts = returns & viable_news
        starts = starts.shift(-1).fillna(False)
        return starts

dynam = News(o, holding_period, cost)
dynam.add_portfolio()

### GET RID OF NEWS RETURN IN REL_RET DATAFRAME

rel_ret = {k: v.rel_ret for k, v in o.iteritems()}
rel_ret = pd.DataFrame(rel_ret)

rel = copy.deepcopy(rel_ret)
for i, d in enumerate(dynam.holdings.index):
    rel.ix[d] = rel.ix[d][~dynam.holdings.ix[d]]

### PERIODIC

number_of_shares = 50

class PosMomentum(PeriodicBacktest):
    def add_data(self):
        pass

    def select_stocks(self, i, v):
        tmp = rel.resample(self.interval, how='sum').ix[v]
        tmp = copy.deepcopy(tmp.dropna())
        tmp.sort()
        stocks = tmp.index[-number_of_shares:]
        return stocks

class NegMomentum(PeriodicBacktest):
    def add_data(self):
        pass

    def select_stocks(self, i, v):
        tmp = rel.resample(self.interval, how='sum').ix[v]
        tmp = copy.deepcopy(tmp.dropna())
        tmp.sort()
        stocks = tmp.index[:number_of_shares]
        return stocks

pper = PosMomentum(o, 'BM')
nper = NegMomentum(o, 'BM')

series = pd.concat([pper.rel_ret, nper.rel_ret], axis=1)
series.rename(columns={0: 'posmom %s' %number_of_shares,
                       1: 'negmom %s' %number_of_shares},
              inplace=True)
series.cumsum().plot()
