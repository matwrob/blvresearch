from blvresearch.universe_generation import get_dict_of_yearly_universes
from blvresearch.totoutgen import TotalOutputGenerator


def get_dict_of_yearly_price_data(dict_of_universes):
    result = dict()
    for k, v in dict_of_universes.items():
        result[k] = PriceData(v, start(k), end(k),
                              news=False, in_currency='USD')
    return result


def get_dict_of_benchmark_model_data(dict_of_universes):
    result = dict()
    for k, v in dict_of_universes.items():
        result[k] = BenchmarkModelData(v, start(k), end(k),
                                       news=True, in_currency='USD')
    return result


def get_full_data(first_year, last_year):
    universes = get_dict_of_yearly_universes(first_year, last_year)
    price_data = get_dict_of_yearly_price_data(universes)
    benchmark_model = get_dict_of_benchmark_model_data(universes)
    tog = TotalOutputGenerator(price_data, benchmark_model)
    return tog.get()
