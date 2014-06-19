"""
OVERVIEW:
A Bollinger Band is a volatility-based envelope, representing a stock's normal
upper and lower trading boundaries. This strategy creates a buy signal when
the price crosses below the lower Bollinger Band, representing an abnormally
low price, but closes within the bands.
Multiple exit strategies are incorporated in the following priority:
(1) Sell at market the day after the price crosses above the upper Band on the
    previous day but doesn't cross on the current day. The idea is to stay in
    the market as long as prices are tracking the upper band.
(2) Sell at market the day after a close below the lower of:
    (a) the low of the day the trade signal was generated, or
    (b) the low of the day before the trade signal was generated
    This condition is in place to cut losses.
(3) Sell at a specified profit target percentage. If the position is not
    profitable, this condition is not used.

PARAMETER DESCRIPTION:
A Bollinger Band is a band plotted two standard deviations away from a simple
moving average. Because they're based on standard deviation, a measure of
volatility, Bollinger Bands adjust to market conditions. Generally, this
indicator is drawn on a chart as an upper band and a lower band through which
price movement is tracked.

bollinger_period: number of days used in the moving average calculation when
                  creating the Bollinger Bands
standard_deviation: by default 2 is used (2 standard deviations)

Source: https://eresearch.fidelity.com/

==============================================================================
Settings (bollinger_period and standard_deviation) can be adjusted to suit the
characteristics of particular securities or trading styles. Bollinger
recommends making small incremental adjustments to the standard deviation
multiplier.
Changing the number of periods for the moving average also affects the number
of periods used to calculate the standard deviation. Therefore, only small
adjustments are required for the standard deviation multiplier. An increase in
the moving average period would automatically increase the number of periods
used to calculate the standard deviation and would also warrant an increase in
the standard deviation multiplier. With a 20-day SMA and 20-day Standard
Deviation, the standard deviation multiplier is set at 2. Bollinger suggests
increasing the standard deviation multiplier to 2.1 for a 50-period SMA and
decreasing the standard deviation multiplier to 1.9 for a 10-period SMA.

Source: http://stockcharts.com/school/doku.php?id=chart_school:technical_indica
        tors:bollinger_bands

"""
from itertools import groupby
import pandas as pd

from blvresearch.concat.signals.utils import (
    remove_consecutive_values
)


def get_signals(data, bollinger_period, no_of_std_deviations=2):
    "bollinger_period = number of days to calculate rolling std & mean"
    returns = data['alpha'].cumsum()
    l_b, m_b, u_b = _get_bands(returns, bollinger_period, std_dev)
    result = _run_logic(returns, l_b, m_b, u_b)
    return remove_consecutive_values(result)


def _run_logic(returns, l_b, m_b, u_b):
    buy_signals = _get_buy_signals(returns, l_b)
    sell_signals = _get_sell_signals(returns, m_b, )


def _get_sell_signals(returns, upper_band):
    start = lower_band.dropna().index[0]
    series_of_signals = returns[start:] > upper_band[start:]
    list_of_tuples = [(k, v) for k, v in series_of_signals.items()]
    list_of_tuples.sort(key=lambda x: x[0])
    result = pd.Series(index=upper_band.index)
    for signal, group in groupby(list_of_tuples, key=lambda x: x[1]):
        tuples = list(group)
        if signal == False:
            signal_day = tuples[-1][0]
            result[signal_day] = True
    return result

def _get_buy_signals(returns, lower_band):
    start = lower_band.dropna().index[0]
    series_of_signals = returns[start:] > lower_band[start:]
    list_of_tuples = [(k, v) for k, v in series_of_signals.items()]
    list_of_tuples.sort(key=lambda x: x[0])

    result = pd.Series(index=lower_band.index)
    for signal, group in groupby(list_of_tuples, key=lambda x: x[1]):
        tuples = list(group)
        if signal == False:
            signal_day = tuples[-1][0]
            result[signal_day] = True
    return result


def _get_bands(returns, no_of_days, no_of_std_dev):
    mvg_std = pd.rolling_std(returns, window=no_of_days)
    middle_band = pd.rolling_mean(returns, window=no_of_days)
    lower_band = middle_band - no_of_std_dev * mvg_std
    upper_band = middle_band + no_of_std_dev * mvg_std
    return lower_band, middle_band, upper_band


def _adjust_series_of_signals(series_of_signals, confirmation_window):
    list_of_tuples = [(k, v) for k, v in series_of_signals.items()]
    list_of_tuples.sort(key=lambda x: x[0])
    result = pd.Series(index=series_of_signals.index)
    for signal, group in groupby(list_of_tuples, key=lambda x: x[1]):
        tuples = list(group)
        if len(tuples) > confirmation_window:
            signal_day = tuples[confirmation_window - 1][0]
            result[signal_day] = True if signal == True else False
    return result
