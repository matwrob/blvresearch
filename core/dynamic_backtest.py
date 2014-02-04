import pandas as pd
import numpy as np

# inherit from DynamicBacktest overwriting
# _get_starting_points_and_holdings

def split_entities_on_zone(dict_of_universes):
    ZONES = ['am', 'eu', 'ap']
    result = {z: list() for z in ZONES}
    for k, v in dict_of_universes.items():
        for z in ZONES:
            result[z].extend(list(v.filter("zone", z).keys()))
    return {k: list(set(v)) for k, v in result.items()}


UNI = load_object('dict_of_uni.pickle')
entities = split_entities_on_zone(UNI)


class DynamicBacktest:
    """
    to run dynamic backtest initiate this class providing:
    * total_output
    * holding_periods: number of periods a given portfolio should be holdings
    * pause_periods: number of periods between the formation period and
                     a period when stocks should be held
    * entities: list of entities, if portfolios should be formed for a certain
                subset, e.g. entities from Europe only
    * data_frequency: provide frequency of returns, by default weekly returns
    * weighting: weighting applied to portfolio members, value-weighting by
                 default, possible also equal-weighting
    * transaction_cost

    """
    def __init__(self, total_output, holding_periods, pause_periods,
                 entities=None, data_frequency='W-SUN', weighting='value',
                 transaction_cost=0):
        self.o = total_output
        self.entities = entities
        self.data_freq = data_frequency
        self.hold_per = holding_periods
        self.pause_per = pause_periods
        self.weight = weighting
        self.trans_cost = transaction_cost

    def run(self):
        self.returns = self._get_returns_from_total_output()
        starting_points = self._get_starting_points_and_holdings()
        holdings = self._get_dataframe_of_holdings(starting_points)
        returns = self.returns[holdings.applymap(bool)]
        result = returns.mean(axis=1).dropna()
        dollar = result.cumsum() *
        return result, result.cumsum()

    def _get_returns_from_total_output(self):
        returns = self.o['abs_ret'].unstack(level=0)
        returns = returns.resample(self.data_freq, how='sum')
        if self.entities:
            return returns[self.entities]
        return returns

    def _get_dataframe_of_holdings(self, starting_points):
        result = pd.DataFrame(data=False, index=self.returns.index,
                              columns=self.returns.columns)
        ind = result.index
        for date, entities in starting_points.items():
            start_loc = result.index.get_loc(date)
            end_loc = start_loc + self.hold_per - 1
            result[ind[start_loc]:ind[end_loc]][entities] = True
        return result

    def _get_starting_points_and_holdings(self):
        raise NotImplementedError('overwrite this function')


class PortfolioCharacteristics:

    def __init__(self, portfolio_returns):
        self.port_ret = portfolio_returns

    def calculate(self):
        mean_excess_returns = self._calc_mean_excess_returns()
        std_deviations = self._calc_std_deviations()
        alphas, t_stats_alpha = self._calc_alphas()
        betas = self._calc_betas()
        sharpe = self._calc_sharpe_ratio()
        skew = self._calc_skeweness()

    def _calc_mean_excess_returns():
        pass



