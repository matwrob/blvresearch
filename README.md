blvresearch
===========

research tools to be used with Bluevalor database


PORTFOLIO:

provides basic objects for data backtesting:
* StockReturns
* PortfolioStrategy
* Portfolio


PERIODIC BACKTEST:

performs backtesting procedure based on total output data provided and optional
list of entities

Stock returns are contained in a class StockReturns, which takes total output
and optional return type (by default absolute return is used).
Initialized StockReturns give access to .monthly, .weekly, and .daily returns.


PLOTTING:

provides infrastructure to create plots of data coming from testing Bluevalor's
data
