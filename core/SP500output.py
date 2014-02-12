import pandas as pd

from concat.core.utils import load_object
from blvresearch.core.sp500 import tick_to_ent_no_dupli
from blvresearch.core.utils import int2datetime

# from concat.core.benchmark_model import BenchmarkModelData
# from blvresearch.core.sentiment import UNIVERSE


# start = '2003-01-02'
# end = '2012-12-31'
# curr = 'USD'
# DATA = BenchmarkModelData(UNIVERSE, start, end, in_currency=curr, news=True)


def get_incl_and_excl_dates_for_SP500():
    temp = pd.read_csv('blvresearch/extras/ticker_rics_sp500_2012.csv')
    temp = temp[['start', 'ending', 'TICKER']]
    temp['index'] = temp['TICKER'].map(tick_to_ent_no_dupli)
    temp = temp.dropna()
    temp.index = temp['index']
    temp = temp.drop(['TICKER', 'index'], axis=1)
    temp = temp[['start', 'ending']].applymap(int2datetime)
    return temp


def remove_data_for_time_when_not_in_SP500(dataframe):
    incl_excl = get_incl_and_excl_dates_for_SP500()
    result = dict()
    for k, v in dataframe.items():
        s, e = incl_excl['start'][k], incl_excl['ending'][k]
        if isinstance(s, pd.Series):
            result[k] = solve_for_more_periods(s, e, v)
        else:
            result[k] = v[s:e]
    return pd.DataFrame(result)


def solve_for_more_periods(starts, ends, values):
    def _get_inbetweens(iterable):
        return [(v[-1], iterable[(i + 1) % len(iterable)][0])
                for i, v in enumerate(iterable) if i < len(iterable) - 1]
    result = values[starts.values[0]:ends.values[-1]]
    periods = list(zip(starts, ends))
    for per in _get_inbetweens(periods):
        result[per[0]:per[1]] = None
    return result


DATA = load_object('bmd_sp500_2003_2013.pickle')
NEWS = remove_data_for_time_when_not_in_SP500(DATA.matrix('news'))
ALPHA = remove_data_for_time_when_not_in_SP500(DATA.matrix('alpha'))
ABSRET = remove_data_for_time_when_not_in_SP500(DATA.matrix('abs_ret'))
