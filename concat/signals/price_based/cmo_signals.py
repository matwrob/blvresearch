"""
OVERVIEW:
This strategy seeks to enter the market when prices are low (CMO value of -50),
as determined by the Chande Momentum Oscillator, combined with a simple price
pattern that looks back over the previous 9 days. The strategy sells when
prices eventually rise so that CMO becomes overbought (CMO value of 50), or at
a certain profit level.

PARAMETER DESCRIPTION:
The Chande Momentum Oscillator, created by Tushar Chande, is similar to RSI,
measuring trend strength. It is calculated by dividing the sum of up and down
day activity over a specified period of time into the difference of up day and
down day activity of that same period. The result is then multiplied by 100 to
arrive at an indicator that oscillates between -100 and 100.
The CMO period represents the number of days used in the CMO calculation.
The default value in this strategy for the CMO period is 20 days.
CMO reaches extreme levels at 50 for overbought and -50 for oversold.

The higher the CMO value the stronger the trend, whereas low CMO values
indicate sideways trading ranges.

Source: https://eresearch.fidelity.com/

"""
from itertools import groupby
import pandas as pd

from blvresearch.concat.signals.utils import (
    remove_consecutive_values
)

BUY_THRESHOLD = -50
SELL_THRESHOLD = 50


def get_cmo_signals(data, periods):
    cmos = _calculate_cmo_values(data['alpha'], periods)
    result = cmos.dropna().map(logic)
    result = _adjust_series_of_signals(result)
    return remove_consecutive_values(result)


def _calculate_cmo_values(returns, periods):
    only_gains = returns.apply(lambda x: 0 if x < 0 else 1)
    only_losses = returns.apply(lambda x: 0 if x >= 0 else 1)
    sums_of_gains = pd.rolling_sum(only_gains, window=periods)
    sums_of_losses = pd.rolling_sum(only_losses, window=periods)
    result = pd.Series(index=sums_of_gains.index)
    for date, sog in sums_of_gains.items():
        result[date] = ((sog - sums_of_losses[date]) /
                        (sog + sums_of_losses[date]))
    return result


def logic(x):
    if x <= BUY_THRESHOLD / 100:
        return True
    elif x >= SELL_THRESHOLD / 100:
        return False


def _adjust_series_of_signals(series_of_signals):
    list_of_tuples = [(k, v) for k, v in series_of_signals.items()]
    list_of_tuples.sort(key=lambda x: x[0])
    result = pd.Series(index=series_of_signals.index)
    for signal, group in groupby(list_of_tuples, key=lambda x: x[1]):
        tuples = list(group)
        if signal in [True, False]:
            signal_day = tuples[-1][0]
            result[signal_day] = True if signal == True else False
    return result


DESCRIPTION_BUY = """
This is a BUY signal generated by Chande Momentum Oscillator.\n
Chande Momentum Oscillator measures strength of the trend using prices of
the last 9 days.\n
CMO says to buy the stock when its value drops below the threshold of -50,
and sell it when its value exceeds +50.
"""

DESCRIPTION_SELL = """
This is a SELL signal generated by Chande Momentum Oscillator.\n
Chande Momentum Oscillator measures strength of the trend using prices of
the last 9 days.\n
CMO says to buy the stock when its value drops below the threshold of -50,
and sell it when its value exceeds +50.
"""

DESCRIPTION_COMMON = """
The Chande Momentum Oscillator was created by Tushar Chande.
To get its value we calculate the difference between all positive and all
negative returns over the last 9 days and divide it by the total return over
this period.
This value is then multiplied by 100 to get an indicator ranging from\n
-100 to +100.\n\n\n

For all trading strategies, tha past performance does
not guarantee future results.
"""


def get_cmo_descr(signal):
    if signal == True:
        result = DESCRIPTION_BUY
    elif signal == False:
        result = DESCRIPTION_SELL
    result += DESCRIPTION_COMMON
    return result
