blvresearch
===========

research tools to be used with Bluevalor database


#########
PORTFOLIO
#########

General description:
provides basic objects for data backtesting:
* StockReturns
* PortfolioStrategy
* Portfolio
* PortfolioCharacteristics

Portfolio formation procedure:
STEP 1. write a "strategy" class, that inherits from PortfolioStrategy
        by overwriting _get_starting_points method with an algorithm of your
        choice

        one can use any type of data available in Bluevalor Model data output

STEP 2. Initiate the object from STEP 1 providing Bluevalor Model data output

STEP 3. Initiate Portfolio class providing result of STEP 2 (i.e. your
        strategy) on init.
        Now you can operate with your portfolio by e.g. checking portfolio
        members over time, or calculating portfolio performance.

STEP 4. Initiate PortfolioCharacteristics class by providing the result of
        STEP 3 on init. This will allow you to check different statistics of
        your portfolio (check description of PortfolioCharacteristics class)


PortfolioStrategy after initiating gives access to the following:
.output = Bluevalor Model data output
.positions = time series with lists of entities for each rebalancing day
any global attributes defined in the class that inherits from PortfolioStrategy
.HOLDING_PERIODS   = how many periods should entities be held in portfolio
.PAUSE_PERIODS     = how many periods should pass between determining portfolio
                     positions and starting to actually hold them
.REBALANCING_FREQUENCY = frequency of rebalancing periods
.PORTFOLIO_SIZE = number of entities held in a portfolios



Explanation of RankingPeriod/RebalancingDay/PausePeriods/HoldingPeriods
relationship:

Rebalancing day vs holding period:
rebalancing day is the day when we decide about the construction of our
portfolio for the next holding period,
we should hold this portfolio starting at the earliest on the next day
this is obtained by shifting portfolio.members by 1 position




PERIODIC BACKTEST:

performs backtesting procedure based on total output data provided and optional
list of entities

Stock returns are contained in a class StockReturns, which takes total output
and optional return type (by default absolute return is used).
Initialized StockReturns give access to .monthly, .weekly, and .daily returns.


Any kind of backtest class should perform only "overview" type of operations
using Portfolio/PortfolioStrategy objects



PLOTTING:

provides infrastructure to create plots of data coming from testing Bluevalor's
data
