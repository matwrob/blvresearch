"""
Signals are based on end of day prices, therefore

a buy signal on Monday can only be obtained after exchange closes,
so the earliest possible trade is on Tuesday morning.

Here we assume we're able to buy the stock on Tuesday morning at Monday's
closing price,

so first return we get from holding this stock is the return from Monday CP to
Tuesday CP (CP = closing price), i.e. Tuesday's return

When we hold a stock, and we get a sell signal, say again on Monday,
this means again the stock exchange is closed (i.e. the return from previous
Friday CP to this Monday CP generated the signal), therefore

we're only able to sell the stock on Tuesday (again we assume we can do this
at the opening of the exchange and again we assume we can sell it at Monday's
CP), therefore
the last return of the period when we held this stock, would be the Monday's
return (because we sold on Tuesday at Monday's CP)

"""

import pandas as pd


class SignalReport:

    WINDOW = 20

    def __init__(self, dict_of_signals, dict_of_data):
        self._dos = dict_of_signals
        self._dod = dict_of_data

    def get(self):
        data = self._get_data()
        self.data = data
        result = self._get_strategy_characteristics(data)
        return self._create_string(result)

    @property
    def winners(self):
        return {k: v for k, v in self.data.items() if v[0] >= 0}

    @property
    def losers(self):
        return {k: v for k, v in self.data.items() if v[0] < 0}

    def _get_strategy_characteristics(self, dict_of_results):
        res = dict()
        winners = {k: v for k, v in dict_of_results.items() if v[0] >= 0}
        losers = {k: v for k, v in dict_of_results.items() if v[0] < 0}
        res['no_of_winners'] = len(winners)
        res['no_of_losers'] = len(losers)
        res['pct_winners'] = len(winners) / len(dict_of_results)
        res['pct_losers'] = len(losers) / len(dict_of_results)
        tmp = pd.Series({k: v[0] for k, v in winners.items()}).mean()
        res['avg_winners'] = tmp
        tmp = pd.Series({k: v[0] for k, v in losers.items()}).mean()
        res['avg_losers'] = tmp
        tmp = pd.DataFrame(
            {k: {'good': len(v[1]['good']), 'bad': len(v[1]['bad'])}
             for k, v in winners.items()}
        ).T
        tmp = tmp['good'].sum() / (tmp['good'].sum() + tmp['bad'].sum())
        res['good_signals_winners'] = tmp
        tmp = pd.DataFrame(
            {k: {'good': len(v[1]['good']), 'bad': len(v[1]['bad'])}
             for k, v in losers.items()}
        ).T
        tmp = tmp['bad'].sum() / (tmp['good'].sum() + tmp['bad'].sum())
        res['bad_signals_losers'] = tmp.sum()
        return res

    def _get_data(self):
        res = dict()
        for sec, entity_signals in self._dos.items():
            if any(entity_signals):
                st = SignalTester(entity_signals, self._dod[sec])
                split = st.split_signals(self.WINDOW)
                ret = st.get_total_return()
                res[sec.factset_entity_id] = (ret, split)
        return res

    def _create_string(self, results):
        s = "Strategy generated profit for %s companies (%s)\n"
        s = s % (results['no_of_winners'], results['pct_winners'])
        s += "Strategy generated loss for %s companies (%s)\n"
        s = s % (results['no_of_losers'], results['pct_losers'])
        s += "Average profit was %s\n" % results['avg_winners']
        s += "Average loss was %s\n" % results['avg_losers']
        s += "Among winners %s of signals were correct (over the next %sTD)\n"
        s = s % (results['good_signals_winners'], self.WINDOW)
        s += "Among losers %s of signals were incorrect (over the next %sTD)\n"
        s = s % (results['bad_signals_losers'], self.WINDOW)
        return s


class SignalTester:

    def __init__(self, entity_signals, entity_data):
        self._s = entity_signals
        self._d = entity_data
        self._r = entity_data['alpha']

    def split_signals(self, window=20):
        self.split_signals = split_signals_into_good_and_bad(self._s,
                                                             self._r,
                                                             window)
        return self.split_signals

    def get_total_return(self):
        self.total_return = get_total_return_on_signals(self._s, self._r)
        return self.total_return


def test_entity_signals(entity_signals, entity_data):
    returns = entity_data['alpha']
    buys = entity_signals[entity_signals == True]
    sells = entity_signals[entity_signals == False]
    buy_periods, sell_periods = _get_total_return(entity_signals, returns)


def split_signals_into_good_and_bad(signals, returns, window=20):
    """returns days that happened to be correct, i.e. generated profit over
    the number of days defined by window, or until the next signal if it
    occurred earlier

    """
    result = {'good': dict(), 'bad': dict()}
    for day, signal in signals.items():
        signal = -1 if signal == False else 1
        ret = _get_return_over_subperiod(day, signals, returns, window)
        if ret * signal > 0:
            result['good'][day.strftime('%Y-%m-%d')] = ret * signal
        else:
            result['bad'][day.strftime('%Y-%m-%d')] = ret * signal
    return result


def _get_return_over_subperiod(day, signals, returns, window):
    next_signals = [d for d in signals.index if d > day]
    if next_signals:
        subperiod = returns[day:][1:window + 1]  # signal day != 1st return day
        if next_signals[0] in subperiod.index:
            return subperiod[day:next_signals[0]].sum()
        else:
            return subperiod[:next_signals[0]].sum()
    return returns[day:][1:].sum()


def get_total_return_on_signals(signals, returns):
    """total return of a trading strategy; sell signals indicate shorting, not
    only liquidating assets held

    """
    temp = _prep_frame_for_total_return_calculation(signals, returns)
    hold_returns = temp['returns'][temp['signals'] == 1]
    sold_returns = temp['returns'][temp['signals'] == 0]
    return hold_returns.sum() - sold_returns.sum()

def _prep_frame_for_total_return_calculation(signals, returns):
    signals = pd.Series(signals, index=returns.index)
    signals = signals.shift(1)
    signals.name, returns.name = 'signals', 'returns'
    result = pd.concat([signals, returns], axis=1)
    result = result[signals.dropna().index[0]:]
    result['signals'].ffill(inplace=True)
    return result


def remove_consecutive_values(series):
    result = series.dropna()
    result[result.shift(1) == result] = None
    result = result.dropna()
    return result
