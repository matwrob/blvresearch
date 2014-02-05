
# Determine frequency of data points
# Available frequencies:
# 'D'       daily frequency (original data)
# 'W-SUN'   weekly frequency (sundays), the same as 'W'
# 'W-FRI'   weekly frequency (fridays)
# 'M'       monthly frequency


# Determine frequency of rebalancing
# By default:
# 'BM'     business-end-of-the-month
# also possible
# 'BMS'    business-start-of-the-month

# class Portfolio:
#     pass


# def aggregate_on_index(df):
#     df.sort(inplace=True)
#     df


class StockReturns:
    """
    container for returns; provide concat model output and return type on init:
    types: 'abs_ret'   (default, total returns, Factset methodology)
           'rel_ret'   (returns relative to Blv benchmarks)
           'alpha'     (risk adjusted returns relative to Blv benchmarks)

    """

    def __init__(self, total_output, type='abs_ret'):
        self.o = total_output
        self.type = type

    @property
    def monthly(self):
        return self._unstacked.resample('M', how='sum')

    @property
    def weekly(self):
        return self._unstacked.resample('W', how='sum')

    @property
    def daily(self):
        return self._unstacked

    @property
    def _unstacked(self):
        return self.o[self.type].unstack(level=0)


class StartingPoints:
    """
    returns:
    * time series of lists of entities (UNIVERSE_SPLIT_TYPE = 'absolute_size')
    * dataframe indexed by timed with columns representing portfolios
    (UNIVERSE_SPLIT_TYPE = 'quantile')

    On init provide:
    * dataframe of returns (indexed by time of a predetermined frequency)
    * portfolio size (will be understood differently depending on
                      UNIVERSE_SPLIT_TYPE variable)
    'quantile' & portfolio_size = 10 =====> 10 portfolios
    'absolute_size' & portfolio_size = 10 ======> portfolios with 10 stocks

    based on a function _get_portfolios and global variable SIZE it

    change rebalancing global value using usual pandas frequencies, this is
    independent of data frequency

    e.g. data frequency might be daily (ranking portfolio returns based on N
    last days), but rebalancing might be performed on a monthly basis

    """
    REBALANCING = 'BM'
    UNIVERSE_SPLIT_TYPE = 'quantile'  # or 'absolute_size'

    def __init__(self, df_of_returns, portfolio_size):
        self.ret = df_of_returns

    def get(self):
        SIZE = lambda x: int(len(x) / 10)
        result = dict()
        for k, v in self._ranking_period_returns.iterrows():
            v = v.dropna()
            v.sort(ascending=False)
            result[k] = list(v[-SIZE(v):].index)
        result = pd.Series(result)
        return self._shift_and_trim_starting_points(result)

    def _get_portfolios(self):
        raise NotImplementedError('overwrite')


class PortfolioStrategy:
    """determines a strategy for portfolio formation over time
    takes

    core function by default takes a random subset of all stocks from the
    universe, should be overwritten by other methodology that returns a time
    series of lists of entities, this methodology can use any type of data
    available in Bluevalor's Model data output

    """
    HOLDING_PERIODS = 1

    def __init__(self, bluevalor_model_output):
        self.output = bluevalor_model_output

    def core_func(self):
        "overwrite this function to implement your own strategy"





class Portfolio:
    """represents the evolution of a portfolio of stocks over time

    on init takes stock_returns and portfolio_strategy:

    .members          to see time series of entities sets on a daily basis
    .performance      to see time series of returns

    feed PortfolioCharacteristics class with Portfolio instance to obtain
    a set of portfolio return characteristics (e.g. alphas, Sharpe rat., etc.)

    """
    def __init__(self, stock_returns, portfolio_strategy):
        self.returns = stock_returns
        self.strategy = portfolio_strategy
        self.hold = holding_periods

    def performance(self, how='mean'):
        pass

    @property
    def members(self):
        pass

    def _members_returns(self):
        "dataframe of returns"
        pass


# class QuantilePortfolios(Portfolios):

#     def __init__(self):
#         pass


# class AbsoluteSizePortfolios(Portfolios):

#     def __init__(self)


