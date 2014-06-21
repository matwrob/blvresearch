import matplotlib.pyplot as plt
import pandas.io.data as web
import datetime as dt
import pandas as pd

from blvutils.finance import to_log_returns


YESTERDAY = dt.datetime.today() - pd.DateOffset(days=1)
START = YESTERDAY - pd.DateOffset(years=2)


def remove_consecutive_values(series):
    result = series.dropna()
    result[result.shift(1) == result] = None
    return result.dropna()


def get_benchmark_return(code="^SSMI"):  # pragma: no cover
    """Adj Close = close price adjusted for dividends and splits

    """
    sp500 = web.DataReader(name=code,
                           data_source="yahoo",
                           start=START,
                           end=YESTERDAY)
    result = to_log_returns(sp500['Adj Close'])
    return result.sum()


def plot_returns_with_signals(data, signals):  # pragma: no cover
    fig = plt.figure()
    ax1 = fig.add_subplot(211,  ylabel='ALPHA')
    cum_alpha = data['alpha'].cumsum()
    cum_alpha.plot(ax=ax1, color='b', lw=2.)

    buy = signals[signals == True]
    sell = signals[signals == False]

    ax1.plot(buy.index, cum_alpha[buy.index], '^', markersize=20, color='g')
    ax1.plot(sell.index, cum_alpha[sell.index], 'v', markersize=20, color='r')
    fig.set_size_inches(28, 35)
    plt.show()
