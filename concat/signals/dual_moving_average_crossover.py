import matplotlib.pyplot as plt
import pandas as pd


LONG_WINDOW = 30
SHORT_WINDOW = 5
CONFIRMATION_WINDOW = 5


def get_signals(data):
    s = pd.ewma(data['alpha'], span=SHORT_WINDOW)
    l = pd.ewma(data['alpha'], span=LONG_WINDOW)
    df = pd.DataFrame(s > l, columns=['s>l'])
    df['block'] = (df['s>l'].shift(1) != df['s>l']).astype(int).cumsum()
    return _create_series_of_signals(df)


def _create_series_of_signals(df):
    result = pd.Series(index=df.index)
    for k, v in df.groupby('block'):
        if len(v) > CONFIRMATION_WINDOW:
            if v['s>l'][0]:
                result[v.index[CONFIRMATION_WINDOW - 1]] = True
            else:
                result[v.index[CONFIRMATION_WINDOW - 1]] = False
    result = _remove_consecutive_values(result)
    return result


def _remove_consecutive_values(series):
    result = series.dropna()
    result[result.shift(1) == result] = None
    result = result.dropna()
    return result


def plot_with_signals(data, signals):
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
