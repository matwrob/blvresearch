# Method: first obtain a frame ("portfolio") with Y-axis being Dates (whole
# period) and X-axis being stocks. For this use DynamicBacktest
# (this frame is obtained by using function starts and then assigning to 
# all cells "False")
# Next step is to get PeriodicBacktest results, in particular, portfolio hold-
# ings (n.port_props.holdings & p.port_props.holdings)
# This gives us the stocks for which we should have "True" values in cells 
# in "portfolio" frame for a certain month
# Last step, get rid of "True" in the surroundings of news. For this, use
# again DynamicBacktest class (pdyn.holdings & ndyn.holdings)

import pandas as pd
import numpy as np
from copy import *
from newsproject import *

o = load_object('eu03_12.p')

############## FIRST STEP ########################### DynamicBacktest
threshold = 2
news_cat = 2
holding_period = 5
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
        returns = self.rel / std > threshold
        volume = self.volume / self.volume.std() > 1
        viable_news = self.news.applymap(viable_news)
        # pay attention to screens used for starts
        starts = returns & viable_news & volume
        # no shift, remove returns on newsday and after newsday
        starts = starts.fillna(False)
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
        # no shift for starts here, want to include news day return as well
        starts = starts.fillna(False)
        return starts

pdyn = PosNews(o, holding_period, cost)
pdyn.add_portfolio()
ndyn = NegNews(o, holding_period, cost)
ndyn.add_portfolio()

# series = pd.concat([pdyn.mean_rel_ret, ndyn.mean_rel_ret],axis=1)
# series.rename(columns={0: 'positive', 1: 'negative'}, inplace=True)
# series.dropna().cumsum().plot()

pos_portfolio = copy.deepcopy(pdyn.starts)
pos_portfolio.values[:] = False
neg_portfolio = copy.deepcopy(ndyn.starts)
neg_portfolio.values[:] = False

################# SECOND STEP ########################### Periodic
threshold = 0.05

class PosMomentum(PeriodicBacktest):
    def add_data(self):
        pass
    def select_stocks(self, i, v):
        tmp = self.rel.resample(self.interval, how='sum').ix[v]
        tmp = copy.deepcopy(tmp.dropna())
        stocks = tmp.index[tmp > threshold]
        return stocks

class NegMomentum(PeriodicBacktest):
    def add_data(self):
        pass
    def select_stocks(self, i, v):
        tmp = self.rel.resample(self.interval, how='sum').ix[v]
        tmp = copy.deepcopy(tmp.dropna())
        stocks = tmp.index[tmp < - threshold]
        return stocks

pper = PosMomentum(o, 'BQ-DEC')
pper.calculate_portfolio_return()
nper = NegMomentum(o, 'BQ-DEC')
nper.calculate_portfolio_return()

# series = pd.concat([pper.rel_ret, nper.rel_ret], axis=1)
# series.rename(columns={0: 'posmom %s' %number_of_shares,
#                        1: 'negmom %s' %number_of_shares},
#               inplace=True)
# series.cumsum().plot()

##################################################################
########################## THIRD STEP ############################
# here I fill up the empty portfolios (pos_portfolio & neg_portfolio) with
# "True" values with the same scheme as in PeriodicBacktest

# get dataframe of relative returns
rel_ret = {k: v.rel_ret for k, v in o.iteritems()}
rel = pd.DataFrame(rel_ret)

# rebalance gives the dates for rebalancing
rebalance = rel.resample('BQ-DEC', how='sum').index
# in the loop we're getting rid of the last period
for i, v in enumerate(rebalance[:-1]):
    # periodic portfolio holdings for the period
    neg_stocks = nper.port_props.holdings[v]
    pos_stocks = pper.port_props.holdings[v]
    # get location of first rebalancing date within 
    # relative returns dataframe (+1 ensures we don't
    # include last day of period we check in the
    # performance period)
    x = rel.index.get_loc(v) + 1
    # start gives the timestamp of x
    start = rel.index[x]
    # for every stock matching criteria (return over last
    # period > thr or < -thr we put True in the portfolio
    # holdings frame)
    pos_portfolio.ix[start:rebalance[i+1], pos_stocks] = True
    neg_portfolio.ix[start:rebalance[i+1], neg_stocks] = True

#####################################################################
######################### FINAL STEP ################################
# here I get rid of portfolio holdings whenever there's holding
# for that cell within DynamicBacktest portfolio
# we want to get flow momentum, without any news momentum

for i, d in enumerate(pos_portfolio.index):
    pos_portfolio.ix[d][pdyn.holdings.ix[d] == True] = False

for i, d in enumerate(neg_portfolio.index):
    neg_portfolio.ix[d][ndyn.holdings.ix[d] == True] = False

# apply the maps of True/False onto relative_returns

rel_pos = copy.deepcopy(rel)
for sec in rel_pos.columns:
    rel_pos[sec] = rel_pos[sec][pos_portfolio[sec]]
trial_pos = rel_pos.mean(axis=1).dropna()
series = pd.concat([pper.rel_ret, trial_pos], axis=1)
series.rename(columns={0: 'with news',
                       1: 'without news'},
              inplace=True)
series.cumsum().plot()

rel_neg = copy.deepcopy(rel)
for sec in rel_neg.columns:
    rel_neg[sec] = rel_neg[sec][neg_portfolio[sec]]
trial_neg = rel_neg.mean(axis=1).dropna()
series = pd.concat([nper.rel_ret, trial_neg], axis=1)
series.rename(columns={0: 'with news',
                       1: 'without news'},
              inplace=True)
series.cumsum().plot()
