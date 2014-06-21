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

from blvresearch.concat.signals.utils import (
    get_benchmark_return
)


class SignalReport:

    WINDOW = 20

    TEMPLATE = ("Strategy generated profit for %s companies (%s)\n" +
                "Strategy generated loss for %s companies (%s)\n" +
                "Strategy outperformed benchmark for %s companies (%s)\n" +
                "Average number of signals per entity: %s\n" +
                "Average return of winners was %s\n" +
                "Average return of losers was %s\n" +
                "Over the next %s trading days after signals:\n" +
                "* %s of signals were correct among winners\n" +
                "* %s of signals were incorrect among losers\n")

    def __init__(self, dict_of_signals, dict_of_data):
        self._dos = dict_of_signals
        self._dod = dict_of_data

    def get(self):
        data = self._get_data()
        chars = StrategyCharacteristics(data)
        return self._create_string(chars)

    def _get_data(self):  # pragma: no cover
        res = dict()
        for sec, entity_signals in self._dos.items():
            if any(entity_signals):
                split = split_signals_into_good_and_bad(
                    entity_signals, self._dod[sec]['alpha'], self.WINDOW
                )
                ret = get_total_return_on_signals(
                    entity_signals, self._dod[sec]['alpha']
                )
                res[sec.factset_entity_id] = (ret, split)
        return res

    def _create_string(self, strategy_characteristics):
        sc = strategy_characteristics
        no_of_win = len(sc.entities_with_positive_total_returns)
        no_of_loss = len(sc.entities_with_negative_total_returns)
        no_of_bench_win = len(sc.entities_that_beat_benchmark)
        pct_of_win = (len(sc.entities_with_positive_total_returns) /
                      len(sc.all_entities))
        pct_of_loss = (len(sc.entities_with_negative_total_returns) /
                       len(sc.all_entities))
        pct_of_bench_win = (len(sc.entities_that_beat_benchmark) /
                            len(sc.all_entities))
        avg_profit_of_win = sc.get_average_return(
            sc.entities_with_positive_total_returns
        )
        avg_profit_of_loss = sc.get_average_return(
            sc.entities_with_negative_total_returns
        )
        no_of_signals = sc.get_numbers_of_good_and_bad_signals(sc.all_entities)
        no_of_signals = (no_of_signals['good'].sum() +
                         no_of_signals['bad'].sum()) / len(sc.all_entities)
        no_of_signals_win = sc.get_numbers_of_good_and_bad_signals(
            sc.entities_with_positive_total_returns
        )
        good_signals_win = (no_of_signals_win['good'].sum() /
                            (no_of_signals_win['good'].sum() +
                             no_of_signals_win['bad'].sum()))

        no_of_signals_loss = sc.get_numbers_of_good_and_bad_signals(
            sc.entities_with_negative_total_returns
        )
        bad_signals_loss = (no_of_signals_loss['bad'].sum() /
                            (no_of_signals_loss['good'].sum() +
                             no_of_signals_loss['bad'].sum()))
        result = self.TEMPLATE % (no_of_win, pct_of_win,
                                  no_of_loss, pct_of_loss,
                                  no_of_bench_win, pct_of_bench_win,
                                  round(no_of_signals, 4),
                                  round(avg_profit_of_win, 4),
                                  round(avg_profit_of_loss, 4),
                                  self.WINDOW,
                                  round(good_signals_win, 4),
                                  round(bad_signals_loss, 4))
        return result


class StrategyCharacteristics:
    """aggregates characteristics of a strategy based on performance of this
    strategy across different securities

    input is a dict with keys being factset_entity_ids and values being tuples,
    where first value of the tuple is a total return generated by this strategy
    and the second value being a dict that splits signals into good and bad
    ones

    """

    def __init__(self, data):
        self.d = data
        self.benchmark = get_benchmark_return()

    @property
    def all_entities(self):
        return self.d

    @property
    def entities_with_positive_total_returns(self):
        return {k: v for k, v in self.d.items() if v[0] >= 0}

    @property
    def entities_with_negative_total_returns(self):
        return {k: v for k, v in self.d.items() if v[0] < 0}

    @property
    def entities_that_beat_benchmark(self):
        return {k: v for k, v in self.d.items() if v[0] > self.benchmark}

    def get_average_return(self, data, signal=None):
        """calculates average return across all entities provided (data),
        if signal variable provided, it calculates for a given signal only

        """
        if signal:
            tmp = {k: pd.Series(v[1][signal]).sum()
                   for k, v in data.items()}
            return pd.Series(tmp).mean()
        tmp = {k: v[0] for k, v in data.items()}
        return pd.Series(tmp).mean()

    def get_numbers_of_good_and_bad_signals(self, data):
        result = pd.DataFrame(
            {k: {'good': len(v[1]['good']), 'bad': len(v[1]['bad'])}
             for k, v in data.items()}
        )
        return result.T


def split_signals_into_good_and_bad(signals, returns, window=20):
    """returns days that happened to be correct, i.e. generated profit over
    the number of days defined by window, or until the next signal if it
    occurred earlier
    initially signal = 0 or signal = 1 (sell or buy respectively)
    sell signal is changed to -1 to get shortselling return

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
    """logic behind the period of time to calculate return over, after the
    signal; if there are other signals that come after the current one and
    they occur within a certain number of days afterwards, then return is
    calculated from initial signal to the next, otherwise from initial signal
    over a specified number of days (window variable)
    if there are no other signals coming afterwards, i.e. current signal is
    the last one, return is calculated over a specified number of days (or
    until the end of series, if there's not enough days left)

    """
    next_signals = [d for d in signals.index if d > day]
    if next_signals:
        subperiod = returns[day:][1:window + 1]  # signal day != 1st return day
        if next_signals[0] in subperiod.index:
            return subperiod[day:next_signals[0]].sum()
        else:
            return subperiod[:next_signals[0]].sum()
    return returns[day:][1:window + 1].sum()


def get_total_return_on_signals(signals, returns):
    """total return of a trading strategy; sell signals indicate shorting, not
    only liquidating assets being currently held

    """
    df = _prep_frame_for_total_return_calculation(signals, returns)
    hold_returns = df['returns'][df['signals'] == 1]
    sold_returns = df['returns'][df['signals'] == 0]
    return hold_returns.sum() - sold_returns.sum()


def _prep_frame_for_total_return_calculation(signals, returns):
    """prepares dataframe to calculate total return based on a series of buy
    and sell signals;
    1) shifts values 1 period ahead, because signal day return shouldn't be
       counted towards final return, because we execute the trade on the next
       day at the earliest
    2) removes everything that happens before the 1st signal
    3) fills forward signal values to indicate days when we hold a stock (True)
       and when we shortsell the stock (False)

    """
    signals = pd.Series(signals, index=returns.index).shift(1)
    signals.name, returns.name = 'signals', 'returns'
    result = pd.concat([signals, returns], axis=1)
    result = result[signals.dropna().index[0]:]
    result['signals'].ffill(inplace=True)
    return result
