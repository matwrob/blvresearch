"""
portfolios: series of lists of entity_ids
research_data: output of get_research_data_by_country or
               get_research_data_by_entity functions

"""
import numpy as np


def calculate_turnover(portfolios):
    result = dict()
    for i, date in enumerate(portfolios.index[:-1]):
        next_date = portfolios.index[i + 1]
        new_stocks = [s for s in portfolios[next_date]
                      if s not in portfolios[date]]
        result[next_date] = len(new_stocks) / len(portfolios[date])
    return result


def calculate_average_beta_of_portfolios(research_data, portfolios, frequency):
    betas = pd.DataFrame({k: v['beta'] for k, v in research_data.items()})
    betas = betas.resample(frequency, how=mean)
    result = dict()
    for date, entities in portfolios.items():
        result[date] = np.mean(betas.loc[date][entities])
    return pd.Series(result)
