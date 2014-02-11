# returns a dataframe (multiindexed) from the input of yearly data collections
# e.g. price data or benchmark model output data
# for a given list of variables

import pandas as pd

from concat.core.prices import to_log_returns
from concat.core.utils import load_object


SECTORS = ['1100', '1200', '1300', '1400', '2100', '2200', '2300', '2400',
           '3100', '3200', '3250', '3300', '3350', '3400', '3500', '4600',
           '4700', '4800', '4900']

sp500 = pd.read_csv('blvresearch/extras/ticker_rics_sp500_2012.csv')
# UNI = load_object('dict_of_uni.pickle')
# PRICES = load_object('price_data_2003_2013_wo_news.pickle')
# MODEL = load_object('benchmark_model_data_2003_2013_w_news.pickle')

# tog = TotalOutputGenerator(PRICES, MODEL)
# total_output = tog.get()


def get_total_output(column, dict_of_yearly_outputs):
    '''provided a name of interest, merges data for that variable for the full
    period using yearly outputs
    '''
    result = pd.DataFrame()
    for k, v in dict_of_yearly_outputs.items():
        result = pd.concat([result, v.matrix(column)])
    return result


class EntityOutputGenerator:

    def __init__(self, list_of_security_ids):
        self.sec_ids= list_of_security_ids

    def get(self, start_date, end_date):
        uni = Universe(self.sec_ids)


class TotalOutputGenerator:


    def __init__(self, yearly_price_data, yearly_benchmark_model_data):
        self.pd = yearly_price_data
        self.bmd = yearly_benchmark_model_data

    def get(self):
        price_df = self._merge_year_by_year(self.pd)
        benchmark_df = self._merge_year_by_year(self.bmd)
        return pd.concat([price_df, benchmark_df], axis=1)

    def _merge_year_by_year(self, dict_of_collections):
        temp = {k: self._create_df_from_collection(v)
                for k, v in dict_of_collections.items()}
        return pd.concat(list(temp.values()))

    def _create_df_from_collection(self, concat_collection):
        result = dict()
        for col in concat_collection.columns:
            df = concat_collection.matrix(col)
            df.name = col
            result[col] = self._to_multi_index(df)
        return pd.DataFrame(result)

    def _to_multi_index(self, output):
        output = output.stack()
        output = output.reorder_levels(order=[1, 0])
        return output


class MultiYearOutputGenerator:

    def __init__(self, dict_of_yearly_outputs):
        self.o = dict_of_yearly_outputs

    def get(self):
        returns = {k: self._to_returns(v) for k, v in self.o.items()}
        news = {k: self._to_relevance(v) for k, v in self.o.items()}
        return self._merge(returns, news)

    def _merge(self, dict_of_returns, dict_of_news):
        output = dict()
        for year, returns in dict_of_returns.items():
            o = pd.concat([returns, dict_of_news[year]], axis=1)
            output[year] = o.rename(columns={0: 'return', 1: 'is_relevant'})
        return output

    def _to_returns(self, yearly_output):
        result = yearly_output.matrix("close")
        result = result.apply(to_log_returns)
        return self._to_multi_index(result)

    def _to_relevance(self, yearly_output):
        result = yearly_output.matrix("news")
        for k, v in result.items():
            v = v.dropna()
            result[k] = v.apply(lambda x: any([n.relevance[k]['score'] > 0.3
                                               for n in x]))
            result[k] = result[k].fillna(False)
        return self._to_multi_index(result)

    def _to_multi_index(self, output):
        output = output.stack()
        output = output.reorder_levels(order=[1, 0])
        return output


def get_NT_dispersions(dict_of_yearly_outputs):
    result = pd.DataFrame(index=pd.date_range("2003-01-01", "2013-12-31",
                                              freq='b'),
                          columns=SECTORS)
    for year, output in dict_of_yearly_outputs.items():
        news_tone = output[output["is_relevant"] == True]["return"]
        for sector_id in SECTORS:
            entities = list(UNI[year].filter("sector", sector_id).keys())
            for k, v in news_tone[entities].groupby(level=1):
                result[sector_id][k] = v.std()
    return result


def get_NT_aggregates(dict_of_yearly_outputs):
    result = pd.DataFrame(index=pd.date_range("2003-01-01", "2013-12-31",
                                              freq='b'),
                          columns=SECTORS)
    for year, output in dict_of_yearly_outputs.items():
        news_tone = output[output["is_relevant"] == True]["return"]
        for sector_id in SECTORS:
            entities = list(UNI[year].filter("sector", sector_id).keys())
            for k, v in news_tone[entities].groupby(level=1):
                result[sector_id][k] = v.mean()
    return result


def get_df_of_daily_mean_sector_returns(total_output):
    result = dict()
    for _id, entities in SECTOR_MEMBERS.items():
        result[_id] = total_output.ix[entities]['abs_ret'].mean(level=1)
    result = pd.DataFrame(result)
    result = result.fillna(0)
    return result


# daily = get_df_of_daily_mean_sector_returns(output)
# weekly = daily.resample("W-SUN", how="sum")

# news = output["news"].fillna(0)


def add_column_is_relevant(output):
    def func(x):
        return any([n.relevance[_id]['score'] > 0.3 for n in x])
    result = dict()
    for group in output.groupby(level=0):
        _id, df = group[0], group[1]
        s = df["news"].dropna()
        result[group[0]] = s.apply(func)
    return result

def add_column_no_f_relevant_news(output):
    result = dict()
    for k, v in output["news"].items():
        if not isinstance(v, float):
            result[k] = len([n for n in v if n.relevance[k[0]]['score'] > 0.3])
    result = pd.Series(result)
    result = pd.concat([output, result], axis=1)
    return result


def _to_relevance(yearly_output):
    news = output["news"].dropna()
    result = dict()
    for k, v in news.groupby(level=0):
        result[k] = v.apply(lambda x: any([n.relevance[k]['score'] > 0.3
                                           for n in x]))
    return result
