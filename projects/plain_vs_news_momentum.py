from blvresearch.core.dynamic_backtest import DynamicBacktest


class OneMonthMomentumPortfolioWINNERS(DynamicBacktest):

    def _get_starting_points_and_holdings(self):
        SIZE = lambda x: int(len(x) / 10)
        result = dict()
        for k, v in self.returns.iterrows():
            v = v.dropna()
            v.sort(ascending=False)
            result[k] = list(v[:SIZE(v)].index)
        result = pd.Series(result)
        return result.shift(self.pause_per + 1).dropna()


class OneMonthMomentumPortfolioWINNERSwithNews(DynamicBacktest):

    def _get_starting_points_and_holdings(self):
        SIZE = lambda x: int(len(x) / 10)
        result = dict()
        for k, v in self.returns.iterrows():
            v = v.dropna()
            v.sort(ascending=False)
            result[k] = list(v[:SIZE(v)].index)
        result = pd.Series(result)
        return result.shift(self.pause_per + 1).dropna()
